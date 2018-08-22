from states.Bases.StateBase import StateBase
from states.Todoist.AutorizedState import AutorizedState

class AskedState(StateBase):
    positive_answers = []
    negative_answers = []

    def __init__(self):
        super().__init__()
        AskedState.create_answers()


    def act(self, data, service):
        message = data['object']['title']

        if message in AskedState.negative_answers:
            self._messages.append('Попробуйте переформулировать описание задачи.') # TODO сделать поумнее
            self._next_state = self
        elif not message in AskedState.positive_answers:
            self._messages.append('Я не понял ответа. Ответьте да или нет, пожалуйста.')
            self._next_state = self
        else:
            self._next_state = AutorizedState()

    @staticmethod
    def create_answers():
        if AskedState.positive_answers == []:
            positive_answers = AskedState._wrap(['Да', 'Ага', 'Верно', 'Правильно', 'Угу'])
            negative_answers = AskedState._wrap(['Нет', 'Не', 'Неверно', 'Неправильно', 'Неа'])

    @staticmethod
    def _wrap(answers):
        answers += [word.lower() for word in answers]
        with_point = [word + '.' for word in answers]
        with_exclamation = [word + '!' for word in answers]

        answers += with_point
        answers += with_exclamation

        return answers