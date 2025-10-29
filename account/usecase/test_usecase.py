from  backbone.interface import UseCaseInterface
from django.http import JsonResponse
from account.validators import TestUserValidator
from account.validators import TestUserValidator


class TestUserUseCase(UseCaseInterface):
    def process_request(self, payload: TestUserValidator):

        return JsonResponse(
            data={"result": f"test pass with number {payload.number}"}, status=200
        )
