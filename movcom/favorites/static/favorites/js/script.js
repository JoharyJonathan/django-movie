$(document).ready(function() {
    $('#search-input').on('keyup', function() {
        let query = $(this).val();
        $.ajax({
            url: "{% url 'search-movies' %}",
            data: {
                'query': query
            },
            dataType: 'json',
            success: function(response) {
                $('#search-results').empty(); // Vider les résultats précédents
                if (response.movies.length > 0) {
                    $.each(response.movies, function(index, movie) {
                        $('#search-results').append(
                            '<div class="movie-item">' +
                            '<img src="' + movie.poster_url + '" alt="' + movie.title + '" style="width: 50px; height: 50px;">' +
                            '<span>' + '<a href="' + movie.detail_url + '">' + movie.title + '</a>' + '</span>' +  // Utiliser l'URL du détail
                            '</div>'
                        );
                    });
                } else {
                    $('#search-results').append('<p>No movies found.</p>');
                }
            }
        });
    });
});