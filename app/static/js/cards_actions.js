function cardShowText(cardid, textid) {
    carddiv = document.getElementById(cardid);
    textdiv = document.getElementById(textid);

    if (textdiv.style.display === "none") {
        textdiv.style.display = "block";
    } else {
        textdiv.style.display = "none";
    };
}
