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
**Status: Fully Implemented (Modular Monolith)**

The backend follows a strict domain-driven design with separation between business logic (`domain/`) and infrastructure (`lib/`).

```text
src/
├── app/
│   ├── domain/                     # Business Logic (Feature Slices)
│   │   ├── assets/                 # Asset Management
│   │   │   ├── models.py           # Asset, AssetType structs
│   │   │   ├── controllers.py      # REST endpoints
│   │   │   └── services.py         # Business logic
│   │   ├── auth/                   # OAuth2 Authentication
│   │   │   ├── models.py           # UserCredentials, CredentialStatus
│   │   │   └── controllers.py      # /auth/login, /auth/callback
│   │   ├── campaigns/              # Campaign Management
│   │   │   ├── models.py           # Campaign, AdResponse structs
│   │   │   ├── controllers.py      # Campaign CRUD endpoints
│   │   │   ├── services.py         # CampaignService (sync logic)
│   │   │   └── mutations.py        # GoogleAdsMutator (policy handling)
│   │   ├── reporting/              # Reporting & Analytics
│   │   │   ├── models.py           # SearchTermRow
│   │   │   ├── controllers.py      # Report endpoints
│   │   │   └── services.py         # GAQLService (query builder)
│   │   └── shared/                 # Shared Models
│   │       └── models.py           # EntityStatus, AdType, ArangoDocument
│   ├── lib/                        # Infrastructure Layer
│   │   ├── ai/                     # AI Integration (Instructor + LiteLLM)
│   │   │   └── client.py           # AIClient stub
├── domain/                     # Business Logic (Feature Slices)
│   ├── assets/                 # Asset Management
│   │   ├── models.py           # Asset, AssetType structs
│   │   ├── controllers.py      # REST endpoints
│   │   └── services.py         # Business logic
│   ├── auth/                   # OAuth2 Authentication
│   │   ├── models.py           # UserCredentials, CredentialStatus
│   │   └── controllers.py      # /auth/login, /auth/callback
│   ├── campaigns/              # Campaign Management
│   │   ├── models.py           # Campaign, AdResponse structs
│   │   ├── controllers.py      # Campaign CRUD endpoints
│   │   ├── services.py         # CampaignService (sync logic)
│   │   └── mutations.py        # GoogleAdsMutator (policy handling)
│   ├── reporting/              # Reporting & Analytics
│   │   ├── models.py           # SearchTermRow
│   │   ├── controllers.py      # Report endpoints
│   │   └── services.py         # GAQLService (query builder)
│   └── shared/                 # Shared Models
│       └── models.py           # EntityStatus, AdType, ArangoDocument
├── lib/                        # Infrastructure Layer
│   ├── ai/                     # AI Integration (Instructor + LiteLLM)
│   │   └── client.py           # AIClient stub
│   ├── auth/                   # Security & OAuth
│   │   ├── security.py         # TokenEncryptor (AES-256-GCM)
│   │   └── service.py          # AuthService (OAuth2 flow)
│   ├── db/                     # Database Layer
│   │   ├── client.py           # ArangoClient (connection management)
│   │   └── init_db.py          # Graph schema initialization
│   └── google_ads/             # Google Ads API Integration
│       └── client.py           # GoogleAdsClientFactory
├── main.py                     # Litestar Application Entrypoint
├── worker.py                       # Arq Worker Configuration
└── seed.py                         # Database seeding script
```

**Key Implementation Details:**
- **Msgspec Structs:** All models use `msgspec.Struct` for strict typing and high-performance serialization
- **ArangoDB Graph:** `AdsGraph` with vertex collections (Customers, Campaigns, AdGroups, Ads, Assets, Keywords) and edge definitions
- **OAuth2 Security:** AES-256-GCM envelope encryption for refresh tokens
- **Sync Logic:** AQL "Upsert-Merge" pattern preserves local changes during Google Ads sync
- **Policy Handling:** Recursive "Try-Catch-Exempt" loop for Google Ads policy violations
- **Background Workers:** Arq integration with Redis for async job processing
- **AI Integration:** Google Gemini 2.5 Flash via `google-genai` SDK with "Schema Bridge" for Msgspec compatibility

### 3.2 Frontend (`frontend/`)
Standard Vite + Svelte setup.
frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   └── icons/         # Standardized Icons (SVG wrapper components)
│   │   └── assets/
│   ├── views/                 # Feature Modules (Hub, Wizard, Team)
│   │   ├── hub/               # The Hub Dashboard
│   │   ├── wizard/            # Campaign Architect (Wizard Module)
│   │   │   ├── CampaignWizard.svelte  # Entry Menu (Sub-Hub)
│   │   │   ├── NewCampaign.svelte     # Main Creation Tool (Split-View)
│   │   │   ├── CampaignOverview.svelte# Placeholder
│   │   │   └── store.svelte.js        # Global Wizard State (Runes)
│   │   └── team/              # Team Management
│   ├── App.svelte             # Main Entry & Router
│   └── main.ts
├── package.json
└── vite.config.ts
```

### 3.2.1 Icon Convention
**Global Rule:**
- **Source:** SVGs are NOT used directly implementation-side.
- **Location:** `frontend/src/lib/components/icons/`.
- **Naming:** `icon_[name].svg`.
- **Component:** For every SVG, a Svelte wrapper must be created in the same directory: `icon_[name].svelte`.
- **Usage:** Import the Svelte component, not the SVG file.
- **Styling:** The wrapper handles size and stroke logic (e.g., via `group-hover`).

### 3.3 Infrastructure
- **Docker Compose:** defined in `docker-compose.yml`.
  - `db`: ArangoDB (Port 8529)
  - `backend`: Litestar (Port 8000)
  - `frontend`: Vite Dev Server (Port 5173)
  - `redis`: Redis (Port 6379) - Job queue for Arq
  - `worker`: Arq Worker - Background job processing

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

## 6. Current Implementation Status
**Status:** **Core MVP Complete / Pre-Alpha** ✅

**Backend:**
- [x] **Modular Monolith Architecture:** Fully implemented with Litestar.
- [x] **ArangoDB Persistence:** `CampaignService` and `CampaignRepository` implemented.
    -   **Graph Schema:** `AdsGraph` with vertex collections (Campaigns, AdGroups, Assets, etc.)
    -   **Deduplication:** Assets use `_key` as SHA-256 hash (per Architecture Spec Section 4.2)
- [x] **Google Ads Mutator:** `GoogleAdsMutator` logic implemented (with mock integration).
- [x] **AI Integration:** `GeminiService` implemented for Deep Research Report analysis.
    -   Uses **Gemini 2.5 Flash** (configurable via `GEMINI_MODEL` env var).
    -   Parses unstructured research reports into `CampaignStructure` (AdGroups, Keywords, Assets).
    -   Full E2E flow verified: Report → AI Analysis → DB Persistence → UI Display.

**Frontend:**
- [x] **Navigation:** "Hub & Spoke" model implemented.
    -   `Hub.svelte`: Main Entry.
    -   `CampaignWizard.svelte`: Sub-Hub for managing campaigns.
- [x] **Creation Workflow (`NewCampaign.svelte`):**
    -   **Import:** "Deep Research" Modal for report text upload.
    -   **Split-View UI:** Left Sidebar (AdGroup Navigation) | Right Panel (Asset Editor).
    -   **Manual Control:** Structured inputs for Language (DE/EN), Location (DACH), and Objective.
    -   **Ad Group Management:** Dynamic list of Ad Groups generated from AI analysis.
    -   **Asset Display:** Headlines and Descriptions with character count indicators.
- [x] **Localization:** Frontend fully translated to German (DE), with specific exceptions for technical terms ("CampaignWizard", "Setup", "Coming Soon").
- [x] **State Management:** `WizardState` (Runes-based) handles complex nested campaign data.

**Infrastructure:**
- [x] **Docker Compose:** All services containerized (db, backend, frontend, redis, worker).
- [x] **Database Init:** `init_db.py` creates graph schema on startup.
- [x] **Logging:** Debug logging available in `logs/` directory (currently disabled, can be re-enabled in `controllers.py`).

**Missing / Next Steps:**
- [ ] **Live Google Ads API:** Still awaiting valid credentials for live testing.
- [ ] **User Authentication:** OAuth2 flow implementation pending.
- [ ] **Deployment:** Staging environment setup.
- [ ] **Asset Editing:** Real-time editing of generated headlines/descriptions.
- [ ] **Keyword Management:** UI for managing keywords per AdGroup.

---
*Last Updated: 2025-12-18 (E2E Deep Research Import Flow Verified)*

