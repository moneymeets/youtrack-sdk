from datetime import date, datetime, timezone

from youtrack_sdk.entities import (
    CustomField,
    DateIssueCustomField,
    EnumBundleElement,
    EnumProjectCustomField,
    FieldType,
    Issue,
    IssueTag,
    Project,
    SimpleIssueCustomField,
    SimpleProjectCustomField,
    SingleEnumIssueCustomField,
    SingleUserIssueCustomField,
    StateBundleElement,
    StateIssueCustomField,
    StateProjectCustomField,
    User,
    UserProjectCustomField,
)

TEST_ISSUE = Issue.construct(
    type="Issue",
    id="1-937",
    id_readable="HD-25",
    created=datetime(2021, 2, 9, 14, 3, 11, tzinfo=timezone.utc),
    updated=datetime(2021, 8, 22, 10, 28, 16, tzinfo=timezone.utc),
    resolved=None,
    project=Project.construct(
        type="Project",
        id="0-1",
        name="Help Desk",
        short_name="HD",
    ),
    reporter=User.construct(
        type="User",
        id="1-3",
        ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
        login="support",
        email="support@example.com",
    ),
    updater=User.construct(
        type="User",
        id="1-17",
        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
        login="max.demo",
        email="max@example.com",
    ),
    summary="Summary text",
    description="Issue description",
    wikified_description="Wikified issue description",
    tags=[
        IssueTag.construct(type="IssueTag", id="5-7", name="Review"),
    ],
    custom_fields=[
        StateIssueCustomField.construct(
            id="110-50",
            name="State",
            type="StateIssueCustomField",
            value=StateBundleElement.construct(
                id="98-37",
                name="In Progress",
                type="StateBundleElement",
            ),
            project_custom_field=StateProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(
                        type="FieldType",
                        id="state[1]",
                    ),
                ),
                type="StateProjectCustomField",
            ),
        ),
        SingleUserIssueCustomField.construct(
            id="111-8",
            name="Assignee",
            type="SingleUserIssueCustomField",
            value=User.construct(
                type="User",
                id="1-10",
                ring_id="20e4e701-7e87-45f8-8492-c448600b7991",
                name="Worker Buddy",
                login="worker",
                email="worker@example.com",
            ),
            project_custom_field=UserProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="user[1]"),
                ),
                type="UserProjectCustomField",
            ),
        ),
        SingleEnumIssueCustomField.construct(
            id="110-49",
            name="Type",
            type="SingleEnumIssueCustomField",
            value=EnumBundleElement.construct(
                id="96-38",
                name="Value One",
                type="EnumBundleElement",
            ),
            project_custom_field=EnumProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="enum[1]"),
                ),
                type="EnumProjectCustomField",
            ),
        ),
        DateIssueCustomField.construct(
            id="145-34",
            name="Due Date",
            type="DateIssueCustomField",
            value=date(2022, 2, 17),
            project_custom_field=SimpleProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="date"),
                ),
            ),
        ),
        SimpleIssueCustomField.construct(
            id="145-35",
            name="Started at",
            type="SimpleIssueCustomField",
            value=datetime(2021, 6, 11, 7, 32, 9, tzinfo=timezone.utc),
            project_custom_field=SimpleProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(
                        type="FieldType",
                        id="date and time",
                    ),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.construct(
            id="145-36",
            name="Multipass",
            type="SimpleIssueCustomField",
            value="1623396729",
            project_custom_field=SimpleProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="string"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.construct(
            id="145-39",
            name="Price",
            type="SimpleIssueCustomField",
            value=4003,
            project_custom_field=SimpleProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="integer"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.construct(
            id="145-37",
            name="Multiplier",
            type="SimpleIssueCustomField",
            value=3.1412,
            project_custom_field=SimpleProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="float"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
        SimpleIssueCustomField.construct(
            id="145-38",
            name="Extra",
            type="SimpleIssueCustomField",
            value=None,
            project_custom_field=SimpleProjectCustomField.construct(
                field=CustomField.construct(
                    type="CustomField",
                    field_type=FieldType.construct(type="FieldType", id="string"),
                ),
                type="SimpleProjectCustomField",
            ),
        ),
    ],
)
