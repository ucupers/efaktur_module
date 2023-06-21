from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class algoritma_pembelian(models.Model): # pembuatan tabel baru
    # nama tabelnya
    _name = 'algoritma.pembelian'

    def show_tree_view(self):
        tree_view_id = self.env['ir.model.data']._xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_tree_view_id')
        form_view_id = self.env['ir.model.data']._xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_form_view_id')
        domain = [('status', '=', 'draft')]
        result = {
            'name' : 'Pembelian B',
            'type' : 'ir.actions.act_window',
            'views' : [[tree_view_id, 'tree'], [form_view_id, 'form']],
            'target' : 'current',
            'res_model' : 'algoritma.pembelian',
            'domain' : domain,
            'limit' : 40
        }
        return result

    # Pembuatan Error Message (Raise)
    @api.model
    def create(self, values):
        res = super(algoritma_pembelian, self).create(values)
        for rec in res:
            tanggal_pembelian = rec.tanggal
            tanggal_skrng = date.today()
            if tanggal_pembelian < tanggal_skrng:
                raise ValidationError(_("Tanggal yang anda inputkan tidak boleh kurang dari tanggal sekarang"))
        return res
    
    def write(self, values):
        res = super(algoritma_pembelian, self).write(values)
        if 'tanggal' in values:
            tanggal_pembelian = self.tanggal
            tanggal_skrng = date.today()
            if tanggal_pembelian < tanggal_skrng:
                raise ValidationError(_("Tanggal yang anda inputkan tidak boleh kurang dari tanggal sekarang"))
        return res

    # Untuk button di form view
    def func_draft(self):
        self.status = 'draft'

    def func_to_approve(self):
        for line in self:
            line.status = 'to_approve'
            # Code untuk run sequence yang sudah dibuat
            if line.name == 'New':
                seq = line.env['ir.sequence'].next_by_code('algoritma.pembelian') or 'New'
                line.name = seq

    def func_approved(self):
        self.status = 'approved'

    def func_done(self):
        self.status = 'done'

    # attribut yang ada pada tabel tersebut
    name = fields.Char(string='Name', default="New") # Char untuk String
    tanggal = fields.Date(string='Tanggal') # Date untuk milih tanggal
    # Selection untuk yang ada pilihannya
    status = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('done','Done')], default="draft")
    # One2many untuk data yang connect ke data lain (ex: ids terdiri dari beberapa id dari _line)
    algoritma_pembelian_ids = fields.One2many('algoritma.pembelian.line', 'algoritma_pembelian_id', string="Algoritma Pembelian Ids")
    # Algoritma_pembelian_brand_relation merupakan tabel relasi untuk many2many, alg_pemb_id untuk primary key alg_pembelian dan brand_id untuk primary key alg_brand
    brand_ids = fields.Many2many('algoritma.brand', 'algoritma_pembelian_brand_relation', 'algoritma_pembelian_id', 'brand_id', string="Brand Ids")

class algoritma_pembelian_line(models.Model):
    _name = "algoritma.pembelian.line"

    # Onchange dipake jadi saat product_id nya berubah, terjadi sesuatu sesuai func yg suda didefinisikan
    @api.onchange('product_id')
    def func_onchange_product_id(self):
        if not self.product_id:
            return {}
        else:
            self.description = self.product_id.name
        return {}
    
    def _func_amount_total(self):
        for line in self:
            line.sub_total = line.quantity * line.price

    # membuat domain (hasil filter / search)
    def _func_domain_product_id(self):
        product_obj = self.env['product.product'].search([('type', '=', 'product')])
        domain = [('id', 'in', product_obj.ids)]
        return domain

    # Many2one untuk data yang dikumpulkan ke 1 model (ex: id di sini masuk ke ids)
    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="Algoritma Pembelian Id")
    # Domain -> jadi product_id yang muncul bakal hasil dari func domain aja
    # product_id = fields.Many2one('product.product', string="Product Id", domain=_func_domain_product_id)
    product_id = fields.Many2one('product.product', string="Product Id")
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity", default=0.0)
    price = fields.Float(string="Price", default=0.0)
    # Field compute digunakan untuk memberikan data tergantung data lainnya, menggunakan func yg sudah didefinisikan 
    sub_total = fields.Float(string="Sub Total", compute=_func_amount_total)
    uom_id = fields.Many2one('uom.uom', string="Uom Id")

class algoritma_brand(models.Model):
    _name = "algoritma.brand"

    name = fields.Char(string="Name")

# Class untuk wizard view / Pop-up view
class algoritma_pembelian_report_wizard(models.TransientModel):
    _name = "algoritma.pembelian.report.wizard"

    name = fields.Char(string="Name")
    periode_awal = fields.Date(string="Periode Awal")
    periode_akhir = fields.Date(string="Periode Akhir")

# Class untuk inheritance model
class product_template(models.Model):
    _inherit = 'product.template'

    def func_approved(self):
        if self.status == 'draft':
            self.status = 'approved'

    status = fields.Selection([('draft','Draft'),('approved','Approved'),('done','Done')], string="Status", default="draft")
