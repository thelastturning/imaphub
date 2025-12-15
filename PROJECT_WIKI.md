# PROJECT WIKI & DOCUMENTATION

> **IMPORTANT:** This document is the **SINGLE SOURCE OF TRUTH** for all planning and implementation. Always consult this file before making architectural decisions or major changes.

---

## 1. Project Overview
**Name:** IMAP Hub
**Modules:** CampaignWizard, Team Overview
**Goal:** Internal enterprise web platform serving as a central hub for marketing operations, primarily orchestrating assets via the CampaignWizard.  
**Core Philosophy:** "Deterministic Flexibility" - Strict types/state for data, flexible graph storage for hierarchy.

## 2. Technology Stack (Fixed)
The stack is non-negotiable as per `ARCHITECTURE.md`.

| Component | Technology | Reasoning |
|-----------|------------|-----------|
| **Backend** | **Litestar** (Python) | High performance, native `msgspec` support, better DI than FastAPI. |
| **Database** | **ArangoDB** | Multi-model (Graph), optimized for hierarchical ad structures. |
| **Frontend** | **Svelte 5** (+ Runes) | Compiler-based reactivity, minimal runtime overhead. Top performance. |
| **State** | **XState** | Deterministic state management for the wizard flows. |
| **Validation**| **Instructor + LiteLLM** | Invisible validation loop for AI outputs. |

## 3. Directory Structure

### 3.1 Backend (`src/`)
*Currently in initial setup. Target structure:*
```text
src/
├── app/
│   ├── domain/                  # Feature Logic (Campaigns, Assets)
│   ├── lib/                     # Infra (DB, Auth, AI)
│   └── main.py                  # Entrypoint
└── seed.py                      # Database seeding script
```

### 3.2 Frontend (`frontend/`)
Standard Vite + Svelte setup.
```text
frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   └── assets/
│   ├── views/                   # Feature Modules (Hub, Wizard, Team)
│   │   ├── hub/                 # The Hub Dashboard
│   │   ├── wizard/              # Campaign Architect
│   │   └── team/                # Team Management
│   ├── App.svelte               # Main Entry & Router
│   └── main.ts
├── package.json
└── vite.config.ts
```

### 3.3 Infrastructure
- **Docker Compose:** defined in `docker-compose.yml`.
  - `db`: ArangoDB (Port 8529)
  - `backend`: Litestar (Port 8000)
  - `frontend`: Vite Dev Server (Port 5173)

## 4. Concepts & Glossary

### The Hub (`/`)
The central dashboard/landing page (Route: `/`). Displays a grid of available "Apps" or modules (e.g., Campaign Architect, Team Overview).

### Campaign Architect (`/wizard`)
*Also known as: CampaignWizard*
The tool for designing campaigns (Route: `/wizard`). Features a 3-column layout:
1.  **Strategy Briefing:** Read-only context.
2.  **Asset Workspace:** Interactive canvas/grid for assets.
3.  **Targeting:** Keywords and demographics.

### Domain Entities
-   **Campaign:** Top-level container.
-   **AdGroup:** Grouping of assets.
-   **Asset:** Creative element (Image, Text, Video). Should be deduplicated.

## 5. Development Rules
1.  **Snapshot First:** Before major refactors, ALWAYS commit current state.
2.  **Verify Architecture:** Check `ARCHITECTURE.md` compliance.
3.  **No Guessing:** If directory structure is unclear, check this Wiki or `ARCHITECTURE.md`.

---
*Last Updated: 2025-12-15*
