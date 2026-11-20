# Page patterns

Compositions built from the kit in `components.md`. Each section is a recipe for a page type or a page region.

## Contents

1. Overview / analytics page (KPI strip + chart + ranked lists)
2. Charts (recharts)
3. List page (table)
4. Detail page
5. Create / edit form page
6. Settings page
7. Period and date filters
8. Maps (optional)

---

## 1. Overview / analytics page

The signature composition: KPIs on top, the main chart **in the same panel**, then a 2-column grid of ranked lists.

```tsx
const [metric, setMetric] = useState<"orders" | "revenue">("revenue")

<PageHeader title="Overview" description="How the business is doing." actions={<RangeSwitcher value={range} onChange={setRange} />} />

<MetricStrip
  metrics={
    <>
      <Metric label="Revenue" value={formatMoney(cur.revenue)} delta={delta(cur.revenue, prev.revenue)}
        active={metric === "revenue"} onClick={() => setMetric("revenue")} isLoading={isLoading} />
      <Metric label="Orders" value={formatNumber(cur.orders)} delta={delta(cur.orders, prev.orders)}
        active={metric === "orders"} onClick={() => setMetric("orders")} isLoading={isLoading} />
      <Metric label="Refunds" value={cur.refunds} delta={{ value: 12, invert: true }} isLoading={isLoading} />
      <Metric label="Online now" value={live} live />
    </>
  }
>
  <div className="border-t border-border/70 px-3 pt-6 pb-4 sm:px-5">
    <TrendChart data={series} metric={metric} />
  </div>
</MetricStrip>

<div className="grid gap-4 lg:grid-cols-2">
  <Panel>
    <PanelHeader title="Top products" actions={<SegmentedControl size="sm" aria-label="Measure" value={by} onValueChange={setBy}
      options={[{ value: "revenue", label: "Revenue" }, { value: "units", label: "Units" }]} />} />
    <PanelContent><BarList items={topProducts} limit={8} formatValue={by === "revenue" ? compactMoney : compact} /></PanelContent>
    <PanelFooter><Link to="/admin/products"><IconArrowsDiagonal className="size-3.5" /> Details</Link></PanelFooter>
  </Panel>
  <Panel>…countries / channels…</Panel>
</div>
```

where `const delta = (c: number, p: number) => { const v = pctChange(c, p); return v == null ? null : { value: v } }`.

Rules:
- 4-7 metrics. Clicking a metric switches the chart series (ink underline marks it). Metrics with no baseline get a `hint` instead of a fake 0% delta.
- Below the hero, panels go in `grid gap-4 lg:grid-cols-2`, stacking on mobile. A "Needs attention" panel (counts that link to filtered lists) is a good third row for admin overviews.
- Controls for the page (range, interval, refresh) are small white `rounded-full`/`rounded-lg` buttons on the canvas in the `PageHeader` actions.
- If two panels compete for attention, merge or remove one.

---

## 2. Charts (recharts + shadcn `ChartContainer`)

```tsx
import { Area, Bar, CartesianGrid, ComposedChart, XAxis, YAxis } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart"

const config = {
  orders: { label: "Orders", color: "var(--data-sky)" },
  revenue: { label: "Revenue", color: "var(--data-coral)" },
} satisfies ChartConfig

export function TrendChart({ data }: { data: { day: string; orders: number; revenue: number }[] }) {
  return (
    <ChartContainer config={config} className="aspect-auto h-72 w-full min-w-0">
      <ComposedChart data={data} margin={{ left: 4, right: 4, top: 8 }}>
        <defs>
          <linearGradient id="fill-orders" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--color-orders)" stopOpacity={0.35} />
            <stop offset="100%" stopColor="var(--color-orders)" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid vertical={false} strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="day" axisLine={false} tickLine={false} tickMargin={8} minTickGap={24}
          tick={{ fill: "var(--muted-foreground)", fontSize: 12 }} />
        <YAxis yAxisId="count" axisLine={false} tickLine={false} width={40} tickCount={5}
          tick={{ fill: "var(--muted-foreground)", fontSize: 12 }} tickFormatter={compact} />
        <YAxis yAxisId="money" orientation="right" axisLine={false} tickLine={false} width={56} tickCount={5}
          tick={{ fill: "var(--muted-foreground)", fontSize: 12 }} tickFormatter={compactMoney} />
        <ChartTooltip cursor={{ stroke: "var(--border)" }} content={<ChartTooltipContent />} />
        <Bar yAxisId="money" dataKey="revenue" fill="var(--color-revenue)" radius={[6, 6, 0, 0]} maxBarSize={28} />
        <Area yAxisId="count" dataKey="orders" type="monotone" stroke="var(--color-orders)" strokeWidth={2}
          fill="url(#fill-orders)" dot={false} activeDot={{ r: 4 }} />
      </ComposedChart>
    </ChartContainer>
  )
}
```

Conventions:
- **Colours from tokens only**: sky for counts, coral for money, `--chart-1..5` for multi-series (max 4). Status colours are not series colours.
- Lines/areas: `monotone`, 2px, no dots (active dot only), area fill a vertical gradient 0.35 → 0.
- Bars: `radius={[6,6,0,0]}`. Mark the current partial period with a lighter or dashed segment.
- Grid: horizontal dashed lines only. No axis lines, no tick lines, no chart border, 4-5 ticks, compact numbers (`1.2k`, `KES 12k`).
- Dual axis only for one count + one money series.
- Legend (if any) or a `SegmentedControl` goes **above** the chart.
- Fixed height (`h-64`–`h-80`) inside a `min-w-0` wrapper. Loading = one `Skeleton` block of the same height. Empty = an `EmptyState` ("No sales in this range"), never an empty axis. Error = `EmptyState variant="error"` with Retry.
- Numbers in the tooltip use the same formatter as the metric strip above.
- Donuts only for 2-5 parts of a whole, with the total in the middle and a legend list beside it.

---

## 3. List page (table)

```tsx
const col = createColumnHelper<User>()
const columns = [
  col.accessor("name", {
    header: "User",
    cell: ({ row: { original: u } }) => (
      <div className="flex items-center gap-3">
        <Avatar className="size-9">
          <AvatarFallback className="bg-data-sky-soft text-sm font-medium text-foreground">{initials(u.name)}</AvatarFallback>
        </Avatar>
        <div className="min-w-0">
          <div className="truncate font-medium text-foreground">{u.name}</div>
          <div className="flex items-center gap-1.5 truncate text-xs text-muted-foreground">
            <CountryFlag code={u.country} /> {u.email} <span aria-hidden>·</span>
            <span title={formatDate(u.createdAt)}>{relativeTime(u.createdAt)}</span>
          </div>
        </div>
      </div>
    ),
  }),
  col.accessor("plan", { header: "Plan", cell: (i) => <StatusBadge status={i.getValue()} /> }),
  col.accessor("status", { header: "Status", cell: (i) => <StatusBadge status={i.getValue()} dot /> }),
  col.accessor("spend", {
    header: () => <div className="text-right">Spend</div>,
    cell: (i) => <div className="text-right tabular-nums">{formatMoney(i.getValue())}</div>,
  }),
  col.display({
    id: "actions",
    header: "",
    cell: ({ row }) => (
      <DataTableRowActions
        viewHref={`/admin/users/${row.original.id}`}
        actions={[{ label: "Edit", icon: <IconPencil />, href: `/admin/users/${row.original.id}/edit` }]}
        destructiveActions={[{ label: "Suspend", icon: <IconBan />, onClick: () => askSuspend(row.original) }]}
      />
    ),
  }),
]

<PageHeader title="Users" description="Everyone who has signed up." actions={<Button render={<Link to="/admin/users/new" />}><IconPlus /> New user</Button>} />
<DataTable
  columns={columns} data={rows} getRowId={(r) => r.id}
  total={total} page={page} pageSize={limit} onPageChange={setPage}
  sorting={sorting} onSortingChange={setSorting}
  isLoading={q.isLoading} isFetching={q.isFetching} isError={q.isError} onRetry={q.refetch}
  toolbar={<DataTableToolbar search={search} onSearchChange={setSearch} filters={[statusFilter]} />}
  emptyTitle={search ? "No users match your search" : "No users yet"}
  emptyAction={!search && <Button render={<Link to="/admin/users/new" />}>Invite the first user</Button>}
/>
```

Rules:
- **Rich first column**: avatar (initials on a soft tint, or logo) + name (`font-medium`) + one muted meta line with small icons/flags and a relative time (absolute date in `title`). Truncate, never wrap names.
- Status and tier as `StatusBadge`. Money right-aligned, `tabular-nums`, entered/shown in major units (KES, USD), never cents.
- Header row has **no background**; header text `text-sm font-medium text-muted-foreground`; rows `py-3.5` with hairline dividers; extra padding on first/last cells.
- Keep pagination, sort, search and filters in the URL (nuqs / `useSearchParams`) so lists are shareable and survive refresh.
- Empty copy differs for "nothing yet" (with a create action) and "no results for these filters" (with reset).
- `isFetching` dims the table slightly; never blank it during refetch.
- At 375px the table scrolls horizontally **inside** its panel.
- Tab-like status filters with counts: `SegmentedControl` above the table instead of a select.

---

## 4. Detail page

```tsx
const { data: user, isLoading, isError } = useUser(id)
useBreadcrumbLabel(user?.name) // before any early return

if (isError) return (
  <EmptyState variant="error" title="User not found" description="It may have been removed, or the link is wrong."
    action={<Button variant="outline" render={<Link to="/admin/users" />}>View all users</Button>} />
)

<PageHeader
  media={<Avatar className="size-12"><AvatarFallback className="bg-data-sky-soft text-base">{initials(user.name)}</AvatarFallback></Avatar>}
  title={user.name}
  statusBadge={<StatusBadge status={user.status} dot />}
  description={<>{user.email} · Joined {formatDate(user.createdAt)}</>}
  actions={<>
    <Button render={<Link to={`/admin/users/${id}/edit`} />}><IconPencil /> Edit</Button>
    <DropdownMenu>
      <DropdownMenuTrigger render={<Button variant="outline" size="icon" aria-label="More actions" />}><IconDots /></DropdownMenuTrigger>
      <DropdownMenuContent align="end">…</DropdownMenuContent>
    </DropdownMenu>
  </>}
/>
<SegmentedControl aria-label="Sections" value={tab} onValueChange={setTab}
  options={[{ value: "overview", label: "Overview" }, { value: "orders", label: "Orders", count: 42 }, { value: "activity", label: "Activity" }]} />
{tab === "overview" && <div className="grid gap-4 lg:grid-cols-3">…</div>}
```

- **No back button.** The breadcrumb shows `Admin › Users › Jane Wanjiku` and is the way back.
- Key facts as a definition list inside a Panel: label `text-sm text-muted-foreground`, value `text-sm text-foreground`, rows divided by hairlines. Copyable ids in `font-mono text-xs` with a copy icon button.
- Tabs synced to the URL (`?tab=orders`).

---

## 5. Create / edit form page

```tsx
<PageHeader title="New coupon" description="Give shoppers a discount at checkout." />
<FormPage
  onSubmit={handleSubmit}
  actions={<>
    <Button type="button" variant="ghost" render={<Link to="/admin/coupons" />}>Cancel</Button>
    <Button type="submit" disabled={m.isPending}>{m.isPending && <IconLoader2 className="animate-spin" />}Create coupon</Button>
  </>}
>
  {serverError && <Alert variant="destructive"><AlertDescription>{serverError}</AlertDescription></Alert>}
  <FormSection title="Details" description="What shoppers type and what they get.">
    <FormField label="Code" htmlFor="code" required error={errors.code} hint="Letters and numbers, no spaces">
      <Input id="code" placeholder="WELCOME10" aria-invalid={!!errors.code} value={code}
        onChange={(e) => setCode(e.target.value.toUpperCase())} onBlur={() => validate("code")} />
    </FormField>
    <FormField label="Discount (KES)" htmlFor="amount" required error={errors.amount}>
      <Input id="amount" type="number" inputMode="decimal" min={0} placeholder="250" />
    </FormField>
    <FormField label="Notes" htmlFor="notes" span="full" hint="Only admins see this.">
      <Textarea id="notes" rows={3} />
    </FormField>
  </FormSection>
  <FormSection title="Limits">…</FormSection>
</FormPage>
```

- Left-aligned, `max-w-4xl`, never `mx-auto` centred. When a form has a summary/preview, use `grid gap-6 2xl:grid-cols-[minmax(0,1fr)_24rem]` with a sticky right column; below `2xl` the side cards go above the form in a 2-up grid, and `FormPage` gets `className="max-w-none"`.
- Sticky action bar at the bottom: **Cancel** is a ghost link to the list/detail (not "Back"), primary is the brand colour with a verb ("Create coupon", "Save changes").
- Validate on blur and on submit; message under the field; `aria-invalid`; focus the first invalid field on submit. Server errors go in a destructive `Alert` at the top. Disable submit while pending with a spinner. Toast success (`sonner`) and navigate to the detail page.
- Right input types: `type="email"`, `inputMode="tel"`, `type="number" inputMode="decimal"` for money in major units, date inputs or a calendar popover. Placeholders show a real example. Hints explain format/units.
- Dialog forms: same `FormField`s inside `DialogContent`, footer Cancel (ghost) then primary. More than ~5 fields → make it a page.
- Edit pages call `useBreadcrumbLabel(record.name)` so the trail reads `Users › Jane › Edit`.

---

## 6. Settings page

```tsx
<SettingsLayout
  nav={[
    { value: "general", label: "General", icon: IconSettings },
    { value: "notifications", label: "Notifications", icon: IconBell },
    { value: "security", label: "Security", icon: IconShieldLock },
  ]}
  value={tab}
  onValueChange={setTab}
  footer={<>
    <SettingsFooterAction icon={IconLogout} onClick={logout}>Log out</SettingsFooterAction>
    <SettingsFooterAction icon={IconTrash} destructive onClick={() => setConfirmDelete(true)}>Delete account</SettingsFooterAction>
  </>}
>
  <SettingsCard title="Profile">
    <SettingsRow>
      <div className="flex items-center gap-4">
        <Avatar className="size-12">…</Avatar>
        <Input className="max-w-xs" value={name} onChange={…} />
        <Button disabled={name === saved || m.isPending}>Save</Button>
      </div>
    </SettingsRow>
  </SettingsCard>
  <SettingsCard>
    <SettingsRow label="Theme" description="Light, dark, or follow your device." control={<Select …/>} />
    <SettingsRow label="Weekly report" description="A summary every Monday." control={<Switch …/>} />
  </SettingsCard>
</SettingsLayout>
```

- `text-3xl` title, left nav (`lg:w-56`) with the **ink** active pill and icons; horizontal scroller on mobile.
- Narrow right column (`max-w-2xl`). Cards with a `title` get a divided header; rows separated by hairlines.
- Saves are inline with their control and stay disabled until the value changes. Toggles save immediately with a toast.
- Footer actions are quiet text buttons; destructive ones turn red only on hover and always confirm.

---

## 7. Period and date filters

- A compact white pill on the canvas: calendar icon + current period + chevron, opening a dropdown of presets (Today, Yesterday, Last 7 days, Last 30 days, Last 12 months, Custom). Selected preset is a radio item.
- Optional previous/next arrow buttons beside it and an icon-only refresh button (`aria-label="Refresh"`).
- Custom opens a two-month calendar in a popover with Start/End inputs, Clear and Apply.
- Sync the period to the URL. Compare against the previous period of the same length for deltas.

---

## 8. Maps (optional, `maplibre-gl`)

For "where are our users":

- Flat map (Mercator, no globe) in a `Panel` with `overflow-hidden` and fixed height (`h-80`–`h-[28rem]`).
- Free basemap with no API key: `https://tiles.openfreemap.org/styles/positron` (light) or `/dark` in dark mode. Keep attribution.
- Countries as HTML markers (`new maplibregl.Marker({ element })`): the country's flag (from `country-flag-icons/string/1x1`) clipped to a circle sized by `sqrt(count)`, a soft `primary/15` halo and a small brand-coloured count badge. Position from an ISO-code → centroid table; you do not need stored coordinates.
- Hover/focus opens a themed popup (`className: "dashboard-map-popup"`). Fit bounds to the data; disable rotate/pitch; zoom buttons only.
- Create the map in an effect and `map.remove()` on cleanup; call `map.resize()` from a `ResizeObserver`.
- **Vite**: set the worker URL explicitly, or the map stays blank in production:
  `import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?url"; maplibregl.setWorkerUrl(workerUrl)`.
  Some servers (nginx without an `mjs` MIME type) serve `.mjs` as `application/octet-stream` and module workers refuse to load. Emit it as `.js`:
  `build.rollupOptions.output.assetFileNames: (a) => a.names.some((n) => n.endsWith(".mjs")) ? "assets/[name]-[hash].js" : "assets/[name]-[hash][extname]"` (use `rolldownOptions` on Vite 8).
- Always pair the map with a `BarList` of the same data (the map alone is not accessible).
