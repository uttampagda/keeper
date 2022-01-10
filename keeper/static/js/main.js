window.onscroll = function() {myFunction()};

// Get the navbar
var navbar = document.getElementById("navbar");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

function locationbutton() {
  const a = document.querySelector('.location-dropdown-content');
  const b = a.style.visibility;
  if (b === 'visible')
  {
    a.style.visibility = "hidden";
    a.style.opacity = "0";
    a.style.transform = "translateY(1rem)";
  }
  else {
    a.style.visibility = "visible";
    a.style.opacity = "1";
    a.style.transform = "translateY(0)";
  }
}

function profilebutton() {
  const a = document.querySelector('.profile-dropdown-content');
  const b = a.style.visibility;
  if (b === 'visible')
  {
    a.style.visibility = "hidden";
    a.style.opacity = "0";
    a.style.transform = "translateY(1rem)";
  }
  else {
    a.style.visibility = "visible";
    a.style.opacity = "1";
    a.style.transform = "translateY(0)";
  }
}