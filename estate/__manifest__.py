{
    'name':'Estate',
    'version':'LGPL-3',
    'depends':['base'],
    'application':True,
    'installable':True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_action.xml',
        'views/estate_offer_form.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv'
    ] 
}
