import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def property_api(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return request.make_json_response({
                "message": "property created"
            }, status=201)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def property_api_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                "message": "property created"
            }]

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        print(property_id)
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        return request.make_json_response({
            "message": "property updated"
        }, status=200)

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        if property_id:
            pass
        else:
            return request.make_json_response({
                "message": "property not found"
            }, status=404)
