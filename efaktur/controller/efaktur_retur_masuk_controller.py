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
    @http.route('/efaktur/efaktur_in_refund_csv', http='http', auth='user', csrf=False)
    def retur_keluar_report_csv(self, **kwargs):
        data_ids = kwargs.get('id')

        # handle header dari httprequest
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/csv'),
                # Untuk nama filenya ditentukan di bawah ini (yg 'efaktur') 
                ('Content-Disposition', content_disposition('retur_masuk_'+ str(date.today()).replace("-", "_") + '.csv'))
            ]
        )