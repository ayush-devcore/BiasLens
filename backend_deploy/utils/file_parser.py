import json
from typing import Optional

import pandas as pd
from fastapi import UploadFile, HTTPException

from config import settings
from utils.validation import (
    ValidationError,
    validate_dataset_structure,
    validate_minimum_rows,
    validate_duplicate_columns,
    validate_json_payload,
    normalize_column_name,
)

SUPPORTED_EXTENSIONS = {".csv", ".json", ".xlsx", ".xls", ".parquet"}
CHUNK_SIZE = 1024 * 1024  # 1MB
MAX_FILE_SIZE_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


async def validate_file_size(file: UploadFile):
    total_size = 0

    while chunk := await file.read(CHUNK_SIZE):
        total_size += len(chunk)

        if total_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
            )

    await file.seek(0)


def _get_extension(filename: str) -> Optional[str]:
    filename = (filename or "").lower().strip()
    for supported in SUPPORTED_EXTENSIONS:
        if filename.endswith(supported):
            return supported
    return None


def _normalize_columns(columns):
    return [normalize_column_name(c) for c in columns]


async def parse_uploaded_file(file: UploadFile) -> pd.DataFrame:
    """Parse any supported file format into a pandas DataFrame."""
    filename = file.filename or ""
    ext = _get_extension(filename)

    if not ext:
        raise ValidationError(
            "UNSUPPORTED_FILE_TYPE",
            f"Unsupported file type. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}.",
            {"supported_extensions": sorted(SUPPORTED_EXTENSIONS)},
            status_code=400,
        )

    # validate file size before reading the file content
    await validate_file_size(file)
    await file.seek(0)
    file_obj = file.file
    try:
        if ext == ".csv":
            file_obj.seek(0)
            try:
                df = pd.read_csv(file_obj, encoding="latin1", low_memory=False)
            except UnicodeDecodeError:
                file_obj.seek(0)
                df = pd.read_csv(file_obj, encoding="latin1", low_memory=False)

        elif ext == ".json":
            # read raw bytes/text from the underlying file and decode safely
            file_obj.seek(0)
            content = file_obj.read()
            if isinstance(content, bytes):
                try:
                    content = content.decode("utf-8")
                except UnicodeDecodeError:
                    content = content.decode("latin1")

            payload = json.loads(content)
            validate_json_payload(payload)
            df = pd.DataFrame(payload)

        else:
            # handle other supported formats
            file_obj.seek(0)
            if ext in (".xlsx", ".xls"):
                df = pd.read_excel(file_obj)
            elif ext == ".parquet":
                df = pd.read_parquet(file_obj)
            else:
                raise ValidationError(
                    "UNSUPPORTED_FILE_TYPE",
                    f"Unsupported file type. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}.",
                    {"supported_extensions": sorted(SUPPORTED_EXTENSIONS)},
                    status_code=400,
                )
    except ValidationError:
        raise
    except json.JSONDecodeError as e:
        raise ValidationError(
            "MALFORMED_JSON",
            f"Failed to parse JSON file: {str(e)}.",
            status_code=422,
        )
    except Exception as e:
        raise ValidationError(
            "PARSE_ERROR",
            f"Failed to parse file: {str(e)}.",
            status_code=422,
        )

    if not isinstance(df, pd.DataFrame):
        raise ValidationError(
            "INVALID_DATASET",
            "Uploaded file could not be parsed into a table.",
            status_code=422,
        )

    df.columns = _normalize_columns(df.columns)
    validate_duplicate_columns(df)
    validate_dataset_structure(df)
    validate_minimum_rows(df, minimum_rows=50)

    return df


def auto_detect_label_column(df: pd.DataFrame) -> Optional[str]:
    """Try to automatically detect the target/label column."""
    cols = df.columns.tolist()

    for kw in settings.LABEL_KEYWORDS:
        if kw in cols:
            return kw

    for col in cols:
        for kw in settings.LABEL_KEYWORDS:
            if kw in col:
                return col

    for col in reversed(cols):
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) == 2:
            return col

    return None


def auto_detect_sensitive_attributes(df: pd.DataFrame, label_col: str) -> list:
    """Auto-detect sensitive attribute columns."""
    detected = []
    cols = [c for c in df.columns if c != label_col]

    for col in cols:
        col_lower = col.lower()
        for kw in settings.SENSITIVE_ATTR_KEYWORDS:
            if kw in col_lower:
                detected.append(col)
                break

    return detected


def preprocess_dataframe(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    """Clean and preprocess the dataframe."""
    df = df.copy()
    df = df.dropna(subset=[label_col])

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    for col in numeric_cols:
        if col != label_col:
            df[col] = df[col].fillna(df[col].median())

    cat_cols = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    for col in cat_cols:
        if not df[col].empty and df[col].mode().shape[0] > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df


def encode_dataframe(df: pd.DataFrame, label_col: str, sensitive_attrs: list):
    """Label encode categorical columns, return encoders map."""
    from sklearn.preprocessing import LabelEncoder

    df = df.copy()
    encoders = {}

    cat_cols = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = {
            "classes": le.classes_.tolist(),
            "encoder": le,
        }

    return df, encoders
