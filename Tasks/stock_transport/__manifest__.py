{
    'name':'stock_transport',
    'version' : '1.0',
    'licence' : 'LGPL-3',
    'description':'Tranport Management System',
    'depends':['stock_picking_batch','fleet'],
    'data':[
        'views/fleet_list_view.xml',
        'views/batch_transfer_form.xml',
        'views/inventory_graph_view.xml',
        'views/inventory_gantt_view.xml',
        'views/transfer_view.xml',
        'securityir.model.access.csv',
    ],
    'installable' : True,
    'application' : True
}
