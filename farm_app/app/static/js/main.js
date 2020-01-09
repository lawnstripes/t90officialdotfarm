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
      farms.update(JSON.parse(this.response)['count']);
    }
    else {
      let cnt = parseInt(document.getElementById('count').textContent);
      farms = new CountUp('count',JSON.parse(this.response)['count']+cnt)
      farms.start();
    }
   }
   xhr.open("GET","http://localhost:5000/farm");
   xhr.send();
}

