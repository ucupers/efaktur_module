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
        'views/faktur_keluaran_view.xml',
        'views/faktur_masukan_view.xml',
        'views/retur_faktur_keluaran_view.xml',
        'views/retur_faktur_masukan_view.xml',
        'views/faktur_menuitem.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'OEEL-1'
}