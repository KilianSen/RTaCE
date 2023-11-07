from dataclasses import dataclass


@dataclass
class Branch:
    origin: object

    function: callable
    args: list
    kwargs: dict

    data_copy: any
