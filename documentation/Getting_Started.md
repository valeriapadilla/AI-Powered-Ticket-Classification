# Getting Started

Welcome to the **AI-Powered Ticket Classification and Prioritization** project. This guide provides step-by-step instructions for setting up and running the fullstack application composed of a modern **Next.js frontend (App Router)** and a robust **FastAPI backend**, enhanced with **LangGraph agents** and **RAG pipelines**.

---

## Table of Contents

* [Prerequisites](#prerequisites)
* [Architecture Overview](#architecture-overview)
* [Project Structure Justification](#project-structure-justification)
* [Installation](#installation)
  * [Install All Dependencies](#install-all-dependencies)
  * [Install Frontend Only](#install-frontend-only)
  * [Install Backend Only](#install-backend-only)
* [Development Workflow](#development-workflow)
  * [Run Fullstack](#run-fullstack)
  * [Run Frontend Only](#run-frontend-only)
  * [Run Backend Only](#run-backend-only)
* [Environment Variables](#environment-variables)
* [Testing & Linting](#testing--linting)
* [Cleaning Build Artifacts](#cleaning-build-artifacts)
* [Contributions](#contributions)

---

## Prerequisites

Ensure you have the following tools installed locally:

* **Node.js v18+** with **NVM** (Node Version Manager)
* **Python 3.12.x**
* **GNU Make**

---

## Architecture Overview

The project is divided into two cleanly decoupled subsystems:

* **Frontend**: A type-safe, component-based application built using Next.js 14 App Router and Tailwind CSS.
* **Backend**: A modular FastAPI service exposing REST endpoints, orchestrating LangGraph-based agents and semantic retrieval (RAG).

```text
repo-root/
├── frontend/           # Next.js 14 App Router frontend
└── backend/            # FastAPI + LangGraph agentic system
```

📎 Refer to [`Architecture`](./Architecture.png) for a complete system diagram.

---

## Project Structure Justification

### Frontend – Next.js (App Router)

```txt
frontend/
├── app/                # Pages and routing
│   ├── layout.tsx      # Global layout
│   ├── page.tsx        # Main dashboard
│   └── tickets/        # View per ticket
├── components/         # Reusable UI components
├── lib/                # API fetchers and type utils
├── public/             # Static assets and architecture diagram
├── styles/             # Tailwind / global CSS
```

* `lib/github.ts`: Abstracts GitHub API calls for reuse.
* `components/`: Promotes separation of UI concerns.
* `tickets/`: Entry point for user–agent interaction per ticket.

### Backend – FastAPI + LangGraph

```txt
backend/
├── app/
│   ├── data/           # Training Data for the Vector DB
│   ├── agents/         # L1, L2, L3, Classifier, Learner
│   ├── api/            # REST endpoints
│   ├── graph/          # LangGraph DAG definition
│   ├── rag/            # Vectorstore + Retriever logic
│   ├── models/         # Pydantic schemas
│   ├── services/       # Business rules / integrations
│   ├── core/           # Logging, config, security
│   └── main.py         # FastAPI entrypoint
├── tests/              # Unit + integration tests
├── requirements.txt    # Python dependencies
```

* `agents/`: Encapsulated reasoning per level of support (e.g., L1, L2, L3).
* `graph/`: LangGraph DAG node orchestration.
* `services/github_service.py`: GitHub API abstraction layer.

---

## Installation

### Install All Dependencies

```bash
make project-install
```

Executing this command performs the following actions:

* Installs frontend dependencies via `npm install`
* Creates and configures Python virtual environment
* Installs backend Python packages from `requirements.txt`

### Install Frontend Only

```bash
make frontend-install
```

### Install Backend Only

```bash
make backend-install
```

If `.venv` does not exist, it will be created automatically.

---

## Development Workflow

### Run Fullstack

```bash
make project-dev
```

This launches:

* `Frontend`: [http://localhost:3000](http://localhost:3000)
* `Backend` : [http://localhost:8000](http://localhost:8000)

### Run Frontend Only

```bash
make frontend-dev
```

### Run Backend Only

```bash
make backend-run
```

---

## Environment Variables

All runtime configuration is managed through a single `.env` file, which **must be created locally** based on the provided template.

> ⚠️ **Do not edit `.env.template` directly.** Instead, initialize your environment file by copying the template:

```bash
cp .env.template .env
```

The `.env.template` file includes a fully documented set of environment variables required for:

* **Agentic AI & LangGraph configuration**
* **GitHub integration**
* **FastAPI runtime settings**
* **Frontend runtime settings**
* **Debug/test flags and logging**
* **Vector database path (FAISS or other)**

→ View the full template: [`.env.template`](./documentation/.env.template)

---

## Testing & Linting

### Frontend

```bash
make frontend-lint      # Run ESLint
make frontend-typecheck # Run TypeScript checks
```

### Backend

```bash
make backend-test       # Run pytest
make backend-lint       # Run Ruff + Black
```

---

## Cleaning Build Artifacts

```bash
make frontend-clean
make backend-clean
```

---

## Contributions

We welcome contributions following professional standards.

Before submitting any changes, ensure that:

* Code adheres to [Clean Code](https://www.clean-code.dev/) principles
* Types are strictly enforced (e.g., TypeScript, Pydantic)
* All unit and integration tests pass
* Linting and formatting rules are respected

For design extensions (e.g., new LangGraph nodes), please consult the system architecture and open a pull request with your proposed changes.

---

Back to [README.md](./README.md)
