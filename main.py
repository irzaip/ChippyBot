import os
from typing import Union
from fastapi import BackgroundTasks, Depends, FastAPI, Body
from pydantic import BaseModel

from TTS.api import TTS
from g2p_id import G2P
from playsound import playsound

from fastapi import FastAPI

app = FastAPI()
g2p = G2P()
tts = TTS(model_path="./models/tts/chk_1260k-inf.pth", config_path="./models/tts/config.json", progress_bar=False, gpu=False)

class KataKata(BaseModel):
    kalimat: str
    speaker: str
    playaudio: bool
    requestaudio: bool

speakers = ['JV-00027', 'JV-00264', 'JV-00658', 'JV-01392', 'JV-01519', 'JV-01932', 'JV-02059', 'JV-02326', 'JV-02884',
 'JV-03187', 'JV-03314', 'JV-03424', 'JV-03727', 'JV-04175', 'JV-04285', 'JV-04588', 'JV-04679', 'JV-04715', 
 'JV-04982', 'JV-05219', 'JV-05522', 'JV-05540', 'JV-05667', 'JV-05970', 'JV-06080', 'JV-06207', 'JV-06383', 
 'JV-06510', 'JV-06941', 'JV-07335', 'JV-07638', 'JV-07765', 'JV-07875', 'JV-08002', 'JV-08178', 'JV-08305', 
 'JV-08736', 'JV-09039', 'JV-09724', 'SU-00060', 'SU-00297', 'SU-00454', 'SU-00600', 'SU-00691', 'SU-00994', 
 'SU-01038', 'SU-01056', 'SU-01359', 'SU-01552', 'SU-01596', 'SU-01855', 'SU-01899', 'SU-02092', 'SU-02395', 
 'SU-02716', 'SU-02953', 'SU-03391', 'SU-03650', 'SU-03694', 'SU-03712', 'SU-03887', 'SU-04190', 'SU-04208', 
 'SU-04511', 'SU-04646', 'SU-04748', 'SU-05051', 'SU-05186', 'SU-05507', 'SU-06003', 'SU-06047', 'SU-06543', 
 'SU-07302', 'SU-07842', 'SU-08338', 'SU-08659', 'SU-08703', 'SU-09243', 'SU-09637', 'SU-09757', 
 'ardi', 'gadis', 'wibowo']


def katakan(kalimat, speaker, playaudio, returnaudio):
    if speaker not in speakers:
        return {"Proses": "Speaker tidak ada"}
    kalimat = kalimat
    kalimat = str(g2p(kalimat))
    print(type(kalimat))
    try:
        tts.tts_to_file(text=kalimat,speaker=speaker, file_path=os.path.dirname(__file__) + 'output.wav')
        if playaudio:
            playsound(os.path.dirname(__file__) + 'output.wav')     
    except:
        pass


@app.get("/")
async def siap():
    text="saya sudah siap menerima perintah"
    text = str(g2p(text))
    print(text)
    try:
        tts.tts_to_file(text=text,speaker="gadis", file_path=os.path.dirname(__file__) + 'output.wav')
        playsound(os.path.dirname(__file__) + 'output.wav')     
        return {"Proses": "Selesai"}
    except:
        return {"Proses": "Ada kesalahan terjadi"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/katakan")
async def katakanlah(item: KataKata, background_task: BackgroundTasks):
    print("hasil:", kalimat)
    if speaker not in speakers:
        return {"Proses": "Speaker tidak ada"}
    kalimat = str(g2p(kalimat))
    background_task.add_task(katakan, kalimat, speaker, playaudio, returnaudio)
    return {"Proses": "Selesai", "Katakan" : kalimat, "speaker" : speaker, "playaudio" : playaudio, "returnaudio" : returnaudio }

@app.post("/test")
def test(item: KataKata):
    text = "saya sudah siap menerima perintah"
    print(item.kalimat)
    text = g2p(text)
    item.kalimat = str(g2p(item.kalimat))
    print("text:", text)
    print("kalimat:", item.kalimat)
    return {"proses": "oke"}


@app.post("/coba")
def coba(item: KataKata):
    return item

