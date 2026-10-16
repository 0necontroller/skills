# 0necontroller Agent Skills

[![skills.sh](https://skills.sh/b/0necontroller/skills)](https://skills.sh/0necontroller/skills)

A collection of high-performance, modular skills for AI coding agents (Claude Code, Cursor, GitHub Copilot, Antigravity, and other compatible assistants), distributed via [`npx skills`](https://skills.sh).

---

## 🚀 Quick Start

Install all skills in this repository directly into your current project:

```bash
npx skills add 0necontroller/skills --all
```

Or install a specific skill:

```bash
npx skills add 0necontroller/skills --skill dashboard-ui
```

### Target a Specific Agent

Target your preferred AI agent directly:

```bash
# Claude Code
npx skills add 0necontroller/skills --agent claude-code

# Cursor
npx skills add 0necontroller/skills --agent cursor

# GitHub Copilot
npx skills add 0necontroller/skills --agent copilot
```

### Global Installation

To make these skills accessible across all your projects on your machine:

```bash
npx skills add 0necontroller/skills -g
```

### One-Off Usage (Without Installing)

Generate prompt context on the fly without persisting to your project configuration:

```bash
npx skills use 0necontroller/skills@dashboard-ui
```

---

## 📦 Available Skills

| Skill | Description | Path | Status |
| :--- | :--- | :--- | :--- |
| **`dashboard-ui`** | Guidelines, design system patterns, and responsive component architectures for crafting modern dashboard user interfaces. | `skills/dashboard-ui/` | ✅ Ready |

---

## 📁 Repository Structure

This repository follows the standard multi-skill layout expected by `npx skills`:

```text
0necontroller/skills/
├── README.md
├── skills/
│   └── dashboard-ui/
│       └── SKILL.md
└── (additional skills...)
```

Each skill contains a `SKILL.md` file featuring standard YAML frontmatter:

```markdown
---
name: skill-name
description: Brief summary of what this skill enables the agent to do.
---

# Skill Instructions and Workflows...
```

---

## 🛠️ Local Development & Testing

You can test new skills locally before pushing commits:

```bash
# Inspect skills detected in your local folder
npx skills add . --list

# Install locally for verification
npx skills add . --all
```

---

## 📄 License

MIT © [0necontroller](https://github.com/0necontroller)
