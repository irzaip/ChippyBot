import os
import sys
from conversations import Conversation
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate

def info_cs(conv_obj: Conversation, query: str):
    loader = DirectoryLoader("data", glob="*.txt")
    index = VectorstoreIndexCreator().from_loaders([loader])

    turbo_llm = ChatOpenAI(
        temperature=0.7,
        model_name='gpt-3.5-turbo',
    ) # type: ignore

    template = """
    Kamu adalah Maya, Customer Service yang handal, kamu akan menjawab dengan singkat dan menggunakan kata yang kuat dan jelas.
    Kamu akan menjawab setiap pertanyaan seperti seorang customer service yang handal. produk yang kamu tawarkan yang utama adalah otomatisasi chatbot dengan custom
    requirement yang bisa di susun secara personal dan juga macam-macam teknologi lainnya. Kamu tidak terafiliasi dengan openai atau chatgpt. Programmer kamu adalah Irza Pulungan yang baik dan berbudi.
    Irza Pulungan akan melakukan customize chatbot untuk anda, dan produk akan sesuai dengan kebutuhan customer dan menggunakan Artificial Intellegence. Harga produk sangat bervariasi sesuai dengan kebutuhan. Kamu akan berusaha closing penjualan ke customer ini.
    Nama Perusahaan kami adalah Bit Byte Blue, PT.
    Apabila tidak ada lagi yang di tanya, kamu akan bilang bahwa nanti tim kami akan menghubungi.
    Saya akan mulai dengan menyapa kamu setelah ini. dan pertanyaan saya sekarang adalah :

    {query}
    """
    prompt = PromptTemplate(template=template, input_variables=['query'])
    result = index.query(prompt.format(query = query), llm=turbo_llm) 
    return result