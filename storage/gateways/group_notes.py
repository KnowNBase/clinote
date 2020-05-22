import typing as t
from typing_extensions import Protocol

from knb.models import Note, User
from knb.use_cases import specs
from knb.use_cases.group_by_tag import IGateway


class IUsersRepo(Protocol):
    def get_user(self, user_id: str) -> User:
        ...


class INotesRepository(Protocol):
    def all_notes(self, spec: specs.Spec) -> t.List[Note]:
        ...


class Gateway(IGateway):
    def __init__(self, notes_repo: INotesRepository, users_repo: IUsersRepo):
        self._notes = notes_repo
        self._users = users_repo

    def get_user(self, user_id: str) -> User:
        return self._users.get_user(user_id)

    def load_notes(self, spec: specs.Spec) -> t.List[Note]:
        return self._notes.all_notes(spec)
