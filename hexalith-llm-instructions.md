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

## Technology Stack

- **.NET 10+** — latest .NET framework (SDK version pinned per repo in `global.json`)
- **C# 14+** — latest language features
- **DAPR 1.18+** — Distributed Application Runtime for microservices
- **.NET Aspire 13.x** — local orchestration of the distributed topology
- **Microsoft Fluent UI Blazor** — UI component library for Blazor apps
- **xUnit v3 + Shouldly + NSubstitute** — testing, assertions, mocking

## Hexalith Ecosystem

The ecosystem is split into **technical modules** (reusable platform
capabilities) and **domain modules** (business domains built on the platform).

| Repository | Role |
| ---------- | ---- |
| [Hexalith](https://github.com/Hexalith/Hexalith) | Core framework and shared components |
| [Hexalith.Builds](https://github.com/Hexalith/Hexalith.Builds) | Centralized build configuration & CI/CD templates |
| [Hexalith.Commons](https://github.com/Hexalith/Hexalith.Commons) | Cross-cutting primitives and helpers |
| [Hexalith.PolymorphicSerializations](https://github.com/Hexalith/Hexalith.PolymorphicSerializations) | Polymorphic JSON serialization |
| [Hexalith.EventStore](https://github.com/Hexalith/Hexalith.EventStore) | DAPR-native event sourcing / domain-service SDK |
| [Hexalith.Tenants](https://github.com/Hexalith/Hexalith.Tenants) | Multi-tenancy domain module |
| [Hexalith.Tenants](https://github.com/Hexalith/Hexalith.Parties) | Parties domain module |
| [Hexalith.FrontComposer](https://github.com/Hexalith/Hexalith.FrontComposer) | UI composition / front-end shell |
| [Hexalith.AI.Tools](https://github.com/Hexalith/Hexalith.AI.Tools) | AI-agent instructions, skills, workflows, commands, jobs |

**Boundary rule:** a domain module contains only domain code. If a capability is
boilerplate shared across modules (hosting, event-store plumbing, serialization,
DI setup, UI scaffolding, test harness helpers), **do not duplicate it** — reuse
the technical module that provides it, or add it to that technical module first,
then consume it.

## Solution Files

**Use the `.slnx` solution only** (modern XML solution format). Never create or
use legacy `.sln` files.

## Domain-Driven Design Architecture

Hexalith modules follow a **vertical-slice architecture** with a separate NuGet
package per layer. A module `Hexalith.{Module}` is organized as:

```text
{ModuleName}/
├── references/Hexalith.Builds/                    # Build configuration (submodule)
├── src/
│   ├── examples/
│   │   └── Hexalith.{Module}.Example/                       # Example implementation
│   ├── libraries/                                           # NuGet package libraries
│   │   ├── Domain/
│   │   │   ├── Hexalith.{Module}/                           # Aggregate roots, entities, state
│   │   │   ├── Hexalith.{Module}.Abstractions/              # Domain interfaces, value objects
│   │   │   └── Hexalith.{Module}.Events/                    # Domain events
│   │   ├── Application/
│   │   │   ├── Hexalith.{Module}.Commands/                  # CQRS command definitions
│   │   │   ├── Hexalith.{Module}.Requests/                  # Queries & view models
│   │   │   ├── Hexalith.{Module}.Application/               # Command & query handlers
│   │   │   ├── Hexalith.{Module}.Application.Abstractions/  # Application interfaces
│   │   │   └── Hexalith.{Module}.Projections/               # Read-model projections
│   │   ├── Infrastructure/
│   │   │   ├── Hexalith.{Module}.Servers/                   # Shared server utilities
│   │   │   ├── Hexalith.{Module}.ApiServer/                 # REST API controllers
│   │   │   ├── Hexalith.{Module}.WebServer/                 # Web server implementation
│   │   │   └── Hexalith.{Module}.WebApp/                    # Blazor web application
│   │   └── Presentation/
│   │       ├── Hexalith.{Module}.UI.Components/             # Reusable Blazor components
│   │       ├── Hexalith.{Module}.UI.Pages/                  # Blazor page components
│   │       └── Hexalith.{Module}.Localizations/             # Language resources
│   └── servers/                        # Docker/deployment projects
└── test/
    └── Hexalith.{Module}.Tests/        # Unit & integration tests
```

### Layer Responsibilities

| Package | Layer | Contents |
| ------- | ----- | -------- |
| `Hexalith.{Module}` | Domain | Aggregate roots, entities, value objects, state |
| `Hexalith.{Module}.Abstractions` | Domain | Domain interfaces, shared value objects |
| `Hexalith.{Module}.Events` | Domain | Domain events |
| `Hexalith.{Module}.Commands` | Application | Command definitions, validators |
| `Hexalith.{Module}.Requests` | Application | Query definitions, view models |
| `Hexalith.{Module}.Application` | Application | Command & query handlers, services |
| `Hexalith.{Module}.Projections` | Application | Event projections, read-model handlers |
| `Hexalith.{Module}.Servers` | Infrastructure | Shared server utilities |
| `Hexalith.{Module}.ApiServer` | Infrastructure | REST API controllers, modules |
| `Hexalith.{Module}.WebServer` | Infrastructure | Web server implementation |
| `Hexalith.{Module}.WebApp` | Infrastructure | Blazor web application |
| `Hexalith.{Module}.UI.Components` | Presentation | Reusable Blazor component library |
| `Hexalith.{Module}.UI.Pages` | Presentation | Page-level Blazor components |
| `Hexalith.{Module}.Localizations` | Presentation | i18n resources |

### Dependency Flow (outer depends on inner)

```text
Presentation → Infrastructure → Application → Domain → Abstractions
```

### Architecture Patterns

- **CQRS** — commands in, events out
- **Event Sourcing** — state is reconstructed by replaying events; no direct mutation
- **DDD aggregates** — pure functions: `Handle(Command, State?) -> DomainResult` with `Apply(Event)` on state
- **DAPR** — state store, pub/sub, and config abstracted via sidecars
- **Multi-tenancy** — built in at the contract level (Domain + AggregateId + TenantId)
- **Aspire orchestration** — full local topology via `aspire run` on the AppHost

### Domain-Module Authoring (domain-centric)

Domain modules built on `Hexalith.EventStore` **must be domain-centric** —
aggregates, commands, events, projections, query handlers, validators, and
contracts only. The platform supplies all run-time boilerplate via the
**domain-service SDK**.

- A domain module **must not** ship its own `*.AppHost`, `*.Aspire`, or
  `*.ServiceDefaults` project, and **must not** re-implement projection/query
  actors, DAPR wiring, telemetry sources, health checks, or event-subscription
  plumbing. If a capability is missing, add it to the platform, not the domain.
- **Host shape** — `Program.cs` is two lines:
  `builder.AddEventStoreDomainService();` then `app.UseEventStoreDomainService();`.
- **Queries** — implement `IDomainQueryHandler` (one per query type); the SDK
  discovers, registers, and routes them.
- **Projections** — implement `IDomainProjectionHandler`; the SDK maps `/project`.
- **Persisted read models** — use `IReadModelStore` + `ReadModelWritePolicy`;
  **pagination cursors** — use `IQueryCursorCodec` / `QueryCursorScope`.
  Do not hand-roll a state store or cursor codec.

## C# Coding Standards

Conventions are enforced by `.editorconfig` and `TreatWarningsAsErrors=true`.

- **Namespaces:** file-scoped (`namespace X.Y.Z;`)
- **Braces:** Allman style (new line before the opening brace)
- **Private fields:** `_camelCase`
- **Nullable** and **implicit usings:** enabled globally
- **Indentation:** 4 spaces, CRLF line endings, UTF-8
- **Primary constructors:** prefer them for classes and records
- **XML documentation:** required on all public, protected, and internal members.
  For records with primary constructors, document properties with `<param>` tags.

```csharp
/// <summary>
/// Represents a customer in the system.
/// </summary>
/// <param name="Id">The unique customer identifier.</param>
/// <param name="Email">The customer's email address.</param>
/// <param name="Name">The customer's full name.</param>
/// <param name="CreatedAt">When the customer was created.</param>
public sealed record Customer(
    string Id,
    string Email,
    string Name,
    DateTimeOffset CreatedAt);
```

### Naming Conventions

| Element | Convention | Example |
| ------- | ---------- | ------- |
| Interfaces | Prefix with `I` | `IOrderRepository` |
| Async methods | Suffix with `Async` | `GetOrderAsync` |
| Event handlers | Suffix with `Handler` | `OrderPlacedHandler` |
| Commands | Imperative verb | `PlaceOrder`, `CancelOrder` |
| Events | Past tense | `OrderPlaced`, `OrderCancelled` |
| Value objects | Noun | `Money`, `Address`, `Email` |
| Aggregates | Domain noun | `Order`, `Customer`, `Product` |

### Error Handling

- `ArgumentException.ThrowIfNullOrWhiteSpace()` for string validation
- `ArgumentNullException.ThrowIfNull()` for null checks
- Domain-specific exceptions for business-rule violations; Result pattern for expected failures
- **Identifiers are ULIDs.** Use `Ulid.TryParse` (or accept any non-whitespace
  string per `AggregateIdentity` rules) for `messageId`, `correlationId`,
  `aggregateId`, `causationId`. `Guid.TryParse` on these fields is **forbidden** —
  ULID and GUID share a 36-char shape only by coincidence.

### Logging

Use source-generated `LoggerMessageAttribute` for high-performance logging:
`static partial` methods, `ILogger` as the first parameter (and `Exception`
second when present), structured named placeholders (`{OrderId}`), declaring
class `partial`.

## User Interface & UX

Module UIs follow the rules in
[`hexalith-ux-instructions.md`](./hexalith-ux-instructions.md). Read it before
working on any module user interface. In short:

- Module UI **must** use the **FrontComposer** technical module and **Blazor
  Fluent UI V5** components.
- **Reuse over hand-rolling** — avoid raw CSS, HTML, JavaScript, or third-party
  components when an equivalent FrontComposer / Fluent UI V5 component exists.
  Only fall back to custom markup when no such component exists.
- **No theme redefinition** — express typography/color/spacing via Fluent UI V5
  component parameters or Fluent 2 design tokens; never recreate
  component-provided styling in CSS, and never use legacy v4/FAST tokens
  (`--type-ramp-*`, `--neutral-*`, `--accent-*`, `--neutral-fill-*`, `--palette-*`).

## Build, Run & Diagnostics

Centralized build configuration comes from `Hexalith.Builds`:
`Hexalith.Build.props`, `Hexalith.Package.props`, and `Directory.Packages.props`
(centralized package versions — no inline `<PackageReference Version>`).

```bash
# Restore & build (Release)
dotnet restore Hexalith.{Module}.slnx
dotnet build Hexalith.{Module}.slnx --configuration Release

# Run the local topology (AppHost lives in the platform/host repo)
aspire run
```

**Aspire workflow:** before changing code, run the AppHost with `aspire run` and
inspect resource state so you start from a known-good baseline. AppHost changes
require restarting the Aspire app. The standalone Aspire MCP server is obsolete —
use the **Aspire agents** integration instead: run `aspire agent init` once to
install the Aspire skills/tools, then drive the running app through the **Aspire
CLI** (`aspire describe` for resource state and endpoints, `aspire otel logs` for
logs and traces, `aspire docs search` for docs). Use the Playwright MCP server for
functional investigations (get navigable endpoints from `aspire describe`). When
adding a resource, use `aspire add`, pick a version aligned with
`Aspire.AppHost.Sdk`, and read the integration docs before editing the AppHost.
Prefer official docs: `https://aspire.dev`,
`https://learn.microsoft.com/dotnet/aspire`.

## Testing Standards

- **Framework:** xUnit v3 · **Assertions:** Shouldly · **Mocking:** NSubstitute · **Coverage:** coverlet
- Test method names use **PascalCase**.
- **Run test projects individually**; use the `.slnx` for restore/build only, not
  solution-level `dotnet test`.
- When `dotnet test` or a solution build is environment-blocked, climb the
  fallback validation ladder before recording validation as blocked:
  1. Run the most focused lane or test project build/run available.
  2. For xUnit v3 filters, build the target test project and invoke the built test
     assembly directly with single-dash `-class` or `-method` arguments; do not rely
     on project-level `dotnet test --filter` under Microsoft.Testing.Platform.
  3. Use serialized `-m:1` Release builds for first-failure triage, adding only
     environment pins such as `-p:NuGetAudit=false` and
     `-p:MinVerVersionOverride=1.0.0` when needed.
  4. Record the exact broad-gate blocker separately from the focused evidence that
     did run, and never weaken the build gate to hide the blocker.
- Organize tests by aggregate: `{Command}Tests.cs`, `{Event}Tests.cs`,
  `{Query}Tests.cs`, `{Aggregate}Tests.cs`.
- Integration tests must assert **state-store end-state** (persisted contents),
  not only API return codes or mock call counts.
- All existing and new tests must pass before a story is complete.

```text
test/
└── Hexalith.{Module}.Tests/
    └── {Aggregate}/
        ├── {Command}Tests.cs
        ├── {Event}Tests.cs
        ├── {Query}Tests.cs
        └── {Aggregate}Tests.cs
```

## Container Images

Images are produced via **.NET SDK container support** (no Dockerfiles). Opt-in
is centralized in `Directory.Build.targets` and enabled per project with
`<EnableContainer>true</EnableContainer>` + `<ContainerRepository>image-name</ContainerRepository>`.
Defaults: base `mcr.microsoft.com/dotnet/aspnet:10.0-alpine`, registry
`registry.hexalith.com`, non-root `app` user, port 8080.

```bash
dotnet publish src/Hexalith.{Module}/Hexalith.{Module}.csproj \
  --configuration Release -t:PublishContainer \
  -p:ContainerArchiveOutputPath=/tmp/{module}.tar.gz
```

## Commit Messages

All commits **must** follow [Conventional Commits](https://www.conventionalcommits.org/)
— required for semantic-release to determine version bumps and changelogs.

Format: `<type>(<optional scope>): <description>`

| Type | Description | Version bump |
| ---- | ----------- | ------------ |
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `perf` | Performance improvement | Patch |
| `docs` | Documentation only | None |
| `refactor` | Code change, no feature/fix | None |
| `test` | Add/modify tests | None |
| `build` / `ci` / `chore` / `style` | Tooling, build, formatting | None |

Rules: imperative mood, lowercase start, no trailing period, keep the subject
under ~50 chars, wrap the body at 72. Breaking changes use `BREAKING CHANGE:` in
the footer or `!` after the type (`feat!:`) → **major** bump.

**Every commit needs a `type:` prefix — no exceptions.** A subject that starts
with a plain-English verb (`Update …`, `Add …`, `Fix …`, `Bump …`) is **not**
conventional: commitlint parses the whole line as the type and fails with
`type-empty` / `subject-empty`. This most often bites on machine-shaped commits
that feel like they don't need a type:

- **Submodule / subproject reference bumps** — do **not** use git's default
  `Update subproject reference for X to latest commit <sha>` message. Rewrite it,
  e.g. `chore(deps): bump Hexalith.Memories submodule to 27bebfa`.
- **Dependency version bumps** — `chore(deps): bump Fluent UI Blazor to 5.x`.
- **Merges, reverts, formatting, config** — still need a type
  (`chore:`, `revert:`, `style:`, `ci:`).

Never bypass the commit hook (`--no-verify`) to sidestep this. Before committing,
sanity-check the subject against the format; you can verify the last commit with
`npx commitlint --last --verbose`.

```text
feat(contracts): add SnapshotInterval to EventStoreOptions
fix(server): prevent duplicate event sequence numbers on concurrent writes
feat!: rename EventEnvelope.StreamId to AggregateId
chore(deps): bump Hexalith.Memories submodule to 27bebfa
```

## Branch Naming

- `feat/<description>` — features and enhancements
- `fix/<description>` — bug fixes
- `docs/<description>` — documentation changes

## CI/CD

- **CI** — GitHub Actions on push/PR to `main`: restore, build (Release), run the
  configured unit/integration suites, optional Aspire end-to-end tests.
- **Release** — on merge to `main` via semantic-release: version from
  Conventional Commits, test, pack, publish NuGet packages, GitHub Release,
  update `CHANGELOG.md`.

## Additional Resources

- [Hexalith Documentation](https://github.com/Hexalith/Hexalith)
- [DAPR Documentation](https://docs.dapr.io/)
- [.NET Aspire](https://learn.microsoft.com/dotnet/aspire)
- [Fluent UI Blazor](https://www.fluentui-blazor.net/)
- [Conventional Commits](https://www.conventionalcommits.org/)
