window.onload = function() {
    setTimeout(function() {
        const messageContainer = document.getElementById('message-container');
        if (messageContainer) {
            messageContainer.style.display = 'none';
        }
    }, 3000);  // 5000 milliseconds = 5 seconds
};


function removeSelectedFavorites() {
    const form = document.getElementById('favorites-form');
    const formData = new FormData(form);
    const csrfToken = formData.get('csrfmiddlewaretoken');

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.json())
      .then(data => {
        if (data.success) {
            alert('Selected jobs removed from favorites.');
            // Optionally, remove the items from the DOM or refresh part of the page
            window.location.reload();  // If you want to simply reload the favorites
        } else {
            alert('Failed to remove jobs from favorites.');
        }
    }).catch(error => {
        console.error('Error removing favorite jobs:', error);
    });
}