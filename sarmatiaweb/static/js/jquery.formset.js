$(document).ready(function() {
    $('.add-item').click(function(ev) {
        ev.preventDefault();
        var count = $('#bosses-form-container').children().length;
        var tmplMarkup = $('#bosses-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#bosses-form-container').append(compiledTmpl);

        // update form count
        $('#id_bosses-TOTAL_FORMS').attr('value', count+1);

    });
});