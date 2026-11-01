#!/usr/bin/env python3
"""Print a Codex thread's recent messages and its turn status.

    read_thread.py --thread UUID [--codex-home ~/.codex] [-n 5] [--maxlen 2000]

The database is opened read-only. Uses internal Codex tables, tested on codex-cli 0.166.0.
"""
import argparse
import os
import sqlite3
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--thread", required=True)
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"))
    parser.add_argument("-n", type=int, default=5)
    parser.add_argument("--maxlen", type=int, default=2000)
    args = parser.parse_args()
    db = os.path.join(os.path.expanduser(args.codex_home), "thread_history_1.sqlite")
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=5)
    rows = con.execute(
        """select created_at_ms, item_type,
                  coalesce(json_extract(item_json,'$.text'), json_extract(item_json,'$.content[0].text'), '')
           from thread_items where thread_id=? and item_type in ('userMessage','agentMessage')
           order by rollout_ordinal desc limit ?""",
        (args.thread, args.n),
    ).fetchall()
    turn = con.execute(
        "select turn_id, status from thread_turns where thread_id=? order by rowid desc limit 1", (args.thread,)
    ).fetchone()
    for created, kind, text in reversed(rows):
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created / 1000))
        who = "agent" if kind == "agentMessage" else "to agent"
        text = (text or "").strip()
        print(f"[{stamp}] {who}: {text[:args.maxlen]}{' ...(cut)' if len(text) > args.maxlen else ''}\n")
    print(f"last turn: {turn[0]} {turn[1]}" if turn else "no turns recorded")


if __name__ == "__main__":
    main()
