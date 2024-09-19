$(document).ready(function() {
    $('#search-input').on('input', function() {
        let query = $(this).val();
        let url = $(this).data('url');  // Récupère l'URL depuis l'attribut data-url
        console.log("URL utilisée : " + url);  // Affiche l'URL dans la console
        $('#spinner').show();  // Afficher le spinner
        if (query.length > 0) {
            $.ajax({
                url: url,  // Utilisation de l'URL dynamique
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    $('#spinner').hide();  // Cacher le spinner
                    $('#search-results').empty();  // Effacer les anciens résultats

                    if (data.movies.length > 0) {
                        data.movies.forEach(function(movie) {
                            // Créer un lien cliquable pour chaque film avec un URL dynamique vers sa page de détail
                            let detailUrl = `http://127.0.0.1:8000/movies/detail/${movie.id}/`;  // Remplacez cette URL si nécessaire
                            console.log(movie.id)
                            $('#search-results').append(
                                `<a class="list-group-item" href="${detailUrl}">${movie.title}</a>`
                            );
                        });
                    } else {
                        $('#search-results').append('<li class="list-group-item">No results found</li>');
                    }
                }
            });
        } else {
            $('#spinner').hide();  // Cacher le spinner si aucun texte n'est entré
            $('#search-results').empty();
        }
    });
});