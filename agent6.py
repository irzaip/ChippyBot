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

def agent_lisa(obj: Conversation, prompt: str) -> str:
    search = DuckDuckGoSearchRun()

    t1 = Tool(
        name = 'search',
        func=search.run,
        description="berguna kalau ada pertanyaan tentang tempat, lokasi, point of interest dan kegiatan bisnis"
    )

    def arti_hidup(action=''):
        print(action)
        return "Arti hidup sebenarnya adalah jemblawakasikatasa"

    dlist = ListDirectoryTool()

    t2 = Tool(
        name = 'arti hidup',
        func=arti_hidup,
        description="berguna apabila ada pertanyaan arti hidup"
    )
    t3 = Tool(
        name = 'list tool',
        func = dlist.run,
        description="berguna ada permintaan melihat isi direktori" 
    )

    
    def wawancara(string):
        print("KODE FOUND!! -- ini dia. {string}")
        return f"kode wawancara ditemukan {string}"

    t4 = Tool(
        name = 'search',
        func = wawancara,
        description="berguna apabila ada penyebutan kode wawancara dengan huruf awal BB dan empat angka dengan format seperti BBXXXX, contohnya BB1234"
    )

    tools=[t4]
    tools.append(t3)
    tools.append(t2)


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
        tools=tools,
        llm=turbo_llm,
        verbose=True,
        max_iteration=3,
        early_stopping_method='generate',
        memory=memory,
        SystemMessagePromptTemplate = sys_prompt,
    )

    return lisa(prompt)['output']

