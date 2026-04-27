// ----------- DOM Ready -----------
document.addEventListener("DOMContentLoaded", function () {

    // ----------- عناصر مورد نیاز -----------
    const navLinks = document.querySelectorAll(".nav a[href^='#']");
    const navToggle = document.querySelector(".nav-toggle");
    const nav = document.querySelector(".nav");
    const posts = document.querySelectorAll(".post");


    // ----------- نمایش پست‌ها هنگام اسکرول -----------
    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                observer.unobserve(entry.target);
            }
        });

    }, {
        threshold: 0.1
    });

    posts.forEach(post => {
        observer.observe(post);
    });


    // ----------- اسکرول نرم روی منوها -----------
    navLinks.forEach(link => {
        link.addEventListener("click", function (e) {

            const targetId = this.getAttribute("href");

            // اگر لینک به سکشن خاص اشاره می‌کند
            if (targetId.startsWith("#") && targetId.length > 1) {

                const targetEl = document.querySelector(targetId);

                if (targetEl) {
                    e.preventDefault();

                    targetEl.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                    // بستن منو در موبایل
                    if (window.innerWidth <= 768 && nav && nav.classList.contains("nav-open")) {
                        nav.classList.remove("nav-open");
                    }
                }
            }
        });
    });


    // ----------- باز/بسته کردن منو در موبایل -----------
    if (navToggle && nav) {
        navToggle.addEventListener("click", function () {
            nav.classList.toggle("nav-open");
        });
    }


    // ----------- افکت کارت پست‌ها -----------
    posts.forEach(post => {

        // hover دسکتاپ
        post.addEventListener("mouseenter", function () {
            this.classList.add("post-hovered");
        });

        post.addEventListener("mouseleave", function () {
            this.classList.remove("post-hovered");
        });

        // موبایل: فوکوس روی پست
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
