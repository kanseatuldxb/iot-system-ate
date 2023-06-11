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

/*
701202133364
319482516594
419445172568
785831581284
502255812693
822876517658
561167241800
522015892551
765020924364
837127908740
*/



const topic = ['/ate/tektron/701202133364','/ate/tektron/319482516594','/ate/tektron/419445172568','/ate/tektron/785831581284','/ate/tektron/502255812693','/ate/tektron/822876517658','/ate/tektron/561167241800','/ate/tektron/522015892551','/ate/tektron/765020924364','/ate/tektron/837127908740']
client.on('connect', () => {
  console.log('Connected')
  client.subscribe(topic, () => {
    console.log(`Subscribe to topic '${topic}'`)
  })
  //client.publish(topic, 'nodejs mqtt test', { qos: 0, retain: false }, (error) => {
  //  if (error) {
  //    console.error(error)
  //  }
  //})
})



client.on('message', (topic, payload) => {
  /*
  var payloadjson = JSON.parse(payload)
  console.log('Received Message:', topic, payload.toString(),JSON.parse(payload).timestamp,payload.timestamp);
  axios.get("http://0.0.0.0:5055", { httpAgent, params: payloadjson}).then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
  });
  */
  console.log('Received Message:', topic, payload.toString(),JSON.parse(payload).timestamp,payload.timestamp);
  var ParsedData = JSON.parse(payload)
  if (ParsedData.alarm != null){
	  var AlarmType = "1643776"
	  if(ParsedData.alarm.toString() == "sos"){
		  AlarmType = "1640064"
	  }
	  axios.post("https://salamah.api.elm.sa/salamahservices/api/v1/client/rull/alarm-notification",{
		"deviceNo": ParsedData.id.toString(),
		"deviceID": ParsedData.id.toString(),
		"deviceName": ParsedData.deviceLoc.toString(),
		"sensorID":  AlarmType,
		"sensorType":  AlarmType,
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
})

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
