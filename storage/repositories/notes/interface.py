import typing as t
from abc import ABCMeta, abstractmethod

from knb.models import Note


class INotesRepository(metaclass=ABCMeta):
    @abstractmethod
    def all_notes(self) -> t.List[Note]:
        """

        """

    @abstractmethod
    def get(self, id: str) -> Note:
        """

        """

    @abstractmethod
    def save(self, note: Note) -> t.Tuple[Note, str]:
        """

        """

    @abstractmethod
    def update(self, old_note_id: str, note: Note):
        """

        """
