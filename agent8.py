import cipi_iface as cp

q = {
1:"Apa yang biasa kamu lakukan untuk bersantai di akhir pekan?",
2:"Apa hobi atau kegiatan favoritmu yang selalu membuatmu merasa senang?",
3:"Apa makanan atau minuman kesukaanmu?",
4:"Apa yang kamu lakukan untuk menghilangkan stres setelah seharian bekerja?",
5:"Apa tempat favoritmu untuk liburan atau perjalanan?",
6:"Apa film atau acara TV favoritmu?",
7:"Apa yang biasanya kamu lakukan saat merasa bosan?",
8:"Apa hal terakhir yang membuatmu merasa sangat senang atau bangga?",
9:"Apa yang kamu pikirkan tentang musik dan genre favoritmu?",
10:"Apa kegiatan yang ingin kamu lakukan tapi belum sempat dilakukan?",
}

for i in q.values():
    print(i)

q = sorted(q, reverse=True)
