import json
import os.path as path
import typing as t

import utils.json as dsjson
from knb.errors import NotFoundError
from knb.models import Note, Tag, User
from storage.repositories.notes.interface import INotesRepository


class Repository(INotesRepository):
    SPLITTER = "\nKNBSPLITTER\n"

    def __init__(self, filepath):
        self.__notes_file = filepath
        self._notes = {}
        if path.isfile(filepath):
            with open(filepath, encoding="utf8") as f:
                data = f.read()
                if data:
                    notes = json.loads(data)
                    for id_, note in notes.items():
                        self._notes[id_] = self.__parse_note(note)

    def all_notes(self):
        return list(self._notes.values())

    def get(self, id: str) -> Note:
        if not self._notes.get(id):
            raise NotFoundError(type="note", id=id)
        return self._notes[id]

    def save(self, note: Note) -> t.Tuple[Note, str]:
        id_ = self.__newid()
        self._notes[id_] = note
        self.sync_to_file()
        return note, id_

    def update(self, old_note_id: str, note: Note):
        self._notes[old_note_id] = note

    def __newid(self) -> str:
        if not self._notes:
            return str(1)
        lastid = list(self._notes.keys())[-1]
        return str(int(lastid) + 1)

    @staticmethod
    def __parse_note(data: dict) -> Note:
        tags = [Tag(**d) for d in data["tags"]]
        return Note(
            summary=data["summary"],
            content=data["content"],
            tags=tags,
            author=User(**data["author"]),
        )

    def sync_to_file(self):
        with open(self.__notes_file, "w", encoding="utf8") as f:
            data = dsjson.dumps(self._notes, indent=2)
            f.write(data)

