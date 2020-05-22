# type: ignore

from dataclasses import is_dataclass, fields
from random import randint
import typing as t
from mimesis import Text


class DataclassFactory:
    def __init__(
        self,
        model: type,
        field_type_map: t.Dict[type, t.Callable[[str, str], t.Any]] = None,
    ):
        self.model = model
        self.__t = Text()
        if field_type_map is None:
            field_type_map = {str: lambda _, __: self.__t.title}
        self.field_type_map = field_type_map

    def create(self):
        model = self.model
        assert model is not None
        assert is_dataclass(model)
        payload = {}
        # noinspection PyDataclass
        for f in fields(model):
            if is_dataclass(f.type):
                value = DataclassFactory(f.type, self.field_type_map).create()
            elif isinstance(f.type, t.GenericMeta):
                origin_type = f.type.__extra__
                if origin_type == list:
                    if list in self.field_type_map.keys():
                        value = self.field_type_map[list](f.name, model.__name__)
                    else:
                        count = randint(0, 10)
                        item_type = f.type.__args__[0]
                        if is_dataclass(item_type):
                            gen = DataclassFactory(item_type, self.field_type_map)
                            value = [gen.create() for _ in range(count)]
                        else:
                            gen = self.field_type_map[item_type]
                            value = [gen(f.name, model.__name__) for _ in range(count)]
                elif origin_type == dict:
                    raise NotImplementedError("factory dict schema")
                else:
                    raise NotImplementedError(f"can't build extra type '{origin_type}'")
            else:
                value = self.field_type_map[f.type](f.name, model.__name__)
            payload[f.name] = value
        return model(**payload)


class PrimitiveFactory:
    def __init__(self):
        self.field_type_map = {}

    def create(self, f, model: type):
        if isinstance(f.type, t.GenericMeta):
            origin_type = f.type.__extra__
            if origin_type == list:
                count = randint(0, 10)
                item_type = f.type.__args__[0]
                if is_dataclass(item_type):
                    gen = DataclassFactory(item_type, self.field_type_map)
                    value = [gen.create() for _ in range(count)]
                else:
                    gen = self.field_type_map[item_type]
                    value = [gen(f.name, model.__name__) for _ in range(count)]
            elif origin_type == dict:
                raise NotImplementedError("factory dict schema")
            else:
                raise NotImplementedError(f"can't build extra type '{origin_type}'")
        else:
            value = self.field_type_map[f.type](f.name, model.__name__)
        return value
