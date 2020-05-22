import typing as t

from knb.errors import NotFoundError
from knb.models import Note


class Repository:
    def __init__(self):
        self._notes = {}

    def all_notes(self) -> t.List[Note]:
        return list(self._notes.values())

    def get(self, id: str) -> Note:
        if not self._notes.get(id):
            raise NotFoundError(type="note", id=id)
        return self._notes[id]

    def save(self, note: Note) -> t.Tuple[Note, str]:
        id_ = self.__newid()
        self._notes[id_] = note
        return note, id_

    def __newid(self) -> str:
        if not self._notes:
            return str(1)
        lastid = list(self._notes.keys())[-1]
        return str(int(lastid) + 1)
