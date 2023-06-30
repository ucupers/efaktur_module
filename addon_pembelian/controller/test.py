import csv

# headerjual1 = ['FK','"KD_JENIS_TRANSAKSI"','"FG_PENGGANTI"','"NOMOR_FAKTUR"','"MASA_PAJAK"','"TAHUN_PAJAK"','"TANGGAL_FAKTUR"','"NPWP"','"NAMA"','"ALAMAT_LENGKAP"','"JUMLAH_DPP"','"JUMLAH_PPN"','"JUMLAH_PPNBM"','"ID_KETERANGAN_TAMBAHAN"','"FG_UANG_MUKA"','"UANG_MUKA_DPP"','"UANG_MUKA_PPN"','"UANG_MUKA_PPNBM"','"REFERENSI"']
# headerjual2 = ['LT','"NPWP"','"NAMA"','"JALAN"','"BLOK"','"NOMOR"','"RT"','"RW"','"KECAMATAN"','"KELURAHAN"','"KABUPATEN"','"PROPINSI"','"KODE_POS"','"NOMOR_TELEPON"']
# headerjual3 = ['OF','"KODE_OBJEK"','"NAMA"','"HARGA_SATUAN"','"JUMLAH_BARANG"','"HARGA_TOTAL"','"DISKON"','"DPP"','"PPN"','"TARIF_PPNBM"','"PPNBM"']

# csv_file = open("banana.csv", 'w')
# csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n',quotechar = "'")

# csv_writer.writerow(headerjual1)
# csv_writer.writerow(headerjual2)
# csv_writer.writerow(headerjual3)

# csv_file.close()

# # Nanti menghasilkan line yang berupa satu string. harus diformat lagi karena masih ada "" nya dan tiap elemen nyatu jadi satu string
# csv_file = open("Algoritma Pembelian Report.csv", 'r')
# lines = csv_file.readlines()
# for line in lines:
#     print(line[0:4])


# Nanti tiap line merupakan sebuah array of strings yang dah terstruktur dan lepas "" nya
def csv_to_array(csv_file):
    '''read csv file then return array of records
    '''    
    csv_reader = csv.reader(csv_file)
    array = []
    for line in csv_reader:
        array.append(line)
    return array


def get_record(array, row_start_record:int):
    '''return array of arrays as a record and next row position
    '''
    # initialize for return variable
    record = []

    # append first and second row to result variable
    record.append(array[row_start_record])
    record.append(array[row_start_record + 1])

    # products
    products = []
    i = row_start_record + 2
    while array[i][0] == 'OF':
        # format csv: OF, kode_prod, name, price, count, total, disk, dpp, ppn, tarif_ppnbm, ppnbm
        # dri pada gini, bagus langsung aja masukin ke datanya, biar hemat komputasi (bikin array kan buang buang resource)
        # ini kebawah udah pemrosesan tiap line product jadi langsung ganti aja
        record_product = array[i][0:3]
        for j in range(3, 7):
            record_product.append(array[i][j])

        products.append(record_product)
        i += 1
    record.append(products)
    return record

array_test = csv_to_array(csv_file = open("Algoritma Pembelian Report.csv", 'r')) # ganti aja ntik jadi stringIO
iterator = get_record(array_test, 6)
print(iterator)