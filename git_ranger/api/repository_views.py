from .serializers import AccessTokenlistSerializer
from .models import AccessTokenlist
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import HttpResponse
from .service import Service


class Repository:
    @api_view(["POST"])
    def get_repo_list(request, pk):
        try:
            data = AccessTokenlist.objects.get(id=pk)
        except AccessTokenlist.DoesNotExist:
            return JsonResponse({"status": "404", "message": "Invalid Access Token Id " + pk})

        if request.method == 'POST':
            try:
                serializer = AccessTokenlistSerializer(data)
                service = Service(serializer.data['value'])
                result = service.get_repo_list()
                if isinstance(result, Exception):
                        return JsonResponse({"code": result.args[0],
                                             "Message": result.args[1]["message"],
                                             "Reference": result.args[1]["documentation_url"]})
                return JsonResponse(result)
            except Exception as result:
                return JsonResponse({"Message": str(result)})