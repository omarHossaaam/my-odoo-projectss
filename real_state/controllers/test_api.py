from odoo import http


class TestApi(http.Controller):

    @http.route("/api/test", method=["Get"], type="http", auth="none", csrf=False)
    def test_endpoint(self):
        print("inside test_endpoint method")
