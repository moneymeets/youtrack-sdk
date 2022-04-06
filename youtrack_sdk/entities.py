from datetime import date, datetime
from typing import Literal, Optional, Sequence

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True  # allow to use field name or alias to populate a model
        frozen = True  # make instance immutable and hashable


class User(BaseModel):
    type: Literal["User", "Me"] = Field(alias="$type", default="User")
    id: Optional[str]
    ring_id: Optional[str] = Field(alias="ringId")
    login: Optional[str]
    email: Optional[str]


class TextFieldValue(BaseModel):
    type: Literal["TextFieldValue"] = Field(alias="$type", default="TextFieldValue")
    id: Optional[str]
    text: Optional[str]
    markdownText: Optional[str]


class PeriodValue(BaseModel):
    type: Literal["PeriodValue"] = Field(alias="$type", default="PeriodValue")
    id: Optional[str]
    minutes: Optional[int]
    presentation: Optional[str]


class BundleElement(BaseModel):
    id: Optional[str]
    name: Optional[str]


class BuildBundleElement(BundleElement):
    type: Literal["BuildBundleElement"] = Field(alias="$type", default="BuildBundleElement")


class VersionBundleElement(BundleElement):
    type: Literal["VersionBundleElement"] = Field(alias="$type", default="VersionBundleElement")


class OwnedBundleElement(BundleElement):
    type: Literal["OwnedBundleElement"] = Field(alias="$type", default="OwnedBundleElement")


class EnumBundleElement(BundleElement):
    type: Literal["EnumBundleElement"] = Field(alias="$type", default="EnumBundleElement")


class StateBundleElement(BundleElement):
    type: Literal["StateBundleElement"] = Field(alias="$type", default="StateBundleElement")


class UserGroup(BaseModel):
    type: Literal["UserGroup"] = Field(alias="$type", default="UserGroup")
    id: Optional[str]
    name: Optional[str]
    ring_id: Optional[str] = Field(alias="ringId")


class IssueCustomField(BaseModel):
    id: Optional[str]
    name: Optional[str]


class TextIssueCustomField(IssueCustomField):
    type: Literal["TextIssueCustomField"] = Field(alias="$type", default="TextIssueCustomField")
    value: Optional[TextFieldValue]


class SimpleIssueCustomField(IssueCustomField):
    type: Literal["SimpleIssueCustomField"] = Field(alias="$type", default="SimpleIssueCustomField")
    value: Optional[datetime | str | int | float]


class DateIssueCustomField(SimpleIssueCustomField):
    type: Literal["DateIssueCustomField"] = Field(alias="$type", default="DateIssueCustomField")
    value: Optional[date]


class PeriodIssueCustomField(IssueCustomField):
    type: Literal["PeriodIssueCustomField"] = Field(alias="$type", default="PeriodIssueCustomField")
    value: Optional[PeriodValue]


class MultiBuildIssueCustomField(IssueCustomField):
    type: Literal["MultiBuildIssueCustomField"] = Field(alias="$type", default="MultiBuildIssueCustomField")
    value: Sequence[BuildBundleElement]


class MultiEnumIssueCustomField(IssueCustomField):
    type: Literal["MultiEnumIssueCustomField"] = Field(alias="$type", default="MultiEnumIssueCustomField")
    value: Sequence[EnumBundleElement]


class MultiGroupIssueCustomField(IssueCustomField):
    type: Literal["MultiGroupIssueCustomField"] = Field(alias="$type", default="MultiGroupIssueCustomField")
    value: Sequence[UserGroup]


class MultiOwnedIssueCustomField(IssueCustomField):
    type: Literal["MultiOwnedIssueCustomField"] = Field(alias="$type", default="MultiOwnedIssueCustomField")
    value: Sequence[OwnedBundleElement]


class MultiUserIssueCustomField(IssueCustomField):
    type: Literal["MultiUserIssueCustomField"] = Field(alias="$type", default="MultiUserIssueCustomField")
    value: Sequence[User]


class MultiVersionIssueCustomField(IssueCustomField):
    type: Literal["MultiVersionIssueCustomField"] = Field(alias="$type", default="MultiVersionIssueCustomField")
    value: Sequence[VersionBundleElement]


class SingleBuildIssueCustomField(IssueCustomField):
    type: Literal["SingleBuildIssueCustomField"] = Field(alias="$type", default="SingleBuildIssueCustomField")
    value: Optional[BuildBundleElement]


class SingleEnumIssueCustomField(IssueCustomField):
    type: Literal["SingleEnumIssueCustomField"] = Field(alias="$type", default="SingleEnumIssueCustomField")
    value: Optional[EnumBundleElement]


class SingleGroupIssueCustomField(IssueCustomField):
    type: Literal["SingleGroupIssueCustomField"] = Field(alias="$type", default="SingleGroupIssueCustomField")
    value: Optional[UserGroup]


class SingleOwnedIssueCustomField(IssueCustomField):
    type: Literal["SingleOwnedIssueCustomField"] = Field(alias="$type", default="SingleOwnedIssueCustomField")
    value: Optional[OwnedBundleElement]


class SingleUserIssueCustomField(IssueCustomField):
    type: Literal["SingleUserIssueCustomField"] = Field(alias="$type", default="SingleUserIssueCustomField")
    value: Optional[User]


class SingleVersionIssueCustomField(IssueCustomField):
    type: Literal["SingleVersionIssueCustomField"] = Field(alias="$type", default="SingleVersionIssueCustomField")
    value: Optional[VersionBundleElement]


class StateIssueCustomField(IssueCustomField):
    type: Literal["StateIssueCustomField"] = Field(alias="$type", default="StateIssueCustomField")
    value: Optional[StateBundleElement]


IssueCustomFieldType = (
    SingleEnumIssueCustomField
    | MultiEnumIssueCustomField
    | SingleBuildIssueCustomField
    | MultiBuildIssueCustomField
    | StateIssueCustomField
    | SingleVersionIssueCustomField
    | MultiVersionIssueCustomField
    | SingleOwnedIssueCustomField
    | MultiOwnedIssueCustomField
    | SingleUserIssueCustomField
    | MultiUserIssueCustomField
    | SingleGroupIssueCustomField
    | MultiGroupIssueCustomField
    | SimpleIssueCustomField
    | DateIssueCustomField
    | PeriodIssueCustomField
    | TextIssueCustomField
)


class Project(BaseModel):
    type: Literal["Project"] = Field(alias="$type", default="Project")
    id: Optional[str]
    name: Optional[str]
    short_name: Optional[str] = Field(alias="shortName")


class IssueTag(BaseModel):
    type: Literal["IssueTag"] = Field(alias="$type", default="IssueTag")
    id: Optional[str]
    name: Optional[str]


class Issue(BaseModel):
    type: Literal["Issue"] = Field(alias="$type", default="Issue")
    id: Optional[str]
    id_readable: Optional[str] = Field(alias="idReadable")
    created: Optional[datetime]
    updated: Optional[datetime]
    resolved: Optional[datetime]
    project: Optional[Project]
    reporter: Optional[User]
    updater: Optional[User]
    summary: Optional[str]
    description: Optional[str]
    wikified_description: Optional[str] = Field(alias="wikifiedDescription")
    uses_markdown: Optional[bool] = Field(alias="usesMarkdown")
    tags: Optional[Sequence[IssueTag]]
    custom_fields: Optional[Sequence[IssueCustomFieldType]] = Field(alias="customFields")


class IssueAttachment(BaseModel):
    type: Literal["IssueAttachment"] = Field(alias="$type", default="IssueAttachment")
    id: Optional[str]
    name: Optional[str]
    author: Optional[User]
    created: Optional[datetime]
    updated: Optional[datetime]
    mime_type: Optional[str] = Field(alias="mimeType")
    url: Optional[str]


class IssueComment(BaseModel):
    type: Literal["IssueComment"] = Field(alias="$type", default="IssueComment")
    id: Optional[str]
    text: Optional[str]
    uses_markdown: Optional[bool] = Field(alias="usesMarkdown")
    text_preview: Optional[str] = Field(alias="textPreview")
    created: Optional[datetime]
    updated: Optional[datetime]
    author: Optional[User]
    attachments: Optional[Sequence[IssueAttachment]]
    deleted: Optional[bool]
