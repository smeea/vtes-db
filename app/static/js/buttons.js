function showAll() {
    var x = document.getElementsByClassName("cardtext");
    var i;
    if (x[0].style.display === "none") {
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "block";
        }
    } else {
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "none";
        }
    }
}
