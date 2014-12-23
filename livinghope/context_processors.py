from livinghope.models import Service

def services_processor(request):
	services = Service.objects.all()
	return {'services': services}

def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'
        
    return {'BASE_URL': scheme + request.get_host(),}