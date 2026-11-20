# Layout shell: sidebar, sticky canvas header, breadcrumbs

The shell is built once. Pages render only their content inside it.

```
┌──────────────┬──────────────────────────────────────────────────────┐
│ [logo] Name  │ [≡]  Admin › Users › Jane Wanjiku            ADMIN   │ ← sticky, canvas/85 + blur, no border
│  Console     │                                                      │
│              │  Users                                  [+ New] [⋯]  │ ← PageHeader
│ Overview     │  Everyone who has signed up.                         │
│ ▣ Dashboard  │                                                      │
│ ▢ Analytics  │  ┌────────────────────────────────────────────────┐  │
│              │  │ Revenue │ Orders │ Users │ Online •            │  │ ← MetricStrip panel
│ Directory    │  │ KES 1.2M│  4,210 │   980 │   12                │  │
│ ▢ Users  ◀── soft brand pill                                     │  │
│              │  └────────────────────────────────────────────────┘  │
│ ─────────    │                                                      │
│ (JD) Jane    │      warm off-white canvas, white panels             │
└──────────────┴──────────────────────────────────────────────────────┘
```

## dashboard-layout.tsx

```tsx
import { useEffect } from "react"
import { Outlet } from "react-router" // Next.js: render {children}
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
import { BreadcrumbLabelProvider } from "@/components/dashboard"
import { AppSidebar } from "./app-sidebar"
import { DashboardHeader } from "./dashboard-header"

export function DashboardLayout() {
  // Portaled overlays (dialogs, menus, selects, popovers) mount on <body>, outside
  // .dashboard-scope. This class gives them the same tokens and font.
  useEffect(() => {
    document.body.classList.add("dashboard-portal")
    return () => document.body.classList.remove("dashboard-portal")
  }, [])

  return (
    <BreadcrumbLabelProvider>
      <SidebarProvider className="dashboard-scope bg-canvas">
        <AppSidebar />
        <SidebarInset className="min-w-0 bg-canvas">
          <DashboardHeader />
          <main className="mx-auto flex w-full max-w-[1440px] min-w-0 flex-1 flex-col gap-6 px-4 pt-2 pb-10 md:px-6 lg:px-8">
            <Outlet />
          </main>
        </SidebarInset>
      </SidebarProvider>
    </BreadcrumbLabelProvider>
  )
}
```

- `min-w-0` on the inset and `main` is required: without it a wide table pushes the whole page sideways.
- Pages do not add their own max-width or page padding.
- If the app only has the dashboard (no marketing pages), you can put the theme on `:root` and drop the scope/portal classes (see `theme.css`).

## nav-config.ts

Single source of truth for the sidebar and static breadcrumbs.

```ts
import type { ComponentType } from "react"
import { IconLayoutDashboard, IconUsers, IconSettings } from "@tabler/icons-react"

export interface NavItem {
  title: string
  url: string
  icon: ComponentType<{ className?: string }>
  exact?: boolean
  /** Pending count pill (e.g. open tickets). */
  count?: number
}

export const navGroups: { label: string; items: NavItem[] }[] = [
  { label: "Overview", items: [{ title: "Dashboard", url: "/admin", icon: IconLayoutDashboard, exact: true }] },
  { label: "Directory", items: [{ title: "Users", url: "/admin/users", icon: IconUsers }] },
  { label: "Operations", items: [{ title: "Settings", url: "/admin/settings", icon: IconSettings }] },
]

/** Static routes → crumb label (+ optional parent). Dynamic routes are matched in the breadcrumbs component. */
export const breadcrumbMap: Record<string, { label: string; parent?: string }> = {
  "/admin": { label: "Dashboard" },
  "/admin/users": { label: "Users" },
  "/admin/users/new": { label: "New user", parent: "/admin/users" },
  "/admin/settings": { label: "Settings" },
}
```

## app-sidebar.tsx

- Same canvas colour as the page, hairline right border (`variant="sidebar"`, not `inset`/`floating`), `collapsible="icon"`.
- Brand block **left-aligned**: logo (32px, `rounded-lg`) + product name (`font-medium`) + muted subtitle ("Admin Console").
- Group labels: sentence case, `text-xs font-medium text-muted-foreground/80`. Not uppercase-tracked.
- **Active item: soft brand pill** `bg-primary/10 text-primary` (hover `bg-primary/15`). Not a solid primary fill, not ink.
- Inactive: `text-foreground/75 hover:bg-sidebar-accent hover:text-foreground`. Items `h-9 rounded-lg`.
- Footer: user row (initials avatar on a soft tint, name, email, sign-out icon button) and an optional quiet "← Public website" link. That link is navigation out of the app, not a back button.
- Close the mobile sheet on navigation.

```tsx
import { Link, useLocation } from "react-router"
import { Badge } from "@/components/ui/badge"
import {
  Sidebar, SidebarContent, SidebarFooter, SidebarGroup, SidebarGroupContent, SidebarGroupLabel,
  SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarRail, useSidebar,
} from "@/components/ui/sidebar"
import { navGroups, type NavItem } from "./nav-config"
import { NavUser } from "./nav-user"

export function AppSidebar(props: React.ComponentProps<typeof Sidebar>) {
  const { pathname } = useLocation()
  const { isMobile, setOpenMobile } = useSidebar()
  const isActive = (i: NavItem) => (i.exact ? pathname === i.url : pathname === i.url || pathname.startsWith(`${i.url}/`))

  return (
    <Sidebar variant="sidebar" collapsible="icon" className="border-r border-sidebar-border/70" {...props}>
      <SidebarHeader className="pt-3">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" className="gap-3 rounded-lg hover:bg-sidebar-accent" render={<Link to="/admin" />}>
              <img src="/logo.png" alt="" className="size-8 shrink-0 rounded-lg object-contain" />
              <div className="grid flex-1 text-left text-sm leading-tight group-data-[collapsible=icon]:hidden">
                <span className="truncate font-medium tracking-tight text-foreground">Product name</span>
                <span className="truncate text-xs text-muted-foreground">Admin Console</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent className="py-1">
        {navGroups.map((group) => (
          <SidebarGroup key={group.label}>
            <SidebarGroupLabel className="text-xs font-medium text-muted-foreground/80">{group.label}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => {
                  const active = isActive(item)
                  const Icon = item.icon
                  return (
                    <SidebarMenuItem key={item.url}>
                      <SidebarMenuButton
                        tooltip={item.title}
                        isActive={active}
                        className={
                          active
                            ? "h-9 rounded-lg bg-primary/10 font-medium text-primary hover:bg-primary/15 hover:text-primary data-active:bg-primary/10 data-active:text-primary"
                            : "h-9 rounded-lg text-foreground/75 hover:bg-sidebar-accent hover:text-foreground"
                        }
                        render={<Link to={item.url} onClick={() => isMobile && setOpenMobile(false)} />}
                      >
                        <Icon className="size-4 shrink-0" />
                        <span className="flex-1 truncate">{item.title}</span>
                        {!!item.count && (
                          <Badge
                            variant={active ? "outline" : "secondary"}
                            className="ml-auto h-4 min-w-4 rounded-full px-1 text-[10px] tabular-nums"
                          >
                            {item.count}
                          </Badge>
                        )}
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  )
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>

      <SidebarFooter>
        <NavUser />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
```

## dashboard-header.tsx

Sticky, on the canvas (no white bar, no border): sidebar trigger as a small white button, breadcrumbs, and a quiet role pill on the right. **No centred logo** (the logo is in the sidebar).

```tsx
import { Badge } from "@/components/ui/badge"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { useBreadcrumbLabelValue } from "@/components/dashboard"
import { DashboardBreadcrumbs } from "./dashboard-breadcrumbs"

export function DashboardHeader({ role }: { role?: string }) {
  const detailLabel = useBreadcrumbLabelValue()
  return (
    <header className="sticky top-0 z-20 flex h-16 shrink-0 items-center justify-between gap-2 bg-canvas/85 px-4 backdrop-blur-md md:px-6 lg:px-8">
      <div className="flex min-w-0 items-center gap-3">
        <SidebarTrigger className="-ml-1 size-9 shrink-0 rounded-lg border border-border/70 bg-card shadow-[0_1px_2px_0_rgb(0_0_0/0.04)] hover:bg-muted" />
        <DashboardBreadcrumbs detailLabel={detailLabel} />
      </div>
      {role && (
        <Badge variant="outline" className="h-7 rounded-full border-border/70 bg-card px-3 text-xs font-medium tracking-wide text-muted-foreground uppercase">
          {role.replace(/_/g, " ")}
        </Badge>
      )}
    </header>
  )
}
```

## dashboard-breadcrumbs.tsx

`Admin › Section › Record`. Static routes from `breadcrumbMap`; detail routes matched by pattern, using the page-provided `detailLabel` (from `useBreadcrumbLabel`) and a short id only as a loading fallback.

```tsx
import { Link, useLocation } from "react-router"
import {
  Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { breadcrumbMap } from "./nav-config"

type Crumb = { label: string; href?: string }
const ROOT: Crumb = { label: "Admin", href: "/admin" }
const shortId = (id: string) => (id.length > 10 ? `${id.slice(0, 8)}…` : id)

// One entry per detail route: [pattern, section label, section href, fallback noun, optional trailing crumb]
const DETAIL_ROUTES: [RegExp, string, string, string, string?][] = [
  [/^\/admin\/users\/([^/]+)\/edit$/, "Users", "/admin/users", "User", "Edit"],
  [/^\/admin\/users\/([^/]+)$/, "Users", "/admin/users", "User"],
]

function crumbsFor(pathname: string, detailLabel?: string): Crumb[] {
  const path = pathname.replace(/\/+$/, "") || "/admin"
  const entry = breadcrumbMap[path]
  if (entry) {
    const parent = entry.parent ? breadcrumbMap[entry.parent] : undefined
    return [ROOT, ...(parent ? [{ label: parent.label, href: entry.parent }] : []), { label: entry.label }]
  }
  for (const [re, section, href, noun, trailing] of DETAIL_ROUTES) {
    const m = path.match(re)
    if (!m) continue
    const name = detailLabel ?? `${noun} #${shortId(m[1])}`
    return trailing
      ? [ROOT, { label: section, href }, { label: name, href: `${href}/${m[1]}` }, { label: trailing }]
      : [ROOT, { label: section, href }, { label: name }]
  }
  return [ROOT]
}

export function DashboardBreadcrumbs({ detailLabel }: { detailLabel?: string }) {
  const crumbs = crumbsFor(useLocation().pathname, detailLabel)
  return (
    <Breadcrumb>
      <BreadcrumbList className="flex-nowrap text-[0.95rem]">
        {crumbs.map((c, i) => {
          const last = i === crumbs.length - 1
          return (
            <span key={`${c.label}-${i}`} className={`inline-flex items-center gap-1.5 ${i === 0 ? "hidden sm:inline-flex" : ""}`}>
              <BreadcrumbItem>
                {last || !c.href ? (
                  <BreadcrumbPage className="max-w-[180px] truncate font-medium text-foreground sm:max-w-xs">{c.label}</BreadcrumbPage>
                ) : (
                  <BreadcrumbLink className="whitespace-nowrap" render={<Link to={c.href} />}>{c.label}</BreadcrumbLink>
                )}
              </BreadcrumbItem>
              {!last && <BreadcrumbSeparator />}
            </span>
          )
        })}
      </BreadcrumbList>
    </Breadcrumb>
  )
}
```

When you add a route: add the nav item and `breadcrumbMap` entry (static) or a `DETAIL_ROUTES` entry (dynamic), and call `useBreadcrumbLabel(record.name)` in the detail page.

## Theme toggle

If the dashboard has a light/dark/system setting, apply `.dark` on `<html>` while the dashboard is mounted and remove it on unmount when the rest of the site is light-only. Store the choice in `localStorage` (wrapped in try/catch).
