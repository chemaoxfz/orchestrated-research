#!/usr/bin/env python3
"""Block until a watched Codex thread changes, print one line, and exit.

Usage:
  wait_threads.py [--codex-home ~/.codex] [--project SUBSTRING] NAME=THREAD_UUID ...

The Codex home defaults to $CODEX_HOME, then ~/.codex.

Run it as a Bash background task while every watched thread is idle, instead of
repeated 30-minute Monitor cycles. It exits on a new item, a new turn or a turn
status change in any listed thread. With --project, it also exits when a new
thread appears whose working folder contains SUBSTRING. Only the first line of
that thread's rollout file is read, to learn its cwd.
After it exits, arm watch_threads.py, which replays from its state files.
The database is opened read-only. Uses internal Codex tables, tested on codex-cli 0.166.0.
"""
import argparse, glob, json, os, sqlite3, sys, time

ap = argparse.ArgumentParser()
ap.add_argument('--codex-home', default=os.environ.get('CODEX_HOME', '~/.codex'))
ap.add_argument('--project', default=None)
ap.add_argument('--poll', type=int, default=20)
ap.add_argument('threads', nargs='+', help='NAME=THREAD_UUID')
args = ap.parse_args()
HOME = os.path.expanduser(args.codex_home)
DB = os.path.join(HOME, 'thread_history_1.sqlite')
THREADS = {uuid: name for name, uuid in (t.split('=', 1) for t in args.threads)}


def q(sql, params=()):
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True, timeout=5)
    try:
        return con.execute(sql, params).fetchall()
    finally:
        con.close()


def snap():
    s = {}
    for th in THREADS:
        o = q('select max(rollout_ordinal) from thread_items where thread_id=?', (th,))[0][0]
        n = q('select count(*) from thread_turns where thread_id=?', (th,))[0][0]
        st = q('select status from thread_turns where thread_id=? order by rowid desc limit 1', (th,))
        s[th] = (o, n, st[0][0] if st else None)
    return s


def cwd_of(th):
    files = glob.glob(os.path.join(HOME, f'sessions/*/*/*/rollout-*{th}.jsonl'))
    if not files:
        return None
    with open(files[0]) as f:
        return (json.loads(f.readline()).get('payload') or {}).get('cwd') or ''


start_ms = int(time.time() * 1000)
base = snap()
for th, name in THREADS.items():
    if base[th][0] is None and base[th][1] == 0:
        print(f'warning: {name} ({th}) has no items in {DB}. Check the thread ID and the Codex home.', file=sys.stderr, flush=True)
ignored = set(THREADS)
errors = 0
print(time.strftime('%H:%M:%S'), 'waiting; baseline', {THREADS[t]: v for t, v in base.items()}, file=sys.stderr, flush=True)
while True:
    time.sleep(args.poll)
    try:
        cur = snap()
        for th, name in THREADS.items():
            if cur[th] != base[th]:
                print(time.strftime('%H:%M:%S'), f'{name} changed: {base[th]} -> {cur[th]}', flush=True)
                sys.exit(0)
        if args.project:
            for (th,) in q('select distinct thread_id from thread_items where created_at_ms > ?', (start_ms,)):
                if th in ignored:
                    continue
                cwd = cwd_of(th)
                if cwd is None:
                    continue  # rollout not written yet; retry on the next poll
                ignored.add(th)
                if args.project in cwd:
                    print(time.strftime('%H:%M:%S'), f'new thread {th} in {cwd[-80:]}', flush=True)
                    sys.exit(0)
        errors = 0
    except SystemExit:
        raise
    except Exception as e:
        errors += 1
        if errors >= 15:
            print(time.strftime('%H:%M:%S'), f'waiter failing repeatedly: {e!r}', flush=True)
            sys.exit(1)
