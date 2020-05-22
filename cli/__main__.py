"""
Usage:
    knb [-hv] <command> [<args>...]
    knb mk
    knb list
    knb show-groups
    knb help

Options:
    (-h|--help)     show this help
    (-v|--version)  show version

Commands:
    mk - make note
    list - list notes
    show-groups - list notes grouped by tags
"""

import docopt  # type: ignore
import sys

from cli.adapters.create_note import create_note_chain
from cli.adapters.list_notes import list_notes_chain
from cli.adapters.show_grouped_notes import group_by_tag_chain
from cli.generator.docopt_generator import Generator

if __name__ == "__main__":

    command_chains = [
        list_notes_chain,
        create_note_chain,
        group_by_tag_chain,
    ]

    g = Generator()
    commands = g(command_chains)

    args = docopt.docopt(__doc__, version="0.0.1", options_first=True)
    # print(args)
    cmd = args["<command>"]
    command = commands.get(cmd)
    if command is None:
        print("command not found", cmd)
        print(__doc__)
        sys.exit(1)
    command(sys.argv[2:])
