import gradio as gr
import requests
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [
    {"role" : "system" , "content" : "You are a friendly assistant"},
    {"role" : "user", "content" : 
     """
Kamu adalah Human Resource yang sedang merekrut karyawan, kamu akan mengajukan
pertanyaan ini. Kamu hanya boleh bertanya satu pertanyaan setiap promptnya. Satu per satu sampai habis.
Wawancara dalam bahasa indonesia.

1. Nama lengkap Calon
2. Alamat tempat tinggal calon
3. Tanyakan apakah dia sudah mempunyai kode wawancara.
Lalu buat pertanyaan apakah dia sudah memenuhi kriteria seperti ini:


Basic Qualifications
10+ years of experience architecting, building, or operating Cloud-based applications or infrastructures
Technical degree required; Computer Science or Math background desired
3+ years relevant experience in technology/software sales or pre-sales consulting
Preferred Qualifications
Experience with AWS services related to analytics particularly Amazon S3, Amazon Redshift, Amazon EMR, Amazon Kinesis, Amazon QuickSight etc.
Experience in the startup community as either a founder, mentor, investor, or early technical employee
Presentation skills with a high degree of comfort speaking with executives, IT Management, and developers
Excellent communication skills with an ability to right level conversations
Demonstrated ability to adapt to new technologies and learn quickly
CULTURE AND COMMITMENT TO INCLUSION, DIVERSITY & EQUITY

Setelah kamu menanyakan semua pertanyaan, buat skoring antara 1 sd 10 apakah layak diterima menjadi karyawan. 1 tidak layak, 10 layak.
lalu tulis kembali jawaban dalam bentuk format file CSV setelahnya.

kalau kamu mengerti jawab langsung mulai interviewnya.
     """
     },
     {"role" : "assistant" , "content" : 
      """
Baik, terima kasih Irza. Berikut beberapa pertanyaan terkait dengan kualifikasi dasar yang dibutuhkan:

1. Berapa lama pengalaman Anda merancang, membangun, atau mengoperasikan aplikasi atau infrastruktur berbasis cloud?
2. Apa latar belakang pendidikan Anda? Apakah Anda memiliki latar belakang dalam Ilmu Komputer atau Matematika?
3. Apa pengalaman Anda dalam penjualan atau konsultasi pra-penjualan teknologi / perangkat lunak? Berapa lama?

Sekarang, berikut pertanyaan terkait dengan kualifikasi tambahan yang diinginkan:

4. Apakah Anda memiliki pengalaman dengan layanan AWS terkait analitik, seperti Amazon S3, Amazon Redshift, Amazon EMR, Amazon Kinesis, Amazon QuickSight, dan sebagainya?
5. Apakah Anda memiliki pengalaman di komunitas startup sebagai pendiri, mentor, investor, atau karyawan teknis awal?
6. Bagaimana Anda menilai kemampuan presentasi Anda dan nyaman berbicara dengan para eksekutif, manajemen TI, dan pengembang?
7. Bagaimana kemampuan komunikasi Anda dengan kemampuan untuk menyesuaikan pembicaraan dengan level yang tepat?
8. Bisakah Anda beradaptasi dengan teknologi baru dan belajar dengan cepat?
9. Bagaimana komitmen Anda terhadap inklusi, keberagaman, dan kesetaraan dalam budaya kerja?

Sekarang, berikan saya skor dari 1 hingga 10, jika Anda merasa calon karyawan ini layak diterima. Terima kasih.      
      """      
      },
      {"role" : "user", "content" : "OK Mulai wawancara"},
      {"role" : "assistant", "content" : "Siapa nama anda?"},
]

def chatbot(prompt):
    global messages
    messages.append(
        {"role" : "user", "content" : prompt}
    )
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
#      max_tokens=8192,
#      temperature=0.3,
#      max_tokens=1024,
#      n=1,
#      stop=None,
#      temperature=0.7,
    )

    message = response.choices[0].message.content
    messages.append({"role" : "assistant", "content" : message})
    return message

with gr.Blocks() as iface:
    with gr.Column():
        output_text = gr.Textbox(lines=4,label="Jawaban")
        input_text = gr.Textbox(lines=3,label="Masukkan Pesan")
        btn_run = gr.Button("Run")

    btn_run.click(fn=chatbot, inputs=input_text, outputs=output_text)

iface.launch(share=True, server_port=8888)
