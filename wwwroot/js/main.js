import { CountUp } from './countUp.js';
var farms = null;

window.onload = function() {
   getData();
   setInterval(getData, 5000);
}

function getData() {
   let xhr = new XMLHttpRequest();
   xhr.onload = function() { 
    if (farms) {
      farms.update(this.response);
    }
    else {
      farms = new CountUp('count',this.response)
      farms.start();
    }
   }
   xhr.open("GET","https://a28b.de/t90FarmCount");
   xhr.send();
}

