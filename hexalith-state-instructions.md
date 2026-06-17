# Hexalith State Instructions

Rules for persisting data in Hexalith domain modules.

## Use Hexalith.EventStore for persistence

- Hexalith domain modules **must** persist all domain data through the
  **Hexalith.EventStore** technical module. EventStore is the single,
  DAPR-native event-sourcing platform for the ecosystem — do **not** introduce
  any other persistence mechanism for domain state.
- **Forbidden** for domain data: Entity Framework Core, direct database/ORM
  access, raw file or blob storage, and hand-rolled DAPR state-store calls. If a
  persistence capability seems missing, add it to `Hexalith.EventStore`, not to
  the domain module.

## Event sourcing is the source of truth

- State is the **fold of events**, never a mutated row. Model writes as
  aggregates with pure `Handle(Command, State?) -> DomainResult` functions that
  emit events, plus `Apply(Event)` on the state to fold them. Reconstruct state
  by replaying events; never update persisted state in place.
- Commands are imperative (`PlaceOrder`); events are past tense (`OrderPlaced`).
  Identifiers are **ULIDs** — use `Ulid.TryParse`, never `Guid.TryParse`.

## Reference the domain-service SDK, not the plumbing

- A domain module references only the **`Hexalith.EventStore.DomainService`**
  package (it pulls in `Client` + `ServiceDefaults` transitively) and ships its
  domain code plus a two-line host:

  ```csharp
  builder.AddEventStoreDomainService();   // discovers & registers the domain
  app.UseEventStoreDomainService();       // maps /process, /replay-state, /query, /project, …
  ```

- A domain module **must not** ship its own `*.AppHost`, `*.Aspire`, or
  `*.ServiceDefaults` project, nor re-implement projection/query actors, DAPR
  wiring, event-subscription plumbing, telemetry sources, or health checks.

## Reads, projections, and persisted read models

- **Queries** — implement one `IDomainQueryHandler` per query type; the SDK
  discovers, registers, and routes them behind `/query`. Do not subclass a
  projection actor or hand-write a query-type `switch`.
- **Projections (full-replay)** — implement `IDomainProjectionHandler`; the SDK
  maps `/project` and dispatches to it. Rebuild the read model from the supplied
  event sequence and hold no state between calls.
- **Persisted read models** — use `IReadModelStore` + `ReadModelWritePolicy` for
  incrementally-updated, multi-key read models. Do **not** hand-roll a state
  store or call the DAPR state-store API directly.
- **Pagination cursors** — use `IQueryCursorCodec` / `QueryCursorScope`. Do not
  hand-roll a cursor codec.

## Verify persistence in tests

- Integration tests must assert **state-store end-state** (persisted contents),
  not only API return codes or mock call counts.
