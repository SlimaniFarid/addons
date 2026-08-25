# RAPPORT FINAL — AUDIT & REMÉDIATION BRANCHE 19.0
## SlimaniFarid/addons — 535 modules — 2026-08-25

---

## 1. CE QUI A ÉTÉ TROUVÉ (analyse intelligente, Batches 1-4)

### Modules impossibles à installer — 47 récupérés
| Cause | Count | Correction |
|-------|-------|-----------|
| SyntaxError (`currency_field` dupliqué ×8, `default=2_years`) | 8 | Lot A ✅ |
| Manifest → fichiers inexistants (freight_audit, yard_management) | 2 | Lot A ✅ |
| Arborescence détruite (iatf_quality_suite, 449 €) | 1 | Lot A ✅ |
| `crm.lead` sans dep crm (lead_scoring_ai) | 1 | Lot B ✅ |
| Dépendances manquantes non-transitives (mrp×11, hr×14, purchase×3...) | 35 | Lot B ✅ |

### Défauts de code corrigés — Lot C (58 correctifs / 24 modules)
- 27 champs `Selection` cassés (bug générateur `default='draft tracking'`, listes vides)
- 9 `Boolean(default='True')` en chaîne
- 9 comodels erronées redirigées vers les vrais noms de modèles du module
- 3 champs `state` absents mais utilisés par les actions → ajoutés
- 2 computes manquants implémentés (`_compute_category` NPS, `_compute_next_due` PM)
- 1 `default='current'` invalide → lambda env.user
- 3 modèles squelettes + ACL créés pour références pendantes vivantes

### Comptabilité fausse — sf_revenue_recognition (Lot D1) ✅
Écritures IFRS15 inversées (débit client !) + compte '411000' codé en dur + journal absent
→ direction corrigée (Dr revenus différés / Cr revenus), comptes paramétrables sur le
contrat + contrainte d'activation + résolution journal général.

### Sécurité & robustesse — Lot D1 ✅
| Module | Faille | Correctif |
|--------|--------|-----------|
| mcp_server_pro | parsing outil cassé (jamais fonctionnel), clé API timing-attack, lecture sudo sans masquage, rate-limit factice | parsing points (`read_sale__order`), `hmac.compare_digest`, masquage champs sensibles, cap 100, fenêtre glissante réelle |
| vendor_portal | accepter/contrer un PO dans tout état, montants négatifs | garde `state='sent'` + montant>0 |
| automation_builder | handler d'erreur crashait (`_logger` absent) | logger défini |
| whatsapp_cloud_api | `cr.commit()` manuel en boucle | supprimé |
| ai_invoice_ocr | création facture sans `account_id`, dépense sans `product_id` | compte de charge partenaire (fallback société), produit expensable requis |

---

## 2. PURGE — Lot E (1 719 items, −22 478 lignes)
- 1 258 `__pycache__`
- 177 dossiers racine `description/` (doublons non-standard)
- ~60 doublons racine `.py` (jumeaux sous-dossiers confirmés identiques)
- 249 entrées manifest `'images'` mortes
**Vérification post-purge : 0 référence morte, 2 883 fichiers compilent.**

---

## 3. COMMITS LOCAUX (branche `fix/security-audit-19.0`)

| Commit | Contenu |
|--------|---------|
| `05e3e58b` | Lot A+B : 47 modules désinstallables réparés |
| `ecf9a2cb` | Lot C : 58 défauts / 24 modules |
| `096bd6f5` | Lot E : purge 1 719 items |
| `2015f716` | Lot D1 : 6 modules cassés réparés (+sécurité MCP) |

*(+ commit antérieur : migration 358 modules + fixes sécurité/stubs)*

---

## 4. ⚠️ DÉCISIONS PRODUIT RESTANTES (Lot D2 — votre arbitrage)

Ces modules s'installent désormais mais leur **promesse reste fausse** :

| Module | Prix | Promesse | Réalité | Options |
|--------|------|----------|---------|---------|
| sf_mcp_server_pro | Pro | Serveur MCP IA pour Odoo | Réparé et sécurisé (D1) mais jamais testé avec un vrai client MCP | Garder / Tester E2E |
| sf_ai_demand_forecast | — | ML Gradient Boosting/RF | Métriques **fabriquées en dur** (MAE 12.5...) ; aucune prédiction générée | A) Implémenter sklearn+deps B) Retirer métriques/UI C) Supprimer |
| sf_ai_doc_intelligence | — | Extraction doc IA | Retourne "Sample Vendor" pour tout | A) Brancher API (modèle = ai_invoice_ocr) B) Supprimer |
| sf_customer_portal_pro | 74,75 € | Portail complet Stripe/PayPal/OAuth2 | Zéro contrôleur HTTP ; refund ≠ remboursement réel ; `sale.subscription` fantôme ; `helpdesk.team` Enterprise | A) Construire (lourd) B) Re-scope manifest C) Supprimer |
| sf_vendor_onboarding_portal | — | Portail fournisseur | Backend seulement (workflow réparé Lot C) | Idem |
| sf_warranty_claims_portal | — | Portail garantie | Backend seulement | Idem |
| sf_lead_scoring_ai | 62,50 € | Scoring auto des leads | Installable ; règles/grade existent mais **aucun moteur de calcul** | A) Implémenter scoring simple pondéré B) Supprimer |
| sf_automation_builder | — | Builder de workflows | Flows s'exécutent sans rien faire ; déclencheurs webhooks/cron absents | A) Moteur minimal (server actions par node) B) Re-scope |
| sf_iatf_quality_suite | 449 € | Toolchain IATF complète | Code riche et réel ; installable depuis Lot A ; **non testé en profondeur** | Recommandé : tests dédiés |

### Points signalés sans action (ambiguïté volontairement conservée)
- `helpdesk.team` (Enterprise) dans customer_portal_pro : crash si installé sans Enterprise → à trancher avec D2-portail
- ~40 modules gardent quelques copies XML/CSV racine inertes (stems non importés) — résidu cosmétique documenté

---

## 5. NON FAIT (hors périmètre validé)
- Exécution réelle sous Odoo 19 (`odoo-bin -i ... --test-enable`) — aucun runtime disponible ici
- Migration des 23 doublons supprimés côté 18.0 : N/A (19.0 déjà propre)
- Tests unitaires pour les ~350 modules registres (recommandé par vagues métier)
