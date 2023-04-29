from listens import *
from preprocess import *


def p
ocess():
    ear.stop()
    pass
    print("Ini prosesnya")

def transcrib():
    global speech
    speech = transcribe_speech(s_iface)
    if speech == None:
        speech = ""
    print("Ini Transkrip:",speech)

def relisten_hotword():
    global att_counter, cipi_recognized, attention, speech
    att_counter = 0
    cipi_recognized = False
    attention = False
    speech=""
    time.sleep(1)

ear = Listen()
ear.set_process(process)
ear.debug = True


ear.start(thres=1200, timeout=0)


while not cipi_recognized:
    print("Start waiting for hotword...")
    ear.start(thres=1200, timeout=0)
    #ear.write_to_file('test.wav')
    dataaudio=np.array(ear.audiodata).flatten()
    sample = au2mfcc(dataaudio)
    sample_reshaped = sample.reshape(1, feature_dim_1, feature_dim_2, channel)
    y_pred = model.predict(sample_reshaped)
    y_max = np.max(y_pred) #nilai akurasi prediksi
    ypred = np.argmax(y_pred) #yg di prediksi adalah cipi
    cipi_recognized = (y_max>0.9 and ypred==1)
    if cipi_recognized: 
        
        #RANDOMIZE this
        #playdetected()
        
        print("Recognized - Predicted:" ,get_labels()[0][ypred],y_max, ypred)

        attention=True
        att_counter = 0
        while attention:
            print("Attention is:",attention)
            #rec_speech(s_iface)
            ear.debug = False
            ear.start(thres=800, timeout=5, process=transcrib)
            if speech: #ada kalimat yg disebut dalam bentuk string
                #RANDOMIZE THIS
                #playdetected()
                reply,humanstate,botstate = sequence(speech,humanstate,botstate)
                if awake:
                    talk_until_complete(reply,s_iface)
                #if the reply not a followup
                if botstate['followup']=="None": 
                    print("not a followup")
                    relisten_hotword()
            else:
                print("blank speech detected")
                speech = " " #kasih sedikit spasi hack
                att_counter += 1
                if att_counter > 1:
                    relisten_hotword()
                    print("\n=============\nGo to wait mode")

