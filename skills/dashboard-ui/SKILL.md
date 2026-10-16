---
name: dashboard-ui
description: Design systems, layout architecture, subtle gradient stats cards, collapsible sidebars, breadcrumbs, date filters, and TanStack data tables for modern dashboards.
---

# Dashboard UI Skill

Comprehensive guidelines, component architectures, and copy-paste-ready implementation patterns for building high-end, responsive administrative and analytics dashboards with Next.js (App Router), Tailwind CSS (v3 or v4), and shadcn/ui.

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
* **`lucide-react`**: Standard icon set.

If missing, install them:
```bash
npm install @tanstack/react-table date-fns lucide-react
# or: pnpm add @tanstack/react-table date-fns lucide-react
# or: bun add @tanstack/react-table date-fns lucide-react
```

---

## 2. Design System & Theme Foundations

All dashboard components rely on semantic CSS variables and subtle, high-contrast visual tokens.

### Theme Tokens (`globals.css`)
```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  --card: 0 0% 100%;
  --card-foreground: 0 0% 3.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 0 0% 3.9%;
  --primary: 330 43% 46%;
  --primary-foreground: 0 0% 98%;
  --muted: 0 0% 96.1%;
  --muted-foreground: 0 0% 45.1%;
  --border: 0 0% 89.8%;
  --radius: 0.5rem;

  /* Sidebar Tokens */
  --sidebar: hsl(0 0% 98%);
  --sidebar-foreground: hsl(240 5.3% 26.1%);
  --sidebar-primary: hsl(240 5.9% 10%);
  --sidebar-primary-foreground: hsl(0 0% 98%);
  --sidebar-accent: hsl(240 4.8% 95.9%);
  --sidebar-accent-foreground: hsl(240 5.9% 10%);
  --sidebar-border: hsl(220 13% 91%);
  --sidebar-ring: hsl(217.2 91.2% 59.8%);
}

.dark {
  --background: 0 0% 3.9%;
  --foreground: 0 0% 98%;
  --card: 0 0% 3.9%;
  --card-foreground: 0 0% 98%;
  --muted: 0 0% 14.9%;
  --muted-foreground: 0 0% 63.9%;
  --border: 0 0% 14.9%;

  /* Dark Sidebar Tokens */
  --sidebar: hsl(240 5.9% 10%);
  --sidebar-foreground: hsl(240 4.8% 95.9%);
  --sidebar-primary: hsl(224.3 76.3% 48%);
  --sidebar-accent: hsl(240 3.7% 15.9%);
  --sidebar-accent-foreground: hsl(240 4.8% 95.9%);
  --sidebar-border: hsl(240 3.7% 15.9%);
}
```

---

## 3. Admin Layout & Sidebar Architecture

### 2.1 Entry Point Layout (`app/admin/layout.tsx`)
The root admin layout wraps pages in `SidebarProvider`, inserts the collapsible `AppSidebar`, and controls the header with mobile triggers.

```tsx
import { AppSidebar } from '@/components/admin/sidebar/app-sidebar';
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger
} from '@/components/ui/sidebar';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        {/* Mobile Header: fixed top blur on small screens, transparent on desktop */}
        <header className="bg-background/95 fixed top-0 right-0 left-0 z-20 flex h-16 shrink-0 items-center gap-2 border-b shadow-xs backdrop-blur transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12 md:static md:border-none md:bg-transparent md:shadow-none">
          <div className="flex w-full items-center justify-between gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <div className="font-semibold text-sm tracking-tight md:hidden">
              Admin Portal
            </div>
            <div className="w-8 md:hidden" />
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex flex-1 flex-col gap-4 p-4 pt-20 md:pt-0">
          {children}
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
```

### 2.2 App Sidebar (`components/admin/sidebar/app-sidebar.tsx`)
Uses `variant="inset"` with `collapsible="icon"` for collapsing down to an icon-only dock.

```tsx
'use client';

import {
  PieChart,
  ShoppingBag,
  Users,
  Settings2,
  Package
} from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail
} from '@/components/ui/sidebar';
import { NavMain } from './nav-main';
import { NavUser } from './nav-user';
import { TeamSwitcher } from './team-switcher';

const navData = [
  {
    title: 'Dashboard',
    url: '/admin',
    icon: PieChart,
    items: [{ title: 'Overview', url: '/admin' }]
  },
  {
    title: 'Orders',
    url: '/admin/orders',
    icon: ShoppingBag,
    items: [
      { title: 'All Orders', url: '/admin/orders' },
      { title: 'Transactions', url: '/admin/orders/transactions' }
    ]
  },
  {
    title: 'Inventory',
    url: '/admin/inventory',
    icon: Package,
    items: [
      { title: 'Products', url: '/admin/inventory/products' },
      { title: 'Low Stock', url: '/admin/inventory/low-stock' }
    ]
  },
  {
    title: 'Users',
    url: '/admin/users',
    icon: Users,
    items: [{ title: 'Customers', url: '/admin/users' }]
  },
  {
    title: 'Settings',
    url: '/admin/settings',
    icon: Settings2,
    items: [{ title: 'General', url: '/admin/settings' }]
  }
];

export function AppSidebar(props: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar variant="inset" collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navData} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={{ name: 'Admin', email: 'admin@company.com' }} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
```

### 2.3 Collapsible Nav with Active State & Counter Pills (`nav-main.tsx`)
Highlights active links, rotates chevrons smoothly, and shows notification counters with `tabular-nums`.

```tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight, type LucideIcon } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger
} from '@/components/ui/collapsible';
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem
} from '@/components/ui/sidebar';

interface NavItem {
  title: string;
  url: string;
  icon?: LucideIcon;
  count?: number;
  items?: { title: string; url: string; count?: number }[];
}

export function NavMain({ items }: { items: NavItem[] }) {
  const pathname = usePathname();

  const isPathActive = (target: string) => {
    if (!target) return false;
    if (pathname === target) return true;
    if (target === '/admin') return false;
    return pathname.startsWith(`${target}/`);
  };

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Platform</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => {
          const subItemActive = item.items?.some((s) => isPathActive(s.url));
          const isActive = subItemActive || isPathActive(item.url);

          return (
            <Collapsible
              key={item.title}
              asChild
              defaultOpen={isActive}
              className="group/collapsible"
            >
              <SidebarMenuItem>
                <CollapsibleTrigger asChild>
                  <SidebarMenuButton tooltip={item.title} isActive={isActive}>
                    {item.icon && <item.icon />}
                    <span>{item.title}</span>
                    {item.count && item.count > 0 && (
                      <span className="bg-primary/10 text-primary mr-1 ml-auto flex h-5 min-w-5 items-center justify-center rounded-full px-1.5 text-[11px] font-semibold tabular-nums">
                        {item.count}
                      </span>
                    )}
                    <ChevronRight
                      className={`transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90 ${
                        item.count ? '' : 'ml-auto'
                      }`}
                    />
                  </SidebarMenuButton>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <SidebarMenuSub>
                    {item.items?.map((subItem) => {
                      const subIsActive = isPathActive(subItem.url);
                      return (
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton asChild isActive={subIsActive}>
                            <Link
                              href={subItem.url}
                              className="flex w-full items-center justify-between"
                            >
                              <span>{subItem.title}</span>
                              {subItem.count && subItem.count > 0 && (
                                <span className="bg-primary ml-auto flex h-4 min-w-4 items-center justify-center rounded-full px-1 text-[10px] font-medium text-white tabular-nums">
                                  {subItem.count}
                                </span>
                              )}
                            </Link>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      );
                    })}
                  </SidebarMenuSub>
                </CollapsibleContent>
              </SidebarMenuItem>
            </Collapsible>
          );
        })}
      </SidebarMenu>
    </SidebarGroup>
  );
}
```

---

## 4. Page Header, Breadcrumbs & Title Hierarchy

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

## 5. Stats Cards with Subtle Gradients

### 4.1 The Gradient & Container Query Pattern
To achieve a high-end look without visual clutter:
1. Apply the parent wildcard selector `*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:bg-gradient-to-t` in light mode.
2. Fall back to `dark:*:data-[slot=card]:bg-card` for clean, matte dark mode cards.
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

## 6. Date Filter Systems

### Pattern A: Quick Preset Buttons + Popover Picker
Best for executive dashboards that alternate between today, yesterday, and specific historical dates.

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

### Pattern B: Date Range Traverser (`DateRangeFilter`)
Best for reports and transaction ledgers with month-by-month traversal buttons (`ChevronLeft`, `ChevronRight`).

```tsx
'use client';

import { useState } from 'react';
import { format, subMonths, addMonths } from 'date-fns';
import { CalendarIcon, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger
} from '@/components/ui/popover';

export function DateRangeFilter({
  rangeStart,
  rangeEnd,
  onRangeChange
}: {
  rangeStart: Date | undefined;
  rangeEnd: Date | undefined;
  onRangeChange: (start: Date | undefined, end: Date | undefined) => void;
}) {
  const [startOpen, setStartOpen] = useState(false);
  const [endOpen, setEndOpen] = useState(false);

  const handlePrev = () => {
    const s = rangeStart || new Date();
    const e = rangeEnd || new Date();
    onRangeChange(subMonths(s, 1), subMonths(e, 1));
  };

  const handleNext = () => {
    const s = rangeStart || new Date();
    const e = rangeEnd || new Date();
    const nextEnd = addMonths(e, 1);
    const today = new Date();
    onRangeChange(addMonths(s, 1), nextEnd > today ? today : nextEnd);
  };

  return (
    <div className="flex flex-wrap items-center gap-2">
      <Button
        variant={!rangeStart && !rangeEnd ? 'default' : 'outline'}
        size="sm"
        onClick={() => onRangeChange(undefined, undefined)}
        className="h-8 text-xs font-medium"
      >
        All Time
      </Button>

      <Button
        variant="outline"
        size="icon"
        onClick={handlePrev}
        className="h-8 w-8"
        title="Previous Month"
      >
        <ChevronLeft className="h-4 w-4" />
      </Button>

      <div className="flex items-center gap-1.5">
        <Popover open={startOpen} onOpenChange={setStartOpen}>
          <PopoverTrigger asChild>
            <Button variant="outline" size="sm" className="h-8 min-w-[110px] text-xs font-normal">
              <CalendarIcon className="text-muted-foreground mr-1.5 h-3.5 w-3.5" />
              {rangeStart ? format(rangeStart, 'MMM d, yyyy') : 'Start Date'}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="p-0" align="center">
            <Calendar
              mode="single"
              selected={rangeStart}
              onSelect={(d) => {
                if (d) {
                  onRangeChange(d, rangeEnd || d);
                  setStartOpen(false);
                }
              }}
              disabled={(d) => d > new Date()}
            />
          </PopoverContent>
        </Popover>

        <span className="text-muted-foreground text-xs font-medium">to</span>

        <Popover open={endOpen} onOpenChange={setEndOpen}>
          <PopoverTrigger asChild>
            <Button variant="outline" size="sm" className="h-8 min-w-[110px] text-xs font-normal">
              <CalendarIcon className="text-muted-foreground mr-1.5 h-3.5 w-3.5" />
              {rangeEnd ? format(rangeEnd, 'MMM d, yyyy') : 'End Date'}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="p-0" align="center">
            <Calendar
              mode="single"
              selected={rangeEnd}
              onSelect={(d) => {
                if (d) {
                  onRangeChange(rangeStart || d, d);
                  setEndOpen(false);
                }
              }}
              disabled={(d) => d > new Date() || (rangeStart ? d < rangeStart : false)}
            />
          </PopoverContent>
        </Popover>
      </div>

      <Button
        variant="outline"
        size="icon"
        onClick={handleNext}
        disabled={rangeEnd ? rangeEnd >= new Date() : true}
        className="h-8 w-8"
        title="Next Month"
      >
        <ChevronRight className="h-4 w-4" />
      </Button>
    </div>
  );
}
```

---

## 7. High-Performance Data Tables (TanStack Table + shadcn)

All dashboard data tables are built with **TanStack Table (`@tanstack/react-table`)** for headless state (sorting, filtering, pagination) and **shadcn `<Table>`** for styled presentation. Always combine with debounced search, facet select filters, status pill badges, and pagination footer.

```tsx
'use client';

import { useState } from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable
} from '@tanstack/react-table';
import { Search, X, ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
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
  isLoading
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel()
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
            className="bg-card pr-9 pl-9 shadow-none"
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
            <SelectTrigger className="w-full bg-card shadow-none sm:w-[170px]">
              <SelectValue placeholder="All Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              {statusOptions.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
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
                    <TableCell key={cell.id} className="py-3">
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
        <div className="border-border/60 bg-muted/20 text-muted-foreground flex items-center justify-between border-t px-4 py-3 text-xs">
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
              className="h-8 w-8 p-0"
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-foreground text-xs font-medium">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onPageChange(Math.min(totalPages, page + 1))}
              disabled={page >= totalPages || isLoading}
              className="h-8 w-8 p-0"
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 8. Status Pill Badges Palette

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

## 9. Development Checklist

When creating a new dashboard view, ensure:
- [ ] Check for `components.json` in the root. If missing, prompt user to initialize shadcn/ui.
- [ ] Ensure required shadcn components are installed via `npx shadcn@latest add <component>`.
- [ ] Ensure `@tanstack/react-table`, `date-fns`, and `lucide-react` are installed in `package.json`.
- [ ] Root uses `<SidebarProvider>` + `<SidebarInset>` with mobile trigger header.
- [ ] Top of page includes `<Breadcrumb>` navigation and clear `<h1>` + `<p className="text-muted-foreground">` subtitle.
- [ ] Stats cards include `data-slot="card"` with subtle upward gradient `*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card`.
- [ ] Metric numbers use `tabular-nums` for clean digit alignment.
- [ ] Tables are wrapped in `border-border/60 bg-card overflow-hidden rounded-xl border shadow-xs`.
- [ ] Table headers use `bg-muted/40` and rows feature `hover:bg-muted/30`.
- [ ] Date filters support quick presets and popover constraint boundaries (`disabled={(d) => d > new Date()}`).
