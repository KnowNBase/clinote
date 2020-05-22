import storage.repositories.notes.dict_memory as notes_memory
import storage.repositories.users.dict_memory as users_memory
from knb.use_cases.specs import PageSpec
from storage.gateways.list_notes_gateway import Gateway
from utils.tests import generate_note


def test_list_page1():
    notes_repo = notes_memory.Repository()
    users_repo = users_memory.Repository()
    gw = Gateway(notes_repo, users_repo)
    gw.notes._notes = {str(i): generate_note() for i in range(0, 150)}
    spec = PageSpec(1, 100)

    notes = gw.load_notes(spec)

    assert len(notes) == 100

    spec = PageSpec(2, 100)

    notes = gw.load_notes(spec)

    assert len(notes) == 50
