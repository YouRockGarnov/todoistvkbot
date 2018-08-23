from states.Evernote.WaitForAutorizeState import WaitForAutorizeState
from states.Bases.NotAutarizedState import NotAutarizedState

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class TodoistNotAutarizedState(NotAutarizedState):
    def __init__(self):
        super().__init__()
        self._mess_ending = '\nРазрешите нашему приложению доступ к аккаунту.'

    def act(self, data, service):
        super().act(data, service)

        user_id = data['object']['user_id']
        self.messages[0] = self.messages[0].format(user_id=user_id)
            # я кидаю в url state=user_id - чтобы знать на какого пользователя пришел ответ от todoists

        from services.TodoistService import TodoistService
        TodoistService.state_pull.add(user_id)
            # чтобы знать какие состояния может прислать обратно todoist
