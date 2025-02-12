const hideMessages = () => {
    const messages = document.querySelectorAll(".message");

    messages.forEach((message) => {
    let opacity = 1;
    const fadeInterval = setInterval(() => {
        opacity -= 0.002;
        message.style.opacity = opacity;

        if (opacity <= 0) {
        clearInterval(fadeInterval);
        message.style.display = "none";
        }
    }, 10);
    });
};

const toggleTheme = () => {
    const themeToggle = document.querySelector('#theme-toggle');
    
    if (themeToggle) {
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', newTheme);
        
        fetch(`/set-theme/${newTheme}/`)
        .then(response => response.json())
        .then(data => {
            console.log('Theme updated:', data);
        });
    });
    }
}

const getJwtToken = async () => {
    try {
        const response = await fetch('/accounts/get-jwt-token/');
        if (response.ok) {
            const data = await response.json();
            return data.access;
        } else {
            console.error('Error fetching JWT token:', response.status);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    toggleTheme();
    hideMessages();
})
  