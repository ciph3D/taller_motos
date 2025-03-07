{
    'name': 'Taller de Motos',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestión de taller de motos',
    'description': """
        Módulo para gestionar un taller de motos
    """,
    'depends': ['base', 'contacts'],
    'data': [
        'security/security.xml',         # Añade esta línea para el archivo XML de seguridad
        'security/ir.model.access.csv',
        'views/partner_views.xml',
    ],
    'installable': True,
    'application': True,
}