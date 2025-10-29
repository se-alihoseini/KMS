import abc
from pydantic import BaseModel

class UseCaseInterface(metaclass=abc.ABCMeta):
    def execute(self, request_model: BaseModel):
        try:
            return self.process_request(request_model)
        except Exception as err:
            raise Exception(err)

    @abc.abstractmethod
    def process_request(self, payload: BaseModel):
        pass
