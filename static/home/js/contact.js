document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".msg-card");

    cards.forEach(card => {

        // دکمه X برای بستن دستی
        const closeBtn = card.querySelector(".msg-close");

        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                card.classList.add("fade-out");
                setTimeout(() => card.remove(), 500);
            });
        }

        // بستن خودکار بعد از 5 ثانیه
        setTimeout(() => {
            card.classList.add("fade-out");
            setTimeout(() => card.remove(), 500);
        }, 5000);

    });

});
document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".msg-card");

    cards.forEach(card => {

        // دکمه X برای بستن دستی
        const closeBtn = card.querySelector(".msg-close");

        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                card.classList.add("fade-out");
                setTimeout(() => card.remove(), 500);
            });
        }

        // بستن خودکار بعد از 5 ثانیه
        setTimeout(() => {
            card.classList.add("fade-out");
            setTimeout(() => card.remove(), 500);
        }, 5000);

    });

});
