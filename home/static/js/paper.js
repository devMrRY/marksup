function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {//action to be performed on time out//
            timer = 0;
            document.forms['quesform'].submit();
        }
    }, 1000);
}

window.onload = function () {
  var t = parseInt(document.getElementById('num').value, 10);
    var time = 60 * t,
        display = document.querySelector('#time');
    startTimer(time, display);
};

// for scrolling to particular question

$(document).ready(function(){
  // Add smooth scrolling to all links
  $("a").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: ($(hash).offset().top)
      }, 800, function(){
   
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
});

function confirmfun() {
  if (confirm("Do you want to submit Yes or No")){
    window.location.href = "http://localhost:8000/home/result/"
  }
}