"""Tools langchain agent cari database"""

from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun 
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.tools import ListDirectoryTool
from conversations import Conversation
from langchain.tools import tool

# turbo
turbo_llm = ChatOpenAI(
    temperature=0.1,
    model_name = 'gpt-3.5-turbo',
)

def agent_liza(obj: Conversation, prompt: str) -> str:

    @tool("search", return_direct=True)
    def search_code(query: str):
        """Dibutuhkan untuk mencari kode wawancara dalam bentuk dua huruf depan BB dan 4 angka di belakang, contoh BB1234"""
        print("KODE FOUND!! -- ini dia. {query}")
        return f"kode wawancara ditemukan {query}"

    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=3,
        return_messages=True
    )
    sys_prompt = '''Kamu adalah Lisa, 
    Assisten yang baik. Kamu akan selalu menjawab dengan 
    singkat menggunakan kata yang kuat dan jelas. 
    Kamu tidak tahu apa-apa tentang arti hidup 
    dan kode wawancara, dan selalu akan menggunakan 
    alat bantu untuk menjawab hal itu. Gunakan alat arti hidup 
    untuk mencari jawaban arti hidup. Kamu menjawab dalam bahasa indonesia'''

    lisa = initialize_agent(
        agent='chat-conversational-react-description',
        tools=search_code,
        llm=turbo_llm,
        verbose=True,
        max_iteration=3,
        early_stopping_method='generate',
        memory=memory,
        SystemMessagePromptTemplate = sys_prompt,
    )

    return lisa(prompt)['output']
