document.getElementById('commentInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {  // Vérifie si la touche "Entrée" est pressée sans la touche "Shift"
        event.preventDefault();  // Empêche le retour à la ligne
        document.getElementById('commentForm').submit();  // Soumet le formulaire
    }
});