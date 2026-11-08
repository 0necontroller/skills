---
name: dashboard-ui
description: Design systems, layout architecture, grouped white sidebars with high-contrast active states, top bar with center logo and user role badge, and TanStack data tables with dedicated View buttons and three-dot immediate action menus.
---

# Dashboard UI Skill

Comprehensive guidelines, component architectures, and copy-paste-ready implementation patterns for building high-end, responsive administrative and operational dashboards with React, Next.js / React Router, Tailwind CSS, and shadcn/ui.

---

## 1. Prerequisites & shadcn/ui Component Installation

Before generating or modifying any dashboard components, the AI agent MUST perform the following prerequisite checks:

### Step 1: Verify shadcn/ui Setup (`components.json`)
Check if `components.json` exists in the project root:
- **If `components.json` is missing**: DO NOT attempt to write or install components blindly. Prompt the user:
  > "shadcn/ui configuration (`components.json`) was not found in this project. Please initialize shadcn/ui first (e.g. `npx shadcn@latest init`) so that component directories and path aliases are properly configured."
- **If `components.json` exists**: Proceed to component verification.

### Step 2: Install Required shadcn/ui Components
Check if the required primitives exist in your designated UI components directory (e.g., `@/components/ui/`). Run `npx shadcn@latest add <component>` for any missing components:

```bash
# Core Layout & Sidebar
npx shadcn@latest add sidebar collapsible separator sheet tooltip avatar dropdown-menu

# Page Header & Breadcrumbs
npx shadcn@latest add breadcrumb badge button

# Stats & Analytics Cards
npx shadcn@latest add card skeleton

# Date Filters
npx shadcn@latest add popover calendar

# Data Tables & Form Controls
npx shadcn@latest add table input select
```

Or install all dashboard essentials in one command:
```bash
npx shadcn@latest add sidebar collapsible separator sheet tooltip avatar dropdown-menu breadcrumb badge button card skeleton popover calendar table input select
```

### Step 3: Verify & Install Core npm Packages
All data tables in this skill are built with **TanStack Table (`@tanstack/react-table`)** combined with shadcn/ui `<Table>`. Ensure the following packages are present in `package.json`:

* **`@tanstack/react-table`**: Table state management, column definitions, pagination, and sorting.
* **`date-fns`**: Date parsing, formatting, and arithmetic for date filters.
* **`@tabler/icons-react`** or **`lucide-react`**: Standard icon set.

If missing, install them:
```bash
npm install @tanstack/react-table date-fns @tabler/icons-react
# or: pnpm add @tanstack/react-table date-fns @tabler/icons-react
# or: bun add @tanstack/react-table date-fns @tabler/icons-react
```

---

## 2. Design System & Theme Foundations

All dashboard components rely on semantic CSS variables, a crisp white sidebar canvas, and subtle, high-contrast visual tokens.

### Theme Tokens (`globals.css`)
```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  --card: 0 0% 100%;
  --card-foreground: 0 0% 3.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 0 0% 3.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --secondary: 24.6 95% 53.1%;
  --secondary-foreground: 0 0% 98%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --border: 214.3 31.8% 91.4%;
  --radius: 0.625rem;

  /* Clean White Sidebar Tokens */
  --sidebar: 0 0% 100%;
  --sidebar-foreground: 222.2 47.4% 11.2%;
  --sidebar-primary: 221.2 83.2% 53.3%;
  --sidebar-primary-foreground: 0 0% 100%;
  --sidebar-accent: 210 40% 96.1%;
  --sidebar-accent-foreground: 222.2 47.4% 11.2%;
  --sidebar-border: 214.3 31.8% 91.4%;
  --sidebar-ring: 221.2 83.2% 53.3%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --border: 217.2 32.6% 17.5%;

  /* Dark Sidebar Tokens */
  --sidebar: 222.2 84% 4.9%;
  --sidebar-foreground: 210 40% 98%;
  --sidebar-primary: 217.2 91.2% 59.8%;
  --sidebar-primary-foreground: 0 0% 100%;
  --sidebar-accent: 217.2 32.6% 17.5%;
  --sidebar-accent-foreground: 210 40% 98%;
  --sidebar-border: 217.2 32.6% 17.5%;
}
```

---

## 3. Dashboard Content Layout (`DashboardLayout.tsx`)

The dashboard layout orchestrates the overall workspace:
1. **Collapsible Trigger on the Left**: An accessible `<SidebarTrigger />` for toggling the sidebar dock.
2. **Brand Logo Centered**: The platform logo positioned prominently in the center of the header bar.
3. **User Role Badge on the Right**: An uppercase monospace badge indicating the authenticated user's authorization tier (e.g., `SYSTEM ADMINISTRATOR`).
4. **Muted Canvas Inset**: Main content wrapped in `<SidebarInset className="bg-muted/15 min-h-screen">` providing subtle separation from white cards and tables.

```tsx
import { Outlet } from "react-router"; // or { children } for Next.js App Router
import { DashboardSidebar } from "./DashboardSidebar";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Badge } from "@/components/ui/badge";
import { useCurrentUser } from "@/hooks/useCurrentUser";

export function DashboardLayout({ children }: { children?: React.ReactNode }) {
  const { user, role } = useCurrentUser();

  return (
    <SidebarProvider>
      <DashboardSidebar />
      <SidebarInset className="bg-muted/15 min-h-screen">
        {/* Header: fixed blur on mobile, clean integrated top bar on desktop */}
        <header className="fixed top-0 right-0 left-0 z-20 flex h-14 shrink-0 items-center gap-2 border-b bg-background/95 px-4 shadow-xs backdrop-blur transition-[width,height] ease-linear md:static md:h-14 md:border-none md:bg-transparent md:px-6 md:shadow-none">
          <div className="flex w-full items-center justify-between gap-2">
            {/* 1. Left: Sidebar Collapse Trigger */}
            <SidebarTrigger className="-ml-1" />

            {/* 2. Center: Brand Logo */}
            <div className="flex items-center gap-2 text-sm font-semibold tracking-tight">
              <img src="/logo.png" alt="Platform Logo" className="w-24 object-contain" />
            </div>

            {/* 3. Right: User Role Pill Badge */}
            {role ? (
              <Badge
                variant="outline"
                className="text-secondary bg-secondary/10 border-secondary uppercase font-mono px-3 py-1.5 text-xs font-semibold"
              >
                {role.replace(/_/g, " ")}
              </Badge>
            ) : (
              <div className="w-8" />
            )}
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex flex-1 flex-col gap-6 p-4 pt-18 md:p-6 md:pt-0">
          {children || <Outlet />}
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
```

---

## 4. Grouped Sidebar Architecture (`DashboardSidebar.tsx`)

The dashboard sidebar provides role-tailored navigation with:
* **Clean White Background**: Structured with `variant="inset"` and `collapsible="icon"`.
* **Grouped Sections**: Navigation items categorized under domain-specific headers (e.g., `WORKSPACE`, `DATA MANAGEMENT`, `QUALITY ASSURANCE`, `ADMINISTRATION`) using uppercase tracking-wider labels.
* **High-Contrast Active Indicator**: Active links use `bg-primary text-primary-foreground font-medium hover:bg-primary hover:text-primary-foreground` to provide unambiguous visual orientation.
* **Notification Pill Counters**: Display real-time pending action counts with dynamic badge variants (`variant={active ? "outline" : "secondary"}`).
* **Footer Profile & Portal Actions**: Includes quick navigation back to the public-facing portal, user avatar with initials fallback, user name/email, and a single-click sign-out action.

```tsx
import { Link, useLocation } from "react-router"; // or next/link and next/navigation
import {
  IconArrowLeft,
  IconBookmark,
  IconChartPie,
  IconCpu,
  IconDatabase,
  IconHistory,
  IconLayoutDashboard,
  IconLogout,
  IconServer,
  IconSettings,
  IconShieldCheck,
  IconUpload,
  IconUser,
  IconUsers,
} from "@tabler/icons-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useCurrentUser } from "@/hooks/useCurrentUser";

interface NavItem {
  title: string;
  url: string;
  icon: React.ComponentType<{ className?: string }>;
  exact?: boolean;
  count?: number;
}

interface NavSection {
  label: string;
  items: NavItem[];
}

export function DashboardSidebar(props: React.ComponentProps<typeof Sidebar>) {
  const location = useLocation();
  const { user, role, canUpload, canReview, canManageUsers, canManageDatasets, isSysAdmin, signOut } =
    useCurrentUser();

  const isItemActive = (url: string, exact?: boolean) => {
    if (exact) return location.pathname === url;
    return location.pathname === url || location.pathname.startsWith(`${url}/`);
  };

  const initials = user
    ? `${user.firstName?.[0] ?? ""}${user.lastName?.[0] ?? ""}`.toUpperCase() || "U"
    : "U";

  // Build role-tailored navigation sections
  const sections: NavSection[] = [
    {
      label: "Workspace",
      items: [
        { title: "Overview", url: "/dashboard", icon: IconLayoutDashboard, exact: true },
        { title: "Saved Bookmarks", url: "/dashboard/saved", icon: IconBookmark },
        { title: "My Profile", url: "/dashboard/profile", icon: IconUser },
      ],
    },
  ];

  if (canUpload) {
    sections.push({
      label: "Data Management",
      items: [
        { title: "Upload Dataset", url: "/dashboard/upload", icon: IconUpload },
        { title: "My Datasets", url: "/dashboard/my-datasets", icon: IconDatabase },
      ],
    });
  }

  if (canReview) {
    sections.push({
      label: "Quality Assurance",
      items: [
        {
          title: "Moderation Queue",
          url: "/dashboard/moderation",
          icon: IconShieldCheck,
          count: 3, // dynamic pending review counter
        },
      ],
    });
  }

  const adminItems: NavItem[] = [];
  if (canManageDatasets) {
    adminItems.push({ title: "Datasets", url: "/dashboard/datasets", icon: IconDatabase });
  }
  if (canManageUsers) {
    adminItems.push({ title: "User Management", url: "/dashboard/users", icon: IconUsers });
  }
  if (isSysAdmin) {
    adminItems.push({ title: "System Health", url: "/dashboard/system-health", icon: IconServer });
    adminItems.push({ title: "System Settings", url: "/dashboard/settings", icon: IconSettings });
  }
  adminItems.push({ title: "Audit Logs", url: "/dashboard/audit-logs", icon: IconHistory });

  if (adminItems.length > 0) {
    sections.push({
      label: "Administration",
      items: adminItems,
    });
  }

  return (
    <Sidebar variant="inset" collapsible="icon" className="bg-card border-r" {...props}>
      {/* Brand Header */}
      <SidebarHeader>
        <div className="flex items-center gap-3 px-2 py-2">
          <img
            src="/favicon.png"
            alt="Logo"
            className="size-8 shrink-0 rounded-md object-contain"
          />
          <div className="grid flex-1 text-left text-sm leading-tight group-data-[collapsible=icon]:hidden">
            <span className="truncate font-semibold tracking-tight text-foreground">
              Portal Workspace
            </span>
            <span className="truncate text-xs text-muted-foreground">
              Operational Management
            </span>
          </div>
        </div>
      </SidebarHeader>

      {/* Grouped Navigation Sections */}
      <SidebarContent>
        {sections.map((section) => (
          <SidebarGroup key={section.label}>
            <SidebarGroupLabel className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/75">
              {section.label}
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {section.items.map((item) => {
                  const active = isItemActive(item.url, item.exact);
                  const Icon = item.icon;
                  return (
                    <SidebarMenuItem key={item.url}>
                      <SidebarMenuButton
                        isActive={active}
                        tooltip={item.title}
                        className={
                          active
                            ? "bg-primary text-primary-foreground font-medium hover:bg-primary hover:text-primary-foreground"
                            : "text-muted-foreground hover:bg-muted hover:text-foreground"
                        }
                        render={
                          <Link to={item.url} className="flex items-center gap-2.5 w-full">
                            <Icon className="size-4 shrink-0" />
                            <span className="truncate flex-1">{item.title}</span>
                            {item.count !== undefined && item.count > 0 && (
                              <Badge
                                variant={active ? "outline" : "secondary"}
                                className="ml-auto text-[10px] font-mono h-4 min-w-4 px-1 flex items-center justify-center rounded-full"
                              >
                                {item.count}
                              </Badge>
                            )}
                          </Link>
                        }
                      />
                    </SidebarMenuItem>
                  );
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>

      {/* Footer Profile & Actions */}
      <SidebarFooter className="border-t bg-card">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Public Portal"
              render={
                <Link
                  to="/"
                  className="flex items-center gap-2.5 text-xs text-muted-foreground hover:text-foreground"
                >
                  <IconArrowLeft className="size-4" />
                  <span>Public Portal</span>
                </Link>
              }
            />
          </SidebarMenuItem>

          <SidebarMenuItem>
            <div className="flex items-center gap-2 p-2 group-data-[collapsible=icon]:p-0">
              <Link
                to="/dashboard/profile"
                className="flex items-center gap-2 flex-1 min-w-0 hover:opacity-80 transition-opacity"
              >
                <Avatar className="size-8">
                  <AvatarFallback className="bg-primary/10 text-primary text-xs font-bold">
                    {initials}
                  </AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-xs leading-tight group-data-[collapsible=icon]:hidden">
                  <span className="truncate font-semibold text-foreground">
                    {user ? `${user.firstName} ${user.lastName}` : "User"}
                  </span>
                  <span className="truncate text-[11px] text-muted-foreground">
                    {user?.email}
                  </span>
                </div>
              </Link>
              <button
                type="button"
                onClick={signOut}
                className="text-muted-foreground hover:text-rose-600 transition-colors p-1 rounded-md hover:bg-rose-500/10 group-data-[collapsible=icon]:hidden cursor-pointer"
                title="Sign out"
              >
                <IconLogout className="size-4" />
              </button>
            </div>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
```

---

## 5. Page Header, Breadcrumbs & Title Hierarchy

Every page starts with a clean header row pairing hierarchical breadcrumbs, an accessible `<h1>` title, a subtitle, and an action/filter toolbar.

```tsx
import Link from 'next/link';
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator
} from '@/components/ui/breadcrumb';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

interface PageHeaderProps {
  breadcrumbs?: { title: string; href?: string }[];
  title: string;
  subtitle?: string;
  statusBadge?: React.ReactNode;
  children?: React.ReactNode; // Action buttons or filters
}

export function PageHeader({
  breadcrumbs,
  title,
  subtitle,
  statusBadge,
  children
}: PageHeaderProps) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        {breadcrumbs && breadcrumbs.length > 0 && (
          <Breadcrumb className="mb-2">
            <BreadcrumbList>
              {breadcrumbs.map((crumb, idx) => {
                const isLast = idx === breadcrumbs.length - 1;
                return (
                  <span key={crumb.title} className="inline-flex items-center gap-1.5">
                    <BreadcrumbItem>
                      {isLast || !crumb.href ? (
                        <BreadcrumbPage>{crumb.title}</BreadcrumbPage>
                      ) : (
                        <BreadcrumbLink asChild>
                          <Link href={crumb.href}>{crumb.title}</Link>
                        </BreadcrumbLink>
                      )}
                    </BreadcrumbItem>
                    {!isLast && <BreadcrumbSeparator />}
                  </span>
                );
              })}
            </BreadcrumbList>
          </Breadcrumb>
        )}

        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-semibold tracking-tight md:text-3xl md:font-bold">
            {title}
          </h1>
          {statusBadge}
        </div>

        {subtitle && (
          <p className="text-muted-foreground text-sm mt-1">
            {subtitle}
          </p>
        )}
      </div>

      {children && (
        <div className="flex flex-wrap items-center gap-2">
          {children}
        </div>
      )}
    </div>
  );
}
```

---

## 6. Stats Cards with Subtle Gradients

### Gradient & Container Query Pattern
1. Apply the parent wildcard selector `*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:bg-gradient-to-t` in light mode.
2. Fall back to `dark:*:data-[slot=card]:bg-card` for clean dark mode cards.
3. Add `@container/card` on the card to scale title typography dynamically (`@[250px]/card:text-3xl`).
4. Display trend indicators via absolute badges in top-right.

```tsx
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

export interface StatItem {
  label: string;
  value: string | number;
  change?: number; // e.g. 12.5 or -3.2
  periodText?: string;
  footerNote?: string;
}

export function StatsGrid({
  items,
  isLoading
}: {
  items: StatItem[];
  isLoading?: boolean;
}) {
  return (
    <div className="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card grid grid-cols-1 gap-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:shadow-xs sm:grid-cols-2 xl:grid-cols-4">
      {items.map((stat, idx) => (
        <Card key={idx} className="@container/card" data-slot="card">
          <CardHeader className="relative pb-2">
            <CardDescription className="font-medium">
              {stat.label}
            </CardDescription>

            <CardTitle className="text-2xl font-bold tracking-tight tabular-nums @[250px]/card:text-3xl">
              {isLoading ? (
                <Skeleton className="h-8 w-28" />
              ) : (
                stat.value
              )}
            </CardTitle>

            {stat.change !== undefined && !isLoading && (
              <div className="absolute top-4 right-4">
                <Badge
                  variant="outline"
                  className={`flex items-center gap-0.5 rounded-lg text-xs font-semibold ${
                    stat.change >= 0
                      ? 'border-green-600/20 bg-green-50 text-green-600 dark:border-green-400/20 dark:bg-green-950 dark:text-green-400'
                      : 'border-red-600/20 bg-red-50 text-red-600 dark:border-red-400/20 dark:bg-red-950 dark:text-red-400'
                  }`}
                >
                  <span>{stat.change >= 0 ? '↑' : '↓'}</span>
                  <span>{Math.abs(stat.change).toFixed(1)}%</span>
                </Badge>
              </div>
            )}
          </CardHeader>

          {(stat.periodText || stat.footerNote) && (
            <CardFooter className="flex-col items-start gap-1 text-xs text-muted-foreground pt-0">
              {stat.periodText && (
                <div className="font-medium text-foreground">
                  {stat.periodText}
                </div>
              )}
              {stat.footerNote && <div>{stat.footerNote}</div>}
            </CardFooter>
          )}
        </Card>
      ))}
    </div>
  );
}
```

---

## 7. Date Filter Systems

### Quick Preset Buttons + Popover Picker
```tsx
'use client';

import { useState } from 'react';
import { format, subDays } from 'date-fns';
import { CalendarIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger
} from '@/components/ui/popover';

export function QuickDateFilter({
  selectedDate,
  onDateChange
}: {
  selectedDate: Date | undefined;
  onDateChange: (date: Date | undefined) => void;
}) {
  const [open, setOpen] = useState(false);

  const isToday =
    selectedDate &&
    format(selectedDate, 'yyyy-MM-dd') === format(new Date(), 'yyyy-MM-dd');

  const isYesterday =
    selectedDate &&
    format(selectedDate, 'yyyy-MM-dd') ===
      format(subDays(new Date(), 1), 'yyyy-MM-dd');

  return (
    <div className="flex flex-wrap items-center gap-2">
      <Button
        variant={!selectedDate ? 'default' : 'outline'}
        size="sm"
        onClick={() => onDateChange(undefined)}
      >
        All Time
      </Button>

      <Button
        variant={isToday ? 'default' : 'outline'}
        size="sm"
        onClick={() => onDateChange(new Date())}
      >
        Today
      </Button>

      <Button
        variant={isYesterday ? 'default' : 'outline'}
        size="sm"
        onClick={() => onDateChange(subDays(new Date(), 1))}
      >
        Yesterday
      </Button>

      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" size="sm" className="min-w-[150px] justify-start">
            <CalendarIcon className="mr-2 h-4 w-4" />
            {selectedDate ? format(selectedDate, 'MMM dd, yyyy') : 'Pick a Date'}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="end">
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={(date) => {
              onDateChange(date);
              setOpen(false);
            }}
            disabled={(d) => d > new Date()}
            autoFocus
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}
```

---

## 8. Data Tables with Dedicated "View" Button & Three-Dot Immediate Action Menu

All operational data tables MUST implement the **Two-Tier Action Column Pattern**:

1. **Immediate Primary Action (Dedicated "View" Button)**:
   * Always visible directly in the table row.
   * Uses `variant="outline"`, `size="sm"`, with an eye icon (`IconEye`).
   * One click immediately navigates to the dedicated full-page view (e.g. `/dashboard/datasets/:id` or `/dashboard/users/:id`).
2. **Three-Dot Quick Actions Menu (`DropdownMenu`)**:
   * Uses `IconDots` / `MoreHorizontal` inside a ghost icon button.
   * **Immediate Actions**: Place instant operations right at the top (e.g., Quick Edit, Status Transitions like Approve / Publish / Suspend / Activate, Access Toggles).
   * **Destructive Actions**: Separated by `<DropdownMenuSeparator />` at the bottom (e.g., Delete with confirmation prompt).

### 8.1 Action Column Definition Example

```tsx
import { ColumnDef } from '@tanstack/react-table';
import {
  IconEye,
  IconDots,
  IconEdit,
  IconCheck,
  IconShieldCheck,
  IconTrash,
  IconUserCheck,
  IconUserX,
  IconExternalLink,
} from '@tabler/icons-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export interface ResourceRow {
  id: string;
  name: string;
  status: 'PENDING' | 'ACTIVE' | 'ARCHIVED';
  ownerEmail: string;
}

export function createResourceColumns(actions: {
  onView: (id: string) => void;
  onEdit: (row: ResourceRow) => void;
  onApprove?: (id: string) => void;
  onToggleStatus?: (id: string, currentStatus: string) => void;
  onDelete: (id: string, name: string) => void;
}): ColumnDef<ResourceRow>[] {
  return [
    {
      accessorKey: 'name',
      header: 'Resource Name',
      cell: ({ row }) => (
        <span className="font-semibold text-foreground">{row.original.name}</span>
      ),
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => {
        const status = row.original.status;
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
            {status}
          </span>
        );
      },
    },
    // The Two-Tier Action Column
    {
      id: 'actions',
      header: () => <div className="text-right">Actions</div>,
      cell: ({ row }) => {
        const item = row.original;

        return (
          <div className="flex items-center justify-end gap-1.5">
            {/* 1. Dedicated View Button: Opens into dedicated full page */}
            <Button
              variant="outline"
              size="sm"
              className="h-7 px-2.5 text-xs font-medium gap-1.5 hover:bg-muted"
              onClick={() => actions.onView(item.id)}
            >
              <IconEye className="size-3.5 text-primary" />
              <span>View</span>
            </Button>

            {/* 2. Three-Dot Actions Menu: Immediate in-place actions & deletion */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="size-7 text-muted-foreground hover:text-foreground"
                  aria-label="More actions"
                >
                  <IconDots className="size-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48 text-xs">
                {/* Secondary Navigation */}
                <DropdownMenuItem
                  onClick={() => actions.onView(item.id)}
                  className="cursor-pointer"
                >
                  <IconEye className="mr-2 size-3.5 text-primary" />
                  View Full Details
                </DropdownMenuItem>

                {/* Immediate In-Place Action: Quick Edit */}
                <DropdownMenuItem
                  onClick={() => actions.onEdit(item)}
                  className="cursor-pointer"
                >
                  <IconEdit className="mr-2 size-3.5 text-muted-foreground" />
                  Quick Edit
                </DropdownMenuItem>

                {/* Immediate Status Transition: Approve / Publish */}
                {item.status === 'PENDING' && actions.onApprove && (
                  <DropdownMenuItem
                    onClick={() => actions.onApprove?.(item.id)}
                    className="cursor-pointer text-emerald-600 dark:text-emerald-400 font-medium"
                  >
                    <IconCheck className="mr-2 size-3.5" />
                    Approve & Publish
                  </DropdownMenuItem>
                )}

                {/* Immediate Status Toggle: Suspend / Activate */}
                {actions.onToggleStatus && (
                  <DropdownMenuItem
                    onClick={() => actions.onToggleStatus?.(item.id, item.status)}
                    className="cursor-pointer"
                  >
                    {item.status === 'ACTIVE' ? (
                      <>
                        <IconUserX className="mr-2 size-3.5 text-amber-500" />
                        Suspend Account
                      </>
                    ) : (
                      <>
                        <IconUserCheck className="mr-2 size-3.5 text-emerald-500" />
                        Activate Account
                      </>
                    )}
                  </DropdownMenuItem>
                )}

                <DropdownMenuSeparator />

                {/* Destructive Action: Permanent Delete */}
                <DropdownMenuItem
                  onClick={() => actions.onDelete(item.id, item.name)}
                  className="cursor-pointer text-destructive focus:text-destructive focus:bg-destructive/10"
                >
                  <IconTrash className="mr-2 size-3.5" />
                  Delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        );
      },
    },
  ];
}
```

### 8.2 Full Data Table Component (`DashboardDataTable.tsx`)

```tsx
'use client';

import { useState } from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { Search, X, ChevronLeft, ChevronRight } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  total: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  searchPlaceholder?: string;
  searchQuery: string;
  onSearchChange: (val: string) => void;
  statusFilter?: string;
  onStatusFilterChange?: (val: string) => void;
  statusOptions?: { label: string; value: string }[];
  isLoading?: boolean;
}

export function DashboardDataTable<TData, TValue>({
  columns,
  data,
  total,
  page,
  pageSize,
  onPageChange,
  searchPlaceholder = 'Search records...',
  searchQuery,
  onSearchChange,
  statusFilter,
  onStatusFilterChange,
  statusOptions,
  isLoading,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const totalPages = Math.ceil(total / pageSize) || 1;
  const isFilterActive = searchQuery || (statusFilter && statusFilter !== 'all');

  return (
    <div className="space-y-3">
      {/* Search & Filter Toolbar */}
      <div className="flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <Search className="text-muted-foreground absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2" />
          <Input
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder={searchPlaceholder}
            className="bg-card pr-9 pl-9 shadow-none text-xs"
          />
          {searchQuery && (
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-1/2 right-1 h-7 w-7 -translate-y-1/2"
              onClick={() => onSearchChange('')}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>

        {statusOptions && onStatusFilterChange && (
          <Select value={statusFilter} onValueChange={onStatusFilterChange}>
            <SelectTrigger className="w-full bg-card shadow-none sm:w-[170px] text-xs">
              <SelectValue placeholder="All Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              {statusOptions.map((opt) => (
                <SelectItem key={opt.value} value={opt.value} className="text-xs">
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}

        {isFilterActive && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              onSearchChange('');
              if (onStatusFilterChange) onStatusFilterChange('all');
            }}
            className="h-9 px-3 text-xs"
          >
            Reset
          </Button>
        )}
      </div>

      {/* Bordered Card Container */}
      <div className="border-border/60 bg-card overflow-hidden rounded-xl border shadow-xs">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((group) => (
              <TableRow key={group.id} className="bg-muted/40">
                {group.headers.map((header) => (
                  <TableHead key={header.id} className="text-xs font-semibold">
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="text-muted-foreground h-32 text-center text-sm"
                >
                  Loading records...
                </TableCell>
              </TableRow>
            ) : table.getRowModel().rows.length > 0 ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  className="hover:bg-muted/30 transition-colors"
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id} className="py-2.5 text-xs">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="text-muted-foreground h-32 text-center text-sm"
                >
                  No records found matching your filters.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>

        {/* Integrated Pagination Footer */}
        <div className="border-border/60 bg-muted/20 text-muted-foreground flex items-center justify-between border-t px-4 py-2.5 text-xs">
          <div>
            Showing{' '}
            <span className="text-foreground font-medium">
              {data.length > 0 ? (page - 1) * pageSize + 1 : 0}
            </span>{' '}
            to{' '}
            <span className="text-foreground font-medium">
              {Math.min(page * pageSize, total)}
            </span>{' '}
            of <span className="text-foreground font-medium">{total}</span> records
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onPageChange(Math.max(1, page - 1))}
              disabled={page <= 1 || isLoading}
              className="h-7 w-7 p-0"
            >
              <ChevronLeft className="h-3.5 w-3.5" />
            </Button>
            <span className="text-foreground text-xs font-medium">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onPageChange(Math.min(totalPages, page + 1))}
              disabled={page >= totalPages || isLoading}
              className="h-7 w-7 p-0"
            >
              <ChevronRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 9. Status Pill Badges Palette

Maintain visual hierarchy across states using outline badges with semi-transparent tinted backgrounds:

```tsx
export const STATUS_VARIANTS: Record<string, { label: string; className: string }> = {
  pending: {
    label: 'Pending',
    className: 'bg-amber-500/10 text-amber-600 border-amber-200 dark:border-amber-800'
  },
  processing: {
    label: 'Processing',
    className: 'bg-blue-500/10 text-blue-600 border-blue-200 dark:border-blue-800'
  },
  active: {
    label: 'Active',
    className: 'bg-emerald-500/10 text-emerald-600 border-emerald-200 dark:border-emerald-800'
  },
  completed: {
    label: 'Completed',
    className: 'bg-emerald-500/10 text-emerald-600 border-emerald-200 dark:border-emerald-800'
  },
  cancelled: {
    label: 'Cancelled',
    className: 'bg-muted text-muted-foreground border-border'
  },
  disputed: {
    label: 'Disputed',
    className: 'bg-rose-500/10 text-rose-600 border-rose-200 dark:border-rose-800'
  }
};
```

---

## 10. Development Checklist

When creating or upgrading a dashboard view, ensure:
- [ ] **Components Config**: Check for `components.json`. If missing, prompt user to initialize shadcn/ui.
- [ ] **Dependencies**: Ensure `@tanstack/react-table`, `date-fns`, and `@tabler/icons-react` / `lucide-react` are installed.
- [ ] **Content Layout**:
  - Root uses `<SidebarProvider>` wrapping the sidebar and `<SidebarInset className="bg-muted/15 min-h-screen">`.
  - Header features `<SidebarTrigger className="-ml-1" />` on the left.
  - Centered brand logo (`<img src="/logo.png" />`).
  - Right-aligned uppercase monospace role pill badge (`<Badge variant="outline" className="text-secondary bg-secondary/10 border-secondary uppercase font-mono px-3 py-1.5">{role}</Badge>`).
  - Main container has `p-4 pt-18 md:p-6 md:pt-0 flex flex-1 flex-col gap-6`.
- [ ] **Sidebar Design**:
  - Crisp white background (`bg-card border-r`).
  - Grouped navigation sections with uppercase labels (`SidebarGroupLabel className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/75"`).
  - High-contrast active indicators (`bg-primary text-primary-foreground font-medium`).
  - Dynamic pending notification pill badges on items.
  - Profile footer featuring user avatar, initials fallback, name, email, and quick logout icon button.
- [ ] **Table Action Pattern**:
  - Dedicated **"View"** button (`variant="outline"`, `size="sm"`, `IconEye`) directly visible in every row, opening into a dedicated detail/edit page.
  - Three-dot menu (`DropdownMenu` / `IconDots`) containing immediate in-place operations (quick edit, status transitions, toggles) and separated destructive delete actions.
- [ ] **Table Visuals**: Tables wrapped in `border-border/60 bg-card overflow-hidden rounded-xl border shadow-xs`, with `bg-muted/40` header and `hover:bg-muted/30` rows.
- [ ] **Stats & Numbers**: Metric numbers use `tabular-nums` for clean digit alignment.
