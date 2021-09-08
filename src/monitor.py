import sys,time,requests,traceback,os
sys.path.append('class/')
from dotenv import load_dotenv
from excepciones import Error
from logger import logger
from datetime import datetime
from ApiRequest import ApiRequest
from Vault import Vault



def botTelegram(msg,minutes):
    Api=ApiRequest(SECTOKEN, LOG,   FICHEROLOG ,LOGLEVEL,_TG) 
    respuesta=Api.EjecutaRequest(requests.get,[_TG+str(msg)],"")
    if minutes>10:
        if LOG:
            LOGGER.hazlog("botTelegram: Imposible comunicar con BOT "+ str(respuesta),1)
        raise Error(1,"botTelegram: botTelegram: Imposible comunicar con BOT  "+ str(respuesta))
    if isinstance(respuesta,int):
        if LOG:        
            LOGGER.hazlog("botTelegram- No es posible comunicar con bot de TG: "+ str(respuesta),1)
        time.sleep(60*minutes)
        return botTelegram(msg, minutes+1)
    else:
        return 200

def QueryApiSubgraph(SC):

    chainId=1
    a=Vault(chainId,'0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9')
    
    valor=(a.HumanpricePerShare())
    
    if float(valor) <float(LIMIT):
        msg="El valor de " +str(a.Symbol())+ " esta por debajo del umbral "  +str(LIMIT) +" Precio actual " + str(valor)
        botTelegram(msg,1)    
    return False
    
# Load .ENV

try:
    load_dotenv()
    _TG=os.getenv("_TG")
    SECTOKEN=False if(os.getenv("SECTOKEN")=="False") else True
    LOG=False if(os.getenv("LOG")=="False") else True
    FICHEROLOG=os.getenv("FICHEROLOG")
    LIMIT=os.getenv("LIMIT")
    LOGLEVEL=int(os.getenv("LOGLEVEL"))
    if LOG:
        LOGGER=logger(FICHEROLOG,LOGLEVEL)
        LOGGER.hazlog("Inicio programa",1)
    SC=os.getenv("SC")
    res=QueryApiSubgraph(SC)


    if res:
        raise Error(1,"Vault Oracle Proceso General: Se ha ejecutado con problemas")
      
except Exception as error:
    msg="Vault Oracle FALLO DEL PROCESO: "+str(error) +" "+str (traceback.format_exc()) 
    LOGGER.hazlog(msg,1)
    botTelegram(msg,1)

