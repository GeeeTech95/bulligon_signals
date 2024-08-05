/*--------------Timer One----------------*/

$(document).ready(function() {
  
    $(".timer").each((index,element)=> {
        setInterval(function() {
            makeTimer(
                $(element).attr("id"),
                $(element).attr("nowDate"),
                $(element).attr("toDate")
            );
          }, 1000);
        
    })
   

    


  
});


function makeTimer(iD,fromDate,toDate) {
   
 
    var endTime = new Date(toDate);
    var endTime = (Date.parse(endTime)) / 1000;
    var now = new Date();
    var now = (Date.parse(now) / 1000);
    var timeLeft = endTime - now;
    var days = Math.floor(timeLeft / 86400);
    var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
    var Xmas95 = new Date(fromDate);
    var hour = Xmas95.getHours();
    var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
    var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
    if (days < "0" ){
      days = "0"
    }
    if (hours < "10") {
      hours = "0" + hours;
    }
    if (minutes < "10") {
      minutes = "0" + minutes;
    }
    if (seconds < "10") {
      seconds = "0" + seconds;
    }
    $(".timer_" + iD + " .days").html( days + "<span>D</span>");
    $(".timer_" + iD + " .hours").html( hours + "<span>H</span>");
    $(".timer_" + iD + " .minutes").html(minutes + "<span>M</span>" );
    $(".timer_" + iD + " .seconds").html(seconds + "<span>S</span>");
  }
 

