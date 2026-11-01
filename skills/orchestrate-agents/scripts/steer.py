#!/usr/bin/env python3
"""Send a message into a running Codex turn through the app-server daemon (turn/steer).

The daemon speaks WebSocket on its Unix control socket (JSON-RPC without the "jsonrpc" field).
turn/steer requires expectedTurnId to equal the active turn, so it never starts a new turn.
With no active turn the script refuses; use `codex queue` then.

  steer.py --thread UUID --probe              initialize and list loaded threads (read-only)
  steer.py --thread UUID --message-file FILE  steer the active turn with FILE's text

Set CODEX_HOME for a second account. Uses internal Codex interfaces, tested on codex-cli 0.166.0.
"""
import argparse, base64, json, os, re, socket, sqlite3, struct, sys, time

DB = os.path.expanduser(os.environ.get("CODEX_HOME", "~/.codex") + "/thread_history_1.sqlite")


def active_turn(thread):
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=30)
    row = con.execute(
        "select turn_id from thread_turns where thread_id=? and status='inProgress' "
        "order by rollout_ordinal desc limit 1",
        (thread,),
    ).fetchone()
    return row[0] if row else None


class Proxy:
    """Minimal WebSocket client on the daemon's Unix control socket."""

    def __init__(self):
        path = os.path.realpath(os.path.expanduser(os.environ.get("CODEX_HOME", "~/.codex") + "/app-server-control/app-server-control.sock"))
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.settimeout(30)
        self.s.connect(path)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(("GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            head += self.s.recv(1)
        if b" 101 " not in head.split(b"\r\n", 1)[0]:
            raise ConnectionError(head.decode(errors="replace"))

    def _frame(self, opcode, payload):
        n = len(payload)
        if n < 126:
            hdr = struct.pack("!BB", 0x80 | opcode, 0x80 | n)
        elif n < 65536:
            hdr = struct.pack("!BBH", 0x80 | opcode, 0x80 | 126, n)
        else:
            hdr = struct.pack("!BBQ", 0x80 | opcode, 0x80 | 127, n)
        mask = os.urandom(4)
        self.s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def send(self, obj):
        self._frame(0x1, json.dumps(obj).encode())

    def _exact(self, n):
        out = b""
        while len(out) < n:
            chunk = self.s.recv(n - len(out))
            if not chunk:
                raise ConnectionError("socket closed")
            out += chunk
        return out

    def _message(self):
        data = b""
        while True:
            b0, b1 = self._exact(2)
            n = b1 & 0x7F
            if n == 126:
                n = struct.unpack("!H", self._exact(2))[0]
            elif n == 127:
                n = struct.unpack("!Q", self._exact(8))[0]
            mask = self._exact(4) if b1 & 0x80 else None
            payload = self._exact(n)
            if mask:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
            op = b0 & 0x0F
            if op == 0x9:
                self._frame(0xA, payload)
                continue
            if op == 0x8:
                raise ConnectionError("server closed the connection")
            data += payload
            if b0 & 0x80:
                return data

    def wait_for(self, rid, timeout=30):
        end = time.time() + timeout
        while time.time() < end:
            msg = json.loads(self._message())
            if msg.get("id") == rid and ("result" in msg or "error" in msg):
                return msg
        raise TimeoutError(f"no response to id {rid}")

    def close(self):
        try:
            self._frame(0x8, b"")
        finally:
            self.s.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread", required=True, help="thread UUID. Use the UUID, because names can repeat.")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--message-file")
    a = ap.parse_args()
    if not a.probe and not a.message_file:
        ap.error("give --probe or --message-file")

    text = None
    turn = None
    if a.message_file:
        text = open(a.message_file).read().strip()
        if not re.match(r"From [^:\n]{1,60}:", text):
            sys.exit("message must start with 'From <sender>:'")
        turn = active_turn(a.thread)
        if not turn:
            sys.exit("no active turn: use `codex queue` instead")

    px = Proxy()
    try:
        px.send({"id": 1, "method": "initialize",
                 "params": {"clientInfo": {"name": "orchestrate-agents", "title": "orchestrate-agents supervisor",
                                           "version": "0.1.0"}}})
        print("initialize:", "ok" if "result" in px.wait_for(1) else "error")
        px.send({"method": "initialized"})
        if a.probe:
            px.send({"id": 2, "method": "thread/loaded/list", "params": {}})
            r = px.wait_for(2)
            ids = r.get("result", {}).get("data", r.get("result"))
            print("loaded threads:", json.dumps(ids)[:600])
            print("target loaded:", a.thread in json.dumps(ids))
        else:
            px.send({"id": 3, "method": "turn/steer",
                     "params": {"threadId": a.thread, "expectedTurnId": turn,
                                "input": [{"type": "text", "text": text, "text_elements": []}]}})
            r = px.wait_for(3)
            print("turn/steer:", json.dumps(r.get("result", r.get("error")))[:600])
    finally:
        px.close()


if __name__ == "__main__":
    main()
