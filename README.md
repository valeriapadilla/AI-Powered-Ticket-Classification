# AI-Powered Ticket Classification and Resolution System

## 📌 Overview

Manual help desk ticket classification is often slow, error-prone, and inconsistent. This project proposes a robust, agent-based AI system to **automatically classify, prioritize, and assist in the resolution of help desk tickets**, reducing response time and improving operational efficiency.

The solution leverages **LLMs (via OpenAI)**, **Retrieval-Augmented Generation (RAG)**, and **LangGraph** to orchestrate autonomous agents specialized in IT support. The system integrates with **GitHub Issues** as the canonical source of tickets and exposes a user interface for engineers and requesters.

---

## 🎯 Objectives

- Automate classification of help desk tickets into L1, L2, and L3 support levels.
- Route tickets deterministically to specialized resolution agents.
- Use vector search and RAG to retrieve relevant past solutions.
- Enable agents to document and learn from new resolutions dynamically.
- Provide traceability, security, and modularity via a layered architecture.
- Offer a frontend interface (Next.js) and backend orchestration (FastAPI).

---

## 📐 Architecture

### 🧠 Agentic Workflow (LangGraph)
![Architecture Diagram](/documentation/Architecture.png)

## 🔎 Classification Levels

Ticket classification is strictly scoped to typical Application Management (AM) scenarios. The classification criteria are aligned with ITIL best practices and corporate support standards.

### L1 Support Agent

- **Scope**: Procedural, routine tasks with low complexity.
- **Examples**:
  - Password resets
  - VPN configuration
  - Software installation (e.g., Office)
  - Folder access requests
  - FAQ-level support
- **Agent Behavior**: Resolves via direct RAG-based lookup; no reasoning required.

### L2 Support Agent

- **Scope**: Intermediate technical issues, system-specific configurations, integration problems.
- **Examples**:
  - Outlook profile errors
  - AD sync issues
  - VPN firewall blockage
  - Advanced software malfunction
- **Agent Behavior**: Uses RAG plus toolchain; may interpret logs or perform multi-step inference.

### L3 Support Agent

- **Scope**: Expert-level diagnostics, code-level bugs, architectural issues, critical incidents.
- **Examples**:
  - Application crashes
  - Unhandled exceptions
  - CI/CD or deployment regression
  - Security incident analysis
- **Agent Behavior**: Deep reasoning, long-context evaluation, suggest code/infrastructure changes.

## 🤖 Agent Definitions

### 🧠 `ClassifierAgent`

- Uses OpenAI + RAG over past labeled tickets.
- Outputs a strict label: `L1`, `L2`, or `L3`.
- Embeds rationale and confidence score.
- Routing is **non-negotiable**; agents may not override this decision.

### 🔧 `L1Agent`, `L2Agent`, `L3Agent`

- Specialize in resolution based on support level.
- Query respective vector store segments.
- If no solution is found, delegate to `LearnerAgent` with structured output.

### 📚 `LearnerAgent`

- Summarizes solution steps.
- Indexes new resolutions into the vector DB.
- Can flag potential misclassifications (but not reroute).

## 💻 System Architecture

### Frontend (Next.js 14, TypeScript)

- Ticket submission and visualization (via GitHub Issues).
- Interaction layer for Users (AM engineers) and Guests (requesters).
- Secure login (future support for GitHub OAuth or enterprise auth).

### Backend (FastAPI, Python 3.12.8)

- RESTful API for ticket retrieval, classification trigger, agent orchestration.
- Integration layer with LangGraph and OpenAI.
- Logging, audit trail, and error handling.
- Deployment-ready via Docker/Kubernetes.

## 🤝 Terminology

| Term         | Definition                                               |
|--------------|----------------------------------------------------------|
| Guest        | The end user submitting a ticket via GitHub Issue       |
| User         | Application Manager (AM) engineer resolving tickets      |
| RAG          | Retrieval-Augmented Generation                           |
| LangGraph    | Framework for composing stateful LLM agent workflows     |
| Vector Store | Embedded knowledge base queried by agents via similarity |
| Tool         | A callable function or API invoked by an agent           |

## 📏 Acceptance Criteria

| Metric                   | Description                                                    |
|--------------------------|----------------------------------------------------------------|
| Classification Accuracy  | Greater than or equal to 90% on a test set of labeled tickets |
| Response Time Reduction  | Measurable decrease in average handling time (AHT)            |
| Coverage                 | Percentage of tickets resolved directly by L1–L3 agents       |
| False Classification Rate| Tickets flagged by `LearnerAgent` for potential misclassification |

## 🚧 Known Constraints and Design Principles

- Agents are **not allowed** to re-route or reclassify tickets.
- The system favors **modularity and traceability** over dynamic agent-to-agent escalation.
- A feedback loop from the `LearnerAgent` is used to **retrain the `ClassifierAgent`** periodically.
- Human-in-the-loop review may be introduced in future iterations to improve oversight.

## 📬 Getting Started
To set up and run the system locally, see the [Getting_Started.md](./documentation/Getting_Started.md) guide.
