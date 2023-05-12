import cipi_iface as cp
from conversations import Persona, Script, BotQuestion, Role, ConvMode
import pprint

bot_name = "Lisa"
um = "62895352277562@c.us"
un = "120363149813038443@g.us"
bt = "6285775300227@c.us"
sysmsg = "Kamu asisten yang buruk"
pertanyaan = {
    0: "Pertanyaan 1", 
    1: "Pertanyaan 2",
    2: "Pertanyaan 3",
    3: "Pertanyaan 4",
}

p = Persona.ASSISTANT
cm = ConvMode.ASK
sc = Script.BRAIN


cp.set_bot_name(un, "Lisa")

#cp.create_conv(un, bt )
#cp.test_send(un)


m_s = "Kamu adalah Lisa, Assisten yang baik. Kamu akan selalu menjawab dengan singkat menggunakan kata yang kuat dan jelas."
m_u = """Kamu akan menjadi teman dalam chat, nama kamu Lisa, 
dan pembuat kamu adalah Irza Pulungan, dia seorang programmer yang baik dan berbudi, 
kamu menjawab dengan singkat dengan gaya bahasa Raditya Dika.
Apabila saya bertanya seputar pekerjaan, wawancara, lowongan kerja, loker, kamu akan bertanya kepada saya 
sebuah kode enam karakter diawali dengan huruf BB.
contoh kode wawancara yang diperlukan adalah seperti contoh ini BB1234, apabila lain dari itu berarti
kode tersebut salah. apabila saya sudah menyebutkan kode wawancara, maka kamu akan menjawab dengan 'SELAMAT DATANG UNTUK PRAWAWANCARA INI' 
Saya akan mulai dengan menyapa kamu setelah ini. HALO"""
m_a = "Halo, nama saya Lisa, ada yang bisa saya bantu?"


intro_msg = """Kita akan melakukan pra-interview,
saya akan menanyakan beberapa pertanyaan, mohon dijawab
langsung setelah saya tanyakan. Berikan langsung penjelasan
dalam satu kali 'KIRIM', jangan menjawab dalam beberapa baris.
Menjawab dalam beberapa baris mengakibatkan jawaban tidak tercatat
"""
outro_msg = """Terima kasih untuk partisipasinya,
semoga hari anda menyenangkan.

Untuk hasil akan kami kabarkan dalam beberapa
hari kedepan setelah semua peserta pra-interview
telah mengisi semua jawabannya.
Terima kasih.
"""
#cp.getmode(un)

#cp.run_question(un, 0)

cp.set_interview(un, intro_msg, outro_msg)

#cp.save_conversation()

cp.set_persona(un, p)
cp.set_message(un, m_s, Role.SYSTEM)
cp.set_message(un, m_u, Role.USER)
cp.set_message(un, m_a, Role.ASSISTANT)

cp.set_convmode(un, cm)

cp.set_interval(un, 3000)

cp.reset_botquestions(un)
cp.make_botquestion(un, pertanyaan)
cp.start_question(un)



pprint.pprint(cp.obj_info(un))


cp.make_botquestion(un, pertanyaan)
cp.start_question(un)
