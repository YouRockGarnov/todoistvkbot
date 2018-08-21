from secretaries.SecretaryBase import ServiceBase
from services.GCalendarService import GCalendarService

class GCalendarSecretary(ServiceBase):
    def __init__(self):
        super().__init__()
        self._service = GCalendarService()