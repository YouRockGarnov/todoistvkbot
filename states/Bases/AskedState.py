from states.Bases.StateBase import StateBase

class AskedState(StateBase):
    positive_answers = []
    negative_answers = []

    def __init__(self, auth_state_type, success_func, success_data):
        super().__init__()
        self._auth_state_type = auth_state_type # иначе они друг друга импортят
        self._success_func = success_func
        self._success_data = success_data
        AskedState.create_answers()

    def get_default_next_state(self):
        pass

    def act(self, data, service):
        message = data['object']['body']

        if message in AskedState.negative_answers:
            self._messages = ['Попробуйте переформулировать описание задачи.'] # TODO сделать поумнее
            self._next_state = self
        elif not message in AskedState.positive_answers:
            self._messages = ['Я не понял ответа. Ответьте да или нет, пожалуйста.']
            self._next_state = self
        else:
            self._next_state = self._auth_state_type()
            self._success_func(**self._success_data)
            self._messages = []

    @staticmethod
    def create_answers():
        if AskedState.positive_answers == []:
            AskedState.positive_answers = AskedState._wrap(['Да', 'Ага', 'Верно', 'Правильно', 'Угу'])
            AskedState.negative_answers = AskedState._wrap(['Нет', 'Не', 'Неверно', 'Неправильно', 'Неа'])

    @staticmethod
    def _wrap(answers):
        answers += [word.lower() for word in answers]
        with_point = [word + '.' for word in answers]
        with_exclamation = [word + '!' for word in answers]

        answers += with_point
        answers += with_exclamation

        return answers