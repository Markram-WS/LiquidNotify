import requests
import hashlib
import json
import hmac
import requests
import numpy as np
from datetime import datetime
import time
    
#Msg Line
def lineSendMas(msg_line):
    url_line = 'https://notify-api.line.me/api/notify'
    token_line = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    headers_line = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token_line}
    reg_line = requests.post(url_line, headers=headers_line , data = {'message':msg_line})
    #print(reg_line.text)
    
# API Liquid info
host = 'https://api.liquid.com'
tokenId = '1448568'
tokenSecret = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

header = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-BTK-APIKEY': tokenSecret,
}


#API sub function
def json_encode(data):
    return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
        j = json_encode(data)
        h = hmac.new(tokenSecret, msg=j.encode(), digestmod=hashlib.sha256)
        return h.hexdigest()
    
def getAllProdut(): 
    path = '/products'
    try:
      response = requests.get(host + path ,timeout=300)
      return json.loads(response.text)
    except:
      return print(response.text)

def getProdutByID(ID): 
    path = '/products/'+str(ID)
    try:
      response = requests.get(host + path,timeout=300)
      return json.loads(response.text)
    except:
      return print(response.text)

def getID(symbol):
  data = getAllProdut()
  #Get ID
  for i in range(len(data)):
    if( data[i]['currency_pair_code']==symbol):
      ProuductID = data[i]['id']
      print("%s  ID : %s, index : %d"%(symbol,data[i]['id'],i))
  return ProuductID

def main():  
    #initialize
    symbol = 'XRPJPY'
    prePrice = 0
    ProuductID = getID(symbol)
    time.sleep(1)
    #--------------------------------------------
    
    try:
      data = getProdutByID(ProuductID)
      pair = data['currency_pair_code']
      bid = np.round(data['market_ask'], 3)
      ask = np.round(data['market_bid'], 3)
      ts = data['timestamp']
      msg =pair +'  '+str(bid)+' | '+str(ask)
      conditionPrice = (np.round(ask,2)*10) % 5
      tm= datetime.fromtimestamp(int(ts.split('.')[0])) 
      print("BID:%0.3f ASK:%0.3f %s" %(bid,ask,tm),end="\r")
      #print("%s BID:%0.3f ASK:%0.3f" %(tm,bid,ask))
      if(prePrice == 0):
          lineSendMas('notification start')
          prePrice=np.round(ask,1)

      if(np.round(ask,1) != prePrice and conditionPrice == 0):
          lineSendMas(msg)
          prePrice=np.round(ask,1)
    except:
      print('bad request',end="\r")
      time.sleep(300)
        
        


while(True):
  main()
  time.sleep(5)

