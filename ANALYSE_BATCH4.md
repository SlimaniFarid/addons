# ANALYSE INTELLIGENTE — BATCH 4 : Dépendances manquantes (crash à l'installation)
## Branche 19.0 — Analyse croisée AST : modèles référencés ↔ `depends` déclarés

> Méthode : extraction AST de tous les `Many2one`/`One2many`/`Many2many`/`_inherit`
> puis vérification que le module propriétaire du modèle est atteignable depuis les
> dépendances déclarées **directement ou par transitivité** (ex. `account` → `product`
> → ok ; `sale` ↛ `purchase` → crash).

---

## 🔴 VERDICT GLOBAL : ~35 modules planteront sur une base propre

Odoo échoue au chargement du registre (`ValueError: Model not found`) dès qu'un
`fields.Many2one('modele.inconnu')` est défini sans l'app qui le fournit.
Sur une base vierge où seule la branche des `depends` est installée, ces modules
**ne peuvent pas s'installer**.

---

## GROUPE 1 — `crm` manquant (2)

| Module | Référence | Depends déclarés |
|--------|-----------|------------------|
| sf_lead_scoring_ai | `crm.lead` | base, mail, account, stock |
| *(déjà signalé Batch 1)* | | |

## GROUPE 2 — `purchase` manquant alors que le module parle d'achats (3)

| Module | Référence |
|--------|-----------|
| sf_po_acknowledgment | `purchase.order` |
| sf_po_budget_check | `purchase.order` |
| sf_purchase_order_aging | `purchase.order` |

Déps = `['base','mail','sale']` — ironique : dépendent de *sale* pour des PO.

## GROUPE 3 — `mrp` manquant — toute la famille Production (14)

Modules avec `depends=['base','mail','sale']` mais champs vers `mrp.production` /
`mrp.workcenter` :

sf_production_capacity_plan, sf_production_line_efficiency,
sf_production_oee_calculator, sf_production_oee_tracker,
sf_production_order_priority, sf_production_order_sequencing,
sf_production_schedule_alert, sf_production_scheduling,
sf_production_waste_tracker, sf_production_yield_analysis,
sf_production_yield_tracker

*(+ variants déjà cassés par ailleurs)*

## GROUPE 4 — `maintenance` manquant (5)

| Module | Référence |
|--------|-----------|
| sf_equipment_utilization | `maintenance.equipment` |
| sf_maintenance_cost_tracker | `maintenance.equipment` |
| sf_maintenance_schedule_optimizer | `maintenance.equipment` |
| sf_preventive_maintenance_pro | `maintenance.equipment` + `maintenance.request` |
| sf_first_article_inspection | `maintenance.equipment` |

## GROUPE 5 — `hr` manquant (14)

`hr.employee` / `hr.department` référencés avec déps sans HR :

sf_customer_care_coaching, sf_customer_care_training, sf_document_expiry_tracker,
sf_employee_1on1_tracker, sf_employee_skill_gap, sf_it_asset_lifecycle,
sf_project_resource_plan, sf_safety_training_tracker, sf_telecom_expense,
sf_shop_floor_terminal, sf_field_service_offline*, sf_senior_living,
sf_spa_wellness, sf_salon_beauty*

\* à confirmer par transitivité `industry_fsm`→`hr`.

## GROUPE 6 — Autres crashes confirmés

| Module | Problème |
|--------|----------|
| sf_ai_contract_analyzer | `sale.order` + `purchase.order` utilisés, ni `sale` ni `purchase` dans les déps (mais `fleet` y est...) |
| sf_intercompany_invoicing | `sale.order` sans `sale` |
| sf_returns_rma | `repair.order` (champ réel dans disposition) sans `repair` — crash garanti au clic comme à l'install |
| sf_ai_demand_forecast & ~20 autres | `product.product` sans `product` — **sauf transitivité** : OK si `sale`/`account` présents ; crash seulement pour les rares modules déps=`['base','mail','stock']` uniquement (à filtrer cas par cas lors du fix) |

## ⚠️ GROUPE 7 — Modèles FANTÔMES (ni Community ni Enterprise standard)

Références vers des modèles inexistants en Odoo 19 standard — crash même si les
déps étaient corrigés :

| Module | Modèle fantôme |
|--------|---------------|
| sf_customer_portal_pro | `helpdesk.team` (Enterprise), `sale.subscription` (**supprimé de Community depuis v15**) |
| sf_subscription_dunning | `dunning.level` |
| sf_quality_inspection | `inspection.plan` (interne ? fichier syntax-error empêche la vérification) |
| sf_preventive_maintenance_pro | `pm.plan` |
| sf_rental_billing | `rental.contract` |
| sf_warehouse_heatmap | `slotting.analysis` |
| sf_construction_boq | `construction.*` ×4 |

⚠️ Plusieurs sont probablement des modèles **internes au module** dont la définition
est illisible à cause des erreurs de syntaxe/doublons déjà recensées — à trancher
fichier par fichier pendant les correctifs.

---

## 📌 FAUX POSITIFS ÉCARTÉS (transitivité vérifiée)

Pour mémoire — NON bloquants grâce aux chaînes de dépendances :
- `product.*`, `uom.*`, `mail.thread` quand `sale`/`account` présents
  (`sale`→`account`→`product`,`mail`) — concerne ~45 flags du scan brut
- `crm.team` via `sale`→`sales_team` (sf_sale_auto_workflow)
- `project.task` via `industry_fsm`→`project` (sf_field_service_offline)
- `report.paperformat` = modèle **de base** (fausse alerte)

---

## 📈 CUMUL FINAL BATCHES 1-4 (branch 19.0)

| Catégorie | Nombre |
|-----------|--------|
| ❌ SyntaxError pur (compile fail) | 8 fichiers / 6 modules |
| ❌ Manifest → fichiers inexistants | 2 (freight_audit, yard_management) |
| ❌ Arborescence détruite (IATF) | 1 |
| ❌ Dépendances manquantes (crash registre) | **~35 nouveaux** |
| ❌ Modèles fantômes | ≥6 |
| 🔴 Selection() sans options | 49 champs / 30 modules |
| 🔴 Comptabilité fausse (revrec) | 1 |
| 🔴 Fonctionnalité factice | 7 modules |
| **TOTAL modules non-installables estimé** | **≈ 55–60 / 535** |

---

## PLAN DE CORRECTION RECOMMANDÉ (ordre optimal)

1. **Lot A — mécanique, faible risque** : corriger 8 SyntaxError + replacer
   arborescence IATF + retirer 2 entrées manifest inexistantes (freight_audit :
   créer les vues OU retirer du manifest) → +11 modules récupérés immédiatement
2. **Lot B — depends** : ajouter les ~35 `depends` manquants (une ligne par
   manifest, risque nul)
3. **Lot C — Selection sans options** : compléter les 49 listes de valeurs
   (nécessite lecture contexte métier par champ)
4. **Lot D — décisions produit** : factice (mcp/automation/ai_doc/portails),
   revrec comptable, lead_scoring_ai → supprimer OU implémenter
5. **Lot E — nettoyage** : 177 dossiers description/, ~45 jeux de fichiers racine
