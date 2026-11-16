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
  (git / commits / commitlint),
  [`hexalith-mcpcli-migration-instructions.md`](./hexalith-mcpcli-migration-instructions.md)
  (versioned MCP/CLI migration index, frozen implementations and owner gates)
- **Shared skills** — reusable agent skills, kept byte-for-byte identical under
  `.claude/skills/` (Claude) and `.agents/skills/` (Codex and other agents):
  - `pushall` — commit, merge, push, and prune across a repository and its
    root-declared submodules (explicit `/pushall` invocation only); also mirrored
    byte-for-byte under `.github/skills/` for GitHub Copilot
  - `aspire` — orchestrate the local distributed topology with the Aspire CLI
  - `playwright-cli` — browser automation for functional testing of running
    resources

## MCP and CLI migration

`Hexalith.McpCli` is the target Hexalith-owned MCP server and CLI. Follow the
[ownership rule](./hexalith-llm-instructions.md#hexalith-mcp-and-cli-ownership)
and [migration plan 1.2.0](./hexalith-mcpcli-migration-instructions.md) for
decorated Contracts, frozen legacy servers, plug-ins and CLIs, and the
outstanding administration scope. Retained implementations receive only safety
and continuity fixes while their approval, authorization, behavior and
retirement gates remain open; they are migration sources, never new-module
templates.

## Commit validation

Use the integrity-locked commitlint tools and policy supplied by the released
Hexalith.Builds pin, rather than installing validation dependencies in this
repository. Before creating a commit, validate its exact full message with the
shared `Github/lib/guard_tools.py` tools and preserve the successful result.
The shared policy rejects CI skip markers and trailers as well as invalid
Conventional Commits.

After adoption, use Python 3.12 or later, Node.js 24 or later and npm. From the
standalone module root, pass the saved message file as the argument below. The
wrapper removes the downloaded tools when validation exits; it requires network
access to install and verify the pinned npm tools.

```bash
run-with-temp python3 - /absolute/path/to/message.txt <<'PY'
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path("references/Hexalith.Builds/Github/lib").resolve()))
from guard_tools import Tools

scratch = Path(os.environ["TMPDIR"]) / "commitlint"
scratch.mkdir()
Tools(scratch).lint_message(Path(sys.argv[1]).read_text(encoding="utf-8"), "candidate")
print("Commit message validation passed.")
PY
```

After Hexalith.CiCd adoption, commit the product changes and run
`python3 references/Hexalith.Builds/check.py` successfully before every push.
Run it from this repository's root in a standalone clone, where Builds is a
direct submodule at its committed pin. It checks the committed perimeter and
commit messages; this documentation/skills repository has no .NET solution,
product tests, packages or containers. Never initialize a nested submodule in an
umbrella checkout to run it. Before adoption, follow the existing required gates;
any substitute preparation proof requires an explicit, repository-specific
approval in Hexalith.CiCd.
