from odoo import http
from odoo.http import request
import json
import time
from werkzeug.exceptions import Unauthorized


class McpController(http.Controller):

    def _check_auth(self, server, headers):
        expected = 'Bearer %s' % server.api_key
        auth = headers.get('Authorization', '')
        if auth != expected:
            raise Unauthorized('Invalid API key')

    def _list_models(self, server):
        return server.get_model_list()

    def _search(self, server, model, kwargs):
        if not server.is_model_allowed(model):
            return {'error': 'model_not_allowed'}
        Model = request.env[model].sudo()
        domain = []
        domain = self._build_domain(Model, kwargs)
        limit = int(kwargs.get('limit', 10))
        fields_ = kwargs.get('fields')
        recs = Model.search(domain, limit=limit)
        return {
            'count': len(recs),
            'records': recs.read(fields_) if fields_ else recs.read(),
        }

    def _build_domain(self, Model, kwargs):
        domain = []
        for key, value in kwargs.items():
            if key in ('limit', 'fields', 'order'):
                continue
            if Model._fields.get(key):
                domain.append((key, '=', value))
        return domain

    def _read(self, server, model, id_):
        if not server.is_model_allowed(model):
            return {'error': 'model_not_allowed'}
        Model = request.env[model].sudo()
        rec = Model.browse(int(id_))
        return rec.read() if rec.exists() else {'error': 'record_not_found'}

    def _handle_tool(self, server, name, params):
        parts = name.split('_')
        if len(parts) >= 2 and parts[0] in ('read', 'search'):
            action, model = parts[0], parts[1]
        else:
            return {'error': 'unknown_tool'}
        if action == 'read':
            return self._read(server, model, params.get('id'))
        return self._search(server, model, params)

    @http.route('/mcp/<code>/json', type='http', auth='public', methods=['POST'], csrf=False)
    def mcp_json(self, code, **kw):
        server = request.env['mcp.server'].sudo().search([('code', '=', code), ('active', '=', True)], limit=1)
        if not server:
            return request.make_response(json.dumps({'error': 'server_not_found'}), [('Content-Type', 'application/json')])
        try:
            self._check_auth(server, request.httprequest.headers)
        except Unauthorized:
            return request.make_response(json.dumps({'error': 'unauthorized'}), [('Content-Type', 'application/json')], 401)

        start = time.time()
        try:
            payload = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return request.make_response(json.dumps({'error': 'invalid_json'}), [('Content-Type', 'application/json')])
        result = self._handle_tool(server, payload.get('tool', ''), payload.get('params', {}))
        elapsed = int((time.time() - start) * 1000)
        request.env['mcp.request.log'].sudo().create({
            'server_id': server.id,
            'tool': payload.get('tool'),
            'params': json.dumps(payload.get('params', {})),
            'result': json.dumps(result)[:2000],
            'status': 'error' if isinstance(result, dict) and result.get('error') else 'success',
            'response_ms': elapsed,
        })
        return request.make_response(json.dumps({'result': result}), [('Content-Type', 'application/json')])
