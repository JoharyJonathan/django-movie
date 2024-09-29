function setEditUserDetails(element) {
    const userId = element.getAttribute('data-user-id');
    document.getElementById('editUserId').value = userId;

    // Récupérez d'autres informations à partir d'une API ou d'une structure de données existante
    // Exemple: remplissez le formulaire avec les détails de l'utilisateur
    // Vous devrez appeler une fonction pour récupérer les détails de l'utilisateur (par exemple, avec une requête AJAX)
}

$(document).ready(function() {
    $('#editUserForm').submit(function(event) {
        event.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: "{% url 'edit-user' user_id=editUserId.value %}",  // Changez cette URL selon votre endpoint
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    location.reload(); // Recharger la page
                } else {
                    alert(response.message);
                }
            },
            error: function(response) {
                alert('An error occurred while updating the user profile.');
            }
        });
    });
});