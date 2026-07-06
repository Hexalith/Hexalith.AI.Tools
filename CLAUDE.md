# AI Assistant Instructions for Developing Hexalith Modules

This file is the **authoritative, self-contained guide** for AI assistants
(Claude, Codex, Copilot, Cursor, …) developing **Hexalith .NET modules**.
`Hexalith.AI.Tools` is the home for these instructions (and for the matching
skills, workflows, commands, and job automation). When this repository is
referenced as a submodule from a Hexalith module, treat this file as the
baseline; the consuming repository's own instructions may add module-specific
rules that take precedence on conflict.

**Do not modify the AI-assistant entrypoint files.** `CLAUDE.md` (Claude),
`AGENTS.md` (Codex / agents), and `.github/copilot-instructions.md` (GitHub
Copilot) are kept **byte-for-byte identical** — each tool reads its own file but
gets exactly the same instructions. Never edit any of them as part of ordinary
module work, in this repository or in a consuming module; when these
instructions must change, update all three together as a deliberate, separate
task.
