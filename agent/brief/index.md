---
title: Otomata Market Analysis
created: 2025-12-22
summary: Analyse concurrentielle B2B AI - 6 segments, 30+ solutions analysées
---

# Otomata Market Analysis

Analyse concurrentielle du marché B2B AI.

## Scope

**Cible:** Mid-size companies (50-500 employés)
**Focus:** Leaders établis + nouveaux entrants disruptifs
**Exclusions:** Pure enterprise (>$100K/an), pure SMB (<$500/mois)

## Segments analysés

| Segment | Status | Leaders | Challengers |
|---------|--------|---------|-------------|
| [AI SDR](segments/ai-sdr.md) | ✅ Done | 11x, Artisan, Regie.ai, Qualified | AiSDR, Persana |
| [Data Enrichment](segments/data-enrichment.md) | ✅ Done | Clay, Apollo, ZoomInfo | Harmonic, Cognism |
| [Process Automation](segments/process-automation.md) | ✅ Done | Zapier, n8n, Make | Relevance AI, Lindy |
| [B2B AI Platforms](segments/b2b-platforms.md) | ✅ Done | Writer, Jasper | Copy.ai |
| [AI Agent Frameworks](segments/ai-agents.md) | ✅ Done | LangChain | CrewAI, AutoGen |
| [Europe & France](segments/europe.md) | ✅ Done | Mistral, lemlist, Cognism, n8n | Dust, Waalaxy, Kaspr |

## Critères d'évaluation

Pour chaque solution:

1. **Business metrics**
   - Funding / Valorisation
   - ARR estimé
   - Croissance

2. **Product**
   - Features clés
   - Différenciateur
   - Stack technique

3. **Go-to-market**
   - Pricing model
   - Target customer
   - Sales motion (PLG vs Sales-led)

4. **Competitive position**
   - Forces
   - Faiblesses
   - Menaces

## Structure fichiers

```
otomata-market-analysis/
├── index.md                 # Ce fichier
├── memento.yaml
├── segments/
│   ├── ai-sdr.md           # AI Sales Development
│   ├── data-enrichment.md  # Data platforms
│   ├── process-automation.md
│   ├── b2b-platforms.md
│   └── ai-agents.md
├── research/               # Notes de recherche brutes
└── synthesis/              # Analyses transversales
```

## Synthèse

→ [Market Overview](synthesis/market-overview.md) - Analyse transversale complète

## Key Insights

1. **Convergence**: Les segments fusionnent (data + outreach + AI SDR) [clay_contrary]
2. **AI-native disruption**: n8n ($2.5B) challenge Zapier ($5B stagnant) [n8n_techfunding_c] [zapier_sacra]
3. **Agent paradigm**: Shift de "workflow" vers "AI employee" [11x_website] [lindy_getlatka]
4. **Commoditisation**: VCs inquiets - 5-10 startups avec succès simultané [techcrunch_ai_sdr]
5. **Winners**: Writer (+4x) [writer_techcrunch], n8n ($2.5B) [n8n_techfunding_c], Clay (6x) [clay_contrary], LangChain ($1.25B) [langchain_series_b]
6. **Losers**: Jasper (-54% revenue) [jasper_sacra], generic SEPs
7. **Opportunité**: Mid-market européen, verticaux, intégration
