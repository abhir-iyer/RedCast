let backToTopBtn = document.createElement("button");
backToTopBtn.id = "backToTopBtn";
backToTopBtn.innerHTML = "⬆ Top";
document.body.appendChild(backToTopBtn);

// Show or hide the button on scroll
window.onscroll = function () {
    if (document.body.scrollTop > 400 || document.documentElement.scrollTop > 400) {
        backToTopBtn.style.display = "block";
        backToTopBtn.style.opacity = 1;
    } else {
        backToTopBtn.style.opacity = 0;
        setTimeout(() => {
            if (backToTopBtn.style.opacity == 0)
                backToTopBtn.style.display = "none";
        }, 300);
    }
};

// Smooth scroll to top on click
backToTopBtn.onclick = function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
};