from services.ServiceBase import ServiceBase
from states.Todoist.NotAutarizedState import TodoistNotAutarizedState
from todoist import TodoistAPI
from db.mymodels import *

class TodoistService(ServiceBase):
    state_pull = set()

    def __init__(self):
        super().__init__()
        # self._api = api.TodoistAPI('6e8811757637846d3671fa121cf670a0accd5803')

    @staticmethod
    def get_auth_url():
        return 'https://todoist.com/oauth/authorize?client_id=fb26051eb06649bb968791f3d7c2f185&scope=data:read_write&state={user_id}'

    @staticmethod
    def get_start_state():
        return TodoistNotAutarizedState()

    def _api_for_user(self, user_id):
        acc = Subscription.get(Subscription.messenger_user_id == user_id).account
        api = TodoistAPI(AccessToken.get(AccessToken.account == acc).token)
        api.sync()
        return api

    def get_project_names(self, user_id):
        api = self._api_for_user(user_id)
        # TODO user can login with email and password

        projects = api.projects.all()
        return [proj['name'] for proj in projects]

    def project_name_to_id(self, proj_name, api):
        projects = api.projects.all()
        return [proj['id'] for proj in projects if proj['name'] == proj_name][0]

    def add_task(self, content, project,  user_id, date_string=''):
        api = self._api_for_user(user_id)
        api.items.add(content=content, project_id=self.project_name_to_id(project, api),
                      date_string=date_string)
        api.commit()

    def delete_task(self, task, proj, user_id):
        api = self._api_for_user(user_id)

        task_id = [item['id'] for item in api.items.all() if item['content'] == task
         and item['project_id'] == self.project_name_to_id(api=api, proj_name=proj)][0]

        item = api.items.get_by_id(task_id)
        item.delete()
        api.commit()

    def get_task(self, task_name, proj_name, user_id):
        api = self._api_for_user(user_id)

        return [item['content'] for item in api.items.all() if item['content'] == task_name
                         and item['project_id'] == self.project_name_to_id(api=api, proj_name=proj_name)][0]