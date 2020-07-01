// ----------------------------------------------------------------------
// used for sending test data to the ODK API websocket endpoint '/stream'
// else: the ODK app would have to be started to produce an image...
//
// run with node:
// $ export RMQ_URL=localhost
// $ node testStreamWebSocket.js
// ----------------------------------------------------------------------

const fs = require('fs');
const WebSocket = require('ws')

function base64_encode(file) {
    var bitmap = fs.readFileSync(file);
    return new Buffer(bitmap).toString('base64');
}

// setup data structure

const base64Img = base64_encode('./062540/16-56-10.0374-52.3736191-4.9146496.jpeg');

let data = { 
    stream_id: '123456',
    img: base64Img, 
    createdAt: new Date().toString(),
    lng: 5.3,
    lat: 50.3,
};

// setup connection

const websocketUrl = "ws://localhost:8080/stream";
console.log(`Starting connection to: ${websocketUrl}`)
const websocketConnection = new WebSocket(websocketUrl);

// send message

websocketConnection.onopen = () => {
    websocketConnection.send(JSON.stringify(data));
    console.log("Message send!")
}

websocketConnection.onmessage = (message) => {
    console.log(`WebSocket error: ${message}`)
}

websocketConnection.onerror = (error) => {
    console.log(`WebSocket error: ${error}`)
}