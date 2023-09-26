from django.db import models
from utils.reusable_methods import create_response, paginate_data
from utils.response_messages import *
from utils.reusable_methods import get_first_error_message


class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseAPIController:
    serializer_class = ""
    filterset_class = ""
    feature_name = ""

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            instance = serialized_data.save()
            response_data = self.serializer_class(instance).data
            return create_response(response_data, SUCCESSFUL, 200)
        else:
            return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), 400)

    def get(self, request):
        instances = self.serializer_class.Meta.model.objects.all()

        filtered_data = self.filterset_class(request.GET, queryset=instances)
        data = filtered_data.qs

        if not data:
            return create_response({}, NO_RECORD, 200)
        paginated_data = paginate_data(data, request)
        count = data.count()

        serialized_data = self.serializer_class(paginated_data, many=True).data
        response_data = {
            "count": count,
            "data": serialized_data,
        }
        return create_response(response_data, SUCCESSFUL, 200)

    def update(self, request):
        if not "id" in request.query_params:
            return create_response({}, ID_NOT_PROVIDED, 400)
        else:
            instance = self.serializer_class.Meta.model.objects.filter(id=request.query_params.get('id')).first()
            if not instance:
                return create_response({}, NOT_FOUND, 404)

            serialized_data = self.serializer_class(instance, data=request.data, partial=True)
            if serialized_data.is_valid():
                response_data = serialized_data.save()
                return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
            else:
                return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), 400)

    def delete(self, request):
        if not "id" in request.query_params:
            return create_response({}, ID_NOT_PROVIDED, 400)
        instance = self.serializer_class.Meta.model.objects.filter(id=request.query_params.get("id")).first()
        if not instance:
            return create_response({}, NOT_FOUND, 404)
        instance.delete()
        return create_response({}, SUCCESSFUL, 200)