from datetime import date, datetime, timezone
from functools import wraps
from pathlib import Path
from unittest import TestCase

import requests_mock

from youtrack_sdk.client import Client
from youtrack_sdk.entities import (
    DateIssueCustomField,
    EnumBundleElement,
    Issue,
    IssueAttachment,
    IssueComment,
    IssueTag,
    Project,
    SimpleIssueCustomField,
    SingleEnumIssueCustomField,
    SingleUserIssueCustomField,
    StateBundleElement,
    StateIssueCustomField,
    User,
)


def mock_response(url: str, response_name: str, method: str = "GET"):
    def wrapper(func):
        @wraps(func)
        @requests_mock.Mocker()
        def inner(self, m, *args, **kwargs):
            m.register_uri(
                method=method,
                url=url,
                text=(Path(__file__).parent / "responses" / f"{response_name}.json").read_text(),
            )
            return func(self, *args, **kwargs)

        return inner

    return wrapper


class TestClient(TestCase):
    def setUp(self):
        self.client = Client(base_url="https://server", token="test")

    @mock_response(url="https://server/api/issues/1", response_name="get_issue")
    def test_get_issue(self):
        self.assertEqual(
            Issue(
                type="Issue",
                id="1-937",
                idReadable="HD-25",
                created=datetime(2021, 2, 9, 14, 3, 11, tzinfo=timezone.utc),
                updated=datetime(2021, 8, 22, 10, 28, 16, tzinfo=timezone.utc),
                resolved=None,
                project=Project(
                    type="Project",
                    id="0-1",
                    name="Help Desk",
                    short_name="HD",
                ),
                reporter=User(
                    type="User",
                    id="1-3",
                    ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
                    login="support",
                    email="support@example.com",
                ),
                updater=User(
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
                    IssueTag(type="IssueTag", id="5-7", name="Review"),
                ],
                custom_fields=[
                    StateIssueCustomField(
                        id="110-50",
                        name="State",
                        type="StateIssueCustomField",
                        value=StateBundleElement(
                            id="98-37",
                            name="In Progress",
                            type="StateBundleElement",
                        ),
                    ),
                    SingleUserIssueCustomField(
                        id="111-8",
                        name="Assignee",
                        type="SingleUserIssueCustomField",
                        value=User(
                            type="User",
                            id="1-10",
                            ring_id="20e4e701-7e87-45f8-8492-c448600b7991",
                            name="Worker Buddy",
                            login="worker",
                            email="worker@example.com",
                        ),
                    ),
                    SingleEnumIssueCustomField(
                        id="110-49",
                        name="Type",
                        type="SingleEnumIssueCustomField",
                        value=EnumBundleElement(
                            id="96-38",
                            name="Value One",
                            type="EnumBundleElement",
                        ),
                    ),
                    DateIssueCustomField(
                        id="145-34",
                        name="Due Date",
                        type="DateIssueCustomField",
                        value=date(2022, 2, 17),
                    ),
                    SimpleIssueCustomField(
                        id="145-35",
                        name="Started at",
                        type="SimpleIssueCustomField",
                        value=datetime(2021, 6, 11, 7, 32, 9, tzinfo=timezone.utc),
                    ),
                    SimpleIssueCustomField(
                        id="145-36",
                        name="Multipass",
                        type="SimpleIssueCustomField",
                        value="100-003-675",
                    ),
                    SimpleIssueCustomField(
                        id="145-39",
                        name="Price",
                        type="SimpleIssueCustomField",
                        value=4003,
                    ),
                    SimpleIssueCustomField(
                        id="145-37",
                        name="Multiplier",
                        type="SimpleIssueCustomField",
                        value=3.1412,
                    ),
                    SimpleIssueCustomField(
                        id="145-38",
                        name="Extra",
                        type="SimpleIssueCustomField",
                        value=None,
                    ),
                ],
            ),
            self.client.get_issue(issue_id="1"),
        )

    @mock_response(url="https://server/api/issues/1/comments", response_name="get_issue_comments")
    def test_get_issue_comments(self):
        self.assertEqual(
            (
                IssueComment(
                    type="IssueComment",
                    id="4-296",
                    text="*Hello*, world!",
                    text_preview="<strong>Hello</strong>, world!",
                    created=datetime(2021, 12, 14, 11, 17, 48, tzinfo=timezone.utc),
                    updated=None,
                    author=User(
                        type="User",
                        id="1-3",
                        ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
                        login="support",
                        email="support@example.com",
                    ),
                    attachments=[],
                    deleted=False,
                ),
                IssueComment(
                    type="IssueComment",
                    id="4-443",
                    text="Sample _comment_",
                    text_preview="Sample <em>comment</em>",
                    created=datetime(2021, 12, 15, 12, 51, 40, tzinfo=timezone.utc),
                    updated=datetime(2021, 12, 15, 13, 8, 20, tzinfo=timezone.utc),
                    author=User(
                        type="User",
                        id="1-17",
                        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
                        login="max.demo",
                        email="max@example.com",
                    ),
                    attachments=[],
                    deleted=True,
                ),
                IssueComment(
                    type="IssueComment",
                    id="4-678",
                    text="Comment with attachments",
                    text_preview="One attachment",
                    created=datetime(2021, 12, 21, 16, 41, 33, tzinfo=timezone.utc),
                    updated=None,
                    author=User(
                        type="User",
                        id="1-9",
                        ring_id="f19c93e1-833b-407b-a4de-7f9a3370aaf3",
                        login="sam",
                        email="sam@example.com",
                    ),
                    attachments=[
                        IssueAttachment(
                            id="8-312",
                            type="IssueAttachment",
                            created=datetime(2021, 12, 21, 16, 41, 33, tzinfo=timezone.utc),
                            updated=datetime(2021, 12, 21, 16, 41, 35, tzinfo=timezone.utc),
                            author=None,
                            url="/attachments/url",
                            mime_type="text/plain",
                            name="test.txt",
                        ),
                    ],
                    deleted=False,
                ),
            ),
            self.client.get_issue_comments(issue_id="1"),
        )

    @mock_response(url="https://server/api/admin/projects", response_name="get_projects")
    def test_get_projects(self):
        self.assertEqual(
            (
                Project(
                    type="Project",
                    id="0-0",
                    name="Demo project",
                    short_name="DEMO",
                ),
                Project(
                    type="Project",
                    id="0-5",
                    name="Help Desk",
                    short_name="HD",
                ),
            ),
            self.client.get_projects(),
        )

    @mock_response(url="https://server/api/issueTags", response_name="get_tags")
    def test_get_tags(self):
        self.assertEqual(
            (
                IssueTag(
                    type="IssueTag",
                    id="6-0",
                    name="productivity",
                ),
                IssueTag(
                    type="IssueTag",
                    id="6-1",
                    name="tip",
                ),
                IssueTag(
                    type="IssueTag",
                    id="6-5",
                    name="Star",
                ),
            ),
            self.client.get_tags(),
        )

    @mock_response(url="https://server/api/users", response_name="get_users")
    def test_get_users(self):
        self.assertEqual(
            (
                User(
                    type="User",
                    id="1-17",
                    ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
                    login="max.demo",
                    email="max@example.com",
                ),
                User(
                    type="User",
                    id="1-3",
                    ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
                    login="support",
                    email="support@example.com",
                ),
                User(
                    type="User",
                    id="1-9",
                    ring_id="f19c93e1-833b-407b-a4de-7f9a3370aaf3",
                    login="sam",
                    email="sam@example.com",
                ),
                User(
                    type="User",
                    id="1-10",
                    ring_id="20e4e701-7e87-45f8-8492-c448600b7991",
                    name="Worker Buddy",
                    login="worker",
                    email="worker@example.com",
                ),
            ),
            self.client.get_users(),
        )
