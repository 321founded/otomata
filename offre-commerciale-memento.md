# MEMENTO - Synthèse pour Offre Commerciale

## L'OFFRE EN 3 NIVEAUX

### Niveau 1 : Claude Code Brut
- Agent IA conversationnel en CLI/SDK
- Exécute des tâches de dev, recherche, automatisation
- Accès aux outils système (bash, fichiers, git)
- Utilisation manuelle, session par session

### Niveau 2 : Claude Code + Memento Framework
- **Scripts agentiques** : Instructions en langage naturel + boîte à outils
- **Workflow guidé mais flexible** : L'IA adapte son parcours aux obstacles
- **Batch processing** : Traitement en masse parallélisé (5 agents simultanés)
- **Intégration Slack** : `@memento` ou `/memento` pour lancer des agents
- **25 outils intégrés** : Sirene, Pappers, Apollo, LinkedIn scraping, Kaspr, etc.

### Niveau 3 : Memento Custom (SaaS)
- **App métier Django** personnalisée
- **Base de données** Companies/Persons enrichissable
- **Dashboard web** pour suivi et visualisation
- **Jobs récurrents** (cron) + scheduling
- **MCP Server** pour connexion Claude.ai desktop
- **Traçabilité totale** : Chaque action, source, coût tracés

---

## LE CONCEPT CLÉ : SCRIPT AGENTIQUE

**Différence avec un script classique :**

| Script classique | Script agentique |
|------------------|------------------|
| Séquence rigide | Objectif + principes |
| Bloque si erreur | Adapte son approche |
| Code à modifier | Contexte à ajuster |
| Déterministe | Créatif |

**Exemple concret** (`instructions-freestyle.md`) :
```markdown
## Objectif
Enrichir {NAME} (SIREN: {SIREN}) avec contacts décideurs

## Outils disponibles
- Pappers (dirigeants officiels)
- LinkedIn (employés vérifiés)
- Kaspr (emails)
- Hunter (pattern email)

## Principes
- Sois resourceful : si une approche échoue, essaie-en une autre
- Qualité > Quantité
- N'abandonne pas trop vite
```

L'IA choisit l'ordre, gère les échecs, s'adapte au contexte de chaque entreprise.

---

## CAS CONCRET 1 : PAYT (Listings Producer)

**Client** : PayT, fintech française (recouvrement B2B)

**Besoin** : Générer des listes qualifiées de cabinets comptables pour prospection

**Pipeline automatisé :**
```
SIRENE (52K comptables FR)
    ↓ Filtrage (20-200 salariés, Top 10 villes)
354 entreprises
    ↓ Enrichissement LinkedIn (70% match)
    ↓ Contacts (Pappers + LinkedIn = 96% couverture)
~1770 contacts
    ↓ Catégorisation IA (DIRIGEANT/COO/CHEF_DE_MISSION)
    ↓ Scoring IA (COEUR_DE_CIBLE/HIGH_POTENTIAL/MEDIUM/LOW)
    ↓ Push vers Lemlist
Campagnes outreach
```

**Résultats :**
- 354 cabinets qualifiés
- ~5 contacts/entreprise
- 90% HIGH_POTENTIAL après scoring
- Performance : ~2 min/company, 1000 companies en ~7h (5 agents parallèles)
- Coût scoring : $0.02/30 companies (Haiku)

**Workflows disponibles :**
- `enrich-company/` : Enrichissement complet d'une entreprise
- `manage-batch/` : Orchestration du traitement en masse
- `lemlist-sync/` : Push automatique vers campagnes
- `score-companies/` : Scoring IA batch

---

## CAS CONCRET 2 : ORANGE CDN BOOST

**Client** : Orange Business Services

**Besoin** : Identifier des partenaires pour ventes indirectes CDN en Europe

**Agents déployés (parallèles) :**
1. `cdn-indirect-sales-strategy` → Framework stratégique
2. `cdn-web-agencies-market` → Segmentation marché
3. `cdn-resellers-listings` → Base de données prospects
4. `cdn-partner-search` → Identification partenaires

**Résultats :**
- **88 partenaires qualifiés** avec scoring 5 dimensions
- **898 MSPs français** identifiés (SIRENE, codes NAF ciblés)
- **264 Core MSPs** haute pertinence CDN
- Scoring automatisé : Critical (8), High (25), Medium (43), Low (12)
- Export Notion pour suivi commercial
- **Reproductible** pour Espagne, Pays-Bas, Afrique

**Automatisation :**
- Collection SIRENE : ~2h vs plusieurs jours manuellement
- 9/10 entreprises prioritaires trouvées automatiquement
- Formats CRM-ready (CSV, JSON, Notion)

---

## ARCHITECTURE TECHNIQUE

```
┌─────────────────────────────────────────────────────────────┐
│                      MEMENTO PLATFORM                       │
├─────────────────────────────────────────────────────────────┤
│  INTERFACES                                                 │
│  ├── WebApp Django (dashboard, viewers, API)               │
│  ├── Slack Bot (@memento, /memento workflows)              │
│  ├── MCP Server (Claude.ai desktop)                        │
│  └── CLI direct                                             │
├─────────────────────────────────────────────────────────────┤
│  WORKER (FastAPI + Claude SDK)                             │
│  ├── Job Manager (claiming atomique, concurrence 5)        │
│  ├── Agent Executor (streaming, tool calls)                │
│  ├── Scheduler (cron jobs)                                 │
│  └── Batch Executor (parallélisation)                      │
├─────────────────────────────────────────────────────────────┤
│  DATA                                                       │
│  ├── PostgreSQL (Chats, Jobs, Companies, Persons)          │
│  ├── File System (agents/, projects/, knowledge)           │
│  └── Git (auto-commit des résultats)                       │
├─────────────────────────────────────────────────────────────┤
│  TOOLS (25 outils, 109 méthodes)                           │
│  ├── Intelligence : Pappers, SIRENE, Apollo, Kaspr         │
│  ├── Scraping : LinkedIn, Crunchbase, Serper, Hunter       │
│  ├── Productivité : Notion, Google Drive/Sheets/Slides     │
│  └── Marketing : Lemlist, Folk CRM                          │
└─────────────────────────────────────────────────────────────┘
```

---

## VALEUR AJOUTÉE

### Pour le Business Development
- **Sourcing automatisé** : SIRENE, Apollo, LinkedIn
- **Enrichissement multi-sources** : 96% couverture (LinkedIn + Pappers)
- **Qualification IA** : Scoring contextualisé
- **Push CRM** : Synchronisation Lemlist, exports CSV

### Pour les Opérations
- **Reproductibilité** : Mêmes workflows, nouveaux segments
- **Scalabilité** : 5 agents parallèles, batch processing
- **Traçabilité** : Chaque action, source, coût documentés
- **Autonomie** : Exécution sans supervision

### Pour l'IT
- **Évolutif via CC** : L'app évolue avec Claude Code
- **Intégrations API** : Google, Slack, Notion, etc.
- **Self-hosted** : Serveur dédié, données maîtrisées

---

## MODÈLE DE DÉPLOIEMENT

**Setup initial :**
- Serveur dédié (Scaleway ou autre)
- App métier Django + PostgreSQL
- Worker Claude SDK (token longue durée)
- Configuration domaine/projet

**Évolution continue :**
- Nouveaux workflows via CC
- Ajout d'outils métier
- Dashboards personnalisés
- Intégrations CRM client

**Modes d'usage :**
1. **Assistant** : Chat ponctuel via Slack/web
2. **Automation** : Jobs récurrents, batch processing
3. **Développement** : Évolution de l'app via CC

---

## CHIFFRES CLÉS

| Métrique | Valeur |
|----------|--------|
| Outils intégrés | 25 (109 méthodes) |
| Concurrence max | 5 agents simultanés |
| Coût enrichissement | ~$0.10-0.20/company (Sonnet) |
| Coût scoring | ~$0.001/company (Haiku) |
| Performance | ~2 min/company (enrichissement complet) |
| Throughput | ~1000 companies/7h (batch 5 agents) |
| Taux enrichissement | 65-70% (LinkedIn) |
| Couverture contacts | 96% (LinkedIn + Pappers) |
