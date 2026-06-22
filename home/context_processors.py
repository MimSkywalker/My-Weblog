
from django.contrib.auth import get_user_model

User = get_user_model()


def site_author(request):

    mohammad = User.objects.filter(username="mohammad").first()

    # خروجی حتماً باید یک دیکشنری باشد تا کلید آن در HTML قابل استفاده شود
    return {
        'mohammad': mohammad
    }
