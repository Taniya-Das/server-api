from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class DatasetFileFormat(StrEnum):
    ARFF = "arff"
    SPARSE_ARFF = "sparse_arff"
    PARQUET = "parquet"


class Visibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class DatasetStatus(StrEnum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    IN_PROCESSING = "in processing"
    IN_PREPARATION = "in_preparation"


class DatasetMetadata(BaseModel):
    id_: int = Field(json_schema_extra={"example": 1}, alias="id")
    visibility: Visibility = Field(json_schema_extra={"example": Visibility.PUBLIC})
    status: DatasetStatus = Field(json_schema_extra={"example": DatasetStatus.ACTIVE})

    name: str = Field(json_schema_extra={"example": "Anneal"})
    licence: str = Field(json_schema_extra={"example": "CC0"})
    version: int = Field(json_schema_extra={"example": 2})
    version_label: str = Field(
        json_schema_extra={
            "example": 2,
            "description": "Not sure how this relates to `version`.",
        },
    )
    language: str = Field(json_schema_extra={"example": "English"})

    creators: list[str] = Field(
        json_schema_extra={"example": ["David Sterling", "Wray Buntine"]},
        alias="creator",
    )
    contributors: list[str] = Field(
        json_schema_extra={"example": ["David Sterling", "Wray Buntine"]},
        alias="contributor",
    )
    citation: str = Field(
        json_schema_extra={"example": "https://archive.ics.uci.edu/ml/citation_policy.html"},
    )
    paper_url: HttpUrl | None = Field(
        json_schema_extra={
            "example": "http://digital.library.adelaide.edu.au/dspace/handle/2440/15227",
        },
    )
    upload_date: datetime = Field(json_schema_extra={"example": datetime(2014, 4, 6, 23, 19, 20)})
    processing_date: datetime | None = Field(
        json_schema_extra={"example": datetime(2019, 7, 9, 15, 22, 3)},
    )
    processing_error: str | None = Field(
        json_schema_extra={"example": "Please provide description XML."},
        alias="error",
    )
    processing_warning: str | None = Field(alias="warning")
    collection_date: str | None = Field(json_schema_extra={"example": "1990"})

    description: str = Field(
        json_schema_extra={"example": "The original Annealing dataset from UCI."},
    )
    description_version: int = Field(json_schema_extra={"example": 2})
    tags: list[str] = Field(json_schema_extra={"example": ["study_1", "uci"]}, alias="tag")
    default_target_attribute: str | None = Field(json_schema_extra={"example": "class"})
    ignore_attribute: list[str] | None = Field(json_schema_extra={"example": "sensitive_feature"})
    row_id_attribute: list[str] | None = Field(json_schema_extra={"example": "ssn"})

    url: HttpUrl = Field(
        json_schema_extra={
            "example": "https://www.openml.org/data/download/1/dataset_1_anneal.arff",
            "description": "URL of the main dataset data file.",
        },
    )
    parquet_url: HttpUrl | None = Field(
        json_schema_extra={
            "example": "http://openml1.win.tue.nl/dataset2/dataset_2.pq",
            "description": "URL of the parquet dataset data file.",
        },
    )
    minio_url: HttpUrl | None = Field(
        json_schema_extra={
            "example": "http://openml1.win.tue.nl/dataset2/dataset_2.pq",
            "description": "Deprecated, I think.",
        },
    )
    file_id: int = Field(json_schema_extra={"example": 1})
    format_: DatasetFileFormat = Field(
        json_schema_extra={"example": DatasetFileFormat.ARFF},
        alias="format",
    )
    original_data_url: list[HttpUrl] | None = Field(
        json_schema_extra={"example": "https://www.openml.org/d/2"},
    )
    md5_checksum: str = Field(json_schema_extra={"example": "d01f6ccd68c88b749b20bbe897de3713"})
