from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from unittest import TestCase
from unittest.mock import ANY, patch

import requests_mock
from requests import ConnectTimeout

import youtrack_sdk.client
from youtrack_sdk.client import Client
from youtrack_sdk.entities import (
    Agile,
    AgileRef,
    Issue,
    IssueAttachment,
    IssueComment,
    IssueLink,
    IssueLinkType,
    IssueTag,
    Project,
    Sprint,
    SprintRef,
    User,
)

from .test_definitions import (
    TEST_AGILE,
    TEST_CUSTOM_ISSUE,
    TEST_CUSTOM_ISSUE_2,
    TEST_ISSUE,
    TEST_ISSUE_2,
    TEST_SPRINT,
    CustomIssue,
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

    @patch.object(youtrack_sdk.client.Session, "request", side_effect=ConnectTimeout)
    def test_client_timeout(self, mock_request):
        client = Client(base_url="https://server", token="test", timeout=123)
        with self.assertRaises(ConnectTimeout):
            client.get_issue(issue_id="1")
        mock_request.assert_called_once_with(method="GET", url=ANY, data=None, files=None, headers=None, timeout=123)

    @mock_response(url="https://server/api/issues/1", response_name="issue")
    def test_get_issue(self):
        self.assertEqual(
            TEST_ISSUE,
            self.client.get_issue(issue_id="1"),
        )

    @mock_response(url="https://server/api/issues/", response_name="issues")
    def test_get_issues(self):
        self.assertEqual(
            (TEST_ISSUE, TEST_ISSUE_2),
            self.client.get_issues(query="in:TD for:me"),
        )

    @mock_response(url="https://server/api/issues/", response_name="issues_custom_model")
    def test_get_issues_custom_model(self):
        self.assertEqual(
            (TEST_CUSTOM_ISSUE, TEST_CUSTOM_ISSUE_2),
            self.client.get_issues(model=CustomIssue, custom_fields=["State", "Type"]),
        )

    @mock_response(url="https://server/api/issues/1/comments", response_name="issue_comments")
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

    @mock_response(url="https://server/api/admin/projects", response_name="projects")
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

    @mock_response(url="https://server/api/issueTags", response_name="tags")
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

    @mock_response(url="https://server/api/users", response_name="users")
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

    @mock_response(url="https://server/api/issueLinkTypes", response_name="issue_link_types")
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

    @mock_response(url="https://server/api/issues/1/links", response_name="issue_links")
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
                            comments_count=5,
                            tags=[],
                            custom_fields=[],
                        ),
                    ],
                    trimmed_issues=[
                        Issue.construct(
                            type="Issue",
                            id="2-46619",
                            id_readable="PT-1840",
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
                            comments_count=0,
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

    @mock_response(url="https://server/api/agiles", response_name="agiles", method="GET")
    def test_get_agiles(self):
        self.assertEqual(
            (
                Agile.construct(
                    type="Agile",
                    id="120-0",
                    name="Demo Board",
                    owner=User.construct(
                        type="User",
                        id="1-17",
                        name="Max Demo",
                        ring_id="c5d08431-dd52-4cdd-9911-7ec3a18ad117",
                        login="max.demo",
                        email="max@example.com",
                    ),
                    visible_for=None,
                    projects=[
                        Project.construct(
                            type="Project",
                            id="0-0",
                            name="Demo project",
                            short_name="DEMO",
                        ),
                    ],
                    sprints=[
                        SprintRef.construct(
                            type="Sprint",
                            id="121-12",
                            name="First sprint",
                        ),
                    ],
                    current_sprint=SprintRef.construct(
                        type="Sprint",
                        id="121-12",
                        name="First sprint",
                    ),
                ),
                TEST_AGILE,
            ),
            self.client.get_agiles(),
        )

    @mock_response(url="https://server/api/agiles/120-8", response_name="agile", method="GET")
    def test_get_agile(self):
        self.assertEqual(
            TEST_AGILE,
            self.client.get_agile(agile_id="120-8"),
        )

    @mock_response(url="https://server/api/agiles/120-8/sprints", response_name="sprints", method="GET")
    def test_get_sprints(self):
        self.assertEqual(
            (
                TEST_SPRINT,
                Sprint.construct(
                    type="Sprint",
                    id="121-11",
                    name="Week 2",
                    goal="Finish everything",
                    start=datetime(2023, 2, 5, 0, 0, tzinfo=timezone.utc),
                    finish=datetime(2023, 2, 18, 23, 59, 59, 999000, tzinfo=timezone.utc),
                    archived=False,
                    is_default=False,
                    unresolved_issues_count=0,
                    agile=AgileRef.construct(
                        type="Agile",
                        id="120-8",
                        name="Kanban",
                    ),
                    issues=[TEST_ISSUE],
                    previous_sprint=None,
                ),
            ),
            self.client.get_sprints(agile_id="120-8"),
        )

    @mock_response(url="https://server/api/agiles/120-8/sprints/121-8", response_name="sprint", method="GET")
    def test_get_sprint(self):
        self.assertEqual(
            TEST_SPRINT,
            self.client.get_sprint(agile_id="120-8", sprint_id="121-8"),
        )
