from dataclasses import dataclass


@dataclass(frozen=True)
class LongUrl:
    url: str

    def __post_init__(self):
        if self.url is None:
            raise ValueError("A url must be provided")
