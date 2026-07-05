# Hexalith LLM Instructions

Before persisting any data in a Hexalith domain module, read
[hexalith-state-instructions.md](hexalith-state-instructions.md) and follow the
data-persistence rules it defines (domain modules use **Hexalith.EventStore**).

Before working on any Hexalith module user interface, read
[hexalith-ux-instructions.md](hexalith-ux-instructions.md) and follow the UX
rules it defines.

When adding or changing C# code, keep each `.cs` file focused on a single C#
object/type. Move additional classes, records, structs, interfaces, enums, and
delegates into their own files named for the object/type.

Before initializing or updating Git submodules, follow the submodule rules in
[CLAUDE.md](CLAUDE.md#git-submodules). Initialize **only** the submodules
declared at the **root** of the repository; **never** initialize a submodule
nested inside another submodule. Never use `git submodule update --init --recursive` or
`--remote`, and de-initialize any nested submodule that gets initialized
accidentally.

Before committing anything, follow the commit-message rules in
[CLAUDE.md](CLAUDE.md#commit-messages). **Every** commit — including submodule /
subproject reference bumps and dependency updates — must start with a
Conventional Commits `type:` prefix (e.g.
`chore(deps): bump Hexalith.Memories submodule to 27bebfa`), or commitlint fails
with `type-empty` / `subject-empty`. Never use git's default
`Update subproject reference …` message verbatim.
