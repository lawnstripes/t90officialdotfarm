import { CountUp } from './countUp.js';
var farms = null;
var socket = io();

window.onload = function() {
  socket.on('connect', () => { 
    this.console.log('connect');
  });
  socket.on('farms', (data) => {
    if (farms) {
      farms.update(data['farms']);
    }
    else {
      farms = new CountUp('count', data['farms']);
      farms.start()
    }
  });
}

function getData() {
   let xhr = new XMLHttpRequest();
   xhr.onload = function() { 
    if (farms) {
      farms.update(JSON.parse(this.response)['farms']);
    }
    else {
      let cnt = parseInt(document.getElementById('count').textContent);
      farms = new CountUp('count',JSON.parse(this.response)['farms'])
      farms.start();
    }
   }
   xhr.open("GET","/farms");
   xhr.send();
}

