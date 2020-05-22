import tempfile

from storage.repositories.notes.json_file import Repository
from utils import factory


def test_note_create():
    _, storefile = tempfile.mkstemp()
    repo = Repository(storefile)

    assert len(repo.all_notes()) == 0
    note = factory.create_note()
    repo.save(note)
    repo.sync_to_file()
    repo = Repository(storefile)

    assert len(repo.all_notes()) == 1
    assert repo.get("1") == note

    repo.sync_to_file()
    note2 = factory.create_note()
    repo = Repository(storefile)
    n, id_ = repo.save(note2)

    assert id_ == "2"

    repo.sync_to_file()
    repo = Repository(storefile)

    assert len(repo.all_notes()) == 2
    assert repo.get("1") == note
    assert repo.get("2") == note2
