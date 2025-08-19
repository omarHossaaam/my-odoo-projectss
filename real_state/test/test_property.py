from odoo.tests.common import Transactioncase


class TestProperty(Transactioncase):
    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref': 'PRT1000',
            'name': 'Property 1000',
            'postcode': '1010',
            'expected_price': 10000,
        })

    def test_01_property_values(self):
        property_id = self.property_01_record
        self.assertRecordValues(property_id, [{
            'ref': 'PRT1000',
            'name': 'Property 1000',
            'postcode': '1010',
            'expected_price': 10000,
        }])
