# AI Agent Development Platforms

Recherche: 2025-12-22

## Définition du segment

Frameworks et plateformes pour développer des agents IA:
- Orchestration multi-agents
- Tooling & observabilité
- Intégration LLMs

## Critères de sélection

- **Leaders**: Adoption massive (>50K GitHub stars), funding significatif
- **Challengers**: Approche différenciée, traction rapide
- **Dev-focused**: API-first, open-source friendly

---

## Leaders

### 1. LangChain / LangGraph / LangSmith
| Métrique | Valeur |
|----------|--------|
| Valorisation | $1.25B (Série B, Oct 2025) |
| Funding | $260M total |
| GitHub Stars | 80K+ |

**Investisseurs:** Sequoia, Benchmark, IVP, CapitalG, Sapphire Ventures

**Corporate investors:** ServiceNow Ventures, Workday Ventures, Cisco, Datadog, Databricks

**Produits:**
- **LangChain**: Framework open-source pour LLM apps
- **LangGraph**: Stateful multi-agent orchestration
- **LangSmith**: Observabilité & debugging

**Fondateur:** Harrison Chase (ex-Robust Intelligence)

**Différenciateur:**
- First-mover advantage (lancé Nov 2022)
- Écosystème le plus mature
- Concept de "chains" devenu standard

---

### 2. Microsoft AutoGen
| Métrique | Valeur |
|----------|--------|
| Origin | Microsoft Research |
| Funding | N/A (Microsoft-backed) |

**Approche:** Conversations asynchrones entre agents spécialisés

**Forces:**
- Multi-agent conversations natif
- Intégration Microsoft ecosystem
- Excellent sur coding tasks

**Différenciateur:** Async-first, agents comme participants de conversation

---

### 3. CrewAI
| Métrique | Valeur |
|----------|--------|
| Status | Open-source |
| Adoption | En forte croissance |

**Approche:** Role-based orchestration

**Features:**
- Abstraction haut niveau
- Role assignment & goal specification
- Documentation extensive

**Différenciateur:** Learning curve faible, focus sur collaboration d'équipes d'agents

---

## Challengers

### 4. LlamaIndex
| Métrique | Valeur |
|----------|--------|
| Focus | RAG & data connectors |

**Produits:**
- LlamaIndex (framework)
- LlamaCloud (managed service)

**Différenciateur:** Spécialisé RAG, complémentaire à LangChain

---

### 5. Haystack (deepset)
| Métrique | Valeur |
|----------|--------|
| Focus | NLP pipelines |

**Différenciateur:** Enterprise NLP, strong in search/QA

---

## Comparaison

| Framework | Best For | Approche | Complexité |
|-----------|----------|----------|------------|
| LangChain | Workflows custom | Graph-based | Moyenne |
| AutoGen | Tâches autonomes | Conversation-based | Moyenne |
| CrewAI | Collaboration agents | Role-based | Faible |
| LlamaIndex | RAG | Data-centric | Faible |

---

## Market Prediction

Gartner prévoit que d'ici 2028, 33% des applications enterprise intégreront des agents IA (vs <1% en 2024).

---

## Tendances

1. **Consolidation**: LangChain domine mais AutoGen/CrewAI gagnent du terrain enterprise
2. **Observability**: LangSmith, Langfuse - debugging agents devient critique
3. **Multi-agent**: Standard pour tâches complexes
4. **Stateful**: LangGraph popularise les workflows avec état
5. **Enterprise adoption**: 90% des entreprises non-tech planifient des agents en production

---

## Sources

- https://blog.langchain.com/series-b/
- https://techcrunch.com/2025/07/08/langchain-is-about-to-become-a-unicorn-sources-say/
- https://www.turing.com/resources/ai-agent-frameworks
- https://langfuse.com/blog/2025-03-19-ai-agent-comparison
