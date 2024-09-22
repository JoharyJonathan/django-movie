// Select/Deselect all checkboxes
document.getElementById('selectAll').onclick = function() {
    var checkboxes = document.getElementsByName('genres_to_delete[]');
    for (var checkbox of checkboxes) {
        checkbox.checked = this.checked;
    }
}