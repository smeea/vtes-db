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
    var v = document.getElementsByName('virtues');
    for (i = 0; i < v.length; i++) {
        v[i].checked = false;
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

$(document).ready(function(){
    function disciplineCheckboxState() {
        $('.js-discipline-container').each(function() {
            let container = $(this);
            let inputBase = container.find('.js-discipline-base');
            let inputSuperior = container.find('.js-discipline-superior');
            if(inputSuperior.is(':checked')) {
                container.removeClass('state0').removeClass('state1').addClass('state2');
                inputSuperior.one('change', function(e){
                    e.preventDefault();
                    inputBase.removeAttr('checked');
                    inputSuperior.removeAttr('checked');
                });
            }else if(inputBase.is(':checked')) {
                container.removeClass('state0').removeClass('state2').addClass('state1');
                inputBase.one('change', function(e){
                    e.preventDefault();
                    inputSuperior.trigger('click');
                    inputBase.removeAttr('checked','checked');
                    inputSuperior.attr('checked','checked');
                });
            }else {
                container.removeClass('state1').removeClass('state2').addClass('state0');
                inputBase.one('change', function(e){
                    e.preventDefault();
                    inputBase.trigger('click');
                    inputBase.attr('checked','checked');
                });
            }
            console.log(inputBase.is('checked') ? 'base: true' : 'base: false');
            console.log(inputSuperior.is('checked') ? 'sup: true' : 'sup: true');
        });
    };

    disciplineCheckboxState();
    $('.js-discipline-container').css("display","block");
    $(".js-discipline-container input").on("change", function() {
        disciplineCheckboxState();
    });
});