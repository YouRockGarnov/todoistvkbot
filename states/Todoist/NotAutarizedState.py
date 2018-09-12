from states.Todoist.WaitForAutorizeState import TodoistWaitForAutorizeState
from states.Bases.NotAutarizedState import NotAutarizedState
from tools.log import logger, logged

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class TodoistNotAutarizedState(NotAutarizedState):
    def __init__(self):
        super().__init__()
        self._mess_ending = '\nРазрешите нашему приложению доступ к аккаунту.'

    def get_default_next_state(self):
        return TodoistWaitForAutorizeState()

    def act(self, data, service):
        super().act(data, service)

        user_id = data['object']['user_id']
        self._messages[0] = self._messages[0].format(user_id=user_id)
            # я кидаю в url state=user_id - чтобы знать на какого пользователя пришел ответ от todoists

        from flask import g
        g.todoist_state_pull.add(user_id)
            # чтобы знать какие состояния может прислать обратно todoist
        logger.info('Added to state_pull in TodoistService {0}.'.format(user_id))
        logger.info(g.todoist_state_pull)
