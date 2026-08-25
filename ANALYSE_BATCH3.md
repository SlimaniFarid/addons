# ANALYSE INTELLIGENTE — BATCH 3 : Finance, Portails, MES + Bug systémique majeur
## Branche 19.0 — Revue de code manuelle approfondie

---

## 📊 SYNTHÈSE BATCH 3

### 🔴 DÉCOUVERTE SYSTÉMIQUE MAJEURE : 49 champs `Selection` SANS OPTIONS

Recherche structurelle (AST) sur tout le dépôt : **49 champs `fields.Selection(...)`
déclarés sans aucune liste de valeurs** dans **~30 modules**. Ce sont des champs
cassés par construction :

```python
# Pattern du bug (généré) :
state = fields.Selection(default='draft tracking', tracking=True)   # vendor_onboarding
operator = fields.Selection(default='eq')                            # lead_scoring_ai
grade = fields.Selection(default='D')                                # lead_scoring_ai
```

Notez `default='draft tracking'` : un copié-collé de `default='draft', tracking=True`
fusionné en une seule chaîne — signature d'une génération de code défaillante.

**Conséquences** : dropdown vide en UI, crash des workflows qui itèrent sur
`selection` (`TypeError: 'NoneType' is not iterable` dans `_get_next_state`),
et échec potentiel au chargement des vues.

**Liste complète des modules touchés** (occurrences réelles hors doublons racine/models) :

| Module | Fichiers touchés |
|--------|------------------|
| sf_agriculture | res_company.py |
| sf_automation_builder | automation_log.py, automation_node.py |
| sf_bank_stmt_import_pro | bank_run.py ×2 champs |
| sf_barcode_label_designer | label_print_batch.py, label_template.py ×2 |
| sf_complaint_8d | complaint_8d.py |
| sf_customer_credit_limits | credit_exposure.py |
| sf_document_expiry_tracker | employee_document.py ×2 |
| sf_esg_reporting | esg_value.py, res_company.py |
| sf_field_dispatch_board | dispatch_ticket.py ×2 |
| sf_franchise | sf_franchise_declaration.py |
| sf_freight_costing | freight_cost.py |
| sf_iatf_quality_suite | ppap.py |
| sf_intercompany_invoicing | ic_sale.py |
| sf_lead_scoring_ai | lead_score.py, scoring_rule.py *(déjà signalé)* |
| sf_lease_ifrs16 | lease_contract.py |
| sf_nps_feedback | nps_campaign.py ×2, nps_response.py |
| sf_preventive_maintenance_pro | pm_plan.py, pm_work_order.py |
| sf_production_scheduling | schedule_plan.py |
| sf_purchase_requisition | purchase_requisition_sf.py |
| sf_quality_inspection | inspection_plan.py, quality_inspection.py |
| sf_rental_billing | rental_contract.py |
| sf_senior_living | care_plan, residence, resident ×2 *(pire cas : 5 champs)* |
| sf_shop_floor_terminal | shop_floor_entry.py |
| sf_subscription_dunning | dunning_case.py |
| sf_vendor_onboarding_portal | vendor_onboarding.py |
| sf_warehouse_heatmap | slotting_analysis.py, slotting_result.py |
| sf_warranty_claims_portal | warranty_claim.py |
| sf_yard_management | sf_yard_zone.py |

---

## 🔴 16. sf_revenue_recognition — ÉCRITURES COMPTABLES FAUSSES (domaine critique)

Module de reconnaissance de revenu IFRS 15. La logique de scheduling existe
(mensuel, point-in-time, allocations SSP). Mais l'écriture générée est **fausse** :

```python
# revrec_contract.py :: action_recognize()
move = self.env['account.move'].create({
    'move_type': 'entry',          # ⚠️ journal_id absent → requis pour 'entry'
    'line_ids': [
        (0, 0, {'account_id': partner.property_account_receivable_id.id,
                'debit': amount}),                       # ❌ DÉBIT CLIENT !
        (0, 0, {'account_id': search([('code','=','411000')]).id,
                'credit': amount}),                      # ❌ COMPTE EN DUR
    ],
})
```

Trois erreurs graves :
1. **Sens de l'écriture inversé** : reconnaître un revenu doit créditer un compte
   de produit et débiter un compte de revenus différés (passif contractuel).
   Ici on **débite la créance client** sans facture → balance âgée faussée,
   rapprochement impossible, TVA polluée.
2. **Compte codé en dur '411000'** : plan comptable français uniquement. Sur tout
   autre plan, `search(...)` retourne vide → `.id` = False → ligne sans compte →
   rejet Odoo. Aucun paramétrage possible.
3. **`journal_id` manquant** sur un `move_type='entry'` → crash probable à la
   création même avant la validation.

De plus les fichiers `revrec_schedule/allocation/journal/obligation.py` sont des
placeholders de 38 octets (`# Models defined in revrec_contract.py`) importés par
`__init__.py` — code mort organisationnel.

**Pour un module comptable, c'est le niveau de gravité maximal : il fabrique des
écritures erronées en base.**

---

## 🔴 17. Portails sans portail — schéma récurrent confirmé

| Module | Contrôleurs | Constat |
|--------|-------------|---------|
| sf_customer_portal_pro | ❌ aucun *(Batch 2)* | 74,75 € vendus |
| sf_vendor_onboarding_portal | ❌ dossier controllers inexistant | + champ Selection cassé → workflow `_get_next_state()` crash au clic |
| sf_warranty_claims_portal | ❌ dossier controllers inexistant | + MÊME bug `Selection(default='draft tracking')` |

Le motif se répète : modules nommés "_portal", dépendances website/portal présentes,
mais **aucune route HTTP, aucune page QWeb** — juste un modèle backend avec boutons.

---

## 🟡 18. Modules migrés simples — échantillon honnête (3 lectures complètes)

**sf_win_loss_analysis, sf_zone_capacity_monitor, sf_succession_plan** (les 358
migrés sont de cette famille) :

✅ Code propre : syntaxe correcte, séquences, multi-société, chatter, workflow
simple, ACL cohérentes, vues basiques présentes.

⚠️ Mais **superficiels** :
- `occupancy_percent` (zone_capacity) est un Float **saisi manuellement** alors que
  `max_pallets` et `current_pallets` existent — le calcul évident n'est pas fait.
- Aucun calcul métier, aucun cron, aucune automatisation : ce sont des registres
  à boutons state.
- Verdict honnête : *installent et fonctionnent, mais livrent le strict minimum
  promis par le summary*. Qualité "acceptable vendu 57-62 €", pas plus.

---

## 📈 CUMUL BATCHES 1-3

| Gravité | Nombre | Détail |
|---------|--------|--------|
| ❌ Install impossible (syntaxe) | 8 | currency_field dupliqué ×8 fichiers, 2_years |
| ❌ Install impossible (manifest/arbo) | 4 | freight_audit, yard_management, iatf_quality_suite, lead_scoring_ai |
| 🔴 Comptabilité fausse | 1 | revenue_recognition (écritures inversées + compte en dur) |
| 🔴 Produit mensonger total | 7 | mcp_server_pro, automation_builder, ai_demand_forecast, ai_doc_intelligence, customer_portal_pro, vendor_onboarding_portal*, warranty_claims_portal* |
| 🔴 Champs cassés systémiques | ~30 modules | 49 Selection sans options |
| 🟠 Réel mais bugs bloquants | 3 | ai_invoice_ocr, whatsapp_cloud_api, vendor_portal |
| 🟡 Superficiel mais fonctionnel | ~358 | famille des registres migrés |

\* *portails sans portail*

---

## PROCHAIN LOT (Batch 4) PROPOSÉ

1. **Vérification croisée manifest ↔ modèles** : modules dont les `depends`
   référencent des modèles d'apps absentes (comme lead_scoring_ai/crm) — scan AST
   des comodel_name/_inherit vs depends sur TOUT le dépôt
2. **Crons & actions serveur orphelines** : data XML référençant des méthodes inexistantes
3. **Modules restants à lecture profonde** : mes_andons, quality_coa, complaint_8d,
   subscription_dunning, preventive_maintenance_pro (touchés par le bug Selection)
