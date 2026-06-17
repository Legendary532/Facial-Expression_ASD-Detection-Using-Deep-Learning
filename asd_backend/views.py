from django.http import JsonResponse

def status(request):
    return JsonResponse({"status": "server is running"})

def predict(request):
    return JsonResponse({"result": "predict endpoint working"})
