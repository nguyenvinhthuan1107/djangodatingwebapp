
from django.http import JsonResponse
from user.models import User

def getJson(request):
    obj = User.objects.all()
    data = { "result" :list(obj.values("_id", "name", "age", "adress"))
            }
    return JsonResponse(data)
