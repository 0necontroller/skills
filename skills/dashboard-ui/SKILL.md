---
name: dashboard-ui
description: Build or restyle admin dashboards and internal tools (React, Tailwind, shadcn/ui, TanStack Table) in a calm "warm canvas" style - white panels with hairline borders on an off-white canvas, medium-weight type, soft brand-tinted active nav, KPI strips with an inline chart, ranked bar lists, segmented tabs, breadcrumb-only navigation (no back buttons), settings pages, sticky-action forms and rich data tables. Use when creating or improving dashboard pages, admin consoles, analytics views, data tables, settings screens or admin forms.
---

# Dashboard UI

Produce dashboards that look calm, considered and expensive: an off-white canvas, white panels, lots of whitespace, one brand colour for action, soft data colours, and numbers that carry the page. The reference feel is modern analytics products (DataFast, Linear, Vercel): quiet chrome, rich content.

This file holds the rules. Copy-paste sources live in `references/`:

| File | What it holds |
| --- | --- |
| `references/theme.css` | Colour, radius and font tokens (light + dark), weight clamp, Tailwind `@theme` mapping |
| `references/components.md` | The kit: Panel, MetricStrip, SegmentedControl, BarList, PageHeader, breadcrumb label hook, EmptyState, StatusBadge, FormPage/Section/Field, Settings*, DataTable, row actions, toolbar, ConfirmDialog, CountryFlag |
| `references/layout.md` | Shell: sidebar, sticky canvas header, breadcrumbs, nav config, portal theming |
| `references/patterns.md` | Recipes: overview/analytics, charts, list, detail, form, settings, period filters, maps |

Read the reference for the part you are building before writing code.

---

## 1. Before you write code

1. **shadcn/ui must be set up.** If `components.json` is missing, stop and ask the user to run `npx shadcn@latest init`. Do not hand-write primitives.
2. **Detect the primitive library** (it changes composition syntax):
   - **Base UI** if `components.json` `style` starts with `base-`, or `package.json` has `@base-ui-components/react` / `@base-ui/react`, or `components/ui/button.tsx` imports from Base UI. Compose with the `render` prop: `<Button render={<Link to="/x" />}>Go</Button>`.
   - **Radix** otherwise. Compose with `asChild`: `<Button asChild><Link href="/x">Go</Link></Button>`.
   The references are written for Base UI; convert as needed. Never mix the two.
3. **Install missing primitives** in one go:
   ```bash
   npx shadcn@latest add sidebar breadcrumb button badge avatar dropdown-menu dialog select input textarea label switch table skeleton tooltip separator popover calendar alert chart sonner
   ```
4. **Packages**: `@tanstack/react-table`, an icon set (`@tabler/icons-react` preferred, or `lucide-react`), `date-fns` if dates are filtered. Optional: `recharts` (via shadcn `chart`), `nuqs` for URL state, `country-flag-icons`, `maplibre-gl`.
5. **Reuse first.** If the project already has a dashboard kit (Panel, PageHeader, DataTable…), read it and use it. Only create missing pieces, in one shared folder (e.g. `@/components/dashboard/`), never page by page.
6. **Theme**: add `references/theme.css` to the global stylesheet. Scope it (`.dashboard-scope` on the layout + `dashboard-portal` on `<body>`) when the app has non-dashboard areas; otherwise put it on `:root`.

---

## 2. Design principles

1. **Warm canvas, white panels.** Page background `bg-canvas` (warm off-white). Content sits in white `Panel`s: `rounded-xl`, `border border-border/70`, a barely-there shadow (`shadow-[0_1px_2px_0_rgb(0_0_0/0.03)]`). The hairline border is the separator, not the shadow. Never nest bordered cards inside a panel; use hairline dividers.
2. **Crisp, not soft.** `--radius: 0.625rem`: controls `rounded-lg`, panels `rounded-xl`, pills `rounded-full`. Never `rounded-2xl`/`rounded-3xl` on panels.
3. **Calm whitespace.** Panel padding `px-5 sm:px-6`, `gap-4`/`gap-6` between panels, table rows `py-3.5`. If a page feels busy, remove things; do not shrink them.
4. **Medium weight for emphasis.** Titles, headings, labels, buttons and nav use `font-medium`. The **only** semibold text is headline stat numbers (with `data-stat`). The theme clamps any other 600+ weight to 500. No `font-bold` anywhere. `font-mono` only for ids, codes and JSON.
5. **One brand colour for action.** `primary` (a deep green by default, rebrand by hue) is for primary CTAs, links, focus ring and positive accents. Primary is never a saturated blue.
6. **"You are here" states.**
   - Sidebar active item: **soft brand pill** `bg-primary/10 text-primary`.
   - Settings tab nav, selected metric underline, selected period: **ink** (`bg-ink text-ink-foreground`, near-black; flips in dark mode).
   - In-panel view switches: `SegmentedControl` (white raised pill on a muted track).
7. **Data has its own palette.** `data-sky` for counts and traffic-like series, `data-coral` for money, each with a `-soft` tint for bars and backgrounds. Status colours (emerald/amber/rose/blue/violet) are only for state, never for series.
8. **One primary action per view.** One primary button plus an optional outline "more" (`⋯`) menu. Everything else is outline or ghost.
9. **Breadcrumbs are the navigation.** The sticky header shows `Admin › Section › Record name`. **No back buttons**, no "← Back" links, no page-level breadcrumb trails. Detail pages set the last crumb to the record's name.
10. **Semantic tokens only.** `bg-card`, `bg-muted`, `text-foreground`, `text-muted-foreground`, `border-border`, `bg-canvas`, `bg-ink`. Never `bg-white`, `text-black`, `slate-*`, `gray-*` or hex in components. This is what makes dark mode free.
11. **Numbers are the content.** `tabular-nums` on every number. Money in major units with currency (`KES 12,400`), compact on axes (`12k`). Deltas are muted text plus a coloured arrow, never coloured badges.
12. **Be specific, not generic.** Avatars with initials on soft tints, flags next to countries, relative times ("3 days ago") with the absolute date on hover, real example placeholders, helpful empty states with a next step.

---

## 3. Typography

| Element | Classes |
| --- | --- |
| Page title (`PageHeader`) | `text-[1.75rem] leading-tight font-medium tracking-tight` |
| Settings title | `text-3xl font-medium tracking-tight` |
| Panel / section title | `text-base font-medium tracking-tight` (settings cards `text-lg`) |
| KPI value | `text-[clamp(1.25rem,14cqi,2rem)] font-semibold tabular-nums` + `data-stat` |
| Body, table cells | `text-sm` |
| Labels, meta, table headers | `text-sm text-muted-foreground` (headers `font-medium`) |
| Hints, errors, deltas | `text-xs` |
| Small-caps footer link | `text-xs font-medium tracking-wider uppercase` |

**Font.** Use the project's brand font if it has one. Otherwise a friendly rounded sans works well with this style (Fredoka via `@fontsource/fredoka`, weights 400/500/600 only), set as `--font-dashboard`. Rounded display fonts look heavy at 600+, which is why emphasis is medium.

---

## 4. Layout and page anatomy

See `references/layout.md` for the shell code.

- **Sidebar**: same colour as the canvas, hairline right border, grouped nav with sentence-case group labels, collapsible to icons, left-aligned logo + product name + muted subtitle, user row in the footer.
- **Header**: sticky `h-16`, `bg-canvas/85 backdrop-blur-md`, no border. Left: sidebar trigger (small white button) + breadcrumbs. Right: quiet role pill. No centred logo, no white top bar.
- **Content**: `mx-auto max-w-[1440px] min-w-0 gap-6 px-4 md:px-6 lg:px-8`. Pages do not add their own padding or max-width.

Every page:

```
PageHeader   title · description · statusBadge · media · actions (1 primary + ⋯)
[Toolbar]    search + filters, or a SegmentedControl, on the canvas
Panel(s)     MetricStrip (+ chart) · DataTable · BarList grid · forms
```

Pick the recipe from `references/patterns.md`: overview/analytics, list, detail, form, settings.

---

## 5. Component rules (summary)

Full sources in `references/components.md`.

- **Panel** over `Card`. `PanelHeader` (`title`, `description`, `actions`, `divided` for tables/lists), `PanelContent`, `PanelFooter` (centred small-caps "Details" link).
- **MetricStrip + Metric** for KPIs: one panel, hairline dividers, 2 columns on mobile, 4-7 metrics, main chart inside the same panel. `delta.invert` when lower is better. `pctChange()` returns `null` without a baseline; then show a `hint`.
- **SegmentedControl** for view switches and tab-like filters, with muted counts ("Pending 12"). `size="sm"` in panel headers.
- **BarList** for ranked data: proportional `data-sky-soft` bars, right-aligned numbers, optional coral `secondaryShare`, `limit` 5-10, rows can link.
- **DataTable**: white panel, header row without background, `text-sm font-medium text-muted-foreground` headers, `py-3.5` rows, rich first column, `StatusBadge` for state, right-aligned `tabular-nums` money, built-in skeleton/empty/error states, horizontal scroll inside the panel.
- **Row actions**: visible outline **View** button + `⋯` menu (immediate actions, separator, destructive actions that open `ConfirmDialog`).
- **StatusBadge**: soft `rounded-full` pills, one central enum → tone map. Emerald healthy, amber attention/pending, rose failed/blocked, blue in progress/trial, violet refunds, brand for premium tiers, muted inactive.
- **EmptyState**: icon tile, title, one sentence, and an action. Not-found pages use it with a "View all …" link, not a back button.
- **Forms**: `FormPage` (left-aligned, `max-w-4xl`, sticky action bar) → `FormSection` (white card, divided header, 2-column grid) → `FormField` (label, required asterisk, hint or error).
- **Settings**: `SettingsLayout` (title, ink-pill left nav, narrow `max-w-2xl` column) → `SettingsCard` → `SettingsRow` (label + description left, control right), quiet footer actions.

---

## 6. Interaction and state

- **URL state** for list pages: page, page size, search, sort, filters and tabs (nuqs or `useSearchParams`). Debounce search ~300ms.
- **Loading**: skeletons shaped like the content (metric values, table rows, bar list rows, chart block). Refetches dim content slightly; never blank it.
- **Empty**: distinguish "nothing yet" (offer a create action) from "no results" (offer reset).
- **Errors**: say what failed and offer Retry. Form server errors appear in a destructive `Alert` at the top of the form.
- **Mutations**: disable the trigger and show a spinner while pending; `sonner` toast on success; confirm destructive actions in a dialog that names the record.
- **Detail pages** call `useBreadcrumbLabel(record.name)` before any early return.

---

## 7. Responsive (must work at 375px)

- Page gutter `px-4`; panels keep their radius.
- `MetricStrip` wraps to 2 columns; panel grids stack; `PageHeader` actions drop below the title.
- Tables scroll horizontally inside their panel; the page never scrolls sideways (`min-w-0` on the shell, panels and chart wrappers).
- Toolbars wrap and search goes full width; `SegmentedControl` and settings nav scroll horizontally.
- The first breadcrumb ("Admin") hides below `sm`; the last truncates.
- Touch targets ≥ 36px for primary interactions.

---

## 8. Dark mode

Everything comes from tokens: canvas goes near-black, cards one step lighter, borders `white/9%`, ink flips to near-white, data soft tints deepen. Custom tints need a `dark:` variant (the StatusBadge tones show how). Charts and maps use CSS variables, never literal colours. Check both themes before finishing.

---

## 9. Accessibility

- One `h1` per page (PageHeader); panel titles are `h2`.
- `SegmentedControl` is a `tablist`: give it `aria-label`. Icon-only buttons need `aria-label` ("More actions", "Refresh", "Clear search").
- Every input has a label (`FormField htmlFor`); errors use `role="alert"` and the control gets `aria-invalid`.
- Do not rely on colour alone: deltas have arrows and text, badges have words.
- Charts and maps have a text alternative (adjacent list/table).
- Respect `prefers-reduced-motion` for pulsing dots and chart animation.

---

## 10. Do / Don't

**Do**
- Canvas background, white `rounded-xl` panels with hairline borders.
- `font-medium` for emphasis; semibold only on stat numbers.
- Soft brand pill for the active sidebar item; ink for settings tabs and selected metric.
- `PageHeader` with one primary action; breadcrumbs with record names.
- KPI strip with the main chart in the same panel; ranked `BarList`s below.
- Rich first table column, `StatusBadge`, right-aligned tabular money, URL-synced table state.
- Left-aligned forms with a sticky action bar, inline validation and toasts.
- Check 375px, dark mode, keyboard focus, and the type checker/linter on changed files.

**Don't**
- Back buttons, "← Back" links, `backHref`, or breadcrumb trails inside pages.
- Centred header logo, uppercase monospace role badges, white top bars with borders.
- Solid `bg-primary` sidebar active state, blue primary, gradient stat cards, coloured trend badges, coloured card borders, heavy shadows.
- `font-bold`/`font-semibold` outside stat numbers; `rounded-2xl`/`rounded-3xl` panels; centred (`mx-auto`) forms.
- Table header backgrounds, `text-xs` table bodies, cramped `py-2` rows.
- Raw colours (`bg-white`, `slate-*`, hex), `asChild` on a Base UI project or `render` on a Radix one.
- Raw ids where a name exists, money in cents, emoji flags (they render as letters on Windows).
- Page-local copies of kit components; two panels competing for the same attention.

---

## 11. Finish checklist

- [ ] Theme tokens present; page uses `bg-canvas`, panels `bg-card`.
- [ ] No back buttons; detail/edit pages set the breadcrumb label.
- [ ] Only stat numbers are semibold; no `rounded-2xl+` panels; no raw colours.
- [ ] Loading, empty, error states for every query-driven region.
- [ ] Table/list state in the URL; destructive actions confirmed.
- [ ] Works at 375px with no horizontal page scroll; dark mode checked.
- [ ] Type check and lint pass for changed files; page opened in a browser with real data and no console errors (say so if you could not).
