from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.pipeline import IngestionPipeline


def test_run_years_with_empty_list() -> None:
    pipeline = IngestionPipeline(
        raw_directory=Path("data/raw"),
    )

    with pytest.raises(
        ValueError,
        match="La liste des années ne peut pas être vide",
    ):
        pipeline.run_years(years=[])


def test_run_years_returns_dataframe() -> None:
    pipeline = IngestionPipeline(
        raw_directory=Path("data/raw"),
    )

    dataframe = pipeline.run_years(
        years=[2023, 2024],
    )

    assert isinstance(dataframe, pd.DataFrame)
    assert not dataframe.empty
    assert "source_year" in dataframe.columns
    assert set(dataframe["source_year"].unique()) == {2023, 2024}