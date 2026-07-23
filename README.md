# CT Quality Review

A small desktop application for reviewing local 3D CT NIfTI files (`.nii` and `.nii.gz`) and writing quality decisions to a CSV report.

## Features

- Folder-based review of non-recursive `.nii` and `.nii.gz` files.
- Alphabetical case order.
- Three synchronized-independent anatomical views: axial, coronal, sagittal.
- Radiological display convention by default.
- One slice slider per view.
- Two-handle HU range control for display windowing.
- Optional physical-aspect display. By default, views fill their panels for fast visual review.
- Compact viewer-first layout for smaller screens.
- Accept, reject, or skip each CT.
- Left and right arrow keys move to the previous and next CT.
- Optional comment per decision.
- Required quality checklist for accept/reject decisions.
- Checklist values can be cleared one by one by clicking a selected radio button again, or all at once.
- Accept is blocked when any quality criterion is bad.
- Reject is blocked when all quality criteria are good.
- Existing CSV reports are resumed.
- Startup screen has separate report actions for loading an existing CSV or creating a new one.
- Optional outcome JSON can be loaded and displayed per matched CT file.
- Decisions are saved by file name and overwritten when reviewed again.
- Relative paths are written to the report.
- Configurable minimum axial slice warning.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

## CSV Columns

```csv
file_name,file_path,status,comment,z_slices,include_abdomen,include_pelvis,sufficient_z_axis,readable_three_planes,artifacts_or_technical_issues,reviewed_at
```

`file_path` is relative to the selected NIfTI folder. `status` is one of `accepted`, `rejected`, or `skipped`.

## Notes

The app reads `.nii.gz` directly. If loading compressed files becomes slow on your dataset, the next optimization should be adding an optional local cache that stores decompressed volumes for faster reopening.
