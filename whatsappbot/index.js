const qrcode = require('qrcode-terminal');
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const { Client } = require('whatsapp-web.js');

const client = new Client();

const app = express();
app.use(bodyParser.json());

client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', async (msg) => {
      if(msg.hasMedia) {
        try {
        const media = await msg.downloadMedia();
        // do something with the media data here
      } catch (e) {
        console.log("Error download");
      }
    }
    try {
      const response = await axios.post('http://localhost:8998/messages', {
        client: "whatsapp",
        text: msg.body,
        user_number: msg.from,
        bot_number: msg.to,
        notifyName: msg._data.notifyName !== undefined ? msg._data.notifyName : "",
        timestamp : msg.timestamp,
        type : msg.type,
        author: msg.author !== undefined ? msg.author : "",
      });
      console.log(msg);

      const chat = await client.getChatById(msg.from);
      chat.sendMessage(response.data.message);

      console.log("-----------------------------------------------------------");
      console.log(response.data);
      console.log("-----------------------------------------------------------");


    } catch (error) {
      console.error(error);
    }
  });

client.initialize();



// REST API to forward message to WhatsApp
app.post('/send', async (req, res) => {
  const { to, message } = req.body;
  try {
    const chat = await client.getChatById(to);
    chat.sendMessage(message);
    res.send('Message sent');
  } catch (error) {
    console.error(error);
    res.status(500).send('Error sending message');
  }
});
  
app.listen(8000, () => {
  console.log('Server listening on port 8000');
});
 

