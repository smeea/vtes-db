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

function clearCrypt() {
    var i;
    var d = document.getElementsByName('disciplines');
    for (i = 0; i < d.length; i++) {
        d[i].checked = false;
    }
    var t = document.getElementsByName('titles');
    for (i = 0; i < t.length; i++) {
        t[i].checked = false;
    }
    var g = document.getElementsByName('group');
    for (i = 0; i < g.length; i++) {
        g[i].checked = false;
    }
    var x = document.getElementsByName('trait');
    for (i = 0; i < x.length; i++) {
        x[i].checked = false;
    }
    document.getElementById('cardtext').value = '';
    document.getElementById('capacitymoreless').value = '<=';
    document.getElementById('capacity').value = 'ANY';
    document.getElementById('clan').value = 'ANY';
    document.getElementById('sect').value = 'ANY';
    document.getElementById('votes').value = 'ANY';
}

function clearLibrary() {
    var i;
    var x = document.getElementsByName('trait');
    for (i = 0; i < x.length; i++) {
        x[i].checked = false;
    }
    document.getElementById('cardtext').value = '';
    document.getElementById('cardtype').value = 'ANY';
    document.getElementById('discipline').value = 'ANY';
    document.getElementById('clan').value = 'ANY';
    document.getElementById('title').value = 'ANY';
    document.getElementById('sect').value = 'ANY';
    document.getElementById('bloodmoreless').value = '<=';
    document.getElementById('blood').value = 'ANY';
    document.getElementById('poolmoreless').value = '<=';
    document.getElementById('pool').value = 'ANY';
}
