# Hexalith LLM Instructions

Before persisting any data in a Hexalith domain module, read
[hexalith-state-instructions.md](hexalith-state-instructions.md) and follow the
data-persistence rules it defines (domain modules use **Hexalith.EventStore**).

Before working on any Hexalith module user interface, read
[hexalith-ux-instructions.md](hexalith-ux-instructions.md) and follow the UX
rules it defines.

Before initializing or updating Git submodules, follow the submodule rules in
[CLAUDE.md](CLAUDE.md#git-submodules). Initialize **only** the submodules
declared at the **root** of the repository; **never** initialize a submodule
nested inside another submodule. Never use `git submodule update --init --recursive` or
`--remote`, and de-initialize any nested submodule that gets initialized
accidentally.
