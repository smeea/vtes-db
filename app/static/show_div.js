function showDiv(card) {
    // document.getElementById(card).style.display = "block";

    var x = document.getElementById(card);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function pageScroll() {
    window.scrollBy(0,1000); // horizontal and vertical scroll increments
}
