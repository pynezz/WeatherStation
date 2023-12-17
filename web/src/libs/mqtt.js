import { createClient } from 'mqtt';

// Use the Docker service name of the MQTT broker as the hostname
export const client = createClient({
    brokerUrl: 'ws://backend_app/ws', // Replace 'websocket-port' with the actual port number
    clientId: 'frontend_app',
});

client.on('connect', () => {
    console.log('Connected to MQTT broker via WebSocket');
    client.subscribe('weather/data', (err) => {
        if (err) {
            console.error('Subscription error:', err);
        }
    });
});

client.on('message', (topic, message) => {
    // Handle incoming messages
    const data = JSON.parse(message.toString());
    // Update your application state/UI here

    console.log("[WSS] Data received: ", data)
});
