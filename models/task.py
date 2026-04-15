from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from datetime import datetime

# Перечисление для приоритета
class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# Перечисление для статуса
class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

# Модель одной задачи
class UserMeTaskResponse(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    parent_task_id: Optional[int] = None  # может быть null
    created_by: int
    created_at: datetime                 # автоматически преобразуется из ISO-строки
    id: int
    status: StatusEnum
    order: int
    board_id: int
    assignee_id: Optional[int] = None    # может быть null
    updated_at: datetime

    class Config:
        # Позволяет использовать алиасы полей, если нужно (необязательно)
        # и задаёт формат сериализации datetime
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Тип для всего ответа – список задач
UserMeTaskListResponse = List[UserMeTaskResponse]
