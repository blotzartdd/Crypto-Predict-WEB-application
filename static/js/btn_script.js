"use strict"

document.getElementById("contact_me").onclick = function () {
    window.location.hash = "#my_contacts2";
};

document.getElementById("about_me").onclick = function () {
    window.location.hash = "#my_contacts1";
};

document.getElementById("my_contacts1").onclick = function () {
    window.location.hash = "#my_contacts2";
};