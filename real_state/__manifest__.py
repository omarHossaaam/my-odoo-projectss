{
    'name': "Real State",
    'summary': 'Diwan For Scientific Solution',
    'author': 'Omar hossam',
    'category': '',
    'version': '0.0.1',
    'description': "",
    'depends': ['base', 'sale_management', 'account', 'purchase', 'mail', 'contacts', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/data.xml',
        'views/Base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/sale_order_view.xml',
        'views/tag_view.xml',
        'views/building_view.xml',
        'reports/property_report.xml',
        'wizard/change_state_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'real_state/static/src/css/property.css',
            'real_state/static/src/components/listView/listView.css',
            'real_state/static/src/components/listView/listView.js',
            'real_state/static/src/components/listView/listView.xml',

        ],
    },
    'application': True,
    'installable': True,
}
