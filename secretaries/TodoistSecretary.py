from secretaries.SecretaryBase import SecretaryBase
from services.TodoistService import TodoistService
from states.Todoist.NotAutarizedState import TodoistNotAutarizedState

class TodoistSecretary(SecretaryBase):
    def __init__(self):
        super().__init__()
        self._service = TodoistService()
        self._state = TodoistNotAutarizedState()