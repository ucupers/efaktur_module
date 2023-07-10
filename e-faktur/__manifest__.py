{
    'name' : 'e-Faktur Indonesia',
    'version' : '1.0.0',
    'category' : 'Tax',
    'summary' : 'e-Faktur Indonesia',
    'description' : """
        Ini merupakan add-on yang akan menambahkan menu e-Faktur pada app Invoice untuk menambah beberapa fitur
        seperti export CSV untuk di-import ke aplikasi e-Faktur milik pemerintah.
    """,
    'author' : 'Ryu & Raihan',
    'depends' : ['l10n_id_efaktur'],
    'data' : [
        'security/ir.model.access.csv',
        'views/algoritma_pembelian_view.xml',
        'views/algoritma_pembelian_action.xml',
        'views/algoritma_pembelian_menuitem.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'OEEL-1'
}