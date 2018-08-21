from states.Bases.StateBase import StateBase


class AutorizedState(StateBase):
    def act(self, data, service):

        # TODO добавить вопрос к пользователю о корректности добавления события

        self._next_state = self

    def parse_message(self, message, service):
        response = {}



    def parse_project(self, message: str, service):
        projects = service.get_project_names()

        contexts = ['в {0}', 'В {0}']
        for project in projects:
            inside = [c.format(project) for c in contexts if c.format(project) in message]
            if inside == []:
                return {'exists': False, 'message': message}
            else:
                return {'exists': True, 'message': message.replace(inside[0], '')}
