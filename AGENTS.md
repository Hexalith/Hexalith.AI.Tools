# AGENTS.md — Codex / Agent Instructions for Developing Hexalith Modules

`Hexalith.AI.Tools` holds the AI-agent instructions for developing Hexalith
modules. The **authoritative, self-contained guide is [`CLAUDE.md`](./CLAUDE.md)** —
read it and follow it in full. This file adds only Codex/agent-specific notes; on
any conflict, the consuming repository's own instructions win, then `CLAUDE.md`.

## Read this first

[`CLAUDE.md`](./CLAUDE.md) is the single source of truth. It covers:

- Technology stack (.NET 10+, C# 14+, DAPR, .NET Aspire, Fluent UI Blazor)
- The Hexalith ecosystem and the technical-vs-domain module boundary
- **Git submodule rules** (root-level only; never recursive/remote; Windows path limits)
- `.slnx`-only solutions
- DDD vertical-slice architecture, layer responsibilities, dependency flow
- Domain-centric authoring (no platform boilerplate in domain modules)
- C# coding standards, naming, error handling (ULID identifiers), logging
- Build/run via Aspire, testing standards, container images
- Conventional Commits, branch naming, CI/CD

## Codex / agent operating notes

- **Searching:** prefer `rg` and `rg --files`. If `rg` is unavailable, fall back
  to `find`, `ls`, or `grep -rn` without changing repository behavior.
- **Aspire:** before changing code, run `aspire run` and inspect resource state so
  you start from a known-good baseline. AppHost changes require a restart. Use the
  Aspire MCP tools to read logs, traces, and resource state when debugging.
- **Stay in scope:** when working inside a domain module, keep changes
  domain-specific (contracts, behaviors, events, projections, flows). Reuse shared
  capabilities from technical modules (`Hexalith.EventStore`,
  `Hexalith.FrontComposer`, `Hexalith.Commons`, `Hexalith.Builds`); if a shared
  capability is missing, add it to the relevant technical module rather than
  duplicating it.
- **Quality gates:** `TreatWarningsAsErrors=true`. Run test projects individually
  (use the `.slnx` for restore/build only). All tests must pass before a change is
  complete. Commits must follow Conventional Commits.
