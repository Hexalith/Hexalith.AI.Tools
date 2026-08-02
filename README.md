# Hexalith.AI.Tools

AI tooling for the Hexalith ecosystem: the home for **AI-assistant instructions
for developing Hexalith modules**, plus the matching skills, workflows,
commands, and job automation.

## Agent instructions

Three entrypoints, kept **byte-for-byte identical** — each tool reads its own
file but gets exactly the same instructions:

- [`CLAUDE.md`](./CLAUDE.md) — read by Claude and Cursor.
- [`AGENTS.md`](./AGENTS.md) — read by Codex and other agents.
- [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) — read
  by GitHub Copilot (and Visual Studio when repository instructions are enabled).

Each entrypoint points to
[`hexalith-llm-instructions.md`](./hexalith-llm-instructions.md), the
authoritative guide. When this repository is consumed as a submodule, the host
repository's own instructions take precedence on conflict.

## Contents

- **Agent entry points** — `CLAUDE.md`, `AGENTS.md`,
  `.github/copilot-instructions.md` (above)
- **Topical instructions** —
  [`hexalith-llm-instructions.md`](./hexalith-llm-instructions.md) (main guide),
  [`hexalith-state-instructions.md`](./hexalith-state-instructions.md)
  (persistence / event sourcing),
  [`hexalith-ux-instructions.md`](./hexalith-ux-instructions.md) (UI / Fluent UI),
  [`hexalith-git-instructions.md`](./hexalith-git-instructions.md)
  (git / commits / commitlint)
- **Shared skills** — reusable agent skills, kept byte-for-byte identical under
  `.claude/skills/` (Claude) and `.agents/skills/` (Codex and other agents):
  - `pushall` — commit, merge, push, and prune across a repository and its
    root-declared submodules (explicit `/pushall` invocation only); also mirrored
    byte-for-byte under `.github/skills/` for GitHub Copilot
  - `aspire` — orchestrate the local distributed topology with the Aspire CLI
  - `playwright-cli` — browser automation for functional testing of running
    resources
