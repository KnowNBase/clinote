from unittest.mock import Mock

from cli.generator.docopt_generator import Generator, DocOptChain
from knb.use_cases import create_note
from utils.tests import generate_note


# noinspection PyUnresolvedReferences
def test_create_one_command():
    note = generate_note()
    gw: IGateway = Mock()
    gw.save_note.return_value = (note, "1")
    gw.get_user.return_value = note.author
    input_parser = Mock()
    input_parser.return_value = create_note.Input(
        user_id="1", summary=note.summary, content=note.content
    )
    output_presentor = Mock()
    chains = [
        DocOptChain(
            usecase=create_note.UseCase,
            dependencies=dict(gateway=gw),
            name="mk",
            command_doc="""
            Usage:
                mk <summary> [CONTENT]
            """,
            parse_input=input_parser,
            present_output=output_presentor,
        )
    ]
    g = Generator()
    commands = g(chains)
    assert commands
    create_note_cmd = commands["mk"]
    create_note_cmd([note.summary, note.content])
    gw.save_note.assert_called_with(note)
