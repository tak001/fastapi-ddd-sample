from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class EntityId:
    value: str

    @classmethod
    def generate(cls) -> "EntityId":
        return cls(value=uuid.uuid4().hex)
