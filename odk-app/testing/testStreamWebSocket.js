// RUN WITH NODE!

// send test data to the api websocket endpoint

const fs = require('fs');
const WebSocket = require('ws')

function base64_encode(file) {
    var bitmap = fs.readFileSync(file);
    return new Buffer(bitmap).toString('base64');
}

// setup data structure

const base64Img = base64_encode('./garbage-1.jpg');

let data = { 
    img: base64Img, 
    createdAt: new Date().toString(),
    lng: 5.3,
    lat: 50.3,
};

// setup connection

const websocket_url = "ws://localhost:8080/stream";
console.log(`Starting connection to: ${websocket_url}`)
const websocketConnection = new WebSocket(websocket_url);

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