# Technisches Architekturdokument: IMAP Hub Plattform

## 1. Executive Summary und Architektonische Vision

Das vorliegende Dokument definiert die technische Spezifikation für den **IMAP Hub**, eine interne Enterprise-Plattform, und deren Kernmodul **CampaignWizard** zur Orchestrierung, Validierung und Verwaltung komplexer Marketing-Assets.

Die Kernphilosophie der Architektur lautet **"Deterministische Flexibilität"**. Da Marketingdaten hierarchisch/vernetzt sind und KI-Modelle probabilistisch arbeiten, muss die technische Basis absolute Strenge bei Datentypen und Zustandsübergängen gewährleisten.

Wir setzen auf einen **Modular Monolith** auf Basis von **Litestar** (Backend), **ArangoDB** (Multi-Model Persistenz) und **Svelte 5** (Frontend mit Runes). Diese Kombination bietet signifikante Performance-Vorteile gegenüber Standards wie FastAPI oder React.

### 1.1 Kernkomponenten

1. **High-Performance Backend (Litestar):** Nutzung von `msgspec` für C-optimierte Serialisierung (2x schneller als Pydantic V2).
2. **Invisible Validation Loop (Instructor + LiteLLM):** Middleware, die LLM-Outputs gegen strikte Schemata validiert und automatisch korrigiert.
3. **Multi-Model Data Fabric (ArangoDB):** Speicherung von Hierarchien als Graph für performante Traversierung.
4. **State-Machine UI (Svelte 5 + XState):** Reaktives Frontend, das komplexe Zustände (Generating -> Validating) mathematisch sicher steuert.

---

## 2. Technologischer Kontext & Stack-Entscheidungen

### 2.1 Backend: Litestar (statt FastAPI)

* **Grund:** FastAPI hat Performance-Grenzen bei komplexer Validierung. Litestar nutzt nativ `msgspec` und bietet besseres Dependency Injection Design.
* **Vorteil:** Höherer Durchsatz bei JSON-intensiven Reporting-Aufgaben.
* **Struktur:** Nutzung von DTOs (Data Transfer Objects) statt reiner Pydantic-Modelle für API-Antworten.

### 2.2 Datenbank: ArangoDB (statt PostgreSQL)

* **Grund:** Google Ads Strukturen sind tiefe Hierarchien (Kampagne -> Gruppe -> Anzeige -> Asset). Relationale Joins sind hier ineffizient.
* **Vorteil:** Native Graph-Traversierung (AQL) ermöglicht Abfragen wie "Finde alle Keywords, die dieses Bild-Asset nutzen" in Millisekunden.

### 2.3 Frontend: Svelte 5 (statt React)

* **Grund:** Reacts Virtual DOM ist bei vielen interaktiven Elementen (Kacheln) oft langsam ("Jank").
* **Vorteil:** Svelte 5 **Runes** (`$state`, `$derived`) kompilieren zu nativem JS-Code ohne Runtime-Overhead.
* **Logik:** **XState** verwaltet den Status des Assistenten, um ungültige Zustände unmöglich zu machen.

---

## 3. Backend-Architektur (Detail)

### 3.1 Ordnerstruktur
Der Ansatz ist ein "Modular Monolith".

```text
src/
├── app/
│   ├── domain/                  # Geschäftslogik (Feature-Slices)
│   │   ├── assets/              # Asset-Architect Logik
│   │   │   ├── controllers.py   # Litestar Handler
│   │   │   ├── services.py      # Business Logic
│   │   │   ├── models.py        # msgspec Structs
│   │   │   └── guards.py        # RBAC Checks
│   │   ├── campaigns/           # Kampagnen-Orchestrierung
│   │   └── reporting/           # Analytics Engine
│   ├── lib/                     # Infrastruktur-Code
│   │   ├── db/                  # ArangoDB Client & Repositories
│   │   ├── ai/                  # LLM Orchestration (Instructor)
│   │   └── auth/                # OIDC Integration (Microsoft)
│   └── main.py                  # Application Entrypoint
```

### 3.2 Middleware: The Invisible Validation Loop
Diese Schicht kapselt die KI-Interaktion:
1. **Request:** Prompt an LLM.
2. **Validation:** Prüft Output gegen Pydantic Schema (z.B. "max 30 Zeichen").
3. **Loop (bei Fehler):** Sendet Fehler + Prompt zurück an LLM ("Kürze auf 30 Zeichen").
4. **Result:** Gibt nur valides Objekt an Controller zurück.

**Tech:** `Instructor` (Python Library) + `LiteLLM` (für Modell-Unabhängigkeit).

---

## 4. Datenhaltung (ArangoDB)

### 4.1 Collections (Schema)
* **Document Collections (Knoten):**
    * `Campaigns` (Metadaten, Budget)
    * `AdGroups`
    * `Assets` (Dedupliziert: Ein Bild existiert nur einmal)
* **Edge Collections (Kanten):**
    * `belongs_to` (AdGroup -> Campaign)
    * `uses_asset` (Ad -> Asset)

### 4.2 Query-Strategie
Nutzung von AQL für Reporting. Aggregationen laufen direkt auf der DB durch Graph-Traversierung, nicht im Python-Code.

---

## 5. Frontend-Spezifikation (Svelte 5)

### 5.1 Reaktivität
* Globaler Store via `$state`.
* Kein unnötiges Re-Rendering ganzer Listen, wenn sich nur eine Kachel ändert.

### 5.2 State Machine
Nutzung von **XState** für den Assistenten-Flow:
* States: `idle`, `generating`, `validating`, `error`.
* Prevents: Klicks auf "Weiter", während im Hintergrund validiert wird.

---

## 6. Asynchronität & Background Jobs

### 6.1 Task Queue: ArQ
* Leichtgewichtige Queue basierend auf `asyncio` und Redis.
* Kein Celery (zu schwergewichtig).
* Aufgabe: Langlaufende API-Calls (Google Ads Mutates, Report Downloads).

### 6.2 Real-Time Feedback
* **Server-Sent Events (SSE):** Litestar streamt Fortschritt ("Generiere 3/10...") an das Frontend.

---

## 7. Sicherheit & Deployment

### 7.1 Auth
* **Microsoft Entra ID (OIDC):** Integration via `Authlib`.
* Session-Cookies (HTTP-only).

### 7.2 Containerisierung
* **Docker:** Separate Container für `backend` (Python), `frontend` (Node/Vite), `db` (ArangoDB), `worker` (ArQ).
* **LLM Proxy:** Lokaler LiteLLM Container (optional) zur Abstraktion von API Keys.