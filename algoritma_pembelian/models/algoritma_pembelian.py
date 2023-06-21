from odoo import models, fields, _

class algoritma_pembelian(models.Model): # pembuatan tabel baru
    # nama tabelnya
    _name = 'algoritma.pembelian'

    # attribut yang ada pada tabel tersebut
    name = fields.Char(string='Name') # Char untuk String
    tanggal = fields.Date(string='Tanggal') # Date untuk milih tanggal
    # Selection untuk yang ada pilihannya
    status = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('done','Done')], default="draft")