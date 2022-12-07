from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from unittest import TestCase

import requests_mock

from youtrack_sdk.client import Client
from youtrack_sdk.entities import (
    Issue,
    IssueAttachment,
    IssueComment,
    IssueLink,
    IssueLinkType,
    IssueTag,
    Project,
    User,
)

from .test_definitions import TEST_ISSUE


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

    @mock_response(url="https://server/api/issues/1", response_name="issue")
    def test_get_issue(self):
        self.assertEqual(
            TEST_ISSUE,
            self.client.get_issue(issue_id="1"),
        )

    @mock_response(url="https://server/api/issues/", response_name="get_issues")
    def test_get_issues(self):
        self.assertEqual(
            (
                Issue.construct(
                    type="Issue",
                    id="12-379",
                    id_readable="TD-001",
                    created=datetime(2022, 10, 26, 9, 44, 44, 495000, tzinfo=timezone.utc),
                    updated=datetime(2022, 10, 27, 16, 46, 11, 562000, tzinfo=timezone.utc),
                    resolved=None,
                    project=Project(
                        type="Project",
                        id="0-4",
                        name="Test Project",
                        short_name="TD",
                    ),
                    reporter=User(
                        type="User",
                        id="12",
                        name="support",
                        ringId="8711cd4-90e3-445d-87ae-0925c9e1159d",
                        login="Support",
                        email=None,
                    ),
                    summary="Project Summary",
                    description="Issue description",
                    wikified_description="",
                    tags=[],
                    custom_fields=[],
                ),
                Issue.construct(
                    type="Issue",
                    id="12-378",
                    id_readable="TD-002",
                    created=datetime(2022, 10, 26, 9, 44, 44, 495000, tzinfo=timezone.utc),
                    updated=datetime(2022, 10, 27, 16, 46, 11, 562000, tzinfo=timezone.utc),
                    resolved=None,
                    project=Project(
                        type="Project",
                        id="0-4",
                        name="Test Project",
                        short_name="TD",
                    ),
                    reporter=User(
                        type="User",
                        id="12",
                        name="support",
                        ringId="8711cd4-90e3-445d-87ae-0925c9e1159d",
                        login="Support",
                        email=None,
                    ),
                    summary="Project Summary",
                    description="Issue description",
                    wikified_description="",
                    tags=[],
                    custom_fields=[],
                ),
            ),
            self.client.get_issues(query="in:TD for:me"),
        )

    @mock_response(url="https://server/api/issues/1/comments", response_name="get_issue_comments")
    def test_get_issue_comments(self):
        self.assertEqual(
            (
                IssueComment.construct(
                    type="IssueComment",
                    id="4-296",
                    text="*Hello*, world!",
                    text_preview="<strong>Hello</strong>, world!",
                    created=datetime(2021, 12, 14, 11, 17, 48, tzinfo=timezone.utc),
                    updated=None,
                    author=User.construct(
                        type="User",
                        id="1-3",
                        ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
                        login="support",
                        email="support@example.com",
                    ),
                    attachments=[],
                    deleted=False,
                ),
                IssueComment.construct(
                    type="IssueComment",
                    id="4-443",
                    text="Sample _comment_",
                    text_preview="Sample <em>comment</em>",
                    created=datetime(2021, 12, 15, 12, 51, 40, tzinfo=timezone.utc),
                    updated=datetime(2021, 12, 15, 13, 8, 20, tzinfo=timezone.utc),
                    author=User.construct(
                        type="User",
                        id="1-17",
                        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
                        login="max.demo",
                        email="max@example.com",
                    ),
                    attachments=[],
                    deleted=True,
                ),
                IssueComment.construct(
                    type="IssueComment",
                    id="4-678",
                    text="Comment with attachments",
                    text_preview="One attachment",
                    created=datetime(2021, 12, 21, 16, 41, 33, tzinfo=timezone.utc),
                    updated=None,
                    author=User.construct(
                        type="User",
                        id="1-9",
                        ring_id="f19c93e1-833b-407b-a4de-7f9a3370aaf3",
                        login="sam",
                        email="sam@example.com",
                    ),
                    attachments=[
                        IssueAttachment.construct(
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
                Project.construct(
                    type="Project",
                    id="0-0",
                    name="Demo project",
                    short_name="DEMO",
                ),
                Project.construct(
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
                IssueTag.construct(
                    type="IssueTag",
                    id="6-0",
                    name="productivity",
                ),
                IssueTag.construct(
                    type="IssueTag",
                    id="6-1",
                    name="tip",
                ),
                IssueTag.construct(
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
                User.construct(
                    type="User",
                    id="1-17",
                    ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
                    login="max.demo",
                    email="max@example.com",
                ),
                User.construct(
                    type="User",
                    id="1-3",
                    ring_id="b0fea1e1-ed18-43f6-a99d-40044fb1dfb0",
                    login="support",
                    email="support@example.com",
                ),
                User.construct(
                    type="User",
                    id="1-9",
                    ring_id="f19c93e1-833b-407b-a4de-7f9a3370aaf3",
                    login="sam",
                    email="sam@example.com",
                ),
                User.construct(
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

    @mock_response(url="https://server/api/issueLinkTypes", response_name="get_issue_link_types")
    def test_get_issue_link_types(self):
        self.assertEqual(
            (
                IssueLinkType.construct(
                    type="IssueLinkType",
                    id="106-0",
                    name="Relates",
                    localized_name=None,
                    source_to_target="relates to",
                    localized_source_to_target=None,
                    target_to_source="",
                    localized_target_to_source=None,
                    directed=False,
                    aggregation=False,
                    read_only=False,
                ),
                IssueLinkType.construct(
                    type="IssueLinkType",
                    id="106-1",
                    name="Depend",
                    localized_name=None,
                    source_to_target="is required for",
                    localized_source_to_target=None,
                    target_to_source="depends on",
                    localized_target_to_source=None,
                    directed=True,
                    aggregation=False,
                    read_only=False,
                ),
                IssueLinkType.construct(
                    type="IssueLinkType",
                    id="106-2",
                    name="Duplicate",
                    localized_name=None,
                    source_to_target="is duplicated by",
                    localized_source_to_target=None,
                    target_to_source="duplicates",
                    localized_target_to_source=None,
                    directed=True,
                    aggregation=True,
                    read_only=True,
                ),
                IssueLinkType.construct(
                    type="IssueLinkType",
                    id="106-3",
                    name="Subtask",
                    localized_name=None,
                    source_to_target="parent for",
                    localized_source_to_target=None,
                    target_to_source="subtask of",
                    localized_target_to_source=None,
                    directed=True,
                    aggregation=True,
                    read_only=True,
                ),
            ),
            self.client.get_issue_link_types(),
        )

    @mock_response(url="https://server/api/issues/1/links", response_name="get_issue_links")
    def test_get_issue_links(self):
        self.assertEqual(
            (
                IssueLink.construct(
                    id="106-0",
                    direction="BOTH",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-0",
                        name="Relates",
                        localized_name=None,
                        source_to_target="relates to",
                        localized_source_to_target=None,
                        target_to_source="",
                        localized_target_to_source=None,
                        directed=False,
                        aggregation=False,
                        read_only=False,
                    ),
                    issues=[],
                    trimmed_issues=[],
                ),
                IssueLink.construct(
                    id="106-1s",
                    direction="OUTWARD",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-1",
                        name="Depend",
                        localized_name=None,
                        source_to_target="is required for",
                        localized_source_to_target=None,
                        target_to_source="depends on",
                        localized_target_to_source=None,
                        directed=True,
                        aggregation=False,
                        read_only=False,
                    ),
                    issues=[],
                    trimmed_issues=[],
                ),
                IssueLink.construct(
                    id="106-1t",
                    direction="INWARD",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-1",
                        name="Depend",
                        localized_name=None,
                        source_to_target="is required for",
                        localized_source_to_target=None,
                        target_to_source="depends on",
                        localized_target_to_source=None,
                        directed=True,
                        aggregation=False,
                        read_only=False,
                    ),
                    issues=[],
                    trimmed_issues=[],
                ),
                IssueLink.construct(
                    id="106-2s",
                    direction="OUTWARD",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-2",
                        name="Duplicate",
                        localized_name=None,
                        source_to_target="is duplicated by",
                        localized_source_to_target=None,
                        target_to_source="duplicates",
                        localized_target_to_source=None,
                        directed=True,
                        aggregation=True,
                        read_only=True,
                    ),
                    issues=[
                        Issue.construct(
                            type="Issue",
                            id="2-46619",
                            id_readable="PT-1839",
                            created=datetime(2022, 9, 26, 13, 50, 12, 810000, tzinfo=timezone.utc),
                            updated=datetime(2022, 10, 5, 6, 28, 57, 291000, tzinfo=timezone.utc),
                            resolved=datetime(2022, 9, 26, 13, 51, 29, 671000, tzinfo=timezone.utc),
                            project=Project.construct(
                                type="Project",
                                id="0-4",
                                name="Test: project",
                                short_name="PT",
                            ),
                            reporter=User.construct(
                                type="User",
                                id="1-52",
                                name="Mary Jane",
                                ring_id="26677773-c425-4f47-b62c-dbfb2ad21e8f",
                                login="mary.jane",
                                email=None,
                            ),
                            updater=User.construct(
                                type="User",
                                id="1-64",
                                name="Paul Lawson",
                                ring_id="d53ece48-4c60-4b88-b93f-68392b975087",
                                login="paul.lawson",
                                email="",
                            ),
                            summary="Fintra Auftrag: 99 - Last Name, First Name",
                            description="",
                            wikified_description="",
                            tags=[],
                            custom_fields=[],
                        ),
                    ],
                    trimmed_issues=[
                        Issue.construct(
                            type="Issue",
                            id="2-46619",
                            id_readable="PT-1839",
                            created=datetime(2022, 9, 26, 13, 50, 12, 810000, tzinfo=timezone.utc),
                            updated=datetime(2022, 10, 5, 6, 28, 57, 291000, tzinfo=timezone.utc),
                            resolved=datetime(2022, 9, 26, 13, 51, 29, 671000, tzinfo=timezone.utc),
                            project=Project.construct(
                                type="Project",
                                id="0-4",
                                name="Test: project",
                                short_name="PT",
                            ),
                            reporter=User.construct(
                                type="User",
                                id="1-52",
                                name="Mary Jane",
                                ring_id="26677773-c425-4f47-b62c-dbfb2ad21e8f",
                                login="mary.jane",
                                email=None,
                            ),
                            updater=User.construct(
                                type="User",
                                id="1-64",
                                name="Paul Lawson",
                                ring_id="d53ece48-4c60-4b88-b93f-68392b975087",
                                login="paul.lawson",
                                email="",
                            ),
                            summary="Fintra Auftrag: 99 - Last Name, First Name",
                            description="",
                            wikified_description="",
                            tags=[],
                            custom_fields=[],
                        ),
                    ],
                ),
                IssueLink.construct(
                    id="106-2t",
                    direction="INWARD",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-2",
                        name="Duplicate",
                        localized_name=None,
                        source_to_target="is duplicated by",
                        localized_source_to_target=None,
                        target_to_source="duplicates",
                        localized_target_to_source=None,
                        directed=True,
                        aggregation=True,
                        read_only=True,
                    ),
                    issues=[],
                    trimmed_issues=[],
                ),
                IssueLink.construct(
                    id="106-3s",
                    direction="OUTWARD",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-3",
                        name="Subtask",
                        localized_name=None,
                        source_to_target="parent for",
                        localized_source_to_target=None,
                        target_to_source="subtask of",
                        localized_target_to_source=None,
                        directed=True,
                        aggregation=True,
                        read_only=True,
                    ),
                    issues=[],
                    trimmed_issues=[],
                ),
                IssueLink.construct(
                    id="106-3t",
                    direction="INWARD",
                    link_type=IssueLinkType.construct(
                        type="IssueLinkType",
                        id="106-3",
                        name="Subtask",
                        localized_name=None,
                        source_to_target="parent for",
                        localized_source_to_target=None,
                        target_to_source="subtask of",
                        localized_target_to_source=None,
                        directed=True,
                        aggregation=True,
                        read_only=True,
                    ),
                    issues=[],
                    trimmed_issues=[],
                ),
            ),
            self.client.get_issue_links(issue_id="1"),
        )

    @mock_response(url="https://server/api/issues/1", response_name="issue", method="POST")
    def test_update_issue(self):
        self.assertEqual(
            TEST_ISSUE,
            self.client.update_issue(issue_id="1", issue=TEST_ISSUE),
        )
