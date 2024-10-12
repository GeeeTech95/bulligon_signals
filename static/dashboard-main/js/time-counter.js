$(document).ready(function () {

    
    function makeTimer(endTime, timerClass) {
        endTime = (Date.parse(endTime)) / 1000; // Convert endTime to seconds
        var now = (Date.parse(new Date())) / 1000; // Get current time in seconds
        var timeLeft = endTime - now; // Calculate time left

        // Check if the time has already expired
        if (timeLeft < 0) {
            $(timerClass + " .days").html("00<span>D</span>");
            $(timerClass + " .hours").html("00<span>H</span>");
            $(timerClass + " .minutes").html("00<span>M</span>");
            $(timerClass + " .seconds").html("00<span>S</span>");
            return; // Stop further calculations if time is up
        }

        var days = Math.floor(timeLeft / 86400);
        var hours = Math.floor((timeLeft % 86400) / 3600);
        var minutes = Math.floor((timeLeft % 3600) / 60);
        var seconds = Math.floor(timeLeft % 60);

        // Pad single digit numbers with a leading zero
        if (hours < 10) hours = "0" + hours;
        if (minutes < 10) minutes = "0" + minutes;
        if (seconds < 10) seconds = "0" + seconds;

        // Update the HTML for the timer
        $(timerClass + " .days").html(days + "<span>D</span>");
        $(timerClass + " .hours").html(hours + "<span>H</span>");
        $(timerClass + " .minutes").html(minutes + "<span>M</span>");
        $(timerClass + " .seconds").html(seconds + "<span>S</span>");
    }

    // Initialize timers dynamically from HTML
    var timers = [];
    
    $('.timer').each(function() {
        var endTime = $(this).attr('toDate'); // Get endTime from HTML attribute
        var timerClass = '.timer_' + $(this).attr('id'); // Create a class selector from the id
        timers.push({ endTime: endTime, class: timerClass }); // Add to timers array
    });

    // Update timers every second
    setInterval(function () {
        timers.forEach(timer => {
            makeTimer(timer.endTime, timer.class);
        });
    }, 1000);
});
