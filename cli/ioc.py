import os

import typing as t


def __init():
    from knb.models import User
    from storage.repositories.users import dict_memory
    from storage.gateways import list_notes_gateway as list_notes
    from storage.gateways import create_note_gateway as create_note
    from storage.gateways import group_notes
    from storage.repositories.notes import json_file

    users_repo = dict_memory.Repository()
    users_repo.users["1"] = User("admin", "first", "last", "middle")

    notes_repo = json_file.Repository(os.path.curdir + "/notes.knb")

    list_notes_gateway = list_notes.Gateway(notes_repo, users_repo)
    create_note_gateway = create_note.Gateway(notes_repo, users_repo)
    group_notes_gateway = group_notes.Gateway(notes_repo, users_repo)
    return [list_notes_gateway, create_note_gateway, group_notes_gateway]


list_notes_gateway, create_note_gateway, group_notes_gateway = __init()


class IoC:
    def __init__(self):
        self.__deps = {}

    def get_dependency(self, name: str) -> t.Any:
        return self.__deps[name]
