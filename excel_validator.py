from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from openpyxl.worksheet.worksheet import Worksheet


MAX_COLUMNS = 100
MAX_ROWS = 5000
MAX_HEADER_LENGTH = 200


@dataclass
class ValidationIssue:
    level: str
    code: str
    message: str
    row: int | None = None
    column: int | None = None


@dataclass
class SheetValidationResult:
    name: str
    row_count: int
    data_row_count: int
    column_count: int
    header_count: int
    empty_row_count: int
    duplicate_headers: list[str]
    empty_headers: list[int]
    issues: list[ValidationIssue]
    usable: bool

    def to_dict(self):
        result = asdict(self)
        result["issues"] = [
            asdict(issue)
            for issue in self.issues
        ]
        return result


def _is_empty(value: Any) -> bool:
    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    return False


def _normalize_header(value: Any) -> str:
    if value is None:
        return ""

    return " ".join(
        str(value).strip().split()
    )


def _row_has_data(values: list[Any]) -> bool:
    return any(
        not _is_empty(value)
        for value in values
    )


def validate_sheet(
    ws: Worksheet
) -> SheetValidationResult:

    issues = []
    rows = []

    row_count = 0
    empty_row_count = 0
    max_columns_seen = 0

    for row_number, row in enumerate(
        ws.iter_rows(values_only=True),
        start=1
    ):

        values = list(row)

        if len(values) > MAX_COLUMNS:

            issues.append(
                ValidationIssue(
                    level="error",
                    code="TOO_MANY_COLUMNS",
                    message=(
                        f"تعداد ستون‌های Sheet بیشتر از "
                        f"{MAX_COLUMNS} ستون است."
                    ),
                    row=row_number
                )
            )

            break

        max_columns_seen = max(
            max_columns_seen,
            len(values)
        )

        if not _row_has_data(values):

            empty_row_count += 1
            continue

        row_count += 1

        if row_count > MAX_ROWS:

            issues.append(
                ValidationIssue(
                    level="error",
                    code="TOO_MANY_ROWS",
                    message=(
                        f"تعداد ردیف‌های دارای اطلاعات "
                        f"بیشتر از حد مجاز {MAX_ROWS} است."
                    ),
                    row=row_number
                )
            )

            break

        rows.append(values)

    # Sheet کاملاً خالی است.
    # این وضعیت هشدار است، نه خطای متوقف‌کننده.
    if not rows:

        issues.append(
            ValidationIssue(
                level="warning",
                code="EMPTY_SHEET",
                message=(
                    "این Sheet هیچ اطلاعات قابل استفاده‌ای ندارد "
                    "و در فرآیند Import نادیده گرفته می‌شود."
                )
            )
        )

        return SheetValidationResult(
            name=ws.title,
            row_count=0,
            data_row_count=0,
            column_count=0,
            header_count=0,
            empty_row_count=empty_row_count,
            duplicate_headers=[],
            empty_headers=[],
            issues=issues,
            usable=False
        )

    headers = rows[0]

    header_count = len(headers)

    empty_headers = []
    normalized_headers = []

    for index, header in enumerate(
        headers,
        start=1
    ):

        normalized = _normalize_header(
            header
        )

        normalized_headers.append(
            normalized
        )

        if not normalized:

            empty_headers.append(index)

            issues.append(
                ValidationIssue(
                    level="warning",
                    code="EMPTY_HEADER",
                    message=(
                        f"ستون شماره {index} عنوان ندارد."
                    ),
                    row=1,
                    column=index
                )
            )

        elif len(normalized) > MAX_HEADER_LENGTH:

            issues.append(
                ValidationIssue(
                    level="warning",
                    code="LONG_HEADER",
                    message=(
                        f"عنوان ستون شماره {index} "
                        f"بیش از {MAX_HEADER_LENGTH} "
                        f"کاراکتر است."
                    ),
                    row=1,
                    column=index
                )
            )

    seen = set()
    duplicate_headers = []

    for header in normalized_headers:

        if not header:
            continue

        if header in seen:

            if header not in duplicate_headers:
                duplicate_headers.append(header)

            continue

        seen.add(header)

    for header in duplicate_headers:

        issues.append(
            ValidationIssue(
                level="error",
                code="DUPLICATE_HEADER",
                message=(
                    f"عنوان ستون «{header}» تکراری است."
                ),
                row=1
            )
        )

    data_row_count = max(
        len(rows) - 1,
        0
    )

    if data_row_count == 0:

        issues.append(
            ValidationIssue(
                level="warning",
                code="NO_DATA_ROWS",
                message=(
                    "بعد از Header هیچ ردیف داده‌ای وجود ندارد."
                )
            )
        )

    if max_columns_seen == 0:

        issues.append(
            ValidationIssue(
                level="error",
                code="NO_COLUMNS",
                message="هیچ ستونی قابل تشخیص نیست."
            )
        )

    has_error = any(
        issue.level == "error"
        for issue in issues
    )

    usable = (
        not has_error
        and header_count > 0
        and data_row_count > 0
    )

    return SheetValidationResult(
        name=ws.title,
        row_count=row_count,
        data_row_count=data_row_count,
        column_count=max_columns_seen,
        header_count=header_count,
        empty_row_count=empty_row_count,
        duplicate_headers=duplicate_headers,
        empty_headers=empty_headers,
        issues=issues,
        usable=usable
    )


def validate_workbook(workbook) -> dict:

    sheets = []

    for sheet_name in workbook.sheetnames:

        ws = workbook[sheet_name]

        result = validate_sheet(ws)

        sheets.append(
            result.to_dict()
        )

    usable_sheets = sum(
        1
        for sheet in sheets
        if sheet["usable"]
    )

    total_errors = 0
    total_warnings = 0

    for sheet in sheets:

        for issue in sheet["issues"]:

            if issue["level"] == "error":
                total_errors += 1

            elif issue["level"] == "warning":
                total_warnings += 1

    return {
        "sheet_count": len(sheets),
        "usable_sheet_count": usable_sheets,
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "sheets": sheets,
        "can_continue": (
            usable_sheets > 0
            and total_errors == 0
        ),
    }
