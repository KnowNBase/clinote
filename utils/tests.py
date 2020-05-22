from mimesis import Text, Person  # type: ignore

from knb.models import Note, User

text = Text()
person = Person()


def generate_note(author=None):
    if author is None:
        author = generate_user()
    return Note(summary=text.title(), content=text.sentence(), author=author)


def generate_user():
    return User(
        username=person.username(),
        first_name=person.first_name(),
        last_name=person.last_name(),
        middle_name=person.surname(),
    )
