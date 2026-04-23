import os
from dataclasses import dataclass

@dataclass
class User:
    """Класс с тестовыми данными пользователей."""
    email: str
    password: str = os.getenv('BASE_PASSWORD', None)

CHARLI = User(email='charlie@example.com')
CHARLI2 = User(email='charlie@example.com', password='password123')
ADMIN = User(email='admin@example.com', password='admin123')
DIANA = User(email='diana@example.com', password='password123')
