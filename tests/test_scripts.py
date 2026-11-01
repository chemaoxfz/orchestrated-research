"""Offline tests for the scripts. Stub executables stand in for codex, claude and dsh.

    python3 -m unittest discover -s tests
"""
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "orchestrated-research" / "scripts"

# Each stub records its argv and stdin, then prints what the real tool prints.
STUBS = {
    "codex": r"""#!/bin/sh
printf '%s\n' "$*" >> "$STUB_LOG"; cat >> "$STUB_LOG"; echo >> "$STUB_LOG"
if [ "$STUB_FAIL" = 1 ]; then echo '{"type":"turn.failed","error":{"message":"out of quota"}}'; exit 1; fi
echo '{"type":"thread.started","thread_id":"thread-codex-1"}'
echo '{"type":"item.completed","item":{"type":"agent_message","text":"note"}}'
echo '{"type":"item.completed","item":{"type":"agent_message","text":"codex reply"}}'
""",
    "claude": r"""#!/bin/sh
printf '%s\n' "$*" >> "$STUB_LOG"; cat >> "$STUB_LOG"; echo >> "$STUB_LOG"
echo '{"type":"result","is_error":false,"session_id":"session-claude-1","result":"claude reply"}'
""",
    "dsh": r"""#!/bin/sh
printf '%s\n' "$*" >> "$STUB_LOG"; cat >> "$STUB_LOG"; echo >> "$STUB_LOG"
echo '{"type":"session","sessionId":"session-dsh-1","cwd":"x"}'
echo '{"type":"text","text":"working"}'
echo '{"type":"status","phase":"turn_end","turn":1,"reason":{"kind":"completed"}}'
echo '{"type":"final","text":"dsh reply"}'
""",
}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.project = self.dir / "proj"
        self.bin = self.dir / "bin"
        self.bin.mkdir()
        for name, body in STUBS.items():
            path = self.bin / name
            path.write_text(body)
            path.chmod(path.stat().st_mode | stat.S_IEXEC)
        self.stub_log = self.dir / "stub.log"
        self.env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}", STUB_LOG=str(self.stub_log))
        done = self.run_py(SCRIPTS / "init_project.py", str(self.project), "--title", "Test Title", "--slug", "demo", "--reader", "a physicist", "--backend", "codex")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.msg = self.project / "m.md"
        self.msg.write_text("From orchestrator: hello\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_py(self, script, *args, env=None, cwd=None):
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, env=env or self.env, cwd=cwd or self.dir)

    def role(self, *args, env=None):
        return self.run_py(self.project / "tools" / "role.py", *args, env=env, cwd=self.project)

    def roster(self):
        return json.loads((self.project / "roles" / "roster.json").read_text())


class TestInit(Base):
    def test_scaffold(self):
        for name in ("AGENTS.md", "PROMPT-LOG.md", "demo-tutorial.tex", "demo-technical.tex", "roles/tutorial-writer/CHARTER.md", ".claude/agents/verifier.md", ".codex/agents/technical-writer.toml", "tools/role.py"):
            self.assertTrue((self.project / name).exists(), name)
        self.assertIn("a physicist", (self.project / "AGENTS.md").read_text())
        self.assertNotIn("{{", (self.project / "macro.tex").read_text())
        self.assertIn("demo-technical.pdf", (self.project / "macro.tex").read_text())
        self.assertEqual(self.roster()["roles"]["tutorial-writer"]["backend"], "codex")

    def test_memory_link_points_at_role_folder(self):
        link = self.project / ".claude" / "agent-memory" / "tutorial-writer"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), (self.project / "roles" / "tutorial-writer").resolve())

    def test_rerun_never_overwrites(self):
        state = self.project / "PROJECT_STATE.md"
        state.write_text("mine\n")
        done = self.run_py(SCRIPTS / "init_project.py", str(self.project), "--title", "Other", "--slug", "demo", "--reader", "r")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(state.read_text(), "mine\n")

    def test_agent_files_parse(self):
        for path in (self.project / ".claude" / "agents").glob("*.md"):
            self.assertTrue(path.read_text().startswith(f"---\nname: {path.stem}\n"))
        try:
            import tomllib
        except ImportError:  # Python below 3.11 has no TOML parser in its standard library.
            return
        for path in (self.project / ".codex" / "agents").glob("*.toml"):
            data = tomllib.loads(path.read_text())
            self.assertEqual(data["name"], path.stem)
            self.assertTrue(data["developer_instructions"].strip())

    def test_protected_agent_folder_only_warns(self):
        other = self.dir / "sandboxed"
        (other / ".codex").mkdir(parents=True)
        (other / ".codex").chmod(0o555)
        try:
            done = self.run_py(SCRIPTS / "init_project.py", str(other), "--title", "T", "--slug", "demo", "--reader", "r")
        finally:
            (other / ".codex").chmod(0o755)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("could not write .codex/agents", done.stdout)
        self.assertTrue((other / "tools" / "records.py").exists())
        for role in ("tutorial-writer", "technical-writer", "fresh-reader", "verifier"):
            self.assertTrue((other / ".claude" / "agents" / f"{role}.md").exists(), role)
        self.assertTrue((other / ".claude" / "agent-memory" / "tutorial-writer").is_symlink())

    def test_special_characters_in_a_title_stay_buildable(self):
        other = self.dir / "special"
        done = self.run_py(SCRIPTS / "init_project.py", str(other), "--title", "Enzymes & 100% control", "--slug", "demo", "--reader", "r")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn(r"Enzymes \& 100\% control", (other / "demo-tutorial.tex").read_text())
        self.assertIn("Enzymes & 100% control", (other / "PROJECT_STATE.md").read_text())

    def test_one_model_refused_for_mixed_backends(self):
        done = self.run_py(SCRIPTS / "init_project.py", str(self.dir / "mixed"), "--title", "T", "--slug", "demo", "--reader", "r",
                           "--tutorial-backend", "claude", "--technical-backend", "codex", "--model", "some-model")
        self.assertEqual(done.returncode, 2)
        self.assertIn("different backends", done.stderr)


class TestRole(Base):
    def test_refuses_message_without_sender(self):
        bad = self.project / "bad.md"
        bad.write_text("hello\n")
        done = self.role("send", "tutorial-writer", "--message-file", str(bad))
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("From <sender>", done.stderr)
        self.assertFalse(self.stub_log.exists())

    def test_refuses_message_not_on_file(self):
        done = self.role("send", "tutorial-writer", "--message-file", "nope.md")
        self.assertNotEqual(done.returncode, 0)

    def test_codex_first_turn_then_resume(self):
        self.assertEqual(self.role("send", "tutorial-writer", "--message-file", str(self.msg)).returncode, 0)
        self.assertEqual(self.roster()["roles"]["tutorial-writer"]["thread"], "thread-codex-1")
        self.assertEqual((self.project / "roles" / "tutorial-writer" / "last-reply.md").read_text().strip(), "codex reply")
        first = self.stub_log.read_text()
        self.assertIn("exec --json", first)
        self.assertIn("CHARTER.md", first)
        self.stub_log.unlink()
        self.assertEqual(self.role("send", "tutorial-writer", "--message-file", str(self.msg)).returncode, 0)
        second = self.stub_log.read_text()
        self.assertIn("exec resume thread-codex-1", second)
        self.assertIn('sandbox_mode="workspace-write"', second)

    def test_claude_backend(self):
        self.role("set", "tutorial-writer", "--backend", "claude")
        self.assertEqual(self.role("send", "tutorial-writer", "--message-file", str(self.msg)).returncode, 0)
        self.assertEqual(self.roster()["roles"]["tutorial-writer"]["thread"], "session-claude-1")
        self.assertIn("--agent tutorial-writer", self.stub_log.read_text())
        self.stub_log.unlink()
        self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        self.assertIn("--resume session-claude-1", self.stub_log.read_text())

    def test_dsh_backend_and_final_event(self):
        self.role("set", "tutorial-writer", "--backend", "dsh")
        self.assertEqual(self.role("send", "tutorial-writer", "--message-file", str(self.msg)).returncode, 0)
        self.assertEqual(self.roster()["roles"]["tutorial-writer"]["thread"], "session-dsh-1")
        self.assertEqual((self.project / "roles" / "tutorial-writer" / "last-reply.md").read_text().strip(), "dsh reply")

    def test_dsh_refuses_full_access(self):
        self.role("set", "tutorial-writer", "--backend", "dsh", "--env", "DSH_PERMISSION_MODE=danger-full-access")
        done = self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        self.assertNotEqual(done.returncode, 0)
        self.assertFalse(self.stub_log.exists())

    def test_failure_is_recorded_and_not_resent(self):
        env = dict(self.env, STUB_FAIL="1")
        done = self.role("send", "tutorial-writer", "--message-file", str(self.msg), env=env)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.stub_log.read_text().count("From orchestrator"), 1)
        self.assertEqual(self.roster()["roles"]["tutorial-writer"]["last_turn"]["status"], "failed")

    def test_lock_blocks_second_turn_and_clears_when_stale(self):
        lock = self.project / "roles" / "tutorial-writer" / ".lock"
        lock.write_text(f"{os.getpid()} now\n")
        done = self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        self.assertEqual(done.returncode, 3)
        lock.write_text("999999 stale\n")
        self.assertEqual(self.role("send", "tutorial-writer", "--message-file", str(self.msg)).returncode, 0)
        self.assertFalse(lock.exists())

    def test_rehydrate_keeps_history_and_starts_fresh(self):
        self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        self.role("rehydrate", "tutorial-writer", "--backend", "claude", "--reason", "quota")
        role = self.roster()["roles"]["tutorial-writer"]
        self.assertIsNone(role["thread"])
        self.assertEqual(role["backend"], "claude")
        self.assertEqual(role["history"][-1]["thread"], "thread-codex-1")
        self.stub_log.unlink()
        self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        log = self.stub_log.read_text()
        self.assertNotIn("--resume", log)
        self.assertIn("CHARTER.md", log)

    def test_moving_backend_clears_the_old_model_and_flags(self):
        self.role("set", "tutorial-writer", "--backend", "codex", "--model", "codex-model", "--args", "-c", "x=1")
        done = self.role("rehydrate", "tutorial-writer", "--backend", "claude", "--reason", "out of quota")
        self.assertIn("cleared model and args", done.stdout)
        role = self.roster()["roles"]["tutorial-writer"]
        self.assertIsNone(role["model"])
        self.assertEqual(role["args"], [])
        printed = self.role("send", "tutorial-writer", "--message-file", str(self.msg), "--dry-run").stdout
        self.assertNotIn("codex-model", printed)
        self.assertNotIn("x=1", printed)

    def test_empty_model_clears_it(self):
        self.role("set", "tutorial-writer", "--model", "some-model")
        self.role("set", "tutorial-writer", "--model", "")
        self.assertIsNone(self.roster()["roles"]["tutorial-writer"]["model"])

    def test_claude_gets_build_tools_unless_set(self):
        self.role("set", "tutorial-writer", "--backend", "claude")
        printed = self.role("send", "tutorial-writer", "--message-file", str(self.msg), "--dry-run").stdout
        self.assertIn("--allowedTools Bash(latexmk *)", printed)
        self.role("set", "tutorial-writer", "--args", "--allowedTools", "Bash(make *)")
        printed = self.role("send", "tutorial-writer", "--message-file", str(self.msg), "--dry-run").stdout
        self.assertIn("Bash(make *)", printed)
        self.assertNotIn("latexmk", printed)

    def test_dsh_says_when_a_model_is_not_applied(self):
        self.role("set", "tutorial-writer", "--backend", "dsh", "--model", "some-model")
        done = self.role("send", "tutorial-writer", "--message-file", str(self.msg), "--dry-run")
        self.assertIn("not applied", done.stderr)

    def test_paused_role_is_not_sent_to(self):
        self.role("set", "tutorial-writer", "--status", "paused")
        done = self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        self.assertEqual(done.returncode, 2)
        self.assertIn("paused", done.stderr)
        self.assertFalse(self.stub_log.exists())

    def test_manual_dry_run_records_nothing(self):
        self.role("set", "tutorial-writer", "--backend", "manual")
        self.assertEqual(self.role("send", "tutorial-writer", "--message-file", str(self.msg), "--dry-run").returncode, 0)
        self.assertFalse((self.project / "roles" / "tutorial-writer" / "turns.jsonl").exists())

    def test_manual_backend_only_records(self):
        self.role("set", "tutorial-writer", "--backend", "manual")
        done = self.role("send", "tutorial-writer", "--message-file", str(self.msg))
        self.assertEqual(done.returncode, 0)
        self.assertFalse(self.stub_log.exists())
        self.assertTrue((self.project / "roles" / "tutorial-writer" / "turns.jsonl").exists())

    def test_add_creates_role_files(self):
        self.assertEqual(self.role("add", "figure-writer", "--backend", "codex").returncode, 0)
        self.assertTrue((self.project / "roles" / "figure-writer" / "CHARTER.md").exists())
        self.assertEqual(self.role("add", "figure-writer", "--backend", "codex").returncode, 2)


class TestRecords(Base):
    def records(self, *args):
        return self.run_py(self.project / "tools" / "records.py", *args, cwd=self.project)

    def write_ledger(self, rows):
        path = self.project / "AUTHOR-LEDGER.md"
        path.write_text(path.read_text() + "\n".join(rows) + "\n")

    def test_ledger_accepts_good_rows(self):
        (self.project / "PROMPT-LOG.md").write_text("please  make the figure\nsmaller and clearer\n")
        self.write_ledger(['| A1 | d | "make the figure smaller" | size | K1 | DONE (Stage 2): figure on p. 14 |', '| A2 | d | "clearer" | clarity | K1 | OPEN |'])
        done = self.records("ledger")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("2 rows", done.stdout)

    def test_a_new_project_passes_its_own_checks(self):
        self.assertEqual(self.records("ledger").returncode, 0)
        self.assertEqual(self.records("results").returncode, 0)
        self.assertEqual(self.records("anchors").returncode, 0)

    def test_short_numbered_evidence_passes_and_empty_cells_fail(self):
        (self.project / "PROMPT-LOG.md").write_text("the real words\n")
        self.write_ledger(['| A1 | d | "real words" | x | K1 | DONE page 1 |', '| A2 | d | "" | x | K1 | OPEN |', '| A3 | d | "real words" | x | K1 | SUPERSEDED |'])
        done = self.records("ledger")
        self.assertEqual(done.returncode, 1)
        self.assertNotIn("A1:", done.stdout)
        self.assertIn("A2: the quote is empty", done.stdout)
        self.assertIn("A3: SUPERSEDED needs", done.stdout)

    def test_ledger_catches_bad_quote_status_and_evidence(self):
        (self.project / "PROMPT-LOG.md").write_text("the real words\n")
        self.write_ledger(['| A1 | d | "invented words" | x | K1 | OPEN |', '| A2 | d | "real words" | x | K1 | MAYBE |', '| A3 | d | "real words" | x | K1 | DONE |'])
        done = self.records("ledger")
        self.assertEqual(done.returncode, 1)
        self.assertIn("A1: quote", done.stdout)
        self.assertIn("A2: status", done.stdout)
        self.assertIn("A3: DONE needs evidence", done.stdout)

    def test_snapshot_writes_checksums_and_never_overwrites(self):
        source = self.project / "demo-tutorial.tex"
        self.assertEqual(self.records("snapshot", "stage1", str(source)).returncode, 0)
        target = self.project / "revisions" / "snapshots" / "stage1"
        self.assertTrue((target / "demo-tutorial.tex").exists())
        self.assertIn("demo-tutorial.tex", (target / "SHA256SUMS").read_text())
        self.assertEqual(self.records("snapshot", "stage1", str(source)).returncode, 1)

    def test_snapshot_keeps_subfolders_and_same_names_apart(self):
        (self.project / "figures" / "plot.py").write_text("a\n")
        (self.project / "code" / "plot.py").write_text("b\n")
        done = self.records("snapshot", "both", "figures/plot.py", "code/plot.py")
        self.assertEqual(done.returncode, 0, done.stderr)
        target = self.project / "revisions" / "snapshots" / "both"
        self.assertEqual((target / "figures" / "plot.py").read_text(), "a\n")
        self.assertEqual((target / "code" / "plot.py").read_text(), "b\n")
        self.assertIn("  figures/plot.py", (target / "SHA256SUMS").read_text())

    def test_snapshot_refuses_two_outside_files_with_one_name(self):
        for folder in ("one", "two"):
            (self.dir / folder).mkdir()
            (self.dir / folder / "x.txt").write_text(folder)
        done = self.records("snapshot", "clash", str(self.dir / "one" / "x.txt"), str(self.dir / "two" / "x.txt"))
        self.assertEqual(done.returncode, 1)
        self.assertFalse((self.project / "revisions" / "snapshots" / "clash").exists())

    def test_words_after_a_result_id_are_a_note(self):
        tex = self.project / "demo-tutorial.tex"
        tex.write_text("A claim. % result: R1 median across seeds\nAnother. % result: R1, R2\n")
        (self.project / "RESULTS-LEDGER.md").write_text("| Result | Value |\n| --- | --- |\n| R1 | 3 |\n| R2 | 4 |\n")
        done = self.records("results", str(tex))
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("2 cited", done.stdout)

    def test_anchors_named_in_the_claim_table_must_exist_and_comments_do_not_count(self):
        (self.project / "demo-tutorial.tex").write_text("Text.\n")
        (self.project / "demo-technical.tex").write_text("% \\techanchor{ghost}\n\\techanchor{real}\n")
        design = self.project / "TECHNICAL-DESIGN.md"
        design.write_text(design.read_text() + "\n| Claim | Anchor |\n| --- | --- |\n| one | `real` |\n| two | ghost |\n")
        done = self.records("anchors")
        self.assertEqual(done.returncode, 1)
        self.assertIn("no anchor for ghost", done.stdout)
        self.assertNotIn("no anchor for real", done.stdout)

    def test_results_and_anchors_find_the_pair_by_themselves(self):
        (self.project / "demo-tutorial.tex").write_text("A claim. % result: R1\n\\techref{one}\n")
        (self.project / "demo-technical.tex").write_text("\\techanchor{one}\n")
        (self.project / "RESULTS-LEDGER.md").write_text("| Result | Value |\n| --- | --- |\n| R1 | 3 |\n")
        self.assertEqual(self.records("anchors").returncode, 0)
        done = self.records("results")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("1 cited in sources", done.stdout)

    def test_results_and_anchors(self):
        tex = self.project / "demo-tutorial.tex"
        tex.write_text("A claim. % result: R1, R2\n\\techref[proof]{prop-one}\n\\techref{prop-two}\n")
        ledger = self.project / "RESULTS-LEDGER.md"
        ledger.write_text("| Result | Value | Data |\n| --- | --- | --- |\n| R1 | 3 | synthetic |\n")
        done = self.records("results", str(tex))
        self.assertEqual(done.returncode, 1)
        self.assertIn("R2", done.stdout)
        companion = self.project / "demo-technical.tex"
        companion.write_text("\\techanchor{prop-one}\n")
        done = self.records("anchors", "--tutorial", str(tex), "--companion", str(companion))
        self.assertEqual(done.returncode, 1)
        self.assertIn("prop-two", done.stdout)
        self.assertNotIn("FAIL no anchor for prop-one", done.stdout)


class TestInstaller(unittest.TestCase):
    def run_install(self, home, *args):
        return subprocess.run(["bash", str(ROOT / "install.sh"), *args], capture_output=True, text=True, env=dict(os.environ, HOME=str(home)))

    def test_links_and_uninstalls(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            done = self.run_install(home)
            self.assertEqual(done.returncode, 0, done.stderr)
            link = home / ".claude" / "skills" / "write-tutorial"
            self.assertTrue(link.is_symlink())
            self.assertTrue((link / "SKILL.md").exists())
            self.assertEqual(self.run_install(home).returncode, 0)
            self.assertTrue(link.is_symlink())
            self.assertEqual(self.run_install(home, "--uninstall").returncode, 0)
            self.assertFalse(link.exists())

    def test_copies_can_be_refreshed_and_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(self.run_install(home, "--copy").returncode, 0)
            copy = home / ".claude" / "skills" / "write-tutorial"
            self.assertFalse(copy.is_symlink())
            (copy / "stale.txt").write_text("old")
            done = self.run_install(home, "--copy")
            self.assertNotIn("SKIPPED", done.stderr)
            self.assertFalse((copy / "stale.txt").exists())
            self.assertEqual(self.run_install(home, "--uninstall").returncode, 0)
            self.assertFalse(copy.exists())

    def test_uninstall_reaches_every_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(self.run_install(home, "--all").returncode, 0)
            self.assertTrue((home / ".gemini" / "skills" / "write-tutorial").is_symlink())
            self.assertEqual(self.run_install(home, "--uninstall").returncode, 0)
            self.assertFalse((home / ".gemini" / "skills" / "write-tutorial").exists())

    def test_project_option_needs_a_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = self.run_install(Path(tmp), "--project")
            self.assertEqual(done.returncode, 2)
            self.assertIn("needs a folder", done.stderr)

    def test_never_replaces_someone_elses_skill_or_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            mine = home / "my-own-skill"
            mine.mkdir()
            skills = home / ".claude" / "skills"
            skills.mkdir(parents=True)
            foreign = skills / "orchestrate-agents"
            foreign.symlink_to(mine)
            real = home / ".agents" / "skills" / "simplify-rules"
            real.mkdir(parents=True)
            done = self.run_install(home)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("SKIPPED", done.stderr)
            self.assertEqual(foreign.resolve(), mine.resolve())
            self.assertFalse(real.is_symlink())
            self.assertEqual(self.run_install(home, "--uninstall").returncode, 0)
            self.assertTrue(foreign.is_symlink())
            self.assertTrue(real.is_dir())


class TestPreflight(unittest.TestCase):
    def test_reports_changes_against_the_baseline_and_writes_nothing(self):
        script = ROOT / "skills" / "polish-manuscript" / "scripts" / "manuscript_preflight.py"
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before.tex"
            after = Path(tmp) / "after.tex"
            before.write_text("\\section{Results}\\label{sec:results}\nA claim, see \\ref{sec:results}.\n")
            after.write_text("\\section{Results}\\label{sec:results}\nA claim, see \\ref{sec:gone}.\n\\authornote{fix this}\nThe readout.\n")
            source = after.read_text()
            done = subprocess.run(
                [sys.executable, str(script), "--target", str(after), "--baseline", str(before), "--annotation-macro", "authornote", "--avoid-term", "read-?outs?", "--json"],
                capture_output=True, text=True,
            )
            self.assertEqual(done.returncode, 0, done.stderr)
            report = json.loads(done.stdout)
            self.assertEqual(after.read_text(), source)
            self.assertEqual(sorted(path.name for path in Path(tmp).iterdir()), ["after.tex", "before.tex"])
        self.assertEqual([note["text"] for note in report["unresolved_notes"]], ["fix this"])
        self.assertEqual([ref["key"] for ref in report["unresolved_literal_references"]], ["sec:gone"])
        self.assertTrue(report["terms_to_review"])


class TestRepository(unittest.TestCase):
    """The rules that AGENTS.md states for this repository."""

    EXPECTED = {"orchestrated-research", "orchestrate-agents", "write-tutorial", "write-companion", "iterate-research", "polish-manuscript", "simplify-rules"}

    def skills(self):
        return sorted(path.parent for path in (ROOT / "skills").glob("*/SKILL.md"))

    def test_all_skills_are_present(self):
        self.assertEqual({folder.name for folder in self.skills()}, self.EXPECTED)

    def test_frontmatter_versions_and_metadata_agree(self):
        versions = {json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]}
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        versions.add(market["plugins"][0]["version"])
        for folder in self.skills():
            text = (folder / "SKILL.md").read_text()
            head = text.split("\n---", 1)[0]
            self.assertIn(f"\nname: {folder.name}\n", head, folder.name)
            found = re.search(r'\n\s+version:\s*"?([0-9.]+)"?', head)
            self.assertTrue(found, f"{folder.name} has no version")
            versions.add(found.group(1))
            self.assertLess(len(text.splitlines()), 500, folder.name)
            self.assertIn(f"${folder.name}", (folder / "agents" / "openai.yaml").read_text(), folder.name)
        self.assertEqual(len(versions), 1, versions)

    def test_relative_links_and_anchors_resolve(self):
        def slug(heading):
            heading = re.sub(r"[`*]", "", heading).strip().lower()
            return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", heading))

        pages = [ROOT / "README.md", ROOT / "AGENTS.md"]
        pages += [path for path in (ROOT / "skills").rglob("*.md") if "assets" not in path.parts]
        broken = []
        for page in pages:
            for target in re.findall(r"\]\(([^)\s]+)\)", page.read_text()):
                if re.match(r"[a-z]+:", target):
                    continue
                name, _, anchor = target.partition("#")
                path = (page.parent / name).resolve() if name else page
                if not path.exists():
                    broken.append(f"{page.relative_to(ROOT)}: {target}")
                elif anchor and path.suffix == ".md":
                    headings = re.findall(r"^#+\s+(.+)$", path.read_text(), re.M)
                    if anchor not in {slug(heading) for heading in headings}:
                        broken.append(f"{page.relative_to(ROOT)}: {target} (no such heading)")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
