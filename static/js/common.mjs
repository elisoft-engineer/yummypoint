const handleNavbarToggler = () => {
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
}
  
const handleOrderStatusElements = () => {
    const orderStatusElements = document.querySelectorAll(".order-status");
    orderStatusElements.forEach((statusElement) => {
    const status = statusElement.textContent.toLowerCase();
    statusElement.classList.add(`status-${status}`);
    });
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