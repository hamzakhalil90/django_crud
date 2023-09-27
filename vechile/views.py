from rest_framework.viewsets import ModelViewSet
from .controller import *


vechile_controller = VechileController()
make_controller = MakeController()

class VechileAPIView(ModelViewSet):
    def get(self,request):
        return vechile_controller.get(request)

    def post(self,request):
        return vechile_controller.post(request)

    def update(self,request):
        return vechile_controller.update(request)

    def delete(self,request):
        return vechile_controller.delete(request)


class MakeAPIView(ModelViewSet):
    def get(self,request):
        return make_controller.get(request)

    def post(self,request):
       return make_controller.post(request)

    def update(self,request):
        return make_controller.update(request)

    def delete(self,request):
        return make_controller.delete(request)