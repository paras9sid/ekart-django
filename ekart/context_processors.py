from django.conf import settings


def paypal_client_id(request):
    return {
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID
    }