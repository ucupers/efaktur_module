headerjual1 = ['FK','"KD_JENIS_TRANSAKSI"','"FG_PENGGANTI"','"NOMOR_FAKTUR"','"MASA_PAJAK"','"TAHUN_PAJAK"','"TANGGAL_FAKTUR"','"NPWP"','"NAMA"','"ALAMAT_LENGKAP"','"JUMLAH_DPP"','"JUMLAH_PPN"','"JUMLAH_PPNBM"','"ID_KETERANGAN_TAMBAHAN"','"FG_UANG_MUKA"','"UANG_MUKA_DPP"','"UANG_MUKA_PPN"','"UANG_MUKA_PPNBM"','"REFERENSI"']
headerjual2 = ['LT','"NPWP"','"NAMA"','"JALAN"','"BLOK"','"NOMOR"','"RT"','"RW"','"KECAMATAN"','"KELURAHAN"','"KABUPATEN"','"PROPINSI"','"KODE_POS"','"NOMOR_TELEPON"']
headerjual3 = ['OF','"KODE_OBJEK"','"NAMA"','"HARGA_SATUAN"','"JUMLAH_BARANG"','"HARGA_TOTAL"','"DISKON"','"DPP"','"PPN"','"TARIF_PPNBM"','"PPNBM"']


# #"JUMLAH_PPN","JUMLAH_PPNBM","ID_KETERANGAN_TAMBAHAN","FG_UANG_MUKA","UANG_MUKA_DPP","UANG_MUKA_PPN","UANG_MUKA_PPNBM","REFERENSI"
# kd_jenis_transaksi = ''
# fg_pengganti = ''
# no_fraktur = ''
# masa_pajak = ''
# tahun_pajak = ''
# tanggal_faktur = ''
# npwp = ''
# alamat = ''
# dpp = ''
# ppn = ''
# ppnbm = ''
# id_ket_tambahan = ''
# fg_muka = ''
# muka_dpp = ''
# muka_ppn = ''
# muka_ppnbm = ''
# referensi = ''

# # saran saya dri pada bikin gini jadinya susah, bikin aja array
# arr_perusahaan_lwn = [] # 17 elemen termasuk kode FK
# arr_perusahaan_kt = [] # 14 elemen termasuk kode FAPR
# arr_produk = [] # 11 elemen termasuk kode OF


from odoo import http
from odoo.http import content_disposition, request
import io
import csv

class ReportCSVAlgoritmaPembelianController(http.Controller):
    @http.route('/efaktur/efaktur_csv', type='http', auth='user', csrf=False)
    def algoritma_pembelian_report_csv(self, **kwargs):
        data_ids = kwargs.get('id')

        # handle header dari httprequest
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/csv'),
                # Untuk nama filenya ditentukan di bawah ini (yg 'efaktur') 
                ('Content-Disposition', content_disposition('efaktur' + '.csv'))
            ]
        )
        

        # Buat object workbook dari library xlsxwriter
        output = io.StringIO()
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\r\n',quotechar = "'")

        # Write header
        csv_writer.writerow(headerjual1)
        csv_writer.writerow(headerjual2)
        csv_writer.writerow(headerjual3)

        # Looping algoritma pembelian yang dipilih
        if data_ids:
            id_list = data_ids.split(',')  # Split the comma-separated IDs into a list
            for data_id in id_list:
                # Retrieve the record algoritma pembelian using the ID
                datastring = []
                record_line = request.env['algoritma.pembelian.line'].search([('algoritma_pembelian_id', '=', int(data_id))])
                
                for line in record_line:
                    # Content / isi table
                    datastring = ['OF']
                    datastring.append('"'+str(line.product_id.display_name)+'"')
                    datastring.append('"'+str(line.description)+'"')
                    datastring.append('"'+str(line.quantity)+'"')
                    datastring.append('"'+str(line.uom_id.name)+'"')
                    datastring.append('"'+str(line.price)+'"')
                    datastring.append('"'+str(line.sub_total)+'"')
                    csv_writer.writerow(datastring)


        # for data in data_record:

        #     # Cari record data algoritma pembelian line yang dipilih user
        #     record_line = request.env['algoritma.pembelian.line'].search([('algoritma_pembelian_id', '=', data.id)])
        #     for line in record_line:
        #         # Content / isi table
        #         datastring = ['OF']
        #         datastring.append('"'+str(line.product_id.display_name)+'"')
        #         datastring.append('"'+str(line.description)+'"')
        #         datastring.append('"'+str(line.quantity)+'"')
        #         datastring.append('"'+str(line.uom_id.name)+'"')
        #         datastring.append('"'+str(line.price)+'"')
        #         datastring.append('"'+str(line.sub_total)+'"')
        #         csv_writer.writerow(datastring)
                
        
        # Memasukkan file excel yang sudah digenerate ke response dan return
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response