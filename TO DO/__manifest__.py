{
    'name': "Todo App",
    'summary': 'Diwan For Scientific Solution',
    'author': 'Omar hossam',
    'category': '',
    'version': '0.0.1',
    'description': "",
    'depends': ['base', 'sale_management', 'account', 'purchase', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
    ],
    'assets': {
    },
    'application': True,
    'installable': True,
}
