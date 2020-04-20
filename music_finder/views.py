from django.http import JsonResponse

def search(request):
    return JsonResponse({
        "message": "nothing to see here"
    })
