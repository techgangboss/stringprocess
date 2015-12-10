from subprocess import call
from subprocess import check_output
import subprocess
import json
import httplib
import urllib
import sys
import mysql.connector

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

    # Getting data from Parse to SQL
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/Transactions/', '', {
        "X-Parse-Application-Id": "QrNi3zPI9lmQq60eFZBsdNrB9LpuTfMB8MPhTJ0n",
        "X-Parse-REST-API-Key": "N9Ix3DMj34lO6b1FTPuwtScWQ2nSt6Q5TAVGsbcv"
    })

    cnx = mysql.connector.connect(host="localhost", user="root", passwd="", db="User")
    cursor = cnx.cursor()

    cnxBC = mysql.connector.connect(host="localhost", user="root", passwd="", db="Blockchain")
    cursorBC = cnxBC.cursor()

    result = json.loads(connection.getresponse().read())
    print "ERROR is ", result['error']
    for m in result: 
        print m
    result = result('results')
    createdAt_array = []

    print result(len(result) - 1)
    m = result(len(result) - 1)
    username = m('username')
    receiver_account_number = m('receiver_account_number')
    receiver_mobile_number = m('receiver_mobile_number')
    objectId = m('objectId')
    receiver_bank_name = m('receiver_bank_name')
    amount = m('amount')
    receiver_last_name = m('receiver_last_name')
    updatedAt = m('updatedAt')
    receiver_first_name = m('receiver_first_name')
    createdAt = m('createdAt')
    createdAt_array.append(createdAt[0:10])
    # sql = "SELECT * FROM nwams;"
    temp = createdAt
    sql = "INSERT INTO `nwams` (`amount`, `receiver_first_name`, `receiver_last_name`, `receiver_user_name`, `receiver_bank_name`, `receiver_account_number`, `total_sent`, `total_received`, `net`, `balance`) VALUES (\'" + str(amount) + "\', \'" + receiver_first_name + "\', \'" + receiver_last_name + "\', \'" + username + "\', \'" + receiver_bank_name + "\', \'" + str(receiver_account_number) + "\', \'" + str(300) + "\', \'" + str(0) + "\', \'" + str(100) + "\', \'" + str(89000) + "\')"
    #print(sql)
    cursor.execute(sql)
    cnx.commit()

    #Get latest values from ledger and apply latest payment
    sql = "SELECT * FROM Ledger"
    cursorBC.execute(sql)
    ledgerLine = []
    dayCreated = createdAt[0:10]
    moneyPerDayCount = 0
    volumePerDayCount = 0
    moneyPerDay = 0
    volumePerDay = 0
    for m in cursorBC:
        ledgerLine = m
        if (m[3] == dayCreated):
            moneyPerDay += m[0]
            volumePerDay += 1
        else:
            dayCreated = m(3)

    totalVolume = ledgerLine(2)

    moneyPerDay +=amount
    volumePerDay += 1
    totalVolume += 1
    dayCreated = createdAt[0:10]

    print volumePerDay, " on the day", dayCreated

    print moneyPerDay, " money per day", dayCreated
    print totalVolume
    totalVolume += 1

    #Update SQL Ledger for Blockchain
    temp = createdAt_array[0]
    y = []

    sqlBC = "INSERT INTO `Ledger` (`money_per_day`, `volume_per_day`, `total_volume`, `date`) VALUES (\'" + str(moneyPerDay) + "\', \'" + str(volumePerDay) + "\', \'" + str(totalVolume) + "\', \'" + str(createdAt) + "\')"

    #bunchofcomments

    cnx.close()
    cnxBC.close()

    #print result
