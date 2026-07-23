from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OUTCOME_FIELDS = ["treatment", "CRS", "sensitivity", "overall_survival", "residual_tumor"]


@dataclass(frozen=True)
class OutcomeMatch:
    values: dict[str, str]


class OutcomeStore:
    def __init__(self, records: dict[str, OutcomeMatch]) -> None:
        self.records = records

    @classmethod
    def from_json(cls, path: Path) -> "OutcomeStore":
        with Path(path).open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, list):
            raise ValueError("Outcome JSON must contain a list of records.")

        records: dict[str, OutcomeMatch] = {}
        duplicates: list[str] = []
        for index, item in enumerate(payload, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"Outcome record #{index} is not an object.")
            record_id = item.get("record_id")
            if not record_id:
                raise ValueError(f"Outcome record #{index} has no record_id.")
            normalized_id = normalize_id(str(record_id))
            if normalized_id in records:
                duplicates.append(normalized_id)
                continue
            records[normalized_id] = OutcomeMatch(
                values={field: _stringify_value(item.get(field)) for field in OUTCOME_FIELDS}
            )

        if duplicates:
            duplicate_text = ", ".join(sorted(set(duplicates)))
            raise ValueError(f"Duplicate normalized record_id values found: {duplicate_text}")
        return cls(records)

    def match_file_name(self, file_name: str) -> OutcomeMatch | None:
        case_id = extract_case_id(file_name)
        if not case_id:
            return None
        return self.records.get(case_id)


def normalize_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()


def extract_case_id(file_name: str) -> str | None:
    match = re.search(r"CT[_-]?(IEO\d+)\.nii(?:\.gz)?$", file_name, flags=re.IGNORECASE)
    if not match:
        return None
    return normalize_id(match.group(1))


def _stringify_value(value: Any) -> str:
    if value is None:
        return "Not available"
    return str(value)
