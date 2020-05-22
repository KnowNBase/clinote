import typing as t
from dataclasses import dataclass

from docopt import docopt  # type: ignore

from glue.chain import Chain


@dataclass
class DocOptChain(Chain):
    name: str
    command_doc: str


class Generator:
    def __call__(self, chains: t.List[DocOptChain]) -> t.Dict[str, t.Callable]:
        commands = {}
        for chain in chains:
            command = create_command(chain)
            command_name = chain.name
            commands[command_name] = command
        return commands


def create_command(link: DocOptChain) -> t.Callable:
    def command(args):
        args = docopt(link.command_doc, argv=args)
        link.compose()(args)

    return command
