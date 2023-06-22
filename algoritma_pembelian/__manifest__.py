{
    'name' : 'Module E-Faktur',
    'version' : '1.0.0',
    'category' : 'Tax',
    'summary' : 'Module E-Faktur',
    'description' : """
        Ini adalah module addons untuk connect ke E-Faktur
    """,
    'author' : 'Ryu & Raihan',
    'depends' : ['web', 'base', 'product', 'stock'], # depends dipake buat pake module laen di modul ini
    'data' : [
        'security/ir.model.access.csv',
        'views/algoritma_pembelian_view.xml',
        'views/algoritma_pembelian_action.xml',
        'views/algoritma_pembelian_menuitem.xml',
        'views/algoritma_pembelian_sequence.xml',
        'views/algoritma_pembelian_cron.xml',
        'reports/algoritma_pembelian_qweb.xml',
        'reports/algoritma_pembelian_qrcode.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'OEEL-1'
}