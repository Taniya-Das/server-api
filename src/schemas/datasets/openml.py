from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class DatasetFileFormat(StrEnum):
    ARFF = "ARFF"
    PARQUET = "parquet"


class DatasetLicence(StrEnum):
    CC0 = "Public"
    OTHER = "other"


class Visibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class DatasetStatus(StrEnum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    IN_PROCESSING = "in processing"


class DatasetMetadata(BaseModel):
    id_: int = Field(example=1, alias="id")
    visibility: Visibility = Field(example=Visibility.PUBLIC)
    status: DatasetStatus = Field(example=DatasetStatus.ACTIVE)

    name: str = Field(example="Anneal")
    licence: DatasetLicence = Field(example=DatasetLicence.CC0)
    version: int = Field(example=2)
    version_label: str = Field(
        example="2",
        description="Not sure how this relates to `version`.",
    )
    language: str = Field(example="English")

    creator: list[str] = Field(example=["David Sterling", "Wray Buntine"])
    contributor: list[str] = Field(example=["David Sterling", "Wray Buntine"])
    citation: str = Field(example="https://archive.ics.uci.edu/ml/citation_policy.html")
    upload_date: datetime = Field(example=datetime(2014, 4, 6, 23, 19, 20))
    processing_date: datetime | None = Field(example=datetime(2019, 7, 9, 15, 22, 3))

    description: str = Field(example="The original Annealing dataset from UCI.")
    description_version: int = Field(example=2)
    tag: list[str] = Field(example=["study_1", "uci"])
    default_target_attribute: str = Field(example="class")

    url: HttpUrl = Field(
        example="https://www.openml.org/data/download/1/dataset_1_anneal.arff",
        description="URL of the main dataset data file.",
    )
    parquet_url: HttpUrl = Field(
        example="http://openml1.win.tue.nl/dataset2/dataset_2.pq",
        description="URL of the parquet dataset data file.",
    )
    minio_url: HttpUrl = Field(
        example="http://openml1.win.tue.nl/dataset2/dataset_2.pq",
        description="Deprecated, I think.",
    )
    file_id: int = Field(example=1)
    format_: DatasetFileFormat = Field(example=DatasetFileFormat.ARFF, alias="format")
    original_data_url: HttpUrl = Field(example="https://www.openml.org/d/2")
    md5_checksum: str = Field(example="d01f6ccd68c88b749b20bbe897de3713")
