from typing import Literal, Optional, Sequence

from pydantic import AwareDatetime, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from pydantic import BaseModel as PydanticBaseModel

from .types import YouTrackDate, YouTrackDateTime


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # allow to use field name or alias to populate a model
        frozen=True,  # make instance immutable and hashable
    )


class User(BaseModel):
    type: Literal["User", "Me"] = Field(alias="$type", default="User")
    id: Optional[str] = None
    name: Optional[str] = None
    ring_id: Optional[str] = Field(alias="ringId", default=None)
    login: Optional[str] = None
    email: Optional[str] = None


class TextFieldValue(BaseModel):
    type: Literal["TextFieldValue"] = Field(alias="$type", default="TextFieldValue")
    id: Optional[str] = None
    text: Optional[str] = None
    markdownText: Optional[str] = None


class PeriodValue(BaseModel):
    type: Literal["PeriodValue"] = Field(alias="$type", default="PeriodValue")
    id: Optional[str] = None
    minutes: Optional[int] = None
    presentation: Optional[str] = None


class BundleElement(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None


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
    id: Optional[str] = None
    name: Optional[str] = None
    ring_id: Optional[str] = Field(alias="ringId", default=None)


class FieldType(BaseModel):
    type: Literal["FieldType"] = Field(alias="$type", default="FieldType")
    id: Optional[str] = None


class CustomField(BaseModel):
    type: Literal["CustomField"] = Field(alias="$type", default="CustomField")
    field_type: Optional[FieldType] = Field(alias="fieldType", default=None)


class ProjectCustomField(BaseModel):
    field: Optional[CustomField] = None


class GroupProjectCustomField(ProjectCustomField):
    type: Literal["GroupProjectCustomField"] = Field(alias="$type", default="GroupProjectCustomField")


class BundleProjectCustomField(ProjectCustomField):
    type: Literal["BundleProjectCustomField"] = Field(alias="$type", default="BundleProjectCustomField")


class BuildProjectCustomField(BundleProjectCustomField):
    type: Literal["BuildProjectCustomField"] = Field(alias="$type", default="BuildProjectCustomField")


class EnumProjectCustomField(BundleProjectCustomField):
    type: Literal["EnumProjectCustomField"] = Field(alias="$type", default="EnumProjectCustomField")


class OwnedProjectCustomField(BundleProjectCustomField):
    type: Literal["OwnedProjectCustomField"] = Field(alias="$type", default="OwnedProjectCustomField")


class StateProjectCustomField(BundleProjectCustomField):
    type: Literal["StateProjectCustomField"] = Field(alias="$type", default="StateProjectCustomField")


class UserProjectCustomField(BundleProjectCustomField):
    type: Literal["UserProjectCustomField"] = Field(alias="$type", default="UserProjectCustomField")


class VersionProjectCustomField(BundleProjectCustomField):
    type: Literal["VersionProjectCustomField"] = Field(alias="$type", default="VersionProjectCustomField")


class SimpleProjectCustomField(ProjectCustomField):
    type: Literal["SimpleProjectCustomField"] = Field(alias="$type", default="SimpleProjectCustomField")


class TextProjectCustomField(SimpleProjectCustomField):
    type: Literal["TextProjectCustomField"] = Field(alias="$type", default="TextProjectCustomField")


class PeriodProjectCustomField(ProjectCustomField):
    type: Literal["PeriodProjectCustomField"] = Field(alias="$type", default="PeriodProjectCustomField")


ProjectCustomFieldType = (
    GroupProjectCustomField
    | BundleProjectCustomField
    | BuildProjectCustomField
    | EnumProjectCustomField
    | OwnedProjectCustomField
    | StateProjectCustomField
    | UserProjectCustomField
    | VersionProjectCustomField
    | SimpleProjectCustomField
    | TextProjectCustomField
    | PeriodProjectCustomField
)


class IssueCustomField(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    project_custom_field: Optional[ProjectCustomFieldType] = Field(alias="projectCustomField", default=None)


class TextIssueCustomField(IssueCustomField):
    type: Literal["TextIssueCustomField"] = Field(alias="$type", default="TextIssueCustomField")
    value: Optional[TextFieldValue] = None


class SimpleIssueCustomField(IssueCustomField):
    type: Literal["SimpleIssueCustomField"] = Field(alias="$type", default="SimpleIssueCustomField")
    value: Optional[YouTrackDateTime | StrictStr | StrictInt | StrictFloat] = None


class DateIssueCustomField(SimpleIssueCustomField):
    type: Literal["DateIssueCustomField"] = Field(alias="$type", default="DateIssueCustomField")
    value: Optional[YouTrackDate] = None


class PeriodIssueCustomField(IssueCustomField):
    type: Literal["PeriodIssueCustomField"] = Field(alias="$type", default="PeriodIssueCustomField")
    value: Optional[PeriodValue] = None


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
    value: Optional[BuildBundleElement] = None


class SingleEnumIssueCustomField(IssueCustomField):
    type: Literal["SingleEnumIssueCustomField"] = Field(alias="$type", default="SingleEnumIssueCustomField")
    value: Optional[EnumBundleElement] = None


class SingleGroupIssueCustomField(IssueCustomField):
    type: Literal["SingleGroupIssueCustomField"] = Field(alias="$type", default="SingleGroupIssueCustomField")
    value: Optional[UserGroup] = None


class SingleOwnedIssueCustomField(IssueCustomField):
    type: Literal["SingleOwnedIssueCustomField"] = Field(alias="$type", default="SingleOwnedIssueCustomField")
    value: Optional[OwnedBundleElement] = None


class SingleUserIssueCustomField(IssueCustomField):
    type: Literal["SingleUserIssueCustomField"] = Field(alias="$type", default="SingleUserIssueCustomField")
    value: Optional[User] = None


class SingleVersionIssueCustomField(IssueCustomField):
    type: Literal["SingleVersionIssueCustomField"] = Field(alias="$type", default="SingleVersionIssueCustomField")
    value: Optional[VersionBundleElement] = None


class StateIssueCustomField(IssueCustomField):
    type: Literal["StateIssueCustomField"] = Field(alias="$type", default="StateIssueCustomField")
    value: Optional[StateBundleElement] = None


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
    id: Optional[str] = None
    name: Optional[str] = None
    short_name: Optional[str] = Field(alias="shortName", default=None)


class Tag(BaseModel):
    type: Literal["Tag"] = Field(alias="$type", default="Tag")
    id: Optional[str] = None
    name: Optional[str] = None


class Issue(BaseModel):
    type: Literal["Issue"] = Field(alias="$type", default="Issue")
    id: Optional[str] = None
    id_readable: Optional[str] = Field(alias="idReadable", default=None)
    created: Optional[AwareDatetime] = None
    updated: Optional[AwareDatetime] = None
    resolved: Optional[AwareDatetime] = None
    project: Optional[Project] = None
    reporter: Optional[User] = None
    updater: Optional[User] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    wikified_description: Optional[str] = Field(alias="wikifiedDescription", default=None)
    comments_count: Optional[int] = Field(alias="commentsCount", default=None)
    tags: Optional[Sequence[Tag]] = None
    custom_fields: Optional[Sequence[IssueCustomFieldType]] = Field(alias="customFields", default=None)


class IssueAttachment(BaseModel):
    type: Literal["IssueAttachment"] = Field(alias="$type", default="IssueAttachment")
    id: Optional[str] = None
    name: Optional[str] = None
    author: Optional[User] = None
    created: Optional[AwareDatetime] = None
    updated: Optional[AwareDatetime] = None
    mime_type: Optional[str] = Field(alias="mimeType", default=None)
    url: Optional[str] = None


class IssueComment(BaseModel):
    type: Literal["IssueComment"] = Field(alias="$type", default="IssueComment")
    id: Optional[str] = None
    text: Optional[str] = None
    text_preview: Optional[str] = Field(alias="textPreview", default=None)
    created: Optional[AwareDatetime] = None
    updated: Optional[AwareDatetime] = None
    author: Optional[User] = None
    attachments: Optional[Sequence[IssueAttachment]] = None
    deleted: Optional[bool] = None


class IssueLinkType(BaseModel):
    type: Literal["IssueLinkType"] = Field(alias="$type", default="IssueLinkType")
    id: Optional[str] = None
    name: Optional[str] = None
    localized_name: Optional[str] = Field(alias="localizedName", default=None)
    source_to_target: Optional[str] = Field(alias="sourceToTarget", default=None)
    localized_source_to_target: Optional[str] = Field(alias="localizedSourceToTarget", default=None)
    target_to_source: Optional[str] = Field(alias="targetToSource", default=None)
    localized_target_to_source: Optional[str] = Field(alias="localizedTargetToSource", default=None)
    directed: Optional[bool] = None
    aggregation: Optional[bool] = None
    read_only: Optional[bool] = Field(alias="readOnly", default=None)


class IssueLink(BaseModel):
    id: Optional[str] = None
    direction: Optional[Literal["OUTWARD", "INWARD", "BOTH"]] = None
    link_type: Optional[IssueLinkType] = Field(alias="linkType", default=None)
    issues: Optional[Sequence[Issue]] = None
    trimmed_issues: Optional[Sequence[Issue]] = Field(alias="trimmedIssues", default=None)


class AgileRef(BaseModel):
    type: Literal["Agile"] = Field(alias="$type", default="Agile")
    id: Optional[str] = None
    name: Optional[str] = None


class SprintRef(BaseModel):
    type: Literal["Sprint"] = Field(alias="$type", default="Sprint")
    id: Optional[str] = None
    name: Optional[str] = None


class Agile(AgileRef):
    owner: Optional[User] = None
    visible_for: Optional[UserGroup] = Field(alias="visibleFor", default=None)
    projects: Optional[Sequence[Project]] = None
    sprints: Optional[Sequence[SprintRef]] = None
    current_sprint: Optional[SprintRef] = Field(alias="currentSprint", default=None)


class Sprint(SprintRef):
    agile: Optional[AgileRef] = None
    goal: Optional[str] = None
    start: Optional[AwareDatetime] = None
    finish: Optional[AwareDatetime] = None
    archived: Optional[bool] = None
    is_default: Optional[bool] = Field(alias="isDefault", default=None)
    issues: Optional[Sequence[Issue]] = None
    unresolved_issues_count: Optional[int] = Field(alias="unresolvedIssuesCount", default=None)
    previous_sprint: Optional[SprintRef] = Field(alias="previousSprint", default=None)
