import logging


humanstate = {}
botstate = {}
text_to_speech = False
chatmode = True
logging.basicConfig(filename="./log/log.txt", level=logging.DEBUG)

def bilang(input):
    if text_to_speech == False:
        print(input)
    else:
        print("TEXT_SP:", input) 



def proses_chat(obrolan, humanstate=humanstate, botstate=botstate):
    global chatmode
    if obrolan == "KELUAR":
        chatmode = False
        bilang("keluar")        
        logging.debug("KELUAR SESSION")
    if obrolan == "AH":
        bilang("dia bilang ah")
    else:
        bilang("nggak ngerti")
    logging.debug("input:" + str(obrolan))

if __name__ == '__main__':

    while chatmode:
        obrolan = input(">")
        proses_chat(obrolan, humanstate, botstate)
