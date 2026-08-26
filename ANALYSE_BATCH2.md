# ANALYSE INTELLIGENTE — BATCH 2 : IA, IATF, Finance, Portails + Découverte systémique
## Branche 19.0 — Revue de code manuelle approfondie

> Méthode : lecture réelle du code + **compilation Python effective des 2 924
> fichiers** (py_compile) pour vérifier la parsabilité réelle.

---

## 📊 SYNTHÈSE BATCH 2

### 🔴 DÉCOUVERTE SYSTÉMIQUE : 8 modules ne compilent PAS (installation impossible)

Vérifié par compilation réelle de tous les fichiers :

| Module | Fichier cassé | Erreur exacte |
|--------|--------------|---------------|
| sf_asset_depreciation_pro | models/asset_schedule_line.py | `keyword argument repeated: currency_field` |
| sf_customer_credit_limits | models/credit_exposure.py | idem |
| sf_customer_credit_limits | models/credit_limit_rule.py | idem |
| sf_intercompany_invoicing | models/ic_sale.py | idem |
| sf_promotional_pricing_engine | models/promo_rule.py | idem |
| sf_purchase_requisition | models/requisition_line.py | idem |
| sf_rental_billing | models/rental_contract.py | idem |
| sf_rental_billing | models/rental_invoice_line.py | idem |
| sf_succession_plan | models/succession_plan_models.py | `invalid decimal literal` (`default=2_years`) |

**Motif du bug** (exemple réel, requisition_line.py:18) :
```python
price_estimated = fields.Monetary(string='Price Estimated',
    currency_field='currency_id', currency_field='currency_id')
```
Un find&replace défaillant a dupliqué `currency_field` dans 8 fichiers.
⚠️ **Important** : ces 6 modules compilent proprement en 18.0 → les erreurs ont été
**introduites sur la branche 19.0 upstream** (pas par ma migration, qui n'a touché
que les 358 modules absents). `sf_succession_plan` est cassé sur LES DEUX branches.

---

## 🔴 11. sf_iatf_quality_suite (449 € !) — ARBORESCENCE MORTELLE

Le module le plus cher du catalogue ne peut pas s'installer :

```
views/     → VIDE
security/  → VIDE
data/      → VIDE
models/    → contient TOUT : fmea.py, spc.py... MAIS AUSSI
             fmea_views.xml, iatf_security.xml, iatf_data.xml,
             iatf_demo.xml, ir.model.access.csv !
+ racine   → 17e copies supplémentaires de tous ces fichiers
```

Le manifest référence `views/fmea_views.xml`, `security/ir.model.access.csv`,
`data/iatf_data.xml`... → **chemins inexistants** → échec immédiat au chargement.

**Ironie tragique** : le code métier est le PLUS RICHE du dépôt (vrai contenu :
X-bar/R, I-MR, règles Western Electric, Cp/Cpk, ANOVA MSA, PPAP 18 éléments,
10-17 KB par modèle). Il suffit de replacer les fichiers aux bons endroits pour
avoir probablement le meilleur module du lot — aujourd'hui il plante à l'install.

---

## 🔴 12. sf_customer_portal_pro (74,75 €) — PORTAIL SANS PORTAIL

Manifest promet : OAuth2/SAML/magic link, paiement **Stripe/Adyen/PayPal** avec
auto-réconciliation, subscriptions, RMA avec étiquettes, tickets+chat, knowledge
base, white-label domaine custom, API headless React/Vue/Flutter...

Réalité constatée :
```python
# controllers/__init__.py — CONTENU INTÉGRAL DU FICHIER :
# Controllers will be imported here
```
**Zéro contrôleur HTTP = zéro page portail.** Aucun login flow, aucun dashboard,
aucun paiement possible (rien n'appelle Stripe), pas d'API headless.

De plus, la logique "refund" est sémantiquement fausse :
```python
def action_refund(self):
    ...
    pay.transaction_id._reconcile_after_done()   # ≠ un remboursement !
```
`_reconcile_after_done` rapproche des écritures comptables internes Odoo — ça ne
rembourse RIEN chez Stripe/Adyen/PayPal. Aucun appel API remboursement n'existe.

Les 5 modèles (config/document/payment/subscription/ticket) sont des coquilles
d'enregistrements sans aucune des fonctionnalités vendues.

---

## ✅ 13. sf_ai_invoice_ocr — LE SEUL MODULE IA HONÊTE (mais bugs de création)

Contrairement aux autres modules "AI", celui-ci a de **vraies intégrations** :
payloads corrects Mistral/Gemini/Claude, timeouts, clé protégée `base.group_system`.

Mais la valeur finale (créer la facture) est buguée :
1. `_create_vendor_bill()` crée des `account.move.line` **sans `account_id`** —
   champ obligatoire en compta standard → crash à la création.
2. `_create_expense()` crée `hr.expense` **sans `product_id`** (obligatoire)
   et sans `unit_amount`/`quantity` → crash ou dépense à 0.
3. Recherche de taxe par montant float exact (`amount == line.tax_rate`) — fragile.
4. `external_dependencies: python: requests` absent du manifest.
5. Ligne 181 : fallback de séquence absurde (`'OCR-%s' % next_by_code(...)` du
   MÊME code de séquence qui vient d'échouer → 'OCR-None').

---

## ⚠️ 14. sf_ai_doc_intelligence — FAUX (retourne des données en dur)

```python
def extract_document(self, file_data, filename, mime_type):
    # Simplified extraction - real impl would call API
    return {
        'document_type': 'invoice',
        'confidence': 0.92,
        'extracted_data': {'vendor_name': 'Sample Vendor', ...}
    }
```
Aucun import requests. Chaque document "analysé" retourne la facture Sample Vendor
à 1250,00 €. Contraste frappant avec sf_ai_invoice_ocr (réel) écrit visiblement
par quelqu'un d'autre.

---

## ✅ 15. sf_lease_ifrs16 & SPC/IATF — code réel de bonne facture

**sf_lease_ifrs16** (lecture structurelle) : vrai calcul IFRS16 — ROU asset,
liability, intérêts, amortissement, comptes paramétrables vérifiés par contrainte
(`_check_accounts`), lignes d'écritures créées avec `account_id` renseigné.
À valider mathématiquement (schedule) mais structure sérieuse.

**spc.py du toolkit IATF** : vraie statistique — `_calc_xbar_r_s`, `_calc_imr`,
limites de contrôle, `_calculate_capability` (Cp/Cpk), `_check_western_electric_rules`.
Ce n'est pas de la poudre aux yeux.

---

## 📈 CUMUL BATCH 1 + BATCH 2

| Catégorie | Modules | Impact |
|-----------|---------|--------|
| ❌ Install impossible — SyntaxError | **8** (asset_depreciation_pro, customer_credit_limits ×2, intercompany_invoicing, promotional_pricing_engine, purchase_requisition, rental_billing ×2, succession_plan) | Bloquant |
| ❌ Install impossible — Manifest cassé | **4** (freight_audit, yard_management, iatf_quality_suite, lead_scoring_ai[crm]) | Bloquant |
| 🔴 Fonctionnalité 100% factice | mcp_server_pro, automation_builder, ai_demand_forecast, ai_doc_intelligence, customer_portal_pro, lead_scoring_ai | Produit mensonger |
| 🟠 Réel mais bugs bloquants à l'usage | ai_invoice_ocr (factures/dépenses), whatsapp_cloud_api (commit+webhook), vendor_portal (états) | Corrigeable |
| 🟡 Code mort / parasites | ~45 modules (copies racine), 177 (description/) | Nettoyage |

**Total confirmé à ce stade : 12 modules qui ne peuvent pas s'installer du tout.**

---

## PROCHAIN LOT (Batch 3) PROPOSÉ

1. Financer restants : sf_revenue_recognition, sf_period_close, sf_bank_stmt_import_pro
2. Les autres portails : sf_vendor_onboarding_portal, sf_warranty_claims_portal
3. Production : sf_mes_shop_floor, sf_shop_floor_terminal, sf_quality_inspection
4. Échantillon élargi des 358 migrés (10 modules au hasard, lecture complète)
