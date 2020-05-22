import typing as t

from cli import ioc
from cli.generator.docopt_generator import DocOptChain
from cli.presentors.note_presentor import present_note
from glue.chain import PresenterTwiks
from knb.use_cases import group_by_tag


def output_presentor(output: group_by_tag.Output, flags: PresenterTwiks):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)
    else:
        if not output.groups:
            print("no notes yet. Create one!")
        for group, notes in output.groups.items():
            print("#", group.name)
            for note in notes:
                if flags.get("summary_only"):
                    print("\t", note.summary)
                else:
                    present_note(note)
                print()


def input_parser(args: t.Dict[str, t.Any], flags: PresenterTwiks) -> group_by_tag.Input:
    flags["summary_only"] = args["--summary"]
    return group_by_tag.Input("1")


cmd_help = """Show notes grouped by tags 
Usage:
    show-groups [options]

Options:
    -s --summary     show only summary of notes
"""

group_by_tag_chain = DocOptChain(
    usecase=group_by_tag.UseCase,
    dependencies=dict(gateway=ioc.list_notes_gateway),
    name="show-groups",
    command_doc=cmd_help,
    parse_input=input_parser,
    present_output=output_presentor,
)
