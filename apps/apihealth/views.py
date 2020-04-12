from django.http import JsonResponse


# Create your views here.
def api_health(request):
    """
    API Health Check which will returns 200.
    """
    data = {
        "success": True
    }
    return JsonResponse(data)
