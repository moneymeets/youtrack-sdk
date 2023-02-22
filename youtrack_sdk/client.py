from http import HTTPStatus
from json import JSONDecodeError
from typing import IO, Optional, Sequence, Type, TypeVar
from urllib.parse import urlencode

from pydantic import parse_obj_as
from requests import HTTPError, Session

from .entities import (
    BaseModel,
    Issue,
    IssueAttachment,
    IssueComment,
    IssueCustomFieldType,
    IssueLink,
    IssueLinkType,
    IssueTag,
    Project,
    User,
)
from .exceptions import YouTrackException, YouTrackNotFound, YouTrackUnauthorized
from .helpers import model_to_field_names, obj_to_json
from .types import IssueLinkDirection

T = TypeVar("T", bound=BaseModel)


class Client:
    def __init__(self, *, base_url: str, token: str, timeout: Optional[float | tuple[float, float]] = None):
        """
        :param base_url: YouTrack instance URL (e.g. https://example.com/youtrack)
        :param token: Permanent YouTrack token
        :param timeout: (optional) How long to wait for the server to send data before giving up,
            as a float, or a (connect timeout, read timeout) tuple
        """
        self._base_url = base_url
        self._timeout = timeout
        self._session = Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
            },
        )

    def _build_url(
        self,
        *,
        path: str,
        fields: Optional[str] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
        **kwargs,
    ) -> str:
        query = urlencode(
            {
                key: str(value).lower() if isinstance(value, bool) else value
                for key, value in {
                    "fields": fields,
                    "$skip": offset,
                    "$top": count,
                    **kwargs,
                }.items()
                if value is not None
            },
            doseq=True,
        )
        return f"{self._base_url}/api{path}?{query}"

    def _send_request(
        self,
        *,
        method: str,
        url: str,
        data: Optional[BaseModel] = None,
        files: Optional[dict[str, IO]] = None,
    ) -> Optional[dict]:
        response = self._session.request(
            method=method,
            url=url,
            data=data and obj_to_json(data),
            files=files,
            headers=data and {"Content-Type": "application/json"},
            timeout=self._timeout,
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise YouTrackNotFound
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise YouTrackUnauthorized
        else:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise YouTrackException(
                    f"Unexpected status code for {method} {url}: {response.status_code}.",
                ) from e

        # Avoid JSONDecodeError if status code was 2xx, but the response content is empty.
        # Some API endpoints return empty, non-JSON responses on success.
        if len(response.content) == 0:
            return

        try:
            return response.json()
        except JSONDecodeError as e:
            raise YouTrackException(
                f"Failed to decode response from {method} {url}, status={response.status_code}",
            ) from e

    def _get(self, *, url: str) -> Optional[dict]:
        return self._send_request(method="GET", url=url)

    def _post(
        self,
        *,
        url: str,
        data: Optional[BaseModel] = None,
        files: Optional[dict[str, IO]] = None,
    ) -> Optional[dict]:
        return self._send_request(
            method="POST",
            url=url,
            data=data,
            files=files,
        )

    def _delete(self, *, url: str) -> Optional[dict]:
        return self._send_request(method="DELETE", url=url)

    def get_issue(self, *, issue_id: str) -> Issue:
        """Read an issue with specific ID.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues.html#get-Issue-method
        """
        return Issue.parse_obj(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}",
                    fields=model_to_field_names(Issue),
                ),
            ),
        )

    def get_issues(
        self,
        *,
        model: Type[T] = Issue,
        query: Optional[str] = None,
        custom_fields: Sequence[str] = (),
        offset: int = 0,
        count: int = -1,
    ) -> Sequence[T]:
        """Get all issues that match the specified query.
        If you don't provide the query parameter, the server returns all issues.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues.html#get_all-Issue-method
        """
        return parse_obj_as(
            tuple[model, ...],
            self._get(
                url=self._build_url(
                    path="/issues/",
                    fields=model_to_field_names(model),
                    query=query,
                    customFields=custom_fields,
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def create_issue(self, *, issue: Issue) -> Issue:
        """Create new issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues.html#create-Issue-method
        """
        return Issue.parse_obj(
            self._post(
                url=self._build_url(
                    path="/issues",
                    fields=model_to_field_names(Issue),
                ),
                data=issue,
            ),
        )

    def update_issue(self, *, issue_id: str, issue: Issue, mute_update_notifications: bool = False) -> Issue:
        """Update an existing issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues.html#update-Issue-method
        """
        return Issue.parse_obj(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}",
                    fields=model_to_field_names(Issue),
                    muteUpdateNotifications=mute_update_notifications,
                ),
                data=issue,
            ),
        )

    def get_issue_custom_fields(
        self,
        *,
        issue_id: str,
        offset: int = 0,
        count: int = -1,
    ) -> Sequence[IssueCustomFieldType]:
        """Get the list of available custom fields of the issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-customFields.html#get_all-IssueCustomField-method
        """
        return parse_obj_as(
            tuple[IssueCustomFieldType, ...],
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/customFields",
                    fields=model_to_field_names(IssueCustomFieldType),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def update_issue_custom_field(self, *, issue_id: str, field: IssueCustomFieldType) -> IssueCustomFieldType:
        """Update specific custom field in the issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-customFields.html#update-IssueCustomField-method
        """
        return parse_obj_as(
            IssueCustomFieldType,
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/customFields/{field.id}",
                    fields=model_to_field_names(IssueCustomFieldType),
                ),
                data=field,
            ),
        )

    def delete_issue(self, *, issue_id: str):
        """Delete the issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues.html#delete-Issue-method
        """
        self._delete(
            url=self._build_url(
                path=f"/issues/{issue_id}",
            ),
        )

    def get_issue_comments(self, *, issue_id: str, offset: int = 0, count: int = -1) -> Sequence[IssueComment]:
        """Get all accessible comments of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-comments.html#get_all-IssueComment-method
        """
        return parse_obj_as(
            tuple[IssueComment, ...],
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments",
                    fields=model_to_field_names(IssueComment),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def create_issue_comment(self, *, issue_id: str, comment: IssueComment) -> IssueComment:
        """Add a new comment to an issue with a specific ID.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-comments.html#create-IssueComment-method
        """
        return IssueComment.parse_obj(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments",
                    fields=model_to_field_names(IssueComment),
                ),
                data=comment,
            ),
        )

    def update_issue_comment(self, *, issue_id: str, comment: IssueComment) -> IssueComment:
        """Update an existing comment of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-comments.html#update-IssueComment-method
        """
        return IssueComment.parse_obj(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments/{comment.id}",
                    fields=model_to_field_names(IssueComment),
                ),
                data=comment,
            ),
        )

    def hide_issue_comment(self, *, issue_id: str, comment_id: str):
        """Hide a specific issue comment.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-comments.html#update-IssueComment-method
        """
        self.update_issue_comment(issue_id=issue_id, comment=(IssueComment(id=comment_id, deleted=True)))

    def delete_issue_comment(self, *, issue_id: str, comment_id: str):
        """Delete a specific issue comment.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-comments.html#delete-IssueComment-method
        """
        self._delete(
            url=self._build_url(
                path=f"/issues/{issue_id}/comments/{comment_id}",
            ),
        )

    def get_issue_attachments(self, *, issue_id: str, offset: int = 0, count: int = -1) -> Sequence[IssueAttachment]:
        """Get a list of all attachments of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-attachments.html#get_all-IssueAttachment-method
        """
        return parse_obj_as(
            tuple[IssueAttachment, ...],
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/attachments",
                    fields=model_to_field_names(IssueAttachment),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def create_issue_attachments(self, *, issue_id: str, files: dict[str, IO]) -> Sequence[IssueAttachment]:
        """Add an attachment to the issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-attachments.html#create-IssueAttachment-method
        https://www.jetbrains.com/help/youtrack/devportal/api-usecase-attach-files.html
        """
        return parse_obj_as(
            tuple[IssueAttachment, ...],
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/attachments",
                    fields=model_to_field_names(IssueAttachment),
                ),
                files=files,
            ),
        )

    def create_comment_attachments(
        self,
        *,
        issue_id: str,
        comment_id: str,
        files: dict[str, IO],
    ) -> Sequence[IssueAttachment]:
        return parse_obj_as(
            tuple[IssueAttachment, ...],
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments/{comment_id}/attachments",
                    fields=model_to_field_names(IssueAttachment),
                ),
                files=files,
            ),
        )

    def get_projects(self, offset: int = 0, count: int = -1) -> Sequence[Project]:
        """Get a list of all available projects in the system.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-admin-projects.html#get_all-Project-method
        """
        return parse_obj_as(
            tuple[Project, ...],
            self._get(
                url=self._build_url(
                    path="/admin/projects",
                    fields=model_to_field_names(Project),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_tags(self, offset: int = 0, count: int = -1) -> Sequence[IssueTag]:
        """Get all tags that are visible to the current user.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issueTags.html#get_all-IssueTag-method
        """
        return parse_obj_as(
            tuple[IssueTag, ...],
            self._get(
                url=self._build_url(
                    path="/issueTags",
                    fields=model_to_field_names(IssueTag),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def add_issue_tag(self, *, issue_id: str, tag: IssueTag):
        self._post(
            url=self._build_url(
                path=f"/issues/{issue_id}/tags",
            ),
            data=tag,
        )

    def get_users(self, offset: int = 0, count: int = -1) -> Sequence[User]:
        """Read the list of users in YouTrack.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-users.html#get_all-User-method
        """
        return parse_obj_as(
            tuple[User, ...],
            self._get(
                url=self._build_url(
                    path="/users",
                    fields=model_to_field_names(User),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_issue_links(self, issue_id: str, offset: int = 0, count: int = -1) -> Sequence[IssueLink]:
        """Read the list of links for the issue in YouTrack.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-links.html#get_all-IssueLink-method
        """
        return parse_obj_as(
            tuple[IssueLink, ...],
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/links",
                    fields=model_to_field_names(IssueLink),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_issue_link_types(self, offset: int = 0, count: int = -1) -> Sequence[IssueLinkType]:
        """Read the list of all available link types in in YouTrack.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issueLinkTypes.html#get_all-IssueLinkType-method
        """
        return parse_obj_as(
            tuple[IssueLinkType, ...],
            self._get(
                url=self._build_url(
                    path="/issueLinkTypes",
                    fields=model_to_field_names(IssueLinkType),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def link_issues(
        self,
        *,
        source_issue_id: str,
        target_issue_id: str,
        link_type_id: str,
        link_direction: IssueLinkDirection,
    ) -> Issue:
        """Link an issue to another issue

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-links-linkID-issues.html#create-Issue-method
        """
        return parse_obj_as(
            Issue,
            self._post(
                url=self._build_url(
                    path=f"/issues/{source_issue_id}/links/{link_type_id}{link_direction.value}/issues",
                    fields=model_to_field_names(Issue),
                ),
                data=Issue(id=target_issue_id),
            ),
        )

    def delete_issue_link(
        self,
        *,
        source_issue_id: str,
        target_issue_id: str,
        link_type_id: str,
    ):
        """Delete the link between issues.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-links-linkID-issues.html#delete-Issue-method
        """
        self._delete(
            url=self._build_url(
                path=f"/issues/{source_issue_id}/links/{link_type_id}/issues/{target_issue_id}",
            ),
        )
