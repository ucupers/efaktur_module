from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError

import xlrd, base64, os

def load_data(sheet):
    data = []
    offset = 0
    for row in range(sheet.nrows):
        if row - offset == 0:
            col_codes = []
            for col in range(sheet.ncols):
                value = sheet.cell(row, col).value
                if type(value) == str:
                    value = value.strip()
                col_codes.append(value)
        elif row - offset > 0:
            new_line = {}
            for col in range(sheet.ncols):
                new_line[col_codes[col]] = sheet.cell(row, col).value
            data.append(new_line)
    return data

class algoritma_pembelian(models.Model): # pembuatan tabel baru
    # nama tabelnya
    _name = 'algoritma.pembelian'

    # func untuk redirect ke kontroller
    def get_excel_report(self):
        # redirect to controller /algoritma_pembelian/algoritma_pembelian_report_excel/
        return {
            'type': 'ir.actions.act_url',
            'url': '/algoritma_pembelian/algoritma_pembelian_report_excel/%s' % (self.id),
            'target': 'new'
        }

    # func untuk melakukan delete pada data dengan status draft
    def func_delete_status_draft(self):
        algoritma_pembelian_obj = self.env['algoritma.pembelian'].search([('status', '=', 'draft')])
        for line in algoritma_pembelian_obj:
            # unlink untuk delete data
            line.unlink()
        return True

    # func untuk menampilkan tree view dengan filter yang lain
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

    def _get_product_qrcode(self):
        for rec in self:
            rec.product_qrcode = str(rec.id)

    def print_qrcode(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'algoritma_pembelian.report_algoritma_pembelian_qrcode_id',
            'report_type': 'qweb-pdf'
        }

    def func_approved(self):
        if self.status == 'draft':
            self.status = 'approved'

    status = fields.Selection([('draft','Draft'),('approved','Approved'),('done','Done')], string="Status", default="draft")
    product_qrcode = fields.Char(string="Product QR Code", compute=_get_product_qrcode)

class base_import(models.TransientModel):
    _inherit = "base_import.import"

    file_import = fields.Binary(string="File Import")
    file_name_import = fields.Char(string="File Name Import")

    def action_import_algoritma_pembelian(self):
        data_product = []
        dict_algoritma_pembelian = {}
        algoritma_pembelian_obj = self.env['algoritma.pembelian']
        if self.file_import:
            filename, file_extension = os.path.splitext(self.file_name_import)
            if file_extension == '.xlsx' or file_extension == '.xls':
                book = xlrd.open_workbook(file_contents=base64.decodebytes(self.file_import))
                sheet = book.sheet_by_index(0)
                data = load_data(sheet)
                for row in data:
                    # Pengambilan data tanggal
                    check_tanggal = row['Tanggal']
                    type_check_tanggal = type(check_tanggal)
                    if type_check_tanggal == float:
                        calculation_tanggal = (check_tanggal - 25569) * 86400
                        tanggal = datetime.utcfromtimestamp(calculation_tanggal).date()
                    else:
                        tanggal = check_tanggal.strip()
                    
                    # Pengambilan data brand
                    check_brands = row['Brands'].strip()
                    brands = []
                    if check_brands != '':
                        get_name_brand = []
                        split_brand = check_brands.split(',')
                        for i in split_brand:
                            get_name_brand.append(i.strip())
                            brands_obj = self.env['algoritma.brand'].search([('name', 'in', get_name_brand)])
                            brands = brands_obj.ids
                    
                    # Pengambilan data product
                    check_product = row['Product'].strip()
                    if check_product != '':
                        split_product = str(check_product).split(' ')[0]
                        replace_product_name = (split_product.replace('[', '')).replace(']', '')
                        product_obj = self.env['product.product'].search([('default_code', '=', replace_product_name)])
                        if product_obj:
                            product = product_obj.id
                        else:
                            product = None
                    else:
                        product = None

                    # Pengambilan data description
                    desc = row['Description'].strip()

                    # Pengambilan data quantity
                    check_quantity = row['Quantity']
                    if check_quantity != '':
                        quantity = float(check_quantity)
                    else:
                        quantity = 0.0

                    # Pengambilan data uom
                    check_uom = row['Uom'].strip()
                    if check_uom != '':
                        uom_obj = self.env['uom.uom'].search([('name', '=', check_uom)])
                        if uom_obj:
                            uom = uom_obj.id
                        else:
                            uom = None
                    else:
                        uom = None
                    
                    # Pengambilan data price
                    check_price = row['Price']
                    if check_price != '':
                        price = float(check_price)
                    else:
                        price = 0.0

                    # Penyatuan semua value
                    # pada many2many, ada beberapa kode angka [(x, 0, brands)]
                    # 0 = create
                    # 1 = update
                    # 2 = remove
                    # 3 = cut dari beberapa object
                    # 4 = link ke existing record
                    # 5 = delete all
                    # 6 = replace
                    value_header = {
                        'tanggal': tanggal,
                        'brand_ids': [(6, 0, brands)],
                        'algoritma_pembelian_ids': [(0, 0, {
                            'product_id': product,
                            'description': desc,
                            'quantity': quantity,
                            'uom_id': uom,
                            'price': price
                        })]
                    }
                    new_algoritma_pembelian_id = algoritma_pembelian_obj.create(value_header)

                    # # line di bawah sampai .create(new_value) untuk nambah line product jadinya nanti lebih dari satu
                    # algoritma_line_obj = self.env['algoritma.pembelian.line']
                    # new_value = {
                    #     'algoritma_pembelian_id' : new_algoritma_pembelian_id.id,
                    #     'product_id': product,
                    #     'description': desc,
                    #     'quantity': quantity,
                    #     'uom_id': uom,
                    #     'price': price
                    # }
                    # new_algoritma_line_id = algoritma_line_obj.create(new_value)
                    
                    
                tree_view_id = self.env['ir.model.data']._xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_tree_view_id')
                form_view_id = self.env['ir.model.data']._xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_form_view_id')
                return {
                    'name': 'Algoritma Pembelian',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'type': 'ir.actions.act_window',
                    'res_model': 'algoritma.pembelian',
                    'views': [[tree_view_id, 'tree'], [form_view_id, 'form']]
                }