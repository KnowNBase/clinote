from dataclasses import dataclass

import typing as t

PresenterTwiks = t.Dict[str, bool]


@dataclass
class Chain:
    usecase: t.Type
    dependencies: t.Dict[str, t.Any]
    parse_input: t.Callable[[t.Dict[str, t.Any], PresenterTwiks], t.Any]
    present_output: t.Callable[[t.Any, PresenterTwiks], t.Any]

    def compose(self) -> t.Callable[[t.Dict[str, t.Any]], t.Any]:
        def use_case_function(args=None):
            UseCase = self.usecase
            uc = UseCase(**self.dependencies)
            flags = {}
            input_ = self.parse_input(args, flags)
            output = uc(input_)
            return self.present_output(output, flags)

        return use_case_function
