from .serializers import AccessTokenlistSerializer
from .models import AccessTokenlist
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .service import Service
import re


class PRStatus:

    @api_view(["POST"])
    def get_pr_status(request, pk, organization=None, repository=None, pr=None):
        try:
            data = AccessTokenlist.objects.get(id=pk)
        except AccessTokenlist.DoesNotExist:
            return JsonResponse({"status":"404", "message": "Invalid Access Token Id "+pk})

        if request.method == 'POST':
            try:
                serializer = AccessTokenlistSerializer(data)
                service = Service(serializer.data['value'])
                if organization is not None:
                    if re.findall('/', organization):
                        if repository.isdigit() and (pr is None):
                            pr = repository
                        organization, repository = organization.split("/")
                if pr is not None:
                    result = service.get_pr_data(organization, repository, pr)
                    print(result)
                else:
                    print(organization, repository)
                    result = service.get_pr_list(organization, repository)
                if isinstance(result, Exception):
                    if result.args[0] == 404:
                        return JsonResponse({"code": 404,
                                             "message": "One of the following arguments" +
                                                        " not found on GitHub. Organization " +
                                             organization + ", Repository " + repository + ", PR " + pr})
                    else:
                        return JsonResponse({"code": result.args[0],
                                             "Message": result.args[1]["message"],
                                             "Reference": result.args[1]["documentation_url"]})
                return JsonResponse(result)

            except Exception as result:
                return JsonResponse({"Message": str(result)})