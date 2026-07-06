# Hexalith LLM Instructions

> **Authoring rule for this file:** Keep it self-contained. Reference **only**
> the topical instruction files that live in this same folder
> (`references/Hexalith.AI.Tools/`, e.g. `hexalith-state-instructions.md` and
> `hexalith-ux-instructions.md`). Never link to a file outside this folder, and
> never link to the agent-instruction entry points that already point here
> (`CLAUDE.md`, `AGENTS.md`, GitHub Copilot instruction files) — those create a
> circular reference. If a rule lives elsewhere, inline it here instead of
> linking out.

Before persisting any data in a Hexalith domain module, read
[hexalith-state-instructions.md](hexalith-state-instructions.md) and follow the
data-persistence rules it defines (domain modules use **Hexalith.EventStore**).

Before working on any Hexalith module user interface, read
[hexalith-ux-instructions.md](hexalith-ux-instructions.md) and follow the UX
rules it defines.

When adding or changing C# code, keep each `.cs` file focused on a single C#
object/type. Move additional classes, records, structs, interfaces, enums, and
delegates into their own files named for the object/type.

Before initializing or updating Git submodules, initialize **only** the
submodules declared in **references/** of the repository; **never** initialize a
submodule nested inside another submodule. Never use
`git submodule update --init --recursive` or `--remote`, and de-initialize any
nested submodule that gets initialized accidentally.

Work on the **`main`** branch by default. Only create or switch to another
branch when the task genuinely requires it.

Before committing anything, use a Conventional Commits message and comply to commitlint check. **Every**
commit — including submodule / subproject reference bumps and dependency
updates — must start with a Conventional Commits `type:` prefix (e.g.
`chore(deps): bump Hexalith.Memories submodule to 27bebfa`), or commitlint fails
with `type-empty` / `subject-empty`. Never use git's default
`Update subproject reference …` message verbatim.
