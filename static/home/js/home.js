// ----------- DOM Ready -----------
document.addEventListener("DOMContentLoaded", function () {
    // عناصر مورد نیاز
    const navLinks = document.querySelectorAll(".nav a[href^='#']");
    const navToggle = document.querySelector(".nav-toggle");
    const nav = document.querySelector(".nav");
    const posts = document.querySelectorAll(".post");

    // ----------- اسکرول نرم روی منوها -----------
    navLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");

            // اگر لینک به سکشن خاص اشاره می‌کند (hash)
            if (targetId.startsWith("#") && targetId.length > 1) {
                const targetEl = document.querySelector(targetId);
                if (targetEl) {
                    e.preventDefault();

                    // اسکرول نرم
                    targetEl.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                    // بستن منو روی موبایل بعد از کلیک
                    if (window.innerWidth <= 768 && nav.classList.contains("nav-open")) {
                        nav.classList.remove("nav-open");
                    }
                }
            }
        });
    });

    // ----------- موبایل منو (باز/بسته کردن) -----------
    if (navToggle && nav) {
        navToggle.addEventListener("click", function () {
            nav.classList.toggle("nav-open");
        });
    }

    // ----------- افکت ساده روی کارت‌های پست -----------
    posts.forEach(post => {
        post.addEventListener("mouseenter", function () {
            this.classList.add("post-hovered");
        });

        post.addEventListener("mouseleave", function () {
            this.classList.remove("post-hovered");
        });

        // روی موبایل: کلیک کردن پست → اسکرول کمی پایین‌تر (احساس focus)
        post.addEventListener("click", function () {
            if (window.innerWidth <= 768) {
                this.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
            }
        });
    });
});
