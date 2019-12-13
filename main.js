import { CountUp } from './countUp.js';

window.onload = function() {
   var xhr = new XMLHttpRequest();
   xhr.onload = function() { 
    var farms = new CountUp('count',this.response)
    farms.start();
   }
   xhr.open("GET","https://a28b.de/t90FarmCount");
   xhr.send();
}
