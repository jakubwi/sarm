jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
    $('#slectAll').click(function(){
        var checked = !$(this).data('checked');
        $('input:checkbox').prop('checked', checked);
        $(this).data('checked', checked);
    });
});
