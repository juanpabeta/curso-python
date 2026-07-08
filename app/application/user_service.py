from infrastructure.file_repository import FileRepository


class UserService:

    def __init__(self, repository: FileRepository):
        self.repository = repository

    def procesar(self):
        return self.repository.read_users()
