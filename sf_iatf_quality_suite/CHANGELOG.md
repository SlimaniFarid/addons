# Changelog — sf_iatf_quality_suite

All notable changes to this module are documented here.

## [18.0.1.0.0] — 2024-08-23 — Version Initiale (Odoo 18.0)
## [19.0.1.0.0] — 2024-08-23 — Version Initiale (Odoo 19.0)

### 🎯 Fonctionnalités Incluses (MVP Complet)

#### FMEA (DFMEA & PFMEA) — AIAG-VDA 2019
- Header FMEA : type (Design/Process), projet APQP, produit, processus, équipe, scope, boundary diagram
- Lignes FMEA : fonction, exigence, mode de défaillance, cause, effet, contrôles prévention/détection
- Ratings S/O/D (1–10) → RPN auto-calculé (S × O × D) + classe (Low/Medium/High/Critical)
- Actions recommandées : responsable, échéance, action réalisée, re-rating (nouveaux S/O/D, nouveau RPN)
- Liaison bidirectionnelle DFMEA ↔ PFMEA via caractéristiques produit/processus
- Workflow : Draft → In Progress → Review → Approved → Active → Obsolete
- Révision avec historique complet (mail.thread)
- Export PDF/Excel format AIAG

#### Control Plan — AIAG 1st Edition
- 3 phases : Prototype, Pre-Launch, Production avec versioning
- Génération auto depuis PFMEA (seuil RPN configurable, défaut 150)
- Lignes : caractéristique produit/processus, spécification (USL/LSL/Target), méthode contrôle, dispositif, équipement, fréquence, taille échantillon, plan de réaction, responsable
- Liaison MSA study par méthode de mesure
- Synchronisation native Odoo `quality.point` à l'activation (création/màj auto)
- Liaison opération processus (`iatf.process.operation`)
- Workflow : Draft → Review → Approved → Active → Obsolete

#### APQP — AIAG 3rd Edition (5 Phases, 23 Éléments)
- Projet : client, produit, dates, phase courante, équipe, manager
- 23 éléments standards pré-chargés à la création (répartis sur 5 phases)
- Statuts par élément : Not Started / In Progress / Complete / N/A
- Phase gates : passage phase suivante bloqué si éléments incomplets
- Traçabilité : liens vers FMEA, Control Plan, PPAP, MSA
- Vue Gantt timeline + Kanban par phase
- Responsable, échéance, date completion, pièces jointes par élément

#### PPAP — AIAG PPAP-4 (18 Éléments, Niveaux 1–5)
- Soumission : client, pièce, niveau (1–5), dates, workflow état
- 18 éléments standards pré-configurés selon niveau (requis/NA auto)
- Statuts élément : Pending → In Progress → Submitted → Reviewed → Approved/Rejected/NA
- Part Submission Warrant (PSW) : auto-rempli depuis données projet, signature déclarative
- Générateur package PDF : couverture, table des matières, 18 éléments + PSW
- Workflow : Draft → Preparing → Submitted → Customer Review → Approved/Rejected/Withdrawn

#### MSA / Gauge R&R — AIAG MSA 4th Edition
- 3 types d'études : Crossed (ANOVA), Nested (destructif), Attribute (Kappa)
- Paramètres : caractéristique, spécification, équipement, pièces, opérateurs, essais
- Calculs Crossed : %GRR (TV & Tolérance), %EV, %AV, %PV, ndc, Cp, Cpk, p-values ANOVA
- Critères acceptation AIAG : <10% acceptable, 10–30% marginal, >30% unacceptable, ndc ≥ 5
- Conclusion auto-déterminée
- Liaison Control Plan line (méthode de mesure)

#### SPC Control Charts — AIAG SPC 2nd Edition
- 7 types de cartes :
  - Variable : X-bar/R (n=2–10), X-bar/S (n>10), I-MR (n=1)
  - Attribute : p, np, c, u
- Limites de contrôle auto-calculées (constantes AIAG : A2, D3, D4, B3, B4)
- Capabilité : Cp, Cpk, Pp, Ppk (court terme via within-subgroup / long terme overall)
- Règles Western Electric 1–4 détectées auto sur nouveaux points :
  1. Point > 3σ (UCL/LCL)
  2. 2 sur 3 points > 2σ même côté
  3. 4 sur 5 points > 1σ même côté
  4. 8 points consécutifs même côté ligne centrale
- Alertes avec workflow : New → Acknowledged → Investigating → Resolved / False Alarm
- IoT-ready : endpoint HTTP pour ingestion capteurs (MQTT/HTTP), déclenche vérification règles temps réel

#### Process Management
- Processus : nom, code, produit, description, diagramme flux (PFD)
- Opérations : séquence, nom, description, centre de travail, équipements
- Base pour PFMEA et Control Plan linkage

### 🔧 Technique & Architecture

- **15 modèles** : FMEA, FMEA Item, Process, Process Operation, Control Plan, CP Line, APQP Project, APQP Element, PPAP Submission, PPAP Element, PPAP PSW, MSA Study, MSA Measurement, SPC Chart, SPC Measurement, SPC Alert
- **Héritage** : `mail.thread`, `mail.activity.mixin` sur tous modèles principaux
- **Séquences** : 7 séquences auto-installées (DFMEA-, PFMEA-, CP-, APQP-, PPAP-, MSA-, SPC-)
- **Sécurité** : 5 groupes hiérarchiques + 7 `ir.rule` multi-company (isolation par société, PPAP visible client/fournisseur)
- **Dépendances** : base, quality, maintenance, mrp, stock, mail, product
- **Vues** : List, Form, Kanban, Pivot (FMEA), Gantt (APQP) — ~7300 lignes XML
- **Compatible** : Odoo 18.0 (cible) & 19.0 (APIs stables, pas d'appels dépréciés)
- **Éditions** : Community & Enterprise
- **Hébergement** : Odoo.sh, On-premise, Docker (pas Odoo Online — code Python)

### 📦 Livrables Commerciaux
- `static/description/index.html` — Fiche produit Apps Store (pitch, bénéfices, captures, FAQ)
- `README.md` — Guide intégrateur (install, config, workflow, troubleshooting)
- `PRICING.md` — Fiche tarifaire + justification vs concurrence
- `CHANGELOG.md` — Ce fichier

---

## Prochaines Versions (Roadmap)

| Version | Cible | Contenu Prévu |
|---------|-------|---------------|
| **18.0.1.1.0 / 19.0.1.1.0** | Q4 2024 | Rapports QWeb PPAP/MSA/SPC finalisés, contrôleur IoT HTTP `/iatf/spc/ingest`, dashboard OWL KPIs qualité |
| **18.0.2.0.0 / 19.0.2.0.0** | Q1 2025 | Portail fournisseur PPAP collaboratif, templates PPAP par profil industrie (Auto/Aero/Medical) |
| **18.0.3.0.0 / 19.0.3.0.0** | Q2 2025 | FMEA logiciel (ISO 26262), DRBFM, intégration PLM/CAO (CATIA, NX, SolidWorks) |