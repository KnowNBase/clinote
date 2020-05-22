import typing as t

from knb.errors import NotFoundError
from knb.models import Note, User
from knb.use_cases.create_note import IGateway
from storage.repositories.notes.interface import INotesRepository


class Gateway(IGateway):
    def __init__(self, note_repo: INotesRepository, user_repo):
        self.users = user_repo
        self.note_repo = note_repo

    def get_user(self, user_id: str) -> User:
        user = self.users.get_user(user_id)
        if user is None:
            raise NotFoundError("user", user_id)
        return user

    def save_note(self, note: Note) -> t.Tuple[Note, str]:
        return self.note_repo.save(note)
