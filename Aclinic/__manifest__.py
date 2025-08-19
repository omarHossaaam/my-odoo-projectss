{
    'name': "Hospital Management System ",
    'summary': 'Diwan For Scientific Solution',
    'author': 'Omar Hossam',
    'category': '',
    'version': '0.0.1',
    'description': "",
    'depends': ['base', 'sale_management', 'account', 'purchase', 'mail', 'contacts',],
    'data': [
        'security/ir.model.access.csv',
        'views/Base_menu.xml',
        'views/hospital_doctor_view.xml',
        'views/hospital_patient.xml',
        'views/hospital_room_view.xml',
         'views/hospital_treatment.xml',
         'views/hospital_appointment.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': True,
}