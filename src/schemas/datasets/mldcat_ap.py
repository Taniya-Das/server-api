"""
Based on MLDCAT-AP 1.0.0: https://semiceu.github.io/MLDCAT-AP/releases/1.0.0/

This is an application profile, aimed to extend the use of DCAT-AP,
originally envisaged for the description of a machine learning process,
developed in collaboration with OpenML.
"""
from __future__ import annotations

from abc import ABC
from enum import StrEnum
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field, HttpUrl

from schemas.datasets.openml import DatasetMetadata, DatasetStatus, Visibility


class JsonLDQualifiedLiteral(BaseModel):
    """Base class for all JSON-LD objects"""

    type_: str = Field(serialization_alias="@type")
    value: str = Field(serialization_alias="@value")

    model_config = {"populate_by_name": True, "extra": "forbid"}


JsonLiteral = JsonLDQualifiedLiteral | str


class JsonLDObject(BaseModel, ABC):
    """Base class for all JSON-LD objects"""

    id_: str = Field(serialization_alias="@id")
    type_: str = Field(serialization_alias="@type")

    model_config = {"populate_by_name": True, "extra": "forbid"}


T = TypeVar("T", bound=JsonLDObject)


class JsonLDObjectReference(BaseModel, Generic[T]):
    id_: str = Field(serialization_alias="@id")

    model_config = {"populate_by_name": True, "extra": "forbid"}

    @classmethod
    def to(cls, json_ld_object: T) -> JsonLDObjectReference[T]:
        """Create a reference to `json_ld_object`"""
        return cls(id_=json_ld_object.id_)


class AccessRights(StrEnum):
    """Recommend values for 'access rights' within DCAT-AP context"""

    #  https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/access-right
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"
    NON_PUBLIC = "NON_PUBLIC"


class Agent(JsonLDObject):
    """Any entity carrying out actions with respect to the (Core) entities Catalogue,
    Datasets, Data Services and Distributions. If the Agent is an organisation,
    the use of the Organization Ontology is recommended.
    """

    type_: Literal["Agent"] = "Agent"
    name: list[JsonLiteral] = Field(default_factory=list, min_length=1)


class MD5Checksum(JsonLDObject):
    """A value that allows the contents of a file to be authenticated.
    This class allows the results of a variety of checksum and cryptographic
    message digest algorithms to be represented.
    """

    type_: Literal["Checksum"] = "Checksum"
    algorithm: Literal[
        "http://spdx.org/rdf/terms#checksumAlgorithm_md5"
    ] = "http://spdx.org/rdf/terms#checksumAlgorithm_md5"
    value: str = Field(serialization_alias="checksumValue")


class FeatureType(StrEnum):
    NOMINAL = "Nominal"
    NUMERIC = "Numeric"


class Feature(JsonLDObject):
    type_: Literal["Feature"] = "Feature"
    name: str = Field()
    feature_type: FeatureType = Field(serialization_alias="type")
    description: JsonLiteral | None = Field(default=None)


class QualityType(JsonLDObject):
    type_: Literal["QualityType"] = "QualityType"
    name: str = Field()
    quality_id: str = Field(serialization_alias="id")


class Quality(JsonLDObject):
    type_: Literal["Quality"] = "Quality"
    quality_type: QualityType = Field(serialization_alias="type")
    value: JsonLiteral = Field()


class Distribution(JsonLDObject):
    type_: Literal["Distribution"] = "Distribution"
    # required
    access_url: list[HttpUrl] = Field(
        default_factory=list,
        min_length=1,
        serialization_alias="accessUrl",
    )
    has_feature: list[JsonLDObjectReference[Feature]] = Field(
        default_factory=list,
        serialization_alias="hasFeature",
        min_length=1,
    )
    has_quality: list[JsonLDObjectReference[Quality]] = Field(
        default_factory=list,
        serialization_alias="hasQuality",
        min_length=1,
    )

    # other
    byte_size: JsonLiteral | None = Field(serialization_alias="byteSize", default=None)
    default_target_attribute: JsonLiteral | None = Field(
        serialization_alias="defaultTargetAttribute",
        default=None,
    )
    download_url: list[HttpUrl] = Field(default_factory=list, serialization_alias="downloadUrl")
    format_: JsonLiteral | None = Field(serialization_alias="format", default=None)
    identifier: JsonLiteral | None = Field(default=None)
    ignore_attribute: list[JsonLiteral] = Field(
        default_factory=list,
        serialization_alias="ignoreAttirbute",
    )
    processing_error: JsonLiteral | None = Field(
        serialization_alias="processingError",
        default=None,
    )
    processing_warning: JsonLiteral | None = Field(
        serialization_alias="processingWarning",
        default=None,
    )
    processing_data: JsonLiteral | None = Field(serialization_alias="processingDate", default=None)
    row_id_attribute: JsonLiteral | None = Field(serialization_alias="rowIDAttribute", default=None)
    title: list[JsonLiteral] = Field(default_factory=list)
    checksum: JsonLDObjectReference[MD5Checksum] | None = Field(default=None)

    access_service: list[JsonLDObjectReference[DataService]] = Field(
        default_factory=list,
        serialization_alias="accessService",
    )
    # has_policy: Policy | None = Field(alias="hasPolicy")
    # language: list[LinguisticSystem] = Field(default_factory=list)
    # licence: LicenceDocument | None = Field()


class Dataset(JsonLDObject):
    type_: Literal["Dataset"] = "Dataset"
    # required
    collection_date: JsonLiteral = Field(serialization_alias="collectionDate")
    description: list[JsonLiteral] = Field(default_factory=list, min_length=1)
    title: list[JsonLiteral] = Field(default_factory=list, min_length=1)

    # other
    access_rights: AccessRights | None = Field(serialization_alias="accessRights", default=None)
    contributor: list[JsonLDObjectReference[Agent]] = Field(default_factory=list)
    creator: Agent | None = Field(default=None)
    distribution: list[JsonLDObjectReference[Distribution]] = Field(
        default_factory=list,
    )
    has_version: list[JsonLDObjectReference[Dataset]] = Field(
        default_factory=list,
        serialization_alias="hasVersion",
    )
    identifier: list[JsonLiteral] = Field(default_factory=list)
    is_referenced_by: list[JsonLiteral] = Field(
        default_factory=list,
        serialization_alias="isReferencedBy",
    )
    is_version_of: list[JsonLDObjectReference[Dataset]] = Field(
        default_factory=list,
        serialization_alias="isVersionOf",
    )
    issued: JsonLiteral | None = Field(default=None)
    keyword: list[JsonLiteral] = Field(default_factory=list)
    landing_page: list[JsonLiteral] = Field(default_factory=list, serialization_alias="landingPage")
    publisher: JsonLDObjectReference[Agent] | None = Field(default=None)
    status: DatasetStatus | None = Field(default=None)
    version_info: JsonLiteral | None = Field(serialization_alias="versionInfo", default=None)
    version_label: JsonLiteral | None = Field(serialization_alias="versionLabel", default=None)
    visibility: Visibility | None = Field(default=None)


class DataService(JsonLDObject):
    type_: Literal["DataService"] = "DataService"
    endpoint_url: HttpUrl = Field(serialization_alias="endpointUrl")
    title: list[JsonLiteral] = Field(default_factory=list, min_length=1)
    serves_dataset: list[JsonLDObjectReference[Dataset]] = Field(
        default_factory=list,
        serialization_alias="servesDataset",
    )


# We need at least one forward reference for type annotation in the cycle
# `Dataset->Distribution->Dataservice->Dataset`, but this is not supported by
# the OpenAI schema checker, so we need to explicitly update the references.
Distribution.model_rebuild()


class JsonLDGraph(BaseModel):
    context: str | dict[str, HttpUrl] = Field(default_factory=dict, serialization_alias="@context")
    graph: list[
        Distribution | DataService | Dataset | Quality | Feature | Agent | MD5Checksum
    ] = Field(default_factory=list, serialization_alias="@graph")

    model_config = {"populate_by_name": True, "extra": "forbid"}


def convert_to_mldcat_ap(dataset: DatasetMetadata) -> JsonLDGraph:
    arff_service = DataService(
        id_="openml-arff-service",
        title=["OpenML ARFF server"],
        endpoint_url="https://www.openml.org/data/download",
    )
    example_feature = Feature(
        id_="example-petal-width",
        name="example_petal_width",
        feature_type=FeatureType.NUMERIC,
        description="Feature information not loaded, this is an example.",
    )

    example_quality = Quality(
        id_="example-quality",
        quality_type=QualityType(
            id_="quality-type-example",
            name="number_of_features",
            quality_id="link_to_definition",
        ),
        value="150",
    )
    checksum = MD5Checksum(id_="checksum-id", value=dataset.md5_checksum)
    # contributor and creator N/A
    distribution = Distribution(
        id_="distribution-id",
        access_url=[f"https://www.openml.org/d/{dataset.id_}"],
        has_feature=[JsonLDObjectReference[Feature].to(example_feature)],
        has_quality=[JsonLDObjectReference[Quality].to(example_quality)],
        default_target_attribute=dataset.default_target_attribute,
        download_url=[dataset.url],
        format_=dataset.format_,
        checksum=JsonLDObjectReference[MD5Checksum].to(checksum),
        access_service=[JsonLDObjectReference[DataService].to(arff_service)],
    )

    mldcat_dataset = Dataset(
        id_=str(dataset.id_),
        type_="Dataset",
        collection_date=str(dataset.upload_date),
        description=[dataset.description],
        title=[dataset.name],
        distribution=[JsonLDObjectReference[Distribution].to(distribution)],
        status=dataset.status,
        version_info=str(dataset.version),
        version_label=dataset.version_label,
        visibility=dataset.visibility,
        keyword=dataset.tags,
        issued=JsonLDQualifiedLiteral(
            value=str(dataset.upload_date),
            type_="http://www.w3.org/2001/XMLSchema#dateTime",
        ),
    )

    return JsonLDGraph(
        context="https://semiceu.github.io/MLDCAT-AP/releases/1.0.0/context/mldcat-ap.jsonld",
        graph=[
            arff_service,
            distribution,
            mldcat_dataset,
            example_feature,
            example_quality,
            checksum,
        ],
    )
