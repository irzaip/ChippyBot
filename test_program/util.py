
def terbilang(angka):
    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan']
    belasan = ['sepuluh', 'sebelas', 'dua belas', 'tiga belas', 'empat belas', 'lima belas', 'enam belas', 'tujuh belas', 'delapan belas', 'sembilan belas']
    puluhan = ['', 'sepuluh', 'dua puluh', 'tiga puluh', 'empat puluh', 'lima puluh', 'enam puluh', 'tujuh puluh', 'delapan puluh', 'sembilan puluh']
    
    if angka < 0:
        return 'minus ' + terbilang(abs(angka))
    
    if angka < 10:
        return satuan[angka]
    
    if angka < 20:
        return belasan[angka-10]
    
    if angka < 100:
        return puluhan[angka//10] + ' ' + satuan[angka%10]
    
    if angka < 1000:
        return satuan[angka//100] + ' ratus ' + terbilang(angka%100)
    
    if angka < 1000000:
        return terbilang(angka//1000) + ' ribu ' + terbilang(angka%1000)
    
    if angka < 1000000000:
        return terbilang(angka//1000000) + ' juta ' + terbilang(angka%1000000)
    
    return 'nilai terlalu besar'

angka = int(input('Masukkan angka: '))
print(terbilang(angka))
