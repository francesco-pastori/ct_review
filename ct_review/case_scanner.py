from __future__ import annotations

from pathlib import Path

from .models import CaseInfo


def scan_cases(folder: Path) -> list[CaseInfo]:
    folder = Path(folder)
    paths = [
        path
        for path in folder.iterdir()
        if path.is_file() and (path.name.endswith(".nii.gz") or path.name.endswith(".nii"))
    ]
    paths.sort(key=lambda path: path.name.lower())

    return [
        CaseInfo(
            index=index,
            file_name=path.name,
            relative_path=path.relative_to(folder).as_posix(),
            absolute_path=path,
        )
        for index, path in enumerate(paths)
    ]
