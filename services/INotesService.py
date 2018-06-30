from services.ServiceBase import ServiceBase
from pyicloud import PyiCloudService
from pyicloud.services.reminders import 

class INotesService(ServiceBase):
    def _connect_to_service(self):
        self._api = PyiCloudService('jappleseed@apple.com', 'password')