import typing as t

import mimesis  # type: ignore

from knb.models import User, Note, Tag


def create_user():
    person = mimesis.Generic().person
    return User(
        username=person.username(),
        first_name=person.first_name(),
        last_name=person.last_name(),
        middle_name=person.surname(),
    )


def create_note(tags: t.List[Tag] = None) -> Note:
    if tags is None:
        tags = []
    text = mimesis.Generic().text
    return Note(
        summary=text.title(),
        content=text.text(),
        tags=tags,
        author=create_user()
    )
