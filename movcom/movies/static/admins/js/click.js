// Fonction pour mettre à jour la classe active
function setActiveLink() {
    const activeLink = localStorage.getItem('activeLink');
    if (activeLink) {
        const link = document.querySelector(`a[href="${activeLink}"]`);
        if (link) {
            // Retirer la classe active de tous les éléments
            document.querySelectorAll('.list-group-item').forEach(item => item.classList.remove('active'));
            // Ajouter la classe active à l'élément correspondant
            link.classList.add('active');
        }
    }
}

// Écouter les clics sur les éléments de la liste
document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('click', function() {
        // Retirer la classe active de tous les éléments
        document.querySelectorAll('.list-group-item').forEach(link => link.classList.remove('active'));
        // Ajouter la classe active à l'élément cliqué
        this.classList.add('active');
        // Enregistrer l'URL du lien actif dans localStorage
        localStorage.setItem('activeLink', this.getAttribute('href'));
    });
});

// Appeler la fonction pour définir le lien actif lors du chargement de la page
document.addEventListener('DOMContentLoaded', setActiveLink);