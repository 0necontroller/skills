# Dashboard kit: copy-paste sources

Create these once in `@/components/dashboard/` (one file per heading, re-exported from an `index.ts`), then build every page from them. Keep hooks/helpers such as `useBreadcrumbLabel` and `pctChange` exported from the same files only if the project's linter allows mixed exports (React Fast Refresh warns); otherwise move them to a sibling `.ts` file. If the project already has an equivalent kit, use it and do not duplicate.

Conventions used below:

- **Composition** is written for shadcn on **Base UI** (`render` prop). On **Radix** shadcn, convert `<X render={<Link to="/a" />}>label</X>` to `<X asChild><Link to="/a">label</Link></X>`. See SKILL.md §1 for how to tell which one the project uses.
- **Router**: `import { Link } from "react-router"`. For Next.js use `import Link from "next/link"` and `href=` instead of `to=`.
- **Icons**: `@tabler/icons-react`. With `lucide-react`, swap names (`IconArrowUp` → `ArrowUp`, `IconDots` → `MoreHorizontal`, `IconEye` → `Eye`, `IconInbox` → `Inbox`, `IconAlertCircle` → `AlertCircle`, `IconLoader2` → `Loader2`).
- `cn` is the shadcn `@/lib/utils` helper.

---

## panel.tsx

The base surface. Prefer it over shadcn `Card` on dashboard pages.

```tsx
import type { ComponentProps, ReactNode } from "react"
import { cn } from "@/lib/utils"

export function Panel({ className, ...props }: ComponentProps<"section">) {
  return (
    <section
      data-slot="panel"
      className={cn(
        "flex min-w-0 flex-col overflow-hidden rounded-xl border border-border/70 bg-card text-card-foreground shadow-[0_1px_2px_0_rgb(0_0_0/0.03)]",
        className,
      )}
      {...props}
    />
  )
}

export interface PanelHeaderProps extends Omit<ComponentProps<"div">, "title"> {
  title?: ReactNode
  description?: ReactNode
  /** Right-aligned controls: SegmentedControl, buttons, sort toggles. */
  actions?: ReactNode
  /** Hairline under the header (use when the body is a table/list). */
  divided?: boolean
}

export function PanelHeader({ title, description, actions, divided, className, children, ...props }: PanelHeaderProps) {
  return (
    <div
      data-slot="panel-header"
      className={cn(
        "flex flex-wrap items-center justify-between gap-3 px-5 pt-5 pb-3 sm:px-6",
        divided && "border-b border-border/70 pb-4",
        className,
      )}
      {...props}
    >
      {(title || description) && (
        <div className="min-w-0 space-y-0.5">
          {title && <h2 className="truncate text-base font-medium tracking-tight text-foreground">{title}</h2>}
          {description && <p className="text-sm text-muted-foreground">{description}</p>}
        </div>
      )}
      {children}
      {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
    </div>
  )
}

export function PanelContent({ className, ...props }: ComponentProps<"div">) {
  return <div data-slot="panel-content" className={cn("px-5 pb-5 sm:px-6", className)} {...props} />
}

/** Centred small-caps footer link ("⤢ DETAILS") under a list. */
export function PanelFooter({ className, ...props }: ComponentProps<"div">) {
  return (
    <div
      data-slot="panel-footer"
      className={cn(
        "flex items-center justify-center gap-2 border-t border-border/60 px-5 py-3 text-xs font-medium tracking-wider text-muted-foreground uppercase [&_a]:inline-flex [&_a]:items-center [&_a]:gap-1.5 [&_a:hover]:text-foreground [&_button]:inline-flex [&_button]:items-center [&_button]:gap-1.5 [&_button:hover]:text-foreground",
        className,
      )}
      {...props}
    />
  )
}
```

---

## metric-strip.tsx

One panel, metrics side by side with hairline dividers, 2 columns on mobile. The value font size scales with the metric's width (container query) so long money values never truncate.

```tsx
import type { ReactNode } from "react"
import { IconArrowDown, IconArrowUp } from "@tabler/icons-react"
import { Skeleton } from "@/components/ui/skeleton"
import { cn } from "@/lib/utils"
import { Panel } from "./panel"

export interface MetricDelta {
  /** Percent change: 14 for +14%, -31 for -31%. */
  value: number
  /** Lower is better (refunds, failures, churn): flips the colour. */
  invert?: boolean
}

export interface MetricProps {
  label: ReactNode
  value: ReactNode
  delta?: MetricDelta | null
  /** Muted text under the value when there is no delta. */
  hint?: ReactNode
  /** Pulsing green dot next to the label (live counts). */
  live?: boolean
  isLoading?: boolean
  /** Selected series (drives the chart below); shows an ink underline. */
  active?: boolean
  onClick?: () => void
  className?: string
}

export function Metric({ label, value, delta, hint, live, isLoading, active, onClick, className }: MetricProps) {
  const Comp = onClick ? "button" : "div"
  const up = (delta?.value ?? 0) > 0
  const flat = !delta || Math.round(delta.value) === 0
  const good = delta?.invert ? !up : up
  const Arrow = up ? IconArrowUp : IconArrowDown
  return (
    <Comp
      type={onClick ? "button" : undefined}
      onClick={onClick}
      className={cn(
        "@container/metric relative flex min-w-0 flex-col gap-1.5 px-4 py-4 text-left xl:px-6",
        onClick && "cursor-pointer transition-colors hover:bg-muted/40",
        active && "after:absolute after:inset-x-4 after:bottom-0 after:h-0.5 after:rounded-full after:bg-ink xl:after:inset-x-6",
        className,
      )}
    >
      <span className="flex min-w-0 items-center gap-1.5 text-sm leading-snug text-muted-foreground">
        {label}
        {live && (
          <span className="relative flex size-2">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-60 motion-reduce:animate-none" />
            <span className="relative inline-flex size-2 rounded-full bg-emerald-500" />
          </span>
        )}
      </span>
      {isLoading ? (
        <Skeleton className="h-9 w-24" />
      ) : (
        <span
          data-stat
          className="truncate text-[clamp(1.25rem,14cqi,2rem)] leading-tight font-semibold tracking-tight text-foreground tabular-nums"
        >
          {value}
        </span>
      )}
      {isLoading ? (
        <Skeleton className="h-3.5 w-12" />
      ) : delta ? (
        <span className="flex items-center gap-1 text-xs text-muted-foreground tabular-nums">
          {Math.abs(Math.round(delta.value))}%
          {!flat && <Arrow className={cn("size-3.5", good ? "text-emerald-600" : "text-rose-500")} stroke={2.25} />}
        </span>
      ) : hint ? (
        <span className="line-clamp-2 text-xs text-muted-foreground">{hint}</span>
      ) : null}
    </Comp>
  )
}

/** Pass `children` (usually the main chart) to render it inside the same panel. */
export function MetricStrip({ metrics, children, className }: { metrics: ReactNode; children?: ReactNode; className?: string }) {
  return (
    <Panel className={className}>
      <div className="grid grid-cols-2 divide-border/70 sm:flex sm:flex-wrap sm:divide-x [&>*]:sm:min-w-[9.5rem] [&>*]:sm:flex-1">
        {metrics}
      </div>
      {children}
    </Panel>
  )
}

/** Percent change; null when there is no baseline. */
export function pctChange(current: number, previous: number): number | null {
  if (!previous) return current ? null : 0
  return ((current - previous) / previous) * 100
}
```

---

## segmented-control.tsx

```tsx
import type { ReactNode } from "react"
import { cn } from "@/lib/utils"

export interface SegmentedOption<T extends string> {
  value: T
  label: ReactNode
  /** Muted count after the label ("Pending 12"). */
  count?: number | string
  icon?: ReactNode
}

export function SegmentedControl<T extends string>({
  value,
  onValueChange,
  options,
  size = "default",
  className,
  "aria-label": ariaLabel,
}: {
  value: T
  onValueChange: (value: T) => void
  options: SegmentedOption<T>[]
  size?: "sm" | "default"
  className?: string
  "aria-label"?: string
}) {
  return (
    <div
      role="tablist"
      aria-label={ariaLabel}
      className={cn(
        "no-scrollbar inline-flex max-w-full items-center gap-0.5 overflow-x-auto rounded-lg border border-border/60 bg-muted/70 p-1",
        className,
      )}
    >
      {options.map((opt) => {
        const active = opt.value === value
        return (
          <button
            key={opt.value}
            type="button"
            role="tab"
            aria-selected={active}
            onClick={() => onValueChange(opt.value)}
            className={cn(
              "inline-flex shrink-0 cursor-pointer items-center gap-1.5 rounded-md px-3.5 whitespace-nowrap transition-all outline-none focus-visible:ring-2 focus-visible:ring-ring [&_svg]:size-4",
              size === "sm" ? "h-7 text-xs" : "h-8 text-sm",
              active
                ? "bg-card font-medium text-foreground shadow-[0_1px_2px_0_rgb(0_0_0/0.06),0_0_0_1px_rgb(0_0_0/0.04)]"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            {opt.icon}
            {opt.label}
            {opt.count !== undefined && <span className="text-muted-foreground tabular-nums">{opt.count}</span>}
          </button>
        )
      })}
    </div>
  )
}
```

---

## bar-list.tsx

Ranked rows with proportional soft background bars and right-aligned numbers.

```tsx
import type { ReactNode } from "react"
import { Link } from "react-router"
import { Skeleton } from "@/components/ui/skeleton"
import { cn } from "@/lib/utils"

export interface BarListItem {
  key: string
  label: ReactNode
  /** Leading 20px icon, flag, favicon or avatar. */
  icon?: ReactNode
  value: number
  /** Second measure as a coral segment after the main bar, 0..1 of the row width. */
  secondaryShare?: number
  href?: string
}

export function BarList({
  items,
  formatValue = (v) => v.toLocaleString(),
  isLoading,
  limit,
  emptyText = "No data yet",
  className,
}: {
  items: BarListItem[]
  formatValue?: (value: number) => ReactNode
  isLoading?: boolean
  limit?: number
  emptyText?: ReactNode
  className?: string
}) {
  if (isLoading) {
    return (
      <div className={cn("space-y-1.5 py-1", className)}>
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-10 rounded-lg" style={{ width: `${90 - i * 12}%` }} />
        ))}
      </div>
    )
  }
  const shown = limit ? items.slice(0, limit) : items
  if (!shown.length) return <p className="py-10 text-center text-sm text-muted-foreground">{emptyText}</p>
  const max = Math.max(...shown.map((i) => i.value), 1)
  const rowCls =
    "relative flex h-10 items-center justify-between overflow-hidden rounded-md pr-1 pl-3 text-sm text-foreground"
  return (
    <ul className={cn("space-y-1", className)}>
      {shown.map((item) => {
        const w = Math.max((item.value / max) * 100, 2)
        const row = (
          <>
            <span className="absolute inset-y-0 left-0 flex" style={{ width: `${w}%` }}>
              <span className="h-full flex-1 rounded-r-md bg-data-sky-soft" />
              {item.secondaryShare ? (
                <span
                  className="h-full rounded-md bg-data-coral-soft"
                  style={{ width: `${Math.min(item.secondaryShare, 1) * 100}%` }}
                />
              ) : null}
            </span>
            <span className="relative flex min-w-0 items-center gap-2.5">
              {item.icon && (
                <span className="flex size-5 shrink-0 items-center justify-center [&_img]:size-5 [&_svg]:size-4.5">
                  {item.icon}
                </span>
              )}
              <span className="truncate">{item.label}</span>
            </span>
            <span className="relative pl-3 font-medium tabular-nums">{formatValue(item.value)}</span>
          </>
        )
        return (
          <li key={item.key}>
            {item.href ? (
              <Link to={item.href} className={cn(rowCls, "transition-opacity hover:opacity-80")}>{row}</Link>
            ) : (
              <div className={rowCls}>{row}</div>
            )}
          </li>
        )
      })}
    </ul>
  )
}
```

---

## page-header.tsx

No breadcrumbs and no back button here: navigation context lives in the layout header (see `references/layout.md`).

```tsx
import type { ReactNode } from "react"
import { cn } from "@/lib/utils"

export interface PageHeaderProps {
  title: ReactNode
  description?: ReactNode
  /** Badge(s) inline after the title (status, tier). */
  statusBadge?: ReactNode
  /** Leading avatar, logo or icon tile (40-48px), for detail pages. */
  media?: ReactNode
  /** One primary action + an optional "more" dropdown. */
  actions?: ReactNode
  className?: string
}

export function PageHeader({ title, description, statusBadge, media, actions, className }: PageHeaderProps) {
  return (
    <div className={cn("flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between", className)}>
      <div className="flex min-w-0 items-center gap-4">
        {media && <div className="shrink-0">{media}</div>}
        <div className="min-w-0 space-y-1">
          <div className="flex flex-wrap items-center gap-2.5">
            <h1 className="truncate text-[1.75rem] leading-tight font-medium tracking-tight text-foreground">{title}</h1>
            {statusBadge}
          </div>
          {description && <p className="text-[0.95rem] text-muted-foreground">{description}</p>}
        </div>
      </div>
      {actions && <div className="flex shrink-0 flex-wrap items-center gap-2">{actions}</div>}
    </div>
  )
}
```

---

## breadcrumb-label.tsx

Lets a detail page replace the id in the last breadcrumb with the record's name. Wrap the dashboard layout in `BreadcrumbLabelProvider`; the header reads `useBreadcrumbLabelValue()`.

```tsx
import { createContext, useContext, useEffect, useState, type ReactNode } from "react"

type Setter = (label: string | undefined) => void
const LabelCtx = createContext<string | undefined>(undefined)
const SetterCtx = createContext<Setter>(() => {})

export function BreadcrumbLabelProvider({ children }: { children: ReactNode }) {
  const [label, setLabel] = useState<string | undefined>()
  return (
    <SetterCtx.Provider value={setLabel}>
      <LabelCtx.Provider value={label}>{children}</LabelCtx.Provider>
    </SetterCtx.Provider>
  )
}

export const useBreadcrumbLabelValue = () => useContext(LabelCtx)

/** Call unconditionally (before early returns); safe with undefined while loading. */
export function useBreadcrumbLabel(label: string | undefined | null) {
  const set = useContext(SetterCtx)
  useEffect(() => {
    set(label ?? undefined)
    return () => set(undefined)
  }, [label, set])
}
```

---

## empty-state.tsx

```tsx
import type { ReactNode } from "react"
import { IconAlertCircle, IconInbox } from "@tabler/icons-react"
import { cn } from "@/lib/utils"

export interface EmptyStateProps {
  icon?: ReactNode
  title: string
  description?: string
  /** Always offer a next step: "Create the first coupon", "View all users". */
  action?: ReactNode
  variant?: "default" | "error"
  className?: string
}

export function EmptyState({ icon, title, description, action, variant = "default", className }: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-2 rounded-xl border border-border/70 bg-card px-6 py-14 text-center",
        className,
      )}
    >
      <div
        className={cn(
          "mb-2 flex size-11 items-center justify-center rounded-lg text-muted-foreground [&_svg]:size-5",
          variant === "error" ? "bg-destructive/10" : "bg-muted",
        )}
      >
        {icon ?? (variant === "error" ? <IconAlertCircle className="text-destructive" /> : <IconInbox />)}
      </div>
      <p className="text-base font-medium text-foreground">{title}</p>
      {description && <p className="max-w-sm text-sm text-muted-foreground">{description}</p>}
      {action && <div className="mt-3">{action}</div>}
    </div>
  )
}
```

---

## status-badge.tsx

Soft pills. Extend `STATUS_MAP` with the project's enums; never invent ad-hoc badge colours in pages.

```tsx
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

const EMERALD = "bg-emerald-500/10 text-emerald-700 border-emerald-600/15 dark:text-emerald-400 dark:border-emerald-400/20"
const AMBER = "bg-amber-500/10 text-amber-700 border-amber-600/15 dark:text-amber-400 dark:border-amber-400/20"
const ROSE = "bg-rose-500/10 text-rose-700 border-rose-600/15 dark:text-rose-400 dark:border-rose-400/20"
const BLUE = "bg-blue-500/10 text-blue-700 border-blue-600/15 dark:text-blue-400 dark:border-blue-400/20"
const VIOLET = "bg-violet-500/10 text-violet-700 border-violet-600/15 dark:text-violet-400 dark:border-violet-400/20"
const MUTED = "bg-muted text-muted-foreground border-border"
const PRIMARY = "bg-primary/10 text-primary border-primary/25"

type Tone = { className: string; dot: string }
const T = {
  good: { className: EMERALD, dot: "bg-emerald-500" },
  warn: { className: AMBER, dot: "bg-amber-500" },
  bad: { className: ROSE, dot: "bg-rose-500" },
  info: { className: BLUE, dot: "bg-blue-500" },
  refund: { className: VIOLET, dot: "bg-violet-500" },
  brand: { className: PRIMARY, dot: "bg-primary" },
  off: { className: MUTED, dot: "bg-muted-foreground" },
} satisfies Record<string, Tone>

// emerald = healthy/done, amber = needs attention/pending, rose = failed/blocked,
// blue = in progress/trial, violet = refunds, brand = premium tier, muted = inactive.
const STATUS_MAP: Record<string, Tone & { label?: string }> = {
  ACTIVE: { ...T.good, label: "Active" },
  COMPLETED: { ...T.good, label: "Completed" },
  PAID: { ...T.good, label: "Paid" },
  RESOLVED: { ...T.good, label: "Resolved" },
  ENABLED: { ...T.good, label: "Enabled" },
  VERIFIED: { ...T.good, label: "Verified" },
  PENDING: { ...T.warn, label: "Pending" },
  OPEN: { ...T.warn, label: "Open" },
  PAST_DUE: { ...T.warn, label: "Past due" },
  NEEDS_RESPONSE: { ...T.warn, label: "Needs response" },
  PROCESSING: { ...T.info, label: "Processing" },
  IN_PROGRESS: { ...T.info, label: "In progress" },
  TRIAL: { ...T.info, label: "Trial" },
  FAILED: { ...T.bad, label: "Failed" },
  EXPIRED: { ...T.bad, label: "Expired" },
  SUSPENDED: { ...T.bad, label: "Suspended" },
  REFUNDED: { ...T.refund, label: "Refunded" },
  CANCELLED: { ...T.off, label: "Cancelled" },
  INACTIVE: { ...T.off, label: "Inactive" },
  DISABLED: { ...T.off, label: "Disabled" },
  ARCHIVED: { ...T.off, label: "Archived" },
}

const normalize = (s: string) => s.trim().toUpperCase().replace(/[\s-]+/g, "_")
const titleCase = (s: string) =>
  s.trim().replace(/[_-]+/g, " ").toLowerCase().replace(/^\w/, (c) => c.toUpperCase())

export function StatusBadge({ status, label, dot = false, className }: { status: string; label?: string; dot?: boolean; className?: string }) {
  const style = STATUS_MAP[normalize(status || "")]
  return (
    <Badge
      variant="outline"
      className={cn(
        "inline-flex h-6 items-center gap-1.5 rounded-full border px-2.5 text-xs font-medium shadow-none",
        style?.className ?? MUTED,
        className,
      )}
    >
      {dot && <span aria-hidden className={cn("size-1.5 shrink-0 rounded-full", style?.dot ?? "bg-muted-foreground")} />}
      {label ?? style?.label ?? titleCase(status || "Unknown")}
    </Badge>
  )
}
```

---

## form-layout.tsx

Left-aligned forms (never centred), white section cards, sticky action bar.

```tsx
import type { FormEvent, ReactNode } from "react"
import { cn } from "@/lib/utils"

export function FormPage({
  onSubmit,
  children,
  actions,
  className,
}: {
  onSubmit: (e: FormEvent<HTMLFormElement>) => void
  children: ReactNode
  /** Cancel (ghost link) + primary submit. */
  actions: ReactNode
  className?: string
}) {
  return (
    <form onSubmit={onSubmit} noValidate className={cn("flex w-full max-w-4xl flex-col gap-4", className)}>
      {children}
      <div className="sticky bottom-3 z-10 mt-2 flex items-center justify-end gap-2 rounded-lg border border-border/70 bg-card/90 px-4 py-3 shadow-[0_8px_24px_-12px_rgb(0_0_0/0.18)] backdrop-blur">
        {actions}
      </div>
    </form>
  )
}

export function FormSection({ title, description, children, className }: { title: ReactNode; description?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <section className={cn("rounded-xl border border-border/70 bg-card shadow-[0_1px_2px_0_rgb(0_0_0/0.03)]", className)}>
      <header className="border-b border-border/70 px-6 py-4">
        <h2 className="text-base font-medium tracking-tight">{title}</h2>
        {description && <p className="mt-0.5 text-sm text-muted-foreground">{description}</p>}
      </header>
      <div className="grid gap-5 px-6 py-5 sm:grid-cols-2">{children}</div>
    </section>
  )
}

/** Label + control + hint/error. `span="full"` stretches across both columns. */
export function FormField({
  label,
  htmlFor,
  hint,
  error,
  required,
  span,
  children,
}: {
  label: ReactNode
  htmlFor?: string
  hint?: ReactNode
  error?: ReactNode
  required?: boolean
  span?: "full"
  children: ReactNode
}) {
  return (
    <div className={cn("flex min-w-0 flex-col gap-1.5", span === "full" && "sm:col-span-2")}>
      <label htmlFor={htmlFor} className="text-sm font-medium text-foreground">
        {label}
        {required && <span className="ml-0.5 text-destructive">*</span>}
      </label>
      {children}
      {error ? (
        <p role="alert" className="text-xs text-destructive">{error}</p>
      ) : hint ? (
        <p className="text-xs text-muted-foreground">{hint}</p>
      ) : null}
    </div>
  )
}
```

---

## settings-layout.tsx

```tsx
import type { ComponentType, ReactNode } from "react"
import { cn } from "@/lib/utils"

export interface SettingsNavItem<T extends string> {
  value: T
  label: string
  icon: ComponentType<{ className?: string }>
}

export function SettingsLayout<T extends string>({
  title = "Settings",
  nav,
  value,
  onValueChange,
  children,
  footer,
}: {
  title?: string
  nav: SettingsNavItem<T>[]
  value: T
  onValueChange: (value: T) => void
  children: ReactNode
  /** Quiet actions under the cards (Logout / Delete account). */
  footer?: ReactNode
}) {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-3xl font-medium tracking-tight">{title}</h1>
      <div className="flex flex-col gap-6 lg:flex-row lg:gap-10">
        <nav className="no-scrollbar flex shrink-0 gap-1 overflow-x-auto lg:w-56 lg:flex-col">
          {nav.map((item) => {
            const Icon = item.icon
            const active = item.value === value
            return (
              <button
                key={item.value}
                type="button"
                onClick={() => onValueChange(item.value)}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "flex h-11 shrink-0 cursor-pointer items-center gap-3 rounded-lg px-4 text-[0.95rem] whitespace-nowrap transition-colors",
                  active ? "bg-ink text-ink-foreground" : "text-foreground/80 hover:bg-muted hover:text-foreground",
                )}
              >
                <Icon className="size-5 shrink-0" />
                {item.label}
              </button>
            )
          })}
        </nav>
        <div className="flex w-full max-w-2xl min-w-0 flex-col gap-4">
          {children}
          {footer && <div className="flex flex-wrap items-center justify-end gap-6 pt-1 text-sm">{footer}</div>}
        </div>
      </div>
    </div>
  )
}

export function SettingsCard({ title, description, children, className }: { title?: ReactNode; description?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <section className={cn("overflow-hidden rounded-xl border border-border/70 bg-card shadow-[0_1px_2px_0_rgb(0_0_0/0.03)]", className)}>
      {title && (
        <header className="border-b border-border/70 px-6 py-4">
          <h2 className="text-lg font-medium tracking-tight">{title}</h2>
          {description && <p className="mt-0.5 text-sm text-muted-foreground">{description}</p>}
        </header>
      )}
      <div className="divide-y divide-border/70">{children}</div>
    </section>
  )
}

/** Label + description left, control right. Pass `children` for a free-form row. */
export function SettingsRow({ label, description, control, children, className }: { label?: ReactNode; description?: ReactNode; control?: ReactNode; children?: ReactNode; className?: string }) {
  if (children) return <div className={cn("px-6 py-5", className)}>{children}</div>
  return (
    <div className={cn("flex flex-col gap-3 px-6 py-5 sm:flex-row sm:items-center sm:justify-between sm:gap-6", className)}>
      <div className="min-w-0">
        <div className="text-[0.95rem] font-medium">{label}</div>
        {description && <p className="mt-0.5 text-sm text-muted-foreground">{description}</p>}
      </div>
      {control && <div className="shrink-0">{control}</div>}
    </div>
  )
}

export function SettingsFooterAction({ icon: Icon, children, onClick, destructive }: { icon: ComponentType<{ className?: string }>; children: ReactNode; onClick?: () => void; destructive?: boolean }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "inline-flex cursor-pointer items-center gap-2 text-foreground/80 transition-colors",
        destructive ? "hover:text-destructive" : "hover:text-foreground",
      )}
    >
      <Icon className="size-4.5" />
      {children}
    </button>
  )
}
```

---

## data-table.tsx

A white panel around shadcn `Table`, driven by TanStack Table. Server pagination and sorting are controlled from outside (URL state).

Written for **TanStack Table v8** (`useReactTable`, `getCoreRowModel`). On v9 (`useTable` + `tableFeatures`), keep the markup and classes and swap the table setup for the v9 API.

```tsx
import type { ReactNode } from "react"
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
  type OnChangeFn,
  type SortingState,
} from "@tanstack/react-table"
import {
  IconArrowDown, IconArrowUp, IconArrowsSort, IconChevronLeft, IconChevronRight, IconRefresh,
} from "@tabler/icons-react"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { cn } from "@/lib/utils"
import { EmptyState } from "./empty-state"

export interface DataTableProps<TData> {
  columns: ColumnDef<TData, any>[]
  data: TData[]
  getRowId?: (row: TData) => string
  total: number
  page: number
  pageSize: number
  onPageChange: (page: number) => void
  sorting?: SortingState
  onSortingChange?: OnChangeFn<SortingState>
  onRowClick?: (row: TData) => void
  isLoading?: boolean
  isFetching?: boolean
  isError?: boolean
  onRetry?: () => void
  /** Search + filters, rendered on the canvas above the panel. */
  toolbar?: ReactNode
  emptyTitle?: string
  emptyDescription?: string
  emptyAction?: ReactNode
}

export function DataTable<TData>({
  columns, data, getRowId, total, page, pageSize, onPageChange, sorting, onSortingChange, onRowClick,
  isLoading, isFetching, isError, onRetry, toolbar,
  emptyTitle = "Nothing here yet", emptyDescription, emptyAction,
}: DataTableProps<TData>) {
  const table = useReactTable({
    data,
    columns,
    getRowId,
    getCoreRowModel: getCoreRowModel(),
    manualSorting: true,
    manualPagination: true,
    state: sorting ? { sorting } : undefined,
    onSortingChange,
  })
  const pages = Math.max(1, Math.ceil(total / pageSize))
  const start = total ? (page - 1) * pageSize + 1 : 0
  const end = Math.min(page * pageSize, total)
  const colCount = table.getVisibleLeafColumns().length

  return (
    <div className="space-y-3">
      {toolbar}
      {isError ? (
        <EmptyState
          variant="error"
          title="Couldn't load these records"
          description="Check your connection and try again."
          action={onRetry && <Button variant="outline" size="sm" onClick={onRetry}><IconRefresh /> Retry</Button>}
        />
      ) : (
        <div className="overflow-hidden rounded-xl border border-border/70 bg-card shadow-[0_1px_2px_0_rgb(0_0_0/0.03)]">
          <div className={cn("overflow-x-auto", isFetching && !isLoading && "opacity-75 transition-opacity")}>
            <Table>
              <TableHeader>
                {table.getHeaderGroups().map((hg) => (
                  <TableRow key={hg.id} className="border-border/70 hover:bg-transparent">
                    {hg.headers.map((h) => {
                      const sortable = h.column.getCanSort() && !!onSortingChange
                      const dir = h.column.getIsSorted()
                      const label = h.isPlaceholder ? null : flexRender(h.column.columnDef.header, h.getContext())
                      return (
                        <TableHead key={h.id} className="h-12 px-4 text-sm font-medium text-muted-foreground first:pl-6 last:pr-6">
                          {sortable ? (
                            <button
                              type="button"
                              onClick={h.column.getToggleSortingHandler()}
                              className="inline-flex cursor-pointer items-center gap-1 font-medium transition-colors hover:text-foreground"
                            >
                              {label}
                              {dir === "asc" ? <IconArrowUp className="size-3.5 text-primary" />
                                : dir === "desc" ? <IconArrowDown className="size-3.5 text-primary" />
                                : <IconArrowsSort className="size-3.5 opacity-40" />}
                            </button>
                          ) : label}
                        </TableHead>
                      )
                    })}
                  </TableRow>
                ))}
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  Array.from({ length: Math.min(pageSize, 8) }).map((_, r) => (
                    <TableRow key={r} className="hover:bg-transparent">
                      {Array.from({ length: colCount }).map((_, c) => (
                        <TableCell key={c} className="px-4 py-4 first:pl-6 last:pr-6">
                          <Skeleton className={cn("h-4", c === 0 ? "w-40" : "w-20")} />
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : table.getRowModel().rows.length ? (
                  table.getRowModel().rows.map((row) => (
                    <TableRow
                      key={row.id}
                      className={cn("border-border/70", onRowClick && "cursor-pointer")}
                      onClick={(e) => {
                        if (!onRowClick) return
                        if ((e.target as HTMLElement).closest("a,button,input,[role=menuitem]")) return
                        onRowClick(row.original)
                      }}
                    >
                      {row.getVisibleCells().map((cell) => (
                        <TableCell key={cell.id} className="px-4 py-3.5 text-sm first:pl-6 last:pr-6">
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow className="hover:bg-transparent">
                    <TableCell colSpan={colCount} className="p-0">
                      <EmptyState className="rounded-none border-0 bg-transparent py-12" title={emptyTitle} description={emptyDescription} action={emptyAction} />
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
          <div className="flex flex-col gap-2.5 border-t border-border/70 px-6 py-3 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
            <div className="tabular-nums">
              Showing <span className="font-medium text-foreground">{start}</span> to{" "}
              <span className="font-medium text-foreground">{end}</span> of{" "}
              <span className="font-medium text-foreground">{total}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="font-medium text-foreground tabular-nums">Page {page} of {pages}</span>
              <div className="flex items-center gap-1">
                <Button variant="outline" size="icon" className="size-7 bg-card shadow-none" aria-label="Previous page" disabled={page <= 1 || isLoading} onClick={() => onPageChange(page - 1)}>
                  <IconChevronLeft className="size-3.5" />
                </Button>
                <Button variant="outline" size="icon" className="size-7 bg-card shadow-none" aria-label="Next page" disabled={page >= pages || isLoading} onClick={() => onPageChange(page + 1)}>
                  <IconChevronRight className="size-3.5" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
```

### Row actions (same file)

A visible outline **View** button plus a three-dot menu: immediate actions, separator, destructive actions (which open a `ConfirmDialog`).

```tsx
import { Link } from "react-router"
import { IconDots, IconEye } from "@tabler/icons-react"
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export interface RowActionItem {
  label: string
  icon?: ReactNode
  onClick?: () => void
  href?: string
  hidden?: boolean
  disabled?: boolean
}

export function DataTableRowActions({
  viewHref,
  onView,
  actions = [],
  destructiveActions = [],
}: {
  viewHref?: string
  onView?: () => void
  actions?: RowActionItem[]
  destructiveActions?: RowActionItem[]
}) {
  const items = actions.filter((a) => !a.hidden)
  const danger = destructiveActions.filter((a) => !a.hidden)
  const viewCls = "h-7 gap-1.5 px-2.5 text-xs font-medium shadow-none hover:bg-muted"
  return (
    <div className="flex items-center justify-end gap-1.5" onClick={(e) => e.stopPropagation()}>
      {viewHref ? (
        <Button variant="outline" size="sm" className={viewCls} render={<Link to={viewHref} />}>
          <IconEye className="size-3.5 text-primary" /> View
        </Button>
      ) : onView ? (
        <Button variant="outline" size="sm" className={viewCls} onClick={onView}>
          <IconEye className="size-3.5 text-primary" /> View
        </Button>
      ) : null}
      {(items.length > 0 || danger.length > 0) && (
        <DropdownMenu>
          <DropdownMenuTrigger
            render={<Button variant="ghost" size="icon" className="size-7 text-muted-foreground hover:text-foreground" aria-label="More actions" />}
          >
            <IconDots className="size-4" />
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-48">
            {items.map((a) =>
              a.href ? (
                <DropdownMenuItem key={a.label} disabled={a.disabled} render={<Link to={a.href} />}>
                  {a.icon}
                  {a.label}
                </DropdownMenuItem>
              ) : (
                <DropdownMenuItem key={a.label} disabled={a.disabled} onClick={a.onClick}>
                  {a.icon}
                  {a.label}
                </DropdownMenuItem>
              ),
            )}
            {items.length > 0 && danger.length > 0 && <DropdownMenuSeparator />}
            {danger.map((a) => (
              <DropdownMenuItem key={a.label} variant="destructive" disabled={a.disabled} onClick={a.onClick}>
                {a.icon}
                {a.label}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      )}
    </div>
  )
}
```

---

## data-table-toolbar.tsx

Sits on the canvas above the table panel. Debounced search, select filters, auto "Reset".

```tsx
import { useEffect, useState, type ReactNode } from "react"
import { IconFilterOff, IconSearch, IconX } from "@tabler/icons-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export interface DataTableFilter {
  id: string
  label: string
  value: string
  options: { label: string; value: string }[]
  onChange: (value: string) => void
}

const ALL = "ALL"

export function DataTableToolbar({
  search = "",
  onSearchChange,
  searchPlaceholder = "Search…",
  filters = [],
  actions,
}: {
  search?: string
  onSearchChange?: (value: string) => void
  searchPlaceholder?: string
  filters?: DataTableFilter[]
  /** Right side: column toggle, export. */
  actions?: ReactNode
}) {
  const [draft, setDraft] = useState(search)
  useEffect(() => setDraft(search), [search])
  useEffect(() => {
    if (draft === search) return
    const t = setTimeout(() => onSearchChange?.(draft), 300)
    return () => clearTimeout(t)
  }, [draft]) // eslint-disable-line react-hooks/exhaustive-deps

  const dirty = !!search || filters.some((f) => f.value !== ALL)

  return (
    <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center">
      {onSearchChange && (
        <div className="relative w-full sm:w-72">
          <IconSearch className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder={searchPlaceholder}
            className="h-8 bg-card pr-8 pl-8 shadow-none"
          />
          {draft && (
            <button
              type="button"
              aria-label="Clear search"
              onClick={() => { setDraft(""); onSearchChange("") }}
              className="absolute top-1/2 right-2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            >
              <IconX className="size-3.5" />
            </button>
          )}
        </div>
      )}
      {filters.map((f) => (
        <Select key={f.id} value={f.value} onValueChange={(v) => v != null && f.onChange(String(v))}>
          <SelectTrigger size="sm" className="h-8 w-full bg-card shadow-none sm:w-40" aria-label={f.label}>
            <SelectValue placeholder={f.label} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All {f.label.toLowerCase()}</SelectItem>
            {f.options.map((o) => (
              <SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      ))}
      {dirty && (
        <Button
          variant="ghost"
          size="sm"
          className="h-8 text-muted-foreground"
          onClick={() => { setDraft(""); onSearchChange?.(""); filters.forEach((f) => f.onChange(ALL)) }}
        >
          <IconFilterOff className="size-3.5" /> Reset
        </Button>
      )}
      {actions && <div className="flex items-center gap-2 sm:ml-auto">{actions}</div>}
    </div>
  )
}
```

For tab-like filters with few values (All / Active / Expired), use a `SegmentedControl` with counts instead of a select.

---

## confirm-dialog.tsx

```tsx
import type { ReactNode } from "react"
import { IconLoader2 } from "@tabler/icons-react"
import { Button } from "@/components/ui/button"
import {
  Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle,
} from "@/components/ui/dialog"

export function ConfirmDialog({
  open,
  onOpenChange,
  title,
  description,
  confirmLabel = "Confirm",
  variant = "default",
  isPending,
  onConfirm,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: ReactNode
  description?: ReactNode
  confirmLabel?: string
  variant?: "default" | "destructive"
  isPending?: boolean
  onConfirm: () => void | Promise<unknown>
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="font-medium">{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <DialogFooter>
          <Button variant="ghost" onClick={() => onOpenChange(false)} disabled={isPending}>Cancel</Button>
          <Button
            variant={variant === "destructive" ? "destructive" : "default"}
            disabled={isPending}
            onClick={async () => { await onConfirm(); onOpenChange(false) }}
          >
            {isPending && <IconLoader2 className="animate-spin" />}
            {confirmLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

---

## country-flag.tsx (optional)

Emoji flags render as letters on Windows, so use SVG flags from `country-flag-icons` (`npm i country-flag-icons`).

```tsx
import * as Flags from "country-flag-icons/react/3x2"
import { hasFlag } from "country-flag-icons"
import { cn } from "@/lib/utils"

export function CountryFlag({ code, className }: { code?: string | null; className?: string }) {
  const iso = code?.trim().toUpperCase()
  if (!iso || !hasFlag(iso)) return <span className={cn("inline-block h-3 w-4.5 rounded-[2px] bg-muted", className)} />
  const Flag = Flags[iso as keyof typeof Flags]
  return <Flag title={iso} className={cn("inline-block h-3 w-4.5 shrink-0 rounded-[2px] shadow-[0_0_0_1px_rgb(0_0_0/0.06)]", className)} />
}
```
