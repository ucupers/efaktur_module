from odoo import models, fields, _

class algoritma_pembelian(models.Model): # pembuatan tabel baru
    # nama tabelnya
    _name = 'algoritma.pembelian'

    # attribut yang ada pada tabel tersebut
    name = fields.Char(string='Name') # Char untuk String
    tanggal = fields.Date(string='Tanggal') # Date untuk milih tanggal
    # Selection untuk yang ada pilihannya
    status = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('done','Done')], default="draft")
    # One2many untuk data yang connect ke data lain (ex: ids terdiri dari beberapa id dari _line)
    algoritma_pembelian_ids = fields.One2many('algoritma.pembelian.line', 'algoritma_pembelian_id', string="Algoritma Pembelian Ids")
    # Algoritma_pembelian_brand_relation merupakan tabel relasi untuk many2many, alg_pemb_id untuk primary key alg_pembelian dan brand_id untuk primary key alg_brand
    brand_ids = fields.Many2many('algoritma.brand', 'algoritma_pembelian_brand_relation', 'algoritma_pembelian_id', 'brand_id', string="Brand Ids")

class algoritma_pembelian_line(models.Model):
    _name = "algoritma.pembelian.line"

    # Many2one untuk data yang dikumpulkan ke 1 model (ex: id di sini masuk ke ids)
    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="Algoritma Pembelian Id")
    product_id = fields.Many2one('product.product', string="Product Id")
    quantity = fields.Float(string="Quantity", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="Uom Id")

class algoritma_brand(models.Model):
    _name = "algoritma.brand"

    name = fields.Char(string="Name")