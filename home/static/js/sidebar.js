/* Set the width of the sidebar to 150px */
function toggleNav() {
  var element = document.getElementById("mySidebar");
  if (element.style.width == "150px") {
      element.style.width = "0px";
  } else {
      element.style.width = "150px";
  }
}

// Get the modal
var modal = document.getElementById('id01');
var modal = document.getElementById('id02');


$(document).ready(function(){
  $('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('div').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementById("myBtn").style.display = "block";
  } else {
    document.getElementById("myBtn").style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}