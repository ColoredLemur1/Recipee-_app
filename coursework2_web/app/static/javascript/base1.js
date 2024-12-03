function toggleLike(event, button) {
    event.preventDefault();
    const icon = button.querySelector('i');
    if (icon.classList.contains('bi-heart')) {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
        button.innerHTML = '<i class="bi bi-heart-fill"></i> Unlike';
    } else {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
        button.innerHTML = '<i class="bi bi-heart"></i> Like';
    }
    button.closest('form').submit();
}