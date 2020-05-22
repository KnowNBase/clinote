import subprocess
import sys
import typing as t
from itertools import filterfalse, chain

from cli import ioc  # type: ignore
from cli.generator.docopt_generator import DocOptChain
from cli.presentors.note_presentor import present_note
from glue.chain import PresenterTwiks
from knb.use_cases import create_note

EOF_ENTER_TIMES = 2


def output_presentor(output: create_note.Output, _: PresenterTwiks):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)

    else:
        print("create note with id:", output.id)
        note = output.note
        if note is None:
            raise NotImplementedError()
        present_note(note)


def input_parser(args: t.Dict[str, t.Any], _: PresenterTwiks) -> create_note.Input:
    summary = args["SUMMARY"]
    content = args["CONTENT"]
    tags = args["TAGS"]
    if tags is None:
        tags = ""
    tags = tags.split(",")

    if args["help"]:
        print(command_doc)
        sys.exit(0)
    if args["--editor"]:
        import tempfile

        tempfilename = ""
        # open/close for flush buffers to file on disk
        with tempfile.NamedTemporaryFile(
                mode="w+", encoding="utf8", delete=False
        ) as tmpfile:
            tempfilename = tmpfile.name
            subprocess.call(["vim", tempfilename])

        with open(tempfilename, "r", encoding="utf8") as tmpfile:
            summary = tmpfile.readline()
            tag_line = tmpfile.readline()
            if tag_line:
                tags = list(
                    filterfalse(
                        lambda a: not a,
                        chain(*[t.split(",") for t in tag_line.split()]),
                    )
                )

            content = tmpfile.read()
            print(type(summary), summary)
            print(type(content), content)

    if args["--interactive"]:
        content = ""
        enter_times = 0

        summary = input("summary>")
        tags_str = input("tags>")
        tags = tags_str.split(",")

        while enter_times < EOF_ENTER_TIMES or not content:
            line = input("content>")
            if line == "":
                if enter_times >= EOF_ENTER_TIMES and not content:
                    print("enter content please or quit with Ctrl+C")
                enter_times += 1
            else:
                enter_times = 0
                content += line + "\n"
    if not (content.strip() and summary.strip()):
        print("content or summary empty. try again")
        sys.exit(1)

    return create_note.Input("1", summary.strip(), content.strip(), tags=tags)


command_doc = f"""Usage:
    mk SUMMARY CONTENT [TAGS]
    mk --interactive
    mk --editor
    mk help

Options:
    --interactive       input note interactive. In this mode you enter 
                        summary as first line, and next lines will become 
                        content. To end content, press Enter {EOF_ENTER_TIMES} times.
    --editor            run external editor using env var EDITOR
"""

create_note_chain = DocOptChain(
    usecase=create_note.UseCase,
    dependencies=dict(gateway=ioc.create_note_gateway),
    name="mk",
    command_doc=command_doc,
    parse_input=input_parser,
    present_output=output_presentor,
)
