$(document).ready(function() {
    $('.add-item2').click(function(ev) {
        ev.preventDefault();
        var count = $('#form-form-container').children().length;
        var tmplMarkup = $('#form-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#form-form-container').append(compiledTmpl);

        // update form count
        $('#id_form-TOTAL_FORMS').attr('value', count+1);

    });
});