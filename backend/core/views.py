from django.http import JsonResponse
from django.utils.timezone import now


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "timestamp": now().isoformat(),
        }
    )

