def count_words(text):
    # Count the number of words in the input text
    num_words = len(text.split())

    # Truncate the input text to a maximum of 5000 characters
    if len(text) > 100:
        text = text[:100]
        # Find the index where the text is cut
        last_word_index = text.rfind(' ')
        return f'{num_words} words, truncated at index {last_word_index}'
    else:
        return f'{num_words} words'

# Example usage
input_text = """
    Bertindak sebagai Pakar Twitter, Penyalin, dan Penulis Hantu. Tulis 3 versi pengait utas tentang 
    Ini adalah topiknya. [[Tulis nada suara yang lucu]]. Menggunakan 2 kalimat. Hindari hastag .. 
    Gunakan sebagai referensi kalimat-kalimat berikut (setiap baris adalah utas yang berbeda): 
    Enam utas untuk menguasai pemasaran: 
    Saya telah melakukan copywriting untuk 100-an halaman arahan dan halaman beranda.  
    Berikut adalah 10 tips copywriting halaman arahan untuk lebih banyak konversi:
    Saya telah menjelajahi lebih dari seribu laman landas.  Inilah cara membuat milik Anda lebih baik:
    17 kiat untuk copywriting yang hebat: 
    Anak-anak berusia 16 tahun menghasilkan $300.000/bulan dengan alat tanpa kode.  
    Mereka secara harfiah membangun mesin pencetak uang.  
    Berikut adalah 8 alat gratis untuk mulai mencetak uang di internet:
    ChatGPT adalah karyawan GRATIS.  Tetapi kebanyakan orang tidak tahu cara membuka potensi penuhnya.  Berikut adalah 10 utas di ChatGPT yang akan menghemat ribuan jam di tahun 2023:
    Anak berusia 21 tahun menghasilkan $ 125.000/bulan hanya dengan menggunakan tanpa kode.  
    Mereka benar-benar mencetak uang dari udara.  
    Berikut adalah 125 alat tanpa kode gratis untuk membuat mesin pencetak uang Anda berikutnya:
    ChatGPT adalah masa depan.  Tetapi kebanyakan orang terjebak pada tingkat pemula.  
    Berikut ini adalah 75 utas ChatGPT yang akan membuat Anda menjadi ahli dalam 3 hari: (Tandai ini untuk nanti)
    Bisnis satu orang saya menghasilkan pendapatan $ 169 ribu / bulan.  Biaya yang saya keluarkan adalah $623/bulan + 2,9% untuk menjalankannya.  Berikut adalah 11 alat tanpa kode dalam tumpukan teknologi saya: 🧵
    Twitter membenci LinkedIn.  Tapi saya akan menghasilkan 130 juta tayangan & $1,4 juta di platform 
    ini pada tahun 2022.   Inilah cara saya menggunakan LinkedIn tidak seperti orang lain: 🧵
"""

output = count_words(input_text)
print(output)

i = input_text.split(" ")
print(i[0:93])