import typing as t

from cli import ioc
from cli.generator.docopt_generator import DocOptChain
from cli.presentors.note_presentor import present_note
from glue.chain import PresenterTwiks
from knb.use_cases import list_notes


def output_presentor(output: list_notes.Output, _: PresenterTwiks):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)
    else:
        if not output.notes:
            print("no notes yet. Create one!")
        for note in output.notes:
            present_note(note)
            print()


def input_parser(args: t.Dict[str, t.Any], _: PresenterTwiks) -> list_notes.Input:
    pg = args["PAGE"]
    if not pg:
        pg = 1

    return list_notes.Input("1", pg)


list_notes_chain = DocOptChain(
    usecase=list_notes.UseCase,
    dependencies=dict(gateway=ioc.list_notes_gateway),
    name="list",
    command_doc="""
                List 
                Usage:
                    list [PAGE]
                """,
    parse_input=input_parser,
    present_output=output_presentor,
)
