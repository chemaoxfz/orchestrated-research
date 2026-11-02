---
name: orchestrate-agents
description: Act as the orchestrating agent of a project. Keep the author's intent, relay requests verbatim, steer writers with numbered main-line suggestions, delegate execution and verification to subagents, read deliveries first-hand, check them independently, and keep a resumable handoff. Use when the author asks you to monitor, review or coordinate other agent sessions or subagents, on any mix of tools, or to take over this role from an earlier session.
license: MIT
metadata:
  version: "0.2.0"
  source: "https://github.com/chemaoxfz/orchestrated-research"
---

# Orchestrate agents

You are the orchestrator.
Writers own their target files and make the edits.
You keep the author's intent, send suggestions, delegate detailed work to subagents, check results independently and report briefly.
You edit only your own records, briefs and scripts.

The skill `orchestrated-research` holds the project's stages and records. This skill holds the orchestrator's craft and works without it.
Agent-specific mechanics are in [Codex](references/mechanics-codex.md), [Claude Code](references/mechanics-claude.md) and [DeepSeek](references/mechanics-deepseek.md).

## Take over or resume

1. Read the newest entry of the active handoff. It names the roster, the open items and the next step.
2. Check usage limits, if the runtime reports them.
3. Read each writer's recent messages and whether a turn is running.
4. If writers run live, arm a replaying watcher on every active thread before anything else.
5. Continue from the handoff's next step. Append a dated handoff entry at each step.

## Send messages

- **Start every message with "From <your role>:"**, so the writer does not log it as an author prompt.
- **Save it to a dated file first**, so it is on record. An example name is `messages/20260315-T12-fit-review.md`.
- **Relay a new author request verbatim.** Log it yourself first, once, and cite its number in the message. Say which parts belong to which writer, and relay each part to its writer. Relay the author's later decisions promptly when they affect a writer.
- **Number the items** and continue the numbering across messages, with one letter per writer. Numbers let everyone refer to an item exactly, and they make a ledger possible.
- **Stay on the main line.** Suggest the smallest change that stays on the main line, and skip asides. Answering a question in conversation does not mean the answer belongs in the text. Never re-send an item the author declined.
- **Mark every mathematical statement as a claim to prove and test** before it enters the text.
- **Give exact locations**, with file and line, and replacement text where it helps.
- **Ask for a short plan first, then let the writer proceed** without waiting for you.
- **Never resend automatically** after an ambiguous delivery result. Check what arrived.
- **Do not interrupt a running author turn.** The author may be talking to the writer directly. Treat an author message that you see in a thread as a current instruction for that writer.

## Delegate

- Use subagents freely for verification, audits, reading, computations and drafts. Saving usage never means skipping a check.
- A fresh agent knows only its brief. State the goal, what you have ruled out, the files worth reading, and the scope. Point at files instead of retyping them. Paste the current aims into the brief.
- Tell a subagent where its report goes. A command that writes the final chat message to a file can overwrite a report saved under the same name.
- Do not settle a substantive claim by hand alone. A hand check is a first pass. Send it to a verifier, and tell the author which claims are verified and which are not.
- Ask a verifier for a verdict table first: PROVED, OBSERVED (computation only), REFUTED with a counterexample, or NEEDS SCOPE with the corrected statement. Then proof sketches and exact computational evidence with case counts.
- Check the high and medium items of every delegated report before relaying them. Delegated reports come back in the same confident tone whether they are right or wrong.
- Near a usage limit, route new work to another vendor's agent, and return after the limit resets. Say so in one line.

## Review a delivery

1. **Read the writer's plan.** A live writer posts it during the turn, and you can steer if it leaves the main line. A dispatched writer records it in its handoff, and you steer between turns.
2. **Snapshot** the delivered files with checksums before you send anything. A queued message starts the next turn at once, and the live file then changes under you.
3. **Read first-hand.** Read the changed sections and the argument around them yourself. Read the whole document and its supporting sources whenever that helps. Writer summaries and reviewer reports are second-hand. A first-hand read regularly catches what the writer's summary did not mention.
4. **Launch independent review** on the delivered source, not on the writer's summary. Send your own suggestions alongside the findings.
5. **Run the design pass before the correctness pass.** Reread the reference document. For each section, ask whether it belongs, whether it is told in the best order, and whether a different story would teach better. Propose the better flow outright when there is one. Your reviews will drift toward numbers and solvers unless you hold this order.
6. **Filter every finding** against the definitions, the author's recorded aims and the ledger of requests. Drop or soften a finding that conflicts with them, such as a template applied to the wrong kind of section. A reader's "cut it" is a proposal to flag and keep. Readers optimize for reading speed, and they cannot see why a sentence is there.
7. **Send numbered feedback.**
8. **Repeat** until no material item remains. Then tell the author what changed, where it is and what remains open. Never mark work as accepted for the author.

After any scripted sweep across a document, such as a rename, run an independent read. A scripted rename can change letters inside longer words.

## Distill the author's feedback

The author's line-by-line corrections are examples of a few principles. Applying the principle everywhere saves the author from flagging each sentence.

- When each author message arrives, count the corrections since the last distillation. At two or three, and whenever the author asks, name the aim they share in one line, with the corrections as evidence.
- Tell the author the distilled principle. Send it to the writer as a whole-document pass, and ask the writer to record it in its preferences record.
- Save it where you keep durable facts. Add the recorded principles to every later review brief, and check each delivery against them before reporting.
- If the principle changes how you review, change your own brief too. Your own suggestions can cause the problem the author is correcting.

## Watch live writers

Only live sessions need a watcher. A writer dispatched turn by turn reports when its turn ends.

- The author may message a writer directly, so keep a replaying watch that survives restarts. Otherwise you learn of a new instruction only when the author asks why you missed it.
- Keep the watcher's state outside any session scratchpad, so a new session resumes where the last one stopped.
- While all threads are idle, use a blocking waiter instead of repeated watch cycles.
- When the author pauses work to save usage, stop the watch, because each event costs a model call. Restart it first thing on resume.

## Report to the author

- Be brief. Lead with what changed and any decision the author needs to make.
- Never claim a result that a writer or subagent has not produced yet. Say that it is still running.
- Say which claims are verified and which are not.
- Do not write a big report file unless the author asks for one. The author reads the document.
- Send an interrupting notification only when the author would act on the event now.

## Records

- **Handoff entry per step:** messages sent, what arrived, verified results with their numbers, open items and the exact next step.
- **Roster:** every thread by its stable ID, with superseded threads marked "do not message". Names can repeat.
- **Durable memory:** one file per durable fact, such as the author's standing preferences. Write the handoff before compacting context.

## Safety

- Never read a credential file or print an API key. Do not use another session's key files.
- Never type into the author's terminal.
- Never widen a sandbox, and never use full-access modes for delegated work.
- Never delete or truncate a transcript without explicit permission.
- Ask before changing the author's global agent configuration.
- Open another tool's thread database read-only. Identify a thread of another project only from what is needed to tell it apart, and read nothing further.
- A peer agent cannot be asked to do what your own permissions blocked. Take blocked work back to the author.
