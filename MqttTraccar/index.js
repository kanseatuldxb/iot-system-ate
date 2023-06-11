const mqtt = require('mqtt')
const axios = require('axios').default;
const http = require('http');
const https = require('https');

const httpAgent = new http.Agent({ keepAlive: true });
const httpsAgent = new https.Agent({ keepAlive: true });



const host = '0.0.0.0'
const port = '1883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `mqtt://${host}:${port}`
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  reconnectPeriod: 1000,
})


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

DeviceAlertList = [
"1640064",
"1643776",
"1826901",
"1782632",
"785831581284",
"502255812693",
"822876517658",
"561167241800",
"522015892551",
"765020924364"
]



const topic = ['/ate/tektron/701202133364','/ate/tektron/319482516594','/ate/tektron/419445172568','/ate/tektron/785831581284','/ate/tektron/502255812693','/ate/tektron/822876517658','/ate/tektron/561167241800','/ate/tektron/522015892551','/ate/tektron/765020924364','/ate/tektron/837127908740']
client.on('connect', () => {
  console.log('Connected')
  client.subscribe(topic, () => {
    console.log(`Subscribe to topic '${topic}'`)
  })
})



client.on('message', (topic, payload) => {
  
	var ParsedData = JSON.parse(payload)
	console.log('Received Message:', topic, payload.toString(),JSON.parse(payload).timestamp,payload.timestamp);
	axios.get("http://0.0.0.0:5055", { httpAgent, params: ParsedData}).then(function (response) {
	console.log(response.data);
	})
	.catch(function (error) {
	console.log(error);
	})
	.then(function () {
	});

	if (ParsedData.firestatus != null && ParsedData.faultstatus != null  ){
		
		if (ParsedData.firestatus == true){
			console.log(DeviceIDList.indexOf(ParsedData.id.toString()),ParsedData.id.toString(),DeviceAlertList[DeviceIDList.indexOf(ParsedData.id.toString())]);
			axios.post("https://salamah.api.elm.sa/salamahservices/api/v1/client/rull/alarm-notification",{
			"deviceNo": ParsedData.id.toString(),
			"deviceID": DeviceIDList.indexOf(ParsedData.id.toString())+1,
			"deviceName": "Building No:"+ ParsedData.buildingNo.toString() +
							",Building Name:"+ ParsedData.buildingName.toString() +
							",Street Address:"+ParsedData.streetAdd.toString() +
							",City Zone:"+ParsedData.cityZone.toString() +
							",City:"+ParsedData.city.toString() +
							",Country:"+ParsedData.contry.toString() +
							",Building Category:"+ParsedData.buildingCategory.toString() +
							",Contact Name:"+ParsedData.contactName.toString() +
							",Contact No:" + ParsedData.contactNo.toString().replace(' ', '').replace('+', '').replace('-', ''),
			"sensorID":  DeviceAlertList[DeviceIDList.indexOf(ParsedData.id.toString())].toString(),
			"sensorType":  "1",
			"deviceLat": ParsedData.lat.toString(),
			"deviceLng": ParsedData.lon.toString(),
			"faultDelay": null,
			"createDateTime": ParsedData.updatedTime.toString(),
			"alarmCount": 1
		  },{headers: {
				'AuthorizationToken': '5d9d8bd5-6324-44dd-a5a8-a3c6399d8a0f',
				'app_id':'2ab1cf3e',
				'app_key':'a09b8f8cb9729203a1a8c4c85a27bea8'
			  }
		  }).then(function (response) {
			console.log(response.data);
		  })
		  .catch(function (error) {
			console.log(error);
		  })
		  .then(function () {
		  });
		}
		if (ParsedData.faultstatus == true){
			axios.post("https://salamah.api.elm.sa/salamahservices/api/v1/client/rull/alarm-notification",{
			"deviceNo": ParsedData.id.toString(),
			"deviceID": DeviceIDList.indexOf(ParsedData.id.toString())+1,
			"deviceName": "Building No:"+ ParsedData.buildingNo.toString() +
							",Building Name:"+ ParsedData.buildingName.toString() +
							",Street Address:"+ParsedData.streetAdd.toString() +
							",City Zone:"+ParsedData.cityZone.toString() +
							",City:"+ParsedData.city.toString() +
							",Country:"+ParsedData.contry.toString() +
							",Building Category:"+ParsedData.buildingCategory.toString() +
							",Contact Name:"+ParsedData.contactName.toString() +
							",Contact No:" + ParsedData.contactNo.toString().replace(' ', '').replace('+', '').replace('-', ''),
			"sensorID":  DeviceAlertList[DeviceIDList.indexOf(ParsedData.id.toString())],
			"sensorType":  "2",
			"deviceLat": ParsedData.lat.toString(),
			"deviceLng": ParsedData.lon.toString(),
			"faultDelay": null,
			"createDateTime": ParsedData.updatedTime.toString(),
			"alarmCount": 1
		  },{headers: {
				'AuthorizationToken': '5d9d8bd5-6324-44dd-a5a8-a3c6399d8a0f',
				'app_id':'2ab1cf3e',
				'app_key':'a09b8f8cb9729203a1a8c4c85a27bea8'
			  }
		  }).then(function (response) {
			console.log(response.data);
		  })
		  .catch(function (error) {
			console.log(error);
		  })
		  .then(function () {
		  });
		}
  
	}
})
  /*

{"id": "701202133364", "deviceName": "0526155458", "updatedTime": "04/09/2022 12:28:30", "firestatus": false, "faultstatus": false, "alarm": null, "contactNo": "0508144086", "contactName": "Arshad", "deviceLoc": "", "buildingNo": "", "buildingName": "", "buildingCategory": "GOV", "streetAdd": "Street Address", "city": "S", "cityZone": "S", "contry": "KSA", "lon": "55.3308045", "lat": "25.2600828", "timestamp": 1649492910, "fireconn": "0", "faultconn": "0"}


"Building No: "+ ParsedData.buildingNo.toString() +
", Building Name: "+ ParsedData.buildingName.toString() +
", Street Address: "+ParsedData.streetAdd.toString() +
", City Zone: "+ParsedData.cityZone.toString() +
", City: "+ParsedData.city.toString() +
", Country: "+ParsedData.contry.toString() +
", Building Category: "+ParsedData.buildingCategory.toString() +
", Contact Name: "+ParsedData.contactName.toString() +
", Contact No.: " +ParsedData.contactNo.toString()


  console.log('Received Message:', topic, payload.toString(),JSON.parse(payload).timestamp,payload.timestamp);
  headersx = {
	  "AuthorizationToken":"5d9d8bd5-6324-44dd-a5a8-a3c6399d8a0f",
	  "app_id":"2ab1cf3e",
	  "app_key":"a09b8f8cb9729203a1a8c4c85a27bea8"
  }
  axios.post("https://salamah.api.elm.sa/salamahservices/api/v1/client/rull/alarm-notification", { headers:headersx, data: payloadjson}).then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
  });

})
  */
/*
client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString());
  axios.get("http://192.168.0.169:5055/?id=1234567890&lat=23.0&lon=25.0&timestamp=1648415734&alarm=sos", { httpAgent }).then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
  });
})
*/
