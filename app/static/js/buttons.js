function showAll() {
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
