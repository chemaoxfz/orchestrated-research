#!/usr/bin/env python3
"""Stream new messages and turn-status changes of Codex threads, one line per event.

Usage:
  watch_threads.py [--codex-home ~/.codex] --state-dir DIR [--maxlen 420] NAME=THREAD_UUID ...

The Codex home defaults to $CODEX_HOME, then ~/.codex.

Run it under a monitor that turns each stdout line into a notification.
The last seen rollout ordinal of each thread is kept in DIR/watch.<uuid8>.state,
so a re-armed watch replays everything that arrived meanwhile.
A thread without a state file starts at its current end.
Author messages are printed in full. Messages from the orchestrator start "From <sender>:".
The database is opened read-only. Uses internal Codex tables, tested on codex-cli 0.166.0.
"""
import argparse, os, re, sqlite3, time

ap = argparse.ArgumentParser()
ap.add_argument('--codex-home', default=os.environ.get('CODEX_HOME', '~/.codex'))
ap.add_argument('--state-dir', required=True)
ap.add_argument('--maxlen', type=int, default=420)
ap.add_argument('threads', nargs='+', help='NAME=THREAD_UUID')
args = ap.parse_args()
DB = os.path.join(os.path.expanduser(args.codex_home), 'thread_history_1.sqlite')
THREADS = {uuid: name for name, uuid in (t.split('=', 1) for t in args.threads)}
STATE = os.path.expanduser(args.state_dir)
os.makedirs(STATE, exist_ok=True)
FULLLEN = 8000


def q(sql, params=()):
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True, timeout=5)
    try:
        return con.execute(sql, params).fetchall()
    finally:
        con.close()


def say(s):
    print(s.replace('\n', ' / '), flush=True)


def state_file(th):
    return os.path.join(STATE, f'watch.{th[:8]}.state')


last, turn = {}, {}
for th, name in THREADS.items():
    if not q('select 1 from thread_items where thread_id=? limit 1', (th,)):
        say(f'warning: {name} ({th}) has no items in {DB}. Check the thread ID and the Codex home.')
    try:
        last[th] = int(open(state_file(th)).read().strip())
    except Exception:
        last[th] = q('select max(rollout_ordinal) from thread_items where thread_id=?', (th,))[0][0] or 0
    turn[th] = None
while True:
    for th, name in THREADS.items():
        try:
            rows = q("""select rollout_ordinal, created_at_ms, item_type,
                        coalesce(json_extract(item_json,'$.text'), json_extract(item_json,'$.content[0].text'), '')
                        from thread_items where thread_id=? and rollout_ordinal>?
                        and item_type in ('userMessage','agentMessage') order by rollout_ordinal""", (th, last[th]))
            for ordn, ms, kind, text in rows:
                t = time.strftime('%H:%M:%S', time.localtime(ms / 1000))
                text = (text or '').strip()
                if kind == 'agentMessage':
                    who = name
                elif re.match(r'From [^:\n]{1,60}:', text):
                    who = f'{text[5:text.index(":")]}->{name}'
                else:
                    who = f'Author->{name}'
                full = who.startswith('Author')
                lim = FULLLEN if full else args.maxlen
                say(f'[{t}] {who}: {text[:lim]}{" …(cut)" if len(text) > lim else ""}')
                last[th] = ordn
            if rows:
                open(state_file(th), 'w').write(str(last[th]))
            cur = q('select turn_id, status from thread_turns where thread_id=? order by rowid desc limit 1', (th,))
            cur = cur[0] if cur else None
            if cur != turn[th]:
                if turn[th] is not None:
                    say(f'[{time.strftime("%H:%M:%S")}] {name} turn {cur[0][:8]} {cur[1]}')
                turn[th] = cur
        except Exception as e:
            say(f'[{time.strftime("%H:%M:%S")}] watch error ({name}): {e}')
            time.sleep(30)
    time.sleep(15)
