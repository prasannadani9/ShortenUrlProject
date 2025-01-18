import hashlib
from datetime import datetime, timedelta
import uuid, base64
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import AccessLogs, UrlDataMainModel

def shorten_url(main_url, expiry_in_mins):
    length = 4
    hash_object = hashlib.sha256(main_url.encode())
    unique_element = hash_object.hexdigest()[:length]
    random_uuid = uuid.uuid4()
    short_uuid = base64.urlsafe_b64encode(random_uuid.bytes).rstrip(b'=').decode('utf-8')
    short_url = f"https://myshort.ly/{short_uuid}/{unique_element}"
    expiry_time = datetime.now() + timedelta(minutes=expiry_in_mins)
    return short_url, expiry_time

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If the request is behind a proxy, the real IP will be the first one in the list
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def access_log_entry(request, short_url):
    url_data = get_object_or_404(UrlDataMainModel, short_url=short_url)
    entry = AccessLogs.objects.create(
        short_url = url_data,
        timestamp = timezone.now(),
        ip_address = get_client_ip(request)
    )