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

const toggler = document.querySelector(".toggler");
const navbar = document.querySelector("#main-nav");
const rightLinks = document.querySelectorAll(".right-link");
let isAppended = false;

toggler.addEventListener("click", () => {
  if (navbar.className === "main-responsive") {
    navbar.className = "main";
    appendedElements = [];
  } else {
    navbar.className = "main-responsive";
    rightLinks.forEach((link) => {
      if (!isAppended) {
        navbar.appendChild(link.cloneNode(true));
      }
    });
    isAppended = true;
  }
});

window.onload = () => {
  hideMessages();

  const orderStatusElements = document.querySelectorAll(".order-status");
  orderStatusElements.forEach((statusElement) => {
    const status = statusElement.textContent.toLowerCase();
    statusElement.classList.add(`status-${status}`);
  });
};

document.addEventListener('DOMContentLoaded', function() {
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
});

