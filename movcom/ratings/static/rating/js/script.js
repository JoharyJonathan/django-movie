jQuery(document).ready(function($) {
    $(".btnrating").on('click', function() {
        var previous_value = $("#selected_rating").val();
        var selected_value = $(this).attr("data-attr");
        $("#selected_rating").val(selected_value);
        $(".selected-rating").html(selected_value);

        for (i = 1; i <= 5; ++i) {
            var $star = $("#rating-star-" + i);
            if (i <= selected_value) {
                $star.addClass('btn-warning').removeClass('btn-default');
            } else {
                $star.addClass('btn-default').removeClass('btn-warning');
            }
        }
    });
});