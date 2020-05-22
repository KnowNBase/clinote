from knb.models import Note


def present_note(note: Note):
    print(note.summary)
    print("-" * len(note.summary))
    if note.tags:
        tags_str = ", ".join(["#" + tag.name for tag in note.tags])
        print(f"<< {tags_str} >>")
    print()
    if note.content:
        print(note.content)
