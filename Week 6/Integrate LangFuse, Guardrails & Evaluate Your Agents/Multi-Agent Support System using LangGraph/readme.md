# 🧠 Multi-Agent Support System (IT & Finance)

A **multi-agent AI support system** built using **LangChain + Amazon Bedrock (Claude 3 Sonnet)** that intelligently routes user questions to specialized agents (IT or Finance) and dynamically decides whether to answer using **internal documents (RAG)** or **external web search**.

---

## 📌 Problem Statement

Design and implement a **multi-agent support system** with the following structure:

### Agent 1: Supervisor Agent
- **Purpose:** Classifies user queries as IT or Finance
- **Action:** Routes queries to the appropriate specialist agent

### Agent 2: IT Agent
- **Purpose:** Handles all IT-related queries
- **Tools:**
  - ReadFile (RAG over internal IT docs)
  - WebSearch (external sources)
- **Example FAQs:**
  - How to set up VPN?
  - What software is approved for use?
  - How to request a new laptop?

### Agent 3: Finance Agent
- **Purpose:** Handles all Finance-related queries
- **Tools:**
  - ReadFile (RAG over internal finance docs)
  - WebSearch (public finance data)
- **Example FAQs:**
  - How to file a reimbursement?
  - Where to find last month's budget report?
  - When is payroll processed?

---

## 🏗️ Architecture Overview

            ┌────────────────────┐
            │    User Query       │
            └─────────┬──────────┘
                      │
                      ▼
            ┌────────────────────┐
            │  Supervisor Agent  │
            │  (Classifier LLM)  │
            └─────────┬──────────┘
            IT        │        Finance
           ┌──────────▼───┐   ┌───────────────┐
           │   IT Agent    │   │ Finance Agent │
           └───────┬──────┘   └───────┬───────┘
                   │                  │
     ┌─────────────▼────────────┐     │
     │  Internal Docs (RAG)      │     │
     │  - Vector DB (Chroma)     │     │
     └─────────────┬────────────┘     │
                   │                  │
            (If insufficient)         │
                   │                  │
                   ▼                  ▼
           ┌────────────────────────────────┐
           │   Web Search (Tavily API)       │
           └────────────────────────────────┘



---

## 🔄 How the System Works

1. User submits a question
2. Supervisor Agent classifies it as **IT** or **Finance**
3. Routed agent retrieves relevant internal documents (RAG)
4. LLM checks if retrieved context is sufficient
5. If insufficient → fallback to Web Search
6. Final answer is generated along with tools used

---

## 🧠 Key Design Decisions

### Why Supervisor Agent?
- Central routing logic
- Easy extensibility
- Clean separation of responsibilities

### Why RAG + Web Search?
- Prevent hallucinations
- Internal docs may be incomplete
- External queries need real-time info

### Why LLM-based Answerability Check?
Instead of heuristics, the LLM decides if the context can answer the question accurately.

---

## ▶️ Running the Application

```
python3 main.py
```

![alt text](image.png)

---
## 🧪 Example Questions

### IT Queries

- How do I set up VPN?

![alt text](image-1.png)

- What software is approved for use?

![alt text](image-2.png)

- How do I request a new laptop?

![alt text](image-3.png)

### Finance Queries

- When is payroll processed?

![alt text](image-4.png)

- How do I file a reimbursement?

![alt text](image-5.png)

- Where can I find last month’s budget report?

![alt text](image-6.png)

### External Knowledge

- Tell about Presidio Solutions Private Limited (formerly known as Coda Global), Chennai

![alt text](image-7.png)

##  What This Application Demonstrates

- Multi-agent architecture

- Intelligent routing

- RAG with fallback strategy

- Enterprise-ready AI design

- Clean, modular codebase

---

## Add LangFuse tracing and monitoring 

```
python3 main.py
```

Visit: https://cloud.langfuse.com

![alt text](image-8.png)

![alt text](image-9.png)

![alt text](image-10.png)

![alt text](image-11.png)

![alt text](image-12.png)

![alt text](image-13.png)

![alt text](image-14.png)

![alt text](image-15.png)

![alt text](image-16.png)

![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-19.png)

![alt text](image-20.png)

![alt text](image-21.png)

![alt text](image-22.png)

---

## Integrate LangChain’s Built‑In Evaluation (AgentEval)

1. Create a grounded evaluation dataset

2. Build evaluation runner

3. Compute metrics

4. Save markdown report

![alt text](image-23.png)

![alt text](image-24.png)

![alt text](image-25.png)
