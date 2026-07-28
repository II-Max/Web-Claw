"""
Table Extractor — Extract, validate, score, and rank
HTML tables. Refactored from V3 table_miner.py.
"""

import io
from typing import Any, Dict, List

import pandas as pd
from bs4 import BeautifulSoup

from core.logger import logger

MIN_ROWS = 2
MIN_COLS = 2


def extract_tables(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Extract all valid tables, ranked by quality score."""

    logger.info("Extracting tables...")

    # Fast path check to avoid pandas overhead
    import re
    if not re.search(r'<table', html, re.IGNORECASE):
        logger.info("No HTML tables found on page (fast path)")
        return {"count": 0, "tables": []}

    try:
        raw_tables = pd.read_html(
            io.StringIO(html),
            header=0,
            thousands=',',
            decimal='.',
            na_values=['-', 'N/A', ''],
        )
    except ValueError:
        logger.info("No HTML tables found on page")
        return {"count": 0, "tables": []}

    ranked = []

    for idx, df in enumerate(raw_tables):
        try:
            if not _is_valid_table(df):
                continue

            score = _score_table(df)

            # Convert DataFrame to serializable format
            table_data = {
                "index": idx + 1,
                "score": score,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": [str(c) for c in df.columns.tolist()],
                "data": df.fillna("").to_dict(orient="records"),
                "preview": df.head(5).fillna("").to_dict(orient="records"),
            }

            ranked.append(table_data)

        except Exception as e:
            logger.warning(f"Error processing table {idx + 1}: {e}")

    # Sort by score descending
    ranked.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"Tables extracted: {len(ranked)} valid out of {len(raw_tables)} found")

    return {
        "count": len(ranked),
        "total_found": len(raw_tables),
        "tables": ranked,
    }


def _is_valid_table(df: pd.DataFrame) -> bool:
    """Check if a table meets minimum quality standards."""

    rows, cols = df.shape

    if rows < MIN_ROWS or cols < MIN_COLS:
        return False

    # Check for mostly empty table
    missing_ratio = df.isnull().mean().mean()
    if pd.isna(missing_ratio) or missing_ratio > 0.8:
        return False

    # Check header quality
    bad_headers = sum(
        1 for col in df.columns
        if "unnamed" in str(col).lower()
    )
    if bad_headers >= len(df.columns):
        return False

    return True


def _score_table(df: pd.DataFrame) -> int:
    """Score a table based on size and data quality."""

    rows, cols = df.shape
    score = rows * cols

    missing_ratio = df.isnull().mean().mean()
    if pd.isna(missing_ratio):
        missing_ratio = 1.0

    score -= int(missing_ratio * 100)

    # Bonus for named columns
    named_cols = sum(
        1 for col in df.columns
        if "unnamed" not in str(col).lower()
    )
    score += named_cols * 5

    return max(score, 0)
