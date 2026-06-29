const CaptchaLoader = {
    isLoaded: false,
    readyPromise: null,

    init: function(formSelector, siteKey) {
        const form = document.querySelector(formSelector);
        if (!form) {
            console.warn("CaptchaLoader: فرم پیدا نشد →", formSelector);
            return;
        }

        // بارگذاری reCAPTCHA هنگام تمرکز (Lazy)
        const loadCaptcha = () => {
            if (!this.isLoaded) {
                this.readyPromise = new Promise((resolve) => {
                    const script = document.createElement('script');
                    script.src = `https://www.google.com/recaptcha/api.js?render=${siteKey}`;
                    script.async = true;
                    script.onload = () => grecaptcha.ready(resolve);
                    document.head.appendChild(script);
                });
                this.isLoaded = true;
            }
        };

        form.addEventListener('focusin', loadCaptcha, { once: true });

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            // ✅ اگر هنوز لود نشده (کاربر مستقیم Submit زد)، اول لود کن
            loadCaptcha();

            this.readyPromise.then(() => {
        grecaptcha.execute(siteKey, { action: 'contact' }).then((token) => {
            // ✅ این input را که django_recaptcha ساخته پیدا کن و مقدارش را بده
            let input = form.querySelector('input[name="captcha"]');
            if (!input) {
                input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'captcha';
                form.appendChild(input);
            }
            input.value = token;
            form.submit();
                });
            });
        });
    }
};