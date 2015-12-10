from subprocess import call
from subprocess import check_output
import subprocess
import json
import httplib
import urllib
import sys

def address_balance(address):
    out = subprocess.check_output(["multichain-cli", "chain2", "getaddressbalances", address]) 
    return out

if __name__ == '__main__':
    print "sending"
    amount = sys.argv[1]
    sender = sys.argv[2]
    recipient = sys.argv[3]
    roberts = '1YKM2c3PWFGXK5pU7msNViFKnELgEnvDT5ahsA'
    nwams = '1MzkirbCMSaiTmm3z8XWAt4v8gGK3NrgLPkpY7'
    murata = '118K6VND8V9fFqCnjbN1xKuk9b4TJbaqppYxLa' 
    jsp = '1Ykjusd1gjVb8qsHzMN1gyYbHohzAYcxP8FqNs'
    usr_list = [roberts,nwams,murata,jsp]
    name_list = ['Robert','Nwamaka','Murat','Jeff']
    nwams_parse = 'DUlGSvYtCF'
    murata_parse = 'jC435I46p7'
    jsp_parse = 'VCHFCvMA4K'
    roberts_parse = 'aunhk1hGha'
    parse_list = [roberts_parse,nwams_parse,murata_parse,jsp_parse]

    balance_list = [0,0,0,0]
    print "The sender is ", sender, " to ", recipient
    call(["multichain-cli", "chain2", "sendassetfrom", sender, recipient, "assetmain", amount])
    
    

    for user in range(len(usr_list)):
        output = address_balance(usr_list[user])
        print "Output"
        #print output
        start = [x for x, v in enumerate(output) if v== '['][1]
        json_data = output[start:]
        text = json.loads(json_data)
        #balance = text[1]['qty']
        for m in range (len(text)):
             #print text[m]['name']
            if(text[m].get('name') == "assetmain"):
                 balance = text[m]['qty']
        print "Balance for ", name_list[user], " is $ ",  balance   
        balance_list[user] = balance
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('PUT', '/1/classes/User/' + parse_list[user], json.dumps({
            "balance": balance
            }), {
            "X-Parse-Application-Id": "QrNi3zPI91mQq60eFZBsdNrB9LpuTfMB8MPhTJ0n",
            "X-Parse-REST-API-Key": "N9Ix3DMj34lO6b1FTPuwtScWQ2nSt6Q5TAVGsbcv"
             })
        result = json.loads(connection.getresponse().read())
        #print result
