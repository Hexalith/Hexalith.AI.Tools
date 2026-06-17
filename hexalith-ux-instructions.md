# Hexalith UX Instructions

Rules for building user interfaces in Hexalith modules.

## Component sources

- Module UI **must always** use the **FrontComposer** technical module and
  **Blazor Fluent UI V5** components.

## Reuse over hand-rolling

- Module UX **must avoid** using raw CSS, HTML tags, JavaScript, or other
  third-party components **when an equivalent component already exists** in
  Blazor Fluent UI V5 or FrontComposer.
- Always reach for the existing FrontComposer / Fluent UI V5 component first.
  Only fall back to custom CSS, HTML, or JavaScript when no such component
  exists.
