from dataclasses import dataclass
from utils import current_year

MAX_REF_KEY_LEN = 100
MAX_TEXT_LEN = 255
MIN_YEAR = 1

REF_TYPES = ["book"]
KEY_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12346789.:_-"

class ReferenceValidationError(ValueError):
    pass

def _validate_fields_not_empty(raw):
    required_labels = {
        "bibtex_key": "bibtex key",
        "reference_type": "reference type",
        "title": "title",
        "author": "author",
        "publisher": "publisher",
    }
    for field, label in required_labels.items():
        if not raw[field]:
            raise ReferenceValidationError(f"Empty {label}.")

def _validate_field_lengths(raw):
    length_limits = {
        "bibtex_key": ("Bibtex key", MAX_REF_KEY_LEN),
        "title": ("Title", MAX_TEXT_LEN),
        "author": ("Author name", MAX_TEXT_LEN),
        "publisher": ("Publisher name", MAX_TEXT_LEN),
    }
    for field, (label, limit) in length_limits.items():
        if len(raw[field]) > limit:
            raise ReferenceValidationError(f"{label} too long. Maximum: {limit} characters")

def _validate_ref_type(raw):
    if raw["reference_type"] not in REF_TYPES:
        raise ReferenceValidationError(
            f"Invalid reference type: {raw['reference_type']}. Allowed types: {REF_TYPES}"
        )

def _validate_key_chars(raw):
    if not all(c in KEY_ALLOWED_CHARS for c in raw["bibtex_key"]):
        raise ReferenceValidationError(
            "Invalid key: use only A-Z, a-z, 0-9, and _ . : -"
        )

def _validate_raw(raw):
    _validate_fields_not_empty(raw)
    _validate_field_lengths(raw)
    _validate_ref_type(raw)
    _validate_key_chars(raw)

def _clean_raw(raw):
    return {key: value.strip() for key, value in raw.items()}

def get_year_int(year_str) -> int:
    try:
        year = int(year_str)
    except ValueError as exc:
        raise ReferenceValidationError("Invalid year. Must be an integer.") from exc

    max_year = current_year()
    if year < MIN_YEAR or year > max_year:
        raise ReferenceValidationError(
            f"The year must be at most {max_year} and at least {MIN_YEAR}."
        )

    return year

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

    @classmethod
    def from_form(cls, form) -> "Reference":
        raw = {
            "bibtex_key": form.get("bibtex_key"),
            "reference_type": form.get("reference_type"),
            "title": form.get("title"),
            "author": form.get("author"),
            "year": form.get("year"),
            "publisher": form.get("publisher"),
        }
        if any(value is None for value in raw.values()):
            raise ReferenceValidationError("Missing fields.")

        cleaned = _clean_raw(raw)
        _validate_raw(cleaned)
        year = get_year_int(cleaned["year"])

        return cls(
            key=cleaned["bibtex_key"],
            type=cleaned["reference_type"],
            title=cleaned["title"],
            author=cleaned["author"],
            year=year,
            publisher=cleaned["publisher"],
        )
