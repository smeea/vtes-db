function showAll(card) {
    var x = document.getElementsByClassName("cardtext");
    if (x[0].style.display === "none") {
        var i;
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "block";
        }
    } else {
        var i;
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "none";
        }
    }
}

function showCard(card) {
    var x = document.getElementById(card);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
