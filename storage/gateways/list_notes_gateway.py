import typing as t

from knb.errors import NotFoundError
from knb.models import Note, User
from knb.use_cases.list_notes import IGateway
from knb.use_cases.specs import Spec, PageSpec
from storage.repositories.notes.interface import INotesRepository


class Gateway(IGateway):
    def __init__(self, notes_repo: INotesRepository, users_repo):
        self.users = users_repo
        self.notes = notes_repo

    def get_user(self, user_id: str) -> User:
        user = self.users.get_user(user_id)
        if user is None:
            raise NotFoundError("user", user_id)
        return user

    def load_notes(self, spec: Spec) -> t.List[Note]:
        result_notes = self.notes.all_notes()
        if isinstance(spec, PageSpec):
            page = spec.page - 1
            offset = spec.items_per_page * page
            limit = spec.items_per_page * (page + 1)
            result_notes = result_notes[offset:limit]
        return result_notes
