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

## Page sections

- Page-like surfaces such as pages, dialogs, and detail panels with **two or
  more sibling titled content sections** must group those sections in a single
  `FluentAccordion`, with one `FluentAccordionItem` per section.
- Keep page titles, breadcrumbs, toolbars, navigation chrome, and single
  primary content regions such as one grid, form, detail view, or chart outside
  the accordion.
- Do not hide the only primary content behind an accordion interaction. When a
  primary section belongs in an accordion with other sibling sections, expand
  the primary item by default.
