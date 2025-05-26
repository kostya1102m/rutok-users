class UserAlreadyExistsError(Exception):
    """Исключение, когда пользователь с указанным email уже существует."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Пользователь с email {email} уже зарегистрирован")

class RoleNotFoundError(Exception):
    """Исключение, когда роль с указанным ID не найдена."""
    def __init__(self, role_id: int):
        self.role_id = role_id
        super().__init__(f"Роль с id {role_id} не найдена")

class DataValidationError(Exception):
    """Исключение для ошибок валидации данных."""
    def __init__(self, message: str):
        super().__init__(message)