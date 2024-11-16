document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('#search-input');
    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        const messages = document.querySelectorAll('.message');
        if(message)
        messages.forEach(function(msg) {
            const text = msg.textContent.toLowerCase();
            if (text.includes(filter)) {
                msg.style.display = '';
            } else {
                msg.style.display = 'none';
            }
        });
    });
});
