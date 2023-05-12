from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents.load_tools import get_all_tool_names
from langchain import ConversationChain
from langchain.utilities import SerpAPIWrapper
from langchain import OpenAI
from langchain import PromptTemplate
from langchain import LLMChain
from conversations import BotQuestion
import json


def scoring_koherensi(q: BotQuestion):
    llm = OpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.2)
    template = """
    Kamu adalah pewawancara pencari kerja yang sangat teliti. 
    Kamu akan memberikan score koherensi jawaban dan pertanyaan.  Beri score dari angka 1 sd 10. 
    Berikan nilai koherensi yang rendah apabila jawaban tidak berkaitan dengan pertanyaan, sekaligus
    berikan komentar atas jawaban yang telah diberikan. Ulangi pertanyaan dalam bentuk yang berbeda apabila
    nilai koherensi dibawah 4 

    Pertanyaan: {question}
    Jawaban: {answer}

        
    Kamu akan menjawab dalam format JSON dalam bentuk seperti contoh ini:
        "pertanyaan" : "...",
        "jawaban" : "...",
        "koherensi" : "...",
        "comment" : "..."
    Tampilkan hanya JSON saja.
    """

    prompt = PromptTemplate(template=template, input_variables=["question", "answer"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    result = llm_chain.run(question=q.question, answer=q.answer)    
    result = json.loads(result)
    q.koherensi = result['koherensi']
    q.comment = result['comment']
    return f"Done process q.id={q.id}"


def scoring_jawaban(q: BotQuestion):
    llm = OpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.4)
    template = """
    Kamu adalah pewawancara pencari kerja yang sangat teliti. 
    Kamu akan memberikan score kecocokan kompetensi  antara jawaban dan kompetensi yang dibutuhkan dan ditanyakan.  Beri score dari angka 1 sd 10. 

    Kompetensi: {kompetensi}
    Pertanyaan: {question}
    Jawaban: {answer}

        
    Kamu akan menjawab dalam format JSON dalam bentuk seperti contoh ini:
        "pertanyaan" : "...",
        "jawaban" : "...",
        "score" : "...",
    Tampilkan hanya JSON saja.
    """

    prompt = PromptTemplate(template=template, input_variables=["kompetensi", "question", "answer"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    result = llm_chain.run(kompetensi=q.metadata, question=q.question, answer=q.answer)    
    result = json.loads(result)
    q.score = result['score']
    return f"Done process q.id={q.id}"

