// حذف کلاس no-js وقتی جاوااسکریپت فعال است
document.documentElement.classList.remove("no-js");

document.addEventListener("DOMContentLoaded", () => {

    // ---------------- عناصر ----------------
    const posts = document.querySelectorAll(".post");
    const sidebarLinks = document.querySelectorAll(".sidebar-nav a");
    const navLinks = document.querySelectorAll("a[href^='#']");
    const nav = document.querySelector(".nav");
    const navToggle = document.querySelector(".nav-toggle");


    // ---------------- فعال شدن لینک صفحه ----------------
    const currentPath = window.location.pathname;

    sidebarLinks.forEach(link => {

        const linkPath = new URL(link.href).pathname;

        if (linkPath === currentPath) {
            link.classList.add("active");
        }

    });


    // ---------------- نمایش پست‌ها هنگام اسکرول ----------------
    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                observer.unobserve(entry.target);
            }
        });

    }, { threshold: 0.1 });

    posts.forEach(post => observer.observe(post));


    // ---------------- اسکرول نرم ----------------
    navLinks.forEach(link => {

        link.addEventListener("click", function (e) {

            const targetId = this.getAttribute("href");

            if (targetId.startsWith("#")) {

                const target = document.querySelector(targetId);

                if (target) {
                    e.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }

            }

        });

    });


    // ---------------- منوی موبایل ----------------
    if (navToggle && nav) {

        navToggle.addEventListener("click", () => {
            nav.classList.toggle("nav-open");
        });

    }


    // ---------------- افکت پست ----------------
    posts.forEach(post => {

        post.addEventListener("mouseenter", () => {
            post.classList.add("post-hovered");
        });

        post.addEventListener("mouseleave", () => {
            post.classList.remove("post-hovered");
        });

        if (window.innerWidth <= 768) {
            post.addEventListener("click", () => {
                post.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
            });
        }

    });

});
