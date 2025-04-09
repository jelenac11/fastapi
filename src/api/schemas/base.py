from pydantic import BaseModel
from sqlalchemy import inspect

from models.base import Base


class SafeBaseModel(BaseModel):
    @classmethod
    def from_orm_safe(cls: type["SafeBaseModel"], instance: Base) -> "SafeBaseModel":
        data = {}
        insp = inspect(instance)

        for name in cls.model_fields:
            if name in insp.unloaded:
                continue
            value = getattr(instance, name, None)
            data[name] = value

        return cls.model_construct(**data, _fields_set=set(data.keys()))
