from typing import Type
from models.base import Base
from pydantic import BaseModel
from sqlalchemy import inspect


class SafeBaseModel(BaseModel):
    @classmethod
    def from_orm_safe(cls: Type["SafeBaseModel"], instance: Base) -> "SafeBaseModel":
        data = {}
        insp = inspect(instance)

        for name, field in cls.model_fields.items():
            if name in insp.unloaded:
                continue
            value = getattr(instance, name, None)
            if isinstance(value, BaseModel):
                data[name] = value
            elif hasattr(field.annotation, "model_validate"):
                data[name] = field.annotation.model_validate(value) if value else None  # type: ignore
            else:
                data[name] = value  # type: ignore

        return cls.model_construct(**data, _fields_set=set(data.keys()))
