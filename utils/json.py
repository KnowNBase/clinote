import dataclasses
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def dumps(
    payload,
    *,
    skipkeys=False,
    ensure_ascii=False,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kwargs
) -> str:
    kwargs["skipkeys"] = skipkeys
    kwargs["ensure_ascii"] = ensure_ascii
    kwargs["check_circular"] = check_circular
    kwargs["allow_nan"] = allow_nan
    kwargs["indent"] = indent
    kwargs["separators"] = separators
    kwargs["default"] = default
    kwargs["sort_keys"] = sort_keys

    return json.dumps(payload, cls=EnhancedJSONEncoder, **kwargs)
