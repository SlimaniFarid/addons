# MCP Server Pro — Test E2E (curl)

Prérequis :
1. Installer le module, ouvrir **MCP Server** et créer un serveur actif.
   - Code : `demo`
   - Allowed models : `res.partner,res.product.product`
   - Copier la clé API générée (>12 caractères).
2. Remplacer `API_KEY` par la clé ci-dessous.

---

## 1. Authentification invalide → 401

```bash
curl -i -X POST http://localhost:8069/mcp/demo/json \
  -H "Content-Type: application/json" \
  -d '{"tool":"search_res__partner","params":{"limit":1}}'
# attendu : {"error": "unauthorized"} avec code HTTP 401
```

## 2. Lecture paginée de partenaires

```bash
curl -s -X POST http://localhost:8069/mcp/demo/json \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tool":"search_res__partner","params":{"limit":2,"fields":["name","email"]}}'
# attendu : {"result":{"count":2,"records":[{"id":..,"name":..,"email":..}, ...]}}
```

## 3. Modèle non autorisé → erreur métier

```bash
curl -s -X POST http://localhost:8069/mcp/demo/json \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tool":"read_res__users","params":{"id":2}}'
# attendu : {"result":{"error":"model_not_allowed"}}
```

## 4. Masquage des champs sensibles

Créer un partenaire puis lire-le ; aucun champ contenant « token/secret/api_key »
ne doit apparaître en clair dans `records` (`***`).

```bash
curl -s -X POST http://localhost:8069/mcp/demo/json \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tool":"read_res__partner","params":{"id":<ID_PARTNER>}}'
```

## 5. Rate limiting → 429

Exécuter en boucle rapide (> max_requests_per_minute du serveur) :

```bash
for i in $(seq 1 70); do
  curl -o /dev/null -s -w "%{http_code}\n" -X POST \
    http://localhost:8069/mcp/demo/json \
    -H "Authorization: Bearer API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"tool":"search_res__partner","params":{"limit":1}}'
done
# attendu : une séquence de 200 puis des 429 {"error":"rate_limited"}
```

## 6. Journalisation

Menu *MCP → Logs* : chaque appel doit tracer tool, statut success/error,
temps de réponse ms, et les appels 429 doivent être absents du log métier
(refusés avant traitement).
