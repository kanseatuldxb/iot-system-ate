#!/usr/bin/env python
# encoding: utf-8

import requests
import os
import json
import base64
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)


DeviceAlertIDList = [
1640064,
1643776,
1826901,
1782632,
7858315,
5022553,
8228765,
5241800,
5292551,
2924364
]

DeviceIDList = [
"701202133364",
"319482516594",
"837127908740",
"419445172568",
"785831581284",
"502255812693",
"822876517658",
"561167241800",
"522015892551",
"765020924364"
]

#http://www.elm-rull.sonictech.ae/api/v1/service1
@app.route('/api/v1/service1', methods=['GET'])
def service1():
    args = request.args
    print(args)
    userName = ""
    password = ""
    try:
        userName = args.get("userName", default="", type=str)
        password = args.get("password", default="", type=str)
        print(userName,password)
    except:
        pass
    #try:
    if(userName != "" and password != ""):
        print(userName,"I am Here",password)
        AuthTokenGen =  userName + ":" + password
        print(AuthTokenGen)
        AuthTokenGenBy = AuthTokenGen.encode('ascii')
        AuthTokenGenB64 = base64.b64encode(AuthTokenGenBy)
        print(AuthTokenGenB64)
        RespDevices=requests.get("http://0.0.0.0/api/devices", headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
        print(RespDevices)
        print(RespDevices.text)
        json_RespDevices = json.loads(RespDevices.text)
        print(json_RespDevices,len(json_RespDevices))
        deviceList = []
        for DeviceSingle in json_RespDevices:
            DeviceParameters = {}
            RespPosParams = {'id' : DeviceSingle['positionId']}
            print(RespPosParams)
            RespPosID=requests.get("http://0.0.0.0/api/positions", params = RespPosParams, headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
            print("###############################################")
            json_RespPosID = json.loads(RespPosID.text) 
            print(json_RespPosID)
            DeviceParameters["deviceIoc"]="/static/images/map.png"
            sensorlistx = [
                {
                  "unit": "",
                  "lng": "null",
                  "sensorName": "Common Fire Alarm",
                  "iocUrl": "/static/images/fire.png",
                  "sensorType": "1",
                  "sensorSignalType":"2",
                  "switcher": "1",
                  "isLine": "1",
                  "updateDateTime": "",
                  "value": "null",
                  "lat": "null",
                  "sensorId": "1"
                },
                {
                  "unit": "",
                  "lng": "null",
                  "sensorName": "Common Fault Alarm",
                  "iocUrl": "/static/images/fault.png",
                  "sensorType": "2",
                  "sensorSignalType":"2",
                  "switcher": "1",
                  "isLine": "1",
                  "updateDateTime": "",
                  "value": "",
                  "lat": "null",
                  "sensorId": "2"
                }
              ]
            sensorlistx[0]["sensorId"] = str(DeviceAlertIDList[DeviceIDList.index(DeviceSingle['uniqueId'])])
            sensorlistx[1]["sensorId"] = str(DeviceAlertIDList[DeviceIDList.index(DeviceSingle['uniqueId'])]+1)
            sensorlistx[0]["value"] = json_RespPosID[0]['attributes']['firestatus']
            sensorlistx[1]["value"] = json_RespPosID[0]['attributes']['faultstatus']
            DeviceParameters["sensorList"]= sensorlistx
            DeviceParameters["deviceLat"]=json_RespPosID[0]['latitude']
            DeviceParameters["defaultTimescale"]=60
            DeviceParameters["faultDelay"]=None
            DeviceParameters["deviceNo"]=DeviceSingle['uniqueId']
            DeviceParameters["deviceId"]=DeviceSingle['id']
            deviceNameStr = "Building No:" + str(json_RespPosID[0]['attributes']['buildingNo']) + ",Building Name:"+ str(json_RespPosID[0]['attributes']['buildingName']) +",Street Address:"+str(json_RespPosID[0]['attributes']['streetAdd']) +",City Zone:"+str(int(json_RespPosID[0]['attributes']['cityZone'])) +",City:"+str(json_RespPosID[0]['attributes']['city']) + ",Country:"+str(json_RespPosID[0]['attributes']['contry']) +",Building Category:"+str(int(json_RespPosID[0]['attributes']['buildingCategory'])) +",Contact Name:"+str(json_RespPosID[0]['attributes']['contactName']) +",Contact No:" +str(json_RespPosID[0]['attributes']['contactNo']).replace("+", "").replace(" ", "").replace("-", "")
            DeviceParameters["deviceName"]=deviceNameStr
            DeviceParameters["createDateTime"]="2022-01-01 11:56:17"#DeviceSingle['lastUpdate']
            DeviceParameters["deviceLng"]=json_RespPosID[0]['longitude']
            deviceList.append(DeviceParameters)
        RespData = {"flag":0,"msg":"Success","deviceList":deviceList}
        #print(RespData)
        return jsonify(RespData)
    else:
        return jsonify({'flag': 1,'msg': 'Required Auth Parameter not found'})
    #except:
    #    return jsonify({'flag': 2,'msg': 'Exception Occured to collect Device Details'})

#http://www.elm-rull.sonictech.ae/api/v1/service1
@app.route('/api/v2/service1', methods=['GET'])
def service1old():
    data = request.json
    userName = ""
    password = ""
    try:
        userName = data['userName']
        password = data['password']
    except:
        pass
    if(userName != "" and password != ""):
        AuthTokenGen =  userName + ":" + password
        print(AuthTokenGen)
        AuthTokenGenBy = AuthTokenGen.encode('ascii')
        AuthTokenGenB64 = base64.b64encode(AuthTokenGenBy)
        print(AuthTokenGenB64)
        RespDevices=requests.get("http://0.0.0.0/api/devices", headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
        print(RespDevices)
        print(RespDevices.text)
        json_RespDevices = json.loads(RespDevices.text)
        print(json_RespDevices,len(json_RespDevices))
        deviceList = []
        for DeviceSingle in json_RespDevices:
            DeviceParameters = {}
            RespPosParams = {'id' : DeviceSingle['positionId']}
            print(RespPosParams)
            RespPosID=requests.get("http://0.0.0.0/api/positions", params = RespPosParams, headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
            print("###############################################")
            json_RespPosID = json.loads(RespPosID.text)            
            DeviceParameters["deviceIoc"]="/static/images/map.png"
            DeviceParameters["sensorList"]= sensorlist
            DeviceParameters["deviceLat"]=json_RespPosID[0]['latitude']
            DeviceParameters["defaultTimescale"]=60
            DeviceParameters["faultDelay"]=None
            DeviceParameters["deviceNo"]=DeviceSingle['uniqueId']
            DeviceParameters["deviceId"]=DeviceSingle['id']
            deviceNameStr = "Building No: " + str(json_RespPosID[0]['attributes']['buildingNo']) + ", Building Name: "+ str(json_RespPosID[0]['attributes']['buildingName']) +", Street Address: "+str(json_RespPosID[0]['attributes']['streetAdd']) +", City Zone: "+str(json_RespPosID[0]['attributes']['cityZone']) +", City: "+str(json_RespPosID[0]['attributes']['city']) + ", Country: "+str(json_RespPosID[0]['attributes']['contry']) +", Building Category: "+str(json_RespPosID[0]['attributes']['buildingCategory']) +", Contact Name: "+str(json_RespPosID[0]['attributes']['contactName']) +", Contact No.: " +str(json_RespPosID[0]['attributes']['contactNo'])
            DeviceParameters["deviceName"]=deviceNameStr
            DeviceParameters["createDateTime"]=DeviceSingle['lastUpdate']
            DeviceParameters["deviceLng"]=json_RespPosID[0]['longitude']
            deviceList.append(DeviceParameters)
        RespData = {"flag":0,"msg":"Success","deviceList":deviceList}
        return jsonify(RespData)
    else:
        return jsonify({'flag': 1,'msg': 'Required Auth Parameter not found'})

#Street Address, City Zone, Country, City
#http://www.elm-rull.sonictech.ae/api/v1/service3
@app.route('/api/v1/service3', methods=['GET'])
def service3():
    args = request.args
    print(args)
    data = request.json
    userName = ""
    password = ""
    deviceNo = ""
    startDate = ""
    endDate = ""
    try:
        userName = args.get("userName", default="", type=str)
        password = args.get("password", default="", type=str)
        print(userName,password)
    except:
        pass
    try:
        deviceNo = data['deviceNo']
        startDate = data['startDate']
        endDate = data['endDate']
        print(deviceNo,startDate,endDate)
    except:
        pass
    try:
        startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S.%f')
        endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S.%f')
        startDate = startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        endDate = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    except:
        return jsonify({'flag': 1,'msg': 'Valid Dates Parameter not found'})
    try:
        if(userName != "" and password != "" and deviceNo != "" and startDate != "" and endDate != ""):
            AuthTokenGen =  userName + ":" + password
            print(AuthTokenGen)
            AuthTokenGenBy = AuthTokenGen.encode('ascii')
            AuthTokenGenB64 = base64.b64encode(AuthTokenGenBy)
            print(AuthTokenGenB64)
            RespDevicesParams = {'uniqueId' : deviceNo}
            RespDevices=requests.get("http://0.0.0.0/api/devices", params = RespDevicesParams, headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
            print(RespDevices)
            print(RespDevices.text)
            json_RespDevices = json.loads(RespDevices.text)
            print(json_RespDevices,len(json_RespDevices))
            deviceList = []
            firealarm = {'name' : 'Common Fire Alarm', 'history':[]}
            faultalarm = {'name' : 'Common Fault Alarm','history':[]}
            for DeviceSingle in json_RespDevices:
                
                print(startDate,endDate)
                RespPosParams = {'deviceId' : DeviceSingle['id'],'from':startDate,'to':endDate}
                RespAlarm=requests.get("http://0.0.0.0/api/reports/events", params =RespPosParams, headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
                print(RespAlarm)
                print(RespAlarm.text)
                json_RespAlarm = json.loads(RespAlarm.text)
                for DeviceAlarmSingle in json_RespAlarm:
                    print(DeviceAlarmSingle)
                    if(DeviceAlarmSingle['type'] == "alarm"):
                        if(DeviceAlarmSingle['attributes']['alarm'] == 'sos'):
                            tempalarm = {'updateDateTime':DeviceAlarmSingle['eventTime'][0:19]}
                            firealarm['history'].append(tempalarm)
                        if(DeviceAlarmSingle['attributes']['alarm'] == 'fault'):
                            tempalarm = {'updateDateTime':DeviceAlarmSingle['eventTime'][0:19]}
                            faultalarm['history'].append(tempalarm)
                #print(json_RespDevices,len(json_RespDevices))
            return jsonify([firealarm,faultalarm])
        else:
            return jsonify({'flag': 1,'msg': 'Required Parameter not found'})
    except:
        return jsonify({'flag': 2,'msg': 'Exception Occured to collect Device Alerts'})

#http://www.elm-rull.sonictech.ae/api/v1/service3
@app.route('/api/v2/service3', methods=['GET'])
def service3old():
    data = request.json
    userName = ""
    password = ""
    deviceNo = ""
    startDate = ""
    endDate = ""
    try:
        userName = data['userName']
        password = data['password']
        deviceNo = data['deviceNo']
        startDate = data['startDate']
        endDate = data['endDate']
    except:
        pass
    try:
        startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S.%f')
        endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S.%f')
        startDate = startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        endDate = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    except:
        return jsonify({'flag': 1,'msg': 'Valid Dates Parameter not found'})
    
    if(userName != "" and password != "" and deviceNo != "" and startDate != "" and endDate != ""):
        AuthTokenGen =  userName + ":" + password
        print(AuthTokenGen)
        AuthTokenGenBy = AuthTokenGen.encode('ascii')
        AuthTokenGenB64 = base64.b64encode(AuthTokenGenBy)
        print(AuthTokenGenB64)
        RespDevicesParams = {'uniqueId' : deviceNo}
        RespDevices=requests.get("http://0.0.0.0/api/devices", params = RespDevicesParams, headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
        print(RespDevices)
        print(RespDevices.text)
        json_RespDevices = json.loads(RespDevices.text)
        print(json_RespDevices,len(json_RespDevices))
        deviceList = []
        firealarm = {'name' : 'Common Fire Alarm', 'history':[]}
        faultalarm = {'name' : 'Common Fault Alarm','history':[]}
        for DeviceSingle in json_RespDevices:
            
            print(startDate,endDate)
            RespPosParams = {'deviceId' : DeviceSingle['id'],'from':startDate,'to':endDate}
            RespAlarm=requests.get("http://0.0.0.0/api/reports/events", params =RespPosParams, headers={"Authorization":"Basic " +AuthTokenGenB64.decode('utf-8')})
            print(RespAlarm)
            print(RespAlarm.text)
            json_RespAlarm = json.loads(RespAlarm.text)
            for DeviceAlarmSingle in json_RespAlarm:
                print(DeviceAlarmSingle)
                if(DeviceAlarmSingle['type'] == "alarm"):
                    if(DeviceAlarmSingle['attributes']['alarm'] == 'sos'):
                        tempalarm = {'updateDateTime':DeviceAlarmSingle['eventTime']}
                        firealarm['history'].append(tempalarm)
                    if(DeviceAlarmSingle['attributes']['alarm'] == 'fault'):
                        tempalarm = {'updateDateTime':DeviceAlarmSingle['eventTime']}
                        faultalarm['history'].append(tempalarm)
            #print(json_RespDevices,len(json_RespDevices))
        return jsonify([firealarm,faultalarm])
    else:
        return jsonify({'flag': 1,'msg': 'Required Parameter not found'})

'''
"Building No: "+ str(json_RespPosID[0]['attributes']['buildingNo']) +
", Building Name: "+ str(json_RespPosID[0]['attributes']['buildingName']) +
", Street Address: "+str(json_RespPosID[0]['attributes']['streetAdd']) +
", City Zone: "+str(json_RespPosID[0]['attributes']['cityZone']) +
", City: "+str(json_RespPosID[0]['attributes']['city']) +
", Country: "+str(json_RespPosID[0]['attributes']['contry']) +
", Building Category: "+str(json_RespPosID[0]['attributes']['buildingCategory']) +
", Contact Name: "+str(json_RespPosID[0]['attributes']['contactName']) +
", Contact No.: " +str(json_RespPosID[0]['attributes']['contactNo'])


"Building No: "+ ParsedData.buildingNo.toString() +
							", Building Name: "+ ParsedData.buildingName.toString() +
							", Street Address: "+ParsedData.streetAdd.toString() +
							", City Zone: "+ParsedData.cityZone.toString() +
							", City: "+ParsedData.city.toString() +
							", Country: "+ParsedData.contry.toString() +
							", Building Category: "+ParsedData.buildingCategory.toString() +
							", Contact Name: "+ParsedData.contactName.toString() +
							", Contact No.: " +ParsedData.contactNo.toString(),
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
