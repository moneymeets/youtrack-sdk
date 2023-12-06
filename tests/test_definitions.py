from datetime import UTC, date, datetime
from typing import Literal, Optional, Sequence

from pydantic import Field

from youtrack_sdk.entities import (
    Agile,
    AgileRef,
    BaseModel,
    CustomField,
    DateIssueCustomField,
    EnumBundleElement,
    EnumProjectCustomField,
    FieldType,
    Issue,
    IssueCustomFieldType,
    Project,
    SimpleIssueCustomField,
    SimpleProjectCustomField,
    SingleEnumIssueCustomField,
    SingleUserIssueCustomField,
    Sprint,
    SprintRef,
    StateBundleElement,
    StateIssueCustomField,
    StateProjectCustomField,
    Tag,
    User,
    UserGroup,
    UserProjectCustomField,
)


class CustomIssue(BaseModel):
    type: Literal["Issue"] = Field(alias="$type", default="Issue")
    id_readable: Optional[str] = Field(alias="idReadable", default=None)
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    resolved: Optional[datetime] = None
    comments_count: Optional[int] = Field(alias="commentsCount", default=None)
    custom_fields: Optional[Sequence[IssueCustomFieldType]] = Field(alias="customFields", default=None)


TEST_STATE_CUSTOM_FIELD = StateIssueCustomField.model_construct(
    id="110-50",
    name="State",
    type="StateIssueCustomField",
    value=StateBundleElement.model_construct(
        id="98-37",
        name="In Progress",
        type="StateBundleElement",
    ),
    project_custom_field=StateProjectCustomField.model_construct(
        field=CustomField.model_construct(
            type="CustomField",
            field_type=FieldType.model_construct(
                type="FieldType",
                id="state[1]",
            ),
        ),
        type="StateProjectCustomField",
    ),
)

TEST_ISSUE = Issue.model_construct(
    type="Issue",
    id="1-937",
    id_readable="HD-25",
    created=datetime(2021, 2, 9, 14, 3, 11, tzinfo=UTC),
    updated=datetime(2021, 8, 22, 10, 28, 16, tzinfo=UTC),
    resolved=None,
    project=Project.model_construct(
        type="Project",
        id="0-1",
        name="Help Desk",
        short_name="HD",
    ),
    reporter=User.model_construct(
        type="User",
        id="1-3",
        ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
        login="support",
        email="support@example.com",
    ),
    updater=User.model_construct(
        type="User",
        id="1-17",
        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
        login="max.demo",
        email="max@example.com",
    ),
    summary="Summary text",
    description="Issue description",
    wikified_description="Wikified issue description",
    comments_count=7,
    tags=[Tag.model_construct(type="Tag", id="5-7", name="Review")],
    custom_fields=[
        TEST_STATE_CUSTOM_FIELD,
        SingleUserIssueCustomField.model_construct(
            id="111-8",
            name="Assignee",
            type="SingleUserIssueCustomField",
            value=User.model_construct(
                type="User",
                id="1-10",
                ring_id="20e4e701-7e87-45f8-8492-c448600b7991",
                name="Worker Buddy",
                login="worker",
                email="worker@example.com",
            ),
            project_custom_field=UserProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="user[1]"),
                ),
                type="UserProjectCustomField",
            ),
        ),
        SingleEnumIssueCustomField.model_construct(
            id="110-49",
            name="Type",
            type="SingleEnumIssueCustomField",
            value=EnumBundleElement.model_construct(
                id="96-38",
                name="Value One",
                type="EnumBundleElement",
            ),
            project_custom_field=EnumProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="enum[1]"),
                ),
                type="EnumProjectCustomField",
            ),
        ),
        DateIssueCustomField.model_construct(
            id="145-34",
            name="Due Date",
            type="DateIssueCustomField",
            value=date(2023, 7, 4),
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="date"),
                ),
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-35",
            name="Started at",
            type="SimpleIssueCustomField",
            value=datetime(2021, 6, 11, 7, 32, 9, tzinfo=UTC),
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(
                        type="FieldType",
                        id="date and time",
                    ),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-36",
            name="Multipass",
            type="SimpleIssueCustomField",
            value="1623396729",
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="string"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-39",
            name="Price",
            type="SimpleIssueCustomField",
            value=4003,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="integer"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-37",
            name="Multiplier",
            type="SimpleIssueCustomField",
            value=3.1412,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="float"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-38",
            name="Extra",
            type="SimpleIssueCustomField",
            value=None,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="string"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
    ],
)

TEST_ISSUE_2 = Issue.model_construct(
    type="Issue",
    id="2-48",
    id_readable="HD-17",
    created=datetime(2022, 10, 26, 9, 44, 44, tzinfo=UTC),
    updated=datetime(2022, 10, 27, 16, 46, 11, tzinfo=UTC),
    resolved=datetime(2022, 10, 30, 18, 1, 55, tzinfo=UTC),
    project=Project.model_construct(
        type="Project",
        id="0-1",
        name="Help Desk",
        short_name="HD",
    ),
    reporter=User.model_construct(
        type="User",
        id="1-1",
        ring_id="8711cd4-90e3-445d-87ae-0925c9e1159d",
        login="alex",
        email="alex@example.com",
    ),
    updater=User.model_construct(
        type="User",
        id="1-17",
        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
        login="max.demo",
        email="max@example.com",
    ),
    summary="Title",
    description="Some text",
    wikified_description="Wikified some text",
    comments_count=0,
    tags=[],
    custom_fields=[
        StateIssueCustomField.model_construct(
            id="110-50",
            name="State",
            type="StateIssueCustomField",
            value=StateBundleElement.model_construct(
                id="98-22",
                name="Fixed",
                type="StateBundleElement",
            ),
            project_custom_field=StateProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(
                        type="FieldType",
                        id="state[1]",
                    ),
                ),
                type="StateProjectCustomField",
            ),
        ),
        SingleUserIssueCustomField.model_construct(
            id="111-8",
            name="Assignee",
            type="SingleUserIssueCustomField",
            value=None,
            project_custom_field=UserProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="user[1]"),
                ),
                type="UserProjectCustomField",
            ),
        ),
        SingleEnumIssueCustomField.model_construct(
            id="110-49",
            name="Type",
            type="SingleEnumIssueCustomField",
            value=EnumBundleElement.model_construct(
                id="96-95",
                name="Other",
                type="EnumBundleElement",
            ),
            project_custom_field=EnumProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="enum[1]"),
                ),
                type="EnumProjectCustomField",
            ),
        ),
        DateIssueCustomField.model_construct(
            id="145-34",
            name="Due Date",
            type="DateIssueCustomField",
            value=None,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="date"),
                ),
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-35",
            name="Started at",
            type="SimpleIssueCustomField",
            value=datetime(2022, 10, 26, 19, 21, 4, tzinfo=UTC),
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(
                        type="FieldType",
                        id="date and time",
                    ),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-36",
            name="Multipass",
            type="SimpleIssueCustomField",
            value="2000000000000",
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="string"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-39",
            name="Price",
            type="SimpleIssueCustomField",
            value=-128,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="integer"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-37",
            name="Multiplier",
            type="SimpleIssueCustomField",
            value=-2.4,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="float"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.model_construct(
            id="145-38",
            name="Extra",
            type="SimpleIssueCustomField",
            value=None,
            project_custom_field=SimpleProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="string"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
    ],
)

TEST_CUSTOM_ISSUE = CustomIssue.model_construct(
    type="Issue",
    id_readable="HD-25",
    created=datetime(2021, 2, 9, 14, 3, 11, tzinfo=UTC),
    updated=datetime(2021, 8, 22, 10, 28, 16, tzinfo=UTC),
    resolved=None,
    comments_count=7,
    custom_fields=[
        StateIssueCustomField.model_construct(
            id="110-50",
            name="State",
            type="StateIssueCustomField",
            value=StateBundleElement.model_construct(
                id="98-37",
                name="In Progress",
                type="StateBundleElement",
            ),
            project_custom_field=StateProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(
                        type="FieldType",
                        id="state[1]",
                    ),
                ),
                type="StateProjectCustomField",
            ),
        ),
        SingleEnumIssueCustomField.model_construct(
            id="110-49",
            name="Type",
            type="SingleEnumIssueCustomField",
            value=EnumBundleElement.model_construct(
                id="96-38",
                name="Value One",
                type="EnumBundleElement",
            ),
            project_custom_field=EnumProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="enum[1]"),
                ),
                type="EnumProjectCustomField",
            ),
        ),
    ],
)

TEST_CUSTOM_ISSUE_2 = CustomIssue.model_construct(
    type="Issue",
    id_readable="HD-17",
    created=datetime(2022, 10, 26, 9, 44, 44, tzinfo=UTC),
    updated=datetime(2022, 10, 27, 16, 46, 11, tzinfo=UTC),
    resolved=datetime(2022, 10, 30, 18, 1, 55, tzinfo=UTC),
    comments_count=0,
    custom_fields=[
        StateIssueCustomField.model_construct(
            id="110-50",
            name="State",
            type="StateIssueCustomField",
            value=StateBundleElement.model_construct(
                id="98-22",
                name="Fixed",
                type="StateBundleElement",
            ),
            project_custom_field=StateProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(
                        type="FieldType",
                        id="state[1]",
                    ),
                ),
                type="StateProjectCustomField",
            ),
        ),
        SingleEnumIssueCustomField.model_construct(
            id="110-49",
            name="Type",
            type="SingleEnumIssueCustomField",
            value=EnumBundleElement.model_construct(
                id="96-95",
                name="Other",
                type="EnumBundleElement",
            ),
            project_custom_field=EnumProjectCustomField.model_construct(
                field=CustomField.model_construct(
                    type="CustomField",
                    field_type=FieldType.model_construct(type="FieldType", id="enum[1]"),
                ),
                type="EnumProjectCustomField",
            ),
        ),
    ],
)

TEST_AGILE = Agile.model_construct(
    type="Agile",
    id="120-8",
    name="Kanban",
    owner=User.model_construct(
        type="User",
        id="1-17",
        name="Max Demo",
        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
        login="max.demo",
        email="max@example.com",
    ),
    visible_for=UserGroup.model_construct(
        type="UserGroup",
        id="3-20",
        name="Registered Users",
        ring_id="38012ba2-2b67-4ca3-a72b-523408d85b6d",
    ),
    projects=[
        Project.model_construct(
            type="Project",
            id="0-13",
            name="Kanban",
            short_name="KANBAN",
        ),
    ],
    sprints=[
        SprintRef.model_construct(
            type="Sprint",
            id="121-8",
            name="Week 1",
        ),
        SprintRef.model_construct(
            type="Sprint",
            id="121-11",
            name="Week 2",
        ),
    ],
    current_sprint=SprintRef.model_construct(
        type="Sprint",
        id="121-11",
        name="Week 2",
    ),
)

TEST_SPRINT = Sprint.model_construct(
    type="Sprint",
    id="121-8",
    name="Week 1",
    goal=None,
    start=datetime(2023, 1, 29, 0, 0, tzinfo=UTC),
    finish=datetime(2023, 2, 4, 23, 59, 59, 999000, tzinfo=UTC),
    archived=False,
    is_default=False,
    unresolved_issues_count=0,
    agile=AgileRef.model_construct(
        type="Agile",
        id="120-8",
        name="Kanban",
    ),
    issues=[],
    previous_sprint=None,
)
