from dataclasses import dataclass


@dataclass(frozen=True)
class OriginalUrl:
    value: str

    def __post_init__(self):
        if self.value is None:
            raise ValueError("A value must be provided")


@dataclass(frozen=True)
class ShortenedUrl:
    value: str

    def __post_init__(self):
        if self.value is None:
            raise ValueError("A value must be provided")
