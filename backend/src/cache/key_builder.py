import hashlib
import inspect
from typing import Callable


class KeyBuilder:
    def __init__(self, prefix: str, func: Callable, *args, **kwargs) -> None:
        self.prefix = prefix
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        bound.arguments.pop("self", None)
        self.id = bound.arguments.pop("id", None)
        self.params = ":".join(
            f"{name}={value}" for name, value in bound.arguments.items()
        )

    @property
    def key(self):
        if self.id:
            return f"{self.prefix}:retrieve:{self.id}"
        hash_payload = (
            f":{hashlib.blake2b(self.params.encode(), digest_size=16).hexdigest()}"
            if self.params
            else ""
        )
        return f"{self.prefix}:list{hash_payload}"
