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
- Colors come from Fluent UI theme color roles (component `Color` parameters or
  Fluent 2 design tokens), never hard-coded values — see
  [No theme redefinition](#no-theme-redefinition).

## No theme redefinition

- Express typography, color, and spacing through **Fluent UI V5 component
  parameters** (e.g. `FluentText` `Size`/`Weight`/`Color`, `FluentStack`
  `Width`/`*Gap`) or **Fluent 2 design tokens** (`--colorNeutralForeground*`,
  `--fontSizeBase*`, `--lineHeightBase*`). **Do not** redefine the theme.
- Hand-authored CSS **must not recreate what a Fluent component already
  provides** — for example a heading ramp via `font-size` / `font-weight` /
  `line-height`, or a foreground role via `color:`. Use the component or token.
- **Never** use legacy Fluent v4 / FAST tokens (`--neutral-foreground-*`,
  `--type-ramp-*`, `--accent-*`, `--neutral-fill-*`, `--palette-*`). They belong
  to the previous major version and do not track the active theme.
- Custom CSS is allowed **only** for layout the design system does not own
  (flex / grid, gaps, user-agent resets) or for a feature Fluent provides no
  component or token for (such as a focusable route-level `<h1>`).
- Where a module guards this with Fluent conformance tests, files still using
  legacy tokens must be tracked as an explicit, allowlisted migration backlog —
  not silently exempted.

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

## Additional Resources

- [Fluent UI Blazor V5](https://fluentui-blazor-v5.azurewebsites.net/)
