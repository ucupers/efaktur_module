from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import float_round, float_repr
from datetime import date
import io
import csv

# Header faktur
FK_HEADER_FAKTUR_KELUAR = ["FK","KD_JENIS_TRANSAKSI","FG_PENGGANTI","NOMOR_FAKTUR","MASA_PAJAK","TAHUN_PAJAK","TANGGAL_FAKTUR","NPWP","NAMA","ALAMAT_LENGKAP","JUMLAH_DPP","JUMLAH_PPN","JUMLAH_PPNBM","ID_KETERANGAN_TAMBAHAN","FG_UANG_MUKA","UANG_MUKA_DPP","UANG_MUKA_PPN","UANG_MUKA_PPNBM","REFERENSI"]
LT_HEADER_FAKTUR_KELUAR = ["LT","NPWP","NAMA","JALAN","BLOK","NOMOR","RT","RW","KECAMATAN","KELURAHAN","KABUPATEN","PROPINSI","KODE_POS","NOMOR_TELEPON"]
OF_HEADER_FAKTUR_KELUAR = ["OF","KODE_OBJEK","NAMA","HARGA_SATUAN","JUMLAH_BARANG","HARGA_TOTAL","DISKON","DPP","PPN","TARIF_PPNBM","PPNBM"]
FM_HEADER_FAKTUR_MASUK = ["FM","KD_JENIS_TRANSAKSI","FG_PENGGANTI","NOMOR_FAKTUR","MASA_PAJAK","TAHUN_PAJAK","TANGGAL_FAKTUR","NPWP","NAMA","ALAMAT_LENGKAP","JUMLAH_DPP","JUMLAH_PPN","JUMLAH_PPNBM","IS_CREDITABLE"]
RK_HEADER_RETUR_KELUAR = ["RK","NPWP","NAMA","KD_JENIS_TRANSAKSI","FG_PENGGANTI","NOMOR_FAKTUR","TANGGAL_FAKTUR","NOMOR_DOKUMEN_RETUR","TANGGAL_RETUR","MASA_PAJAK_RETUR","TAHUN_PAJAK_RETUR","NILAI_RETUR_DPP","NILAI_RETUR_PPN","NILAI_RETUR_PPNBM"]
RM_HEADER_RETUR_MASUK = ["RM","NPWP","NAMA","KD_JENIS_TRANSAKSI","FG_PENGGANTI","NOMOR_FAKTUR","TANGGAL_FAKTUR","IS_CREDITABLE","NOMOR_DOKUMEN_RETUR","TANGGAL_RETUR","MASA_PAJAK_RETUR","TAHUN_PAJAK_RETUR","NILAI_RETUR_DPP","NILAI_RETUR_PPN","NILAI_RETUR_PPNBM"]

class ReportCSVEfakturKeluaranController(http.Controller):
    @http.route('/efaktur/efaktur_out_invoice_csv', type='http', auth='user', csrf=False)
    def efaktur_keluar_report_csv(self, **kwargs):
        data_ids = kwargs.get('id')

        # handle header dari httprequest
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/csv'),
                # Untuk nama filenya ditentukan di bawah ini (yg 'efaktur') 
                ('Content-Disposition', content_disposition('efaktur_keluar_'+ str(date.today()).replace("-", "_") + '.csv'))
            ]
        )

        # Prepare output variable to store content
        output = io.StringIO()
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n',quotechar = "'")
        
        # write header
        csv_writer.writerow(FK_HEADER_FAKTUR_KELUAR)
        csv_writer.writerow(LT_HEADER_FAKTUR_KELUAR)
        csv_writer.writerow(OF_HEADER_FAKTUR_KELUAR)

        # loop to process each data from each id
        if data_ids: # check if data_ids not empty
            id_list = data_ids.split(',')  # Split the comma-separated IDs into a list
            
            for data_id in id_list:
                datafk = {}
                datalt = {}

                # Retrieve the record using the ID (in odoo, invoices and others stored in 1 table, account_move)
                move = request.env['account.move'].search([('id', '=', int(data_id))])

                # taken from efaktur module, aight temporary spam kopas
                # FK line
                datafk['FK'] = '"FK"'
                datafk['KD_JENIS_TRANSAKSI'] = '"' + str(move.l10n_id_tax_number[0:2] or 0) + '"'
                datafk['FG_PENGGANTI'] = '"' + str(move.l10n_id_tax_number[2:3] or 0) + '"'
                datafk['NOMOR_FAKTUR'] = '"' + str(move.l10n_id_tax_number[3:] or 0) + '"'
                datafk['MASA_PAJAK'] = '"' + str(move.invoice_date.month) + '"'
                datafk['TAHUN_PAJAK'] = '"' + str(move.invoice_date.year) + '"'
                datafk['TANGGAL_FAKTUR'] = '"' + str('{0}/{1}/{2}'.format(move.invoice_date.day, move.invoice_date.month, move.invoice_date.year)) + '"'
                datafk['NPWP'] = '"' + str(move.partner_id.vat) + '"'
                datafk['NAMA'] =  '"' + str(move.partner_id.name if datafk['NPWP'] == '000000000000000' else move.partner_id.l10n_id_tax_name or move.partner_id.name) + '"'
                datafk['ALAMAT_LENGKAP'] = '"' + str(move.partner_id.contact_address.replace('\n', '') if datafk['NPWP'] == '000000000000000' else move.partner_id.l10n_id_tax_address or move.partner_id.street) + '"'
                datafk['JUMLAH_DPP'] = '"' + str(int(float_round(move.amount_untaxed, 0))) + '"' # currency rounded to the unit
                datafk['JUMLAH_PPN'] = '"' + str(int(float_round(move.amount_tax, 0, rounding_method="DOWN"))) + '"'  # tax amount ALWAYS rounded down
                datafk['JUMLAH_PPNBM'] = '"0"'
                datafk['ID_KETERANGAN_TAMBAHAN'] = '"' + str('1' if move.l10n_id_kode_transaksi == '07' else '') + '"'
                datafk['FG_UANG_MUKA'] = '"0"'
                datafk['UANG_MUKA_DPP'] = '"0"'
                datafk['UANG_MUKA_PPN'] ='"0"'
                datafk['UANG_MUKA_PPNBM'] = '"0"'
                datafk['REFERENSI'] = '""'
                
                # LT Line
                company_id = move.company_id.id
                current_company = request.env['res.company'].search([('id', '=', str(company_id))])
                
                datalt['LT'] = '"FAPR"'
                datalt['NPWP'] = '"' + str(current_company.vat) + '"'
                datalt['NAMA'] = '"' + str(current_company.name) + '"'
                datalt['JALAN'] = '"' + str(current_company.street) + '"'
                datalt['BLOK'] = '""'
                datalt['NOMOR'] = '""'
                datalt['RT'] = '""'
                datalt['RW'] = '""'
                datalt['KECAMATAN'] = '""'
                datalt['KELURAHAN'] = '""'
                datalt['KABUPATEN'] = '"' + str(current_company.city) + '"'
                datalt['PROPINSI'] = '"' + str(current_company.state_id.name) + '"'
                datalt['KODE_POS'] = '"' + str(current_company.zip) + '"'
                datalt['NOMOR_TELEPON'] = '"' + str(current_company.phone) + '"'
                
                csv_writer.writerow(datafk.values())
                csv_writer.writerow(datalt.values())
                
                # OF Lines
                for line in move.line_ids.filtered(lambda l: l.display_type == 'product'):
                    decimal_places = current_company.currency_id.decimal_places
                    # discount = 1 - (line.discount / 100)
                    total_price = line.quantity * line.price_unit

                    dataof = {}
                    dataof['OF'] = '"OF"'
                    dataof['KODE_OBJEK'] = '"' + str(line.product_id.default_code or '') + '"'
                    dataof['NAMA'] = '"' + str(line.product_id.name or '') + '"'
                    dataof['HARGA_SATUAN'] = '"' + str(float_repr(float_round(line.price_unit, decimal_places), decimal_places)) + '"'
                    dataof['JUMLAH_BARANG'] = '"' + str(line.quantity) + '"'
                    dataof['HARGA_TOTAL'] = '"' + str(float_repr(float_round(total_price, decimal_places), decimal_places)) + '"'
                    dataof['DISKON'] = '"' + str(line.discount) + '"'
                    dataof['DPP'] = '"' + str(float_round(line.price_subtotal, decimal_places)) + '"'
                    dataof['PPN'] = '"' + str(float_round(line.price_total - line.price_subtotal, decimal_places)) + '"'
                    dataof['TARIF_PPNBM'] = '"0"'
                    dataof['PPNBM'] = '"0"'
                    csv_writer.writerow(dataof.values())
        
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response
