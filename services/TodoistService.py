from services.ServiceBase import ServiceBase


class TodoistService(ServiceBase):
    state_pull = set()

    @staticmethod
    def get_auth_url():
        return 'https://todoist.com/oauth/authorize?client_id=fb26051eb06649bb968791f3d7c2f185&scope=data:read_write&state={user_id}'