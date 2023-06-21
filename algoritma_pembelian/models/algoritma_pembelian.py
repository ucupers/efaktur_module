from odoo import models, fields, _

class algoritma_pembelian(models.Model): # pembuatan tabel baru
    # nama tabelnya
    _name = 'algoritma.pembelian'

    # attribut yang ada pada tabel tersebut
    name = fields.Char(string='Name') # Char untuk String
    tanggal = fields.Date(string='Tanggal') # Date untuk milih tanggal
    # Selection untuk yang ada pilihannya
    status = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('done','Done')], default="draft")
    algoritma_pembelian_ids = fields.One2many('algoritma.pembelian.line', 'algoritma_pembelian_id', string="Algoritma Pembelian Ids")

class algoritma_pembelian_line(models.Model):
    _name = "algoritma.pembelian.line"

    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="Algoritma Pembelian Id")
    product_id = fields.Many2one('product.product', string="Product Id")
    quantity = fields.Float(string="Quantity", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="Uom Id")
