from secretaries.SecretaryBase import SecretaryBase
from services.EvernoteService import EvernoteService

class EvernoteSecretary(SecretaryBase):
    def __init__(self):
        super().__init__()
        self._service = EvernoteService()