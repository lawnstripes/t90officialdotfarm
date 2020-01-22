import { CountUp } from './countUp.js';
var farms = null;
var socket = io();

window.onload = function() {
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