from dataclasses import dataclass

@dataclass
class Reference:
    type: str
    key: str
    author: str
    title: str
    year: int
    publisher: str

    def __str__(self):
        return f"{self.key}: {self.title} by {self.author}"
