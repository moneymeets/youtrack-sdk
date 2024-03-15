from http import HTTPMethod, HTTPStatus
from json import JSONDecodeError
from typing import IO, Optional, Sequence, Type
from urllib.parse import urlencode

from pydantic import TypeAdapter
from requests import HTTPError, Session

from .entities import (
    Agile,
    BaseModel,
    Issue,
    IssueAttachment,
    IssueComment,
    IssueCustomFieldType,
    IssueLink,
    IssueLinkType,
    IssueWorkItem,
    Project,
    Sprint,
    Tag,
    User,
    WorkItemType,
)
from .exceptions import YouTrackException, YouTrackNotFound, YouTrackUnauthorized
from .helpers import model_to_field_names, obj_to_json
from .types import IssueLinkDirection


class Client:
    def __init__(
        self,
        *,
        base_url: str,
        token: str,
        timeout: Optional[float | tuple[float, float]] = None,
    ):
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
        method: HTTPMethod,
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
        return self._send_request(method=HTTPMethod.GET, url=url)

    def _post(
        self,
        *,
        url: str,
        data: Optional[BaseModel] = None,
        files: Optional[dict[str, IO]] = None,
    ) -> Optional[dict]:
        return self._send_request(
            method=HTTPMethod.POST,
            url=url,
            data=data,
            files=files,
        )

    def _delete(self, *, url: str) -> Optional[dict]:
        return self._send_request(method=HTTPMethod.DELETE, url=url)

    def get_absolute_url(self, *, path: str) -> str:
        return f"{self._base_url}{path}"

    def get_issue(self, *, issue_id: str) -> Issue:
        """Read an issue with specific ID.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues.html#get-Issue-method
        """
        return Issue.model_validate(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}",
                    fields=model_to_field_names(Issue),
                ),
            ),
        )

    def get_issues[T](
        self,
        *,
        model: Type[T] = Issue,
        query: Optional[str] = None,
        custom_fields: Sequence[str] = (),
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[T]:
        """Get all issues that match the specified query.
        If you don't provide the query parameter, the server returns all issues.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues.html#get_all-Issue-method
        """
        return TypeAdapter(tuple[model, ...]).validate_python(
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
        return Issue.model_validate(
            self._post(
                url=self._build_url(
                    path="/issues",
                    fields=model_to_field_names(Issue),
                ),
                data=issue,
            ),
        )

    def update_issue(
        self,
        *,
        issue_id: str,
        issue: Issue,
        mute_update_notifications: bool = False,
    ) -> Issue:
        """Update an existing issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues.html#update-Issue-method
        """
        return Issue.model_validate(
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
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[IssueCustomFieldType]:
        """Get the list of available custom fields of the issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-customFields.html#get_all-IssueCustomField-method
        """
        return TypeAdapter(tuple[IssueCustomFieldType, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/customFields",
                    fields=model_to_field_names(IssueCustomFieldType),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def update_issue_custom_field(
        self,
        *,
        issue_id: str,
        field: IssueCustomFieldType,
        mute_update_notifications: bool = False,
    ) -> IssueCustomFieldType:
        """Update specific custom field in the issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-customFields.html#update-IssueCustomField-method
        """
        return TypeAdapter(IssueCustomFieldType).validate_python(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/customFields/{field.id}",
                    fields=model_to_field_names(IssueCustomFieldType),
                    muteUpdateNotifications=mute_update_notifications,
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

    def get_issue_comments(
        self,
        *,
        issue_id: str,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[IssueComment]:
        """Get all accessible comments of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-comments.html#get_all-IssueComment-method
        """
        return TypeAdapter(tuple[IssueComment, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments",
                    fields=model_to_field_names(IssueComment),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def create_issue_comment(
        self,
        *,
        issue_id: str,
        comment: IssueComment,
    ) -> IssueComment:
        """Add a new comment to an issue with a specific ID.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-comments.html#create-IssueComment-method
        """
        return IssueComment.model_validate(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments",
                    fields=model_to_field_names(IssueComment),
                ),
                data=comment,
            ),
        )

    def update_issue_comment(
        self,
        *,
        issue_id: str,
        comment: IssueComment,
        mute_update_notifications: bool = False,
    ) -> IssueComment:
        """Update an existing comment of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-comments.html#update-IssueComment-method
        """
        return IssueComment.model_validate(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments/{comment.id}",
                    fields=model_to_field_names(IssueComment),
                    muteUpdateNotifications=mute_update_notifications,
                ),
                data=comment,
            ),
        )

    def hide_issue_comment(self, *, issue_id: str, comment_id: str):
        """Hide a specific issue comment.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-comments.html#update-IssueComment-method
        """
        self.update_issue_comment(
            issue_id=issue_id,
            comment=(IssueComment(id=comment_id, deleted=True)),
        )

    def delete_issue_comment(self, *, issue_id: str, comment_id: str):
        """Delete a specific issue comment.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-issues-issueID-comments.html#delete-IssueComment-method
        """
        self._delete(
            url=self._build_url(
                path=f"/issues/{issue_id}/comments/{comment_id}",
            ),
        )

    def get_issue_attachments(
        self,
        *,
        issue_id: str,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[IssueAttachment]:
        """Get a list of all attachments of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-attachments.html#get_all-IssueAttachment-method
        """
        return TypeAdapter(tuple[IssueAttachment, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/attachments",
                    fields=model_to_field_names(IssueAttachment),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def create_issue_attachments(
        self,
        *,
        issue_id: str,
        files: dict[str, IO],
    ) -> Sequence[IssueAttachment]:
        """Add an attachment to the issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-attachments.html#create-IssueAttachment-method
        https://www.jetbrains.com/help/youtrack/devportal/api-usecase-attach-files.html
        """
        return TypeAdapter(tuple[IssueAttachment, ...]).validate_python(
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
        return TypeAdapter(tuple[IssueAttachment, ...]).validate_python(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/comments/{comment_id}/attachments",
                    fields=model_to_field_names(IssueAttachment),
                ),
                files=files,
            ),
        )

    def get_issue_work_items(
        self,
        *,
        issue_id: str,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[IssueWorkItem]:
        """Get the list of all work items of the specific issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-timeTracking-workItems.html#get_all-IssueWorkItem-method
        """
        return TypeAdapter(tuple[IssueWorkItem, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/timeTracking/workItems",
                    fields=model_to_field_names(IssueWorkItem),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def create_issue_work_item(self, *, issue_id: str, issue_work_item: IssueWorkItem) -> IssueWorkItem:
        """Add a new work item to the issue.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-timeTracking-workItems.html#create-IssueWorkItem-method
        """
        return IssueWorkItem.model_validate(
            self._post(
                url=self._build_url(
                    path=f"/issues/{issue_id}/timeTracking/workItems",
                    fields=model_to_field_names(IssueWorkItem),
                ),
                data=issue_work_item,
            ),
        )

    def get_projects(self, offset: Optional[int] = None, count: Optional[int] = None) -> Sequence[Project]:
        """Get a list of all available projects in the system.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-admin-projects.html#get_all-Project-method
        """
        return TypeAdapter(tuple[Project, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path="/admin/projects",
                    fields=model_to_field_names(Project),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_project_work_item_types(
        self,
        *,
        project_id: str,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[WorkItemType]:
        """Get the list of all work item types that are used in the project.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-admin-projects-projectID-timeTrackingSettings-workItemTypes.html#get_all-WorkItemType-method
        """
        return TypeAdapter(tuple[WorkItemType, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/admin/projects/{project_id}/timeTrackingSettings/workItemTypes",
                    fields=model_to_field_names(WorkItemType),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_tags(self, offset: Optional[int] = None, count: Optional[int] = None) -> Sequence[Tag]:
        """Get all tags that are visible to the current user.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-tags.html#get_all-Tag-method
        """
        return TypeAdapter(tuple[Tag, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path="/tags",
                    fields=model_to_field_names(Tag),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def add_issue_tag(self, *, issue_id: str, tag: Tag):
        """Tag the issue with an existing tag.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-tags.html#create-Tag-method
        """
        self._post(
            url=self._build_url(
                path=f"/issues/{issue_id}/tags",
            ),
            data=tag,
        )

    def get_users(self, offset: Optional[int] = None, count: Optional[int] = None) -> Sequence[User]:
        """Read the list of users in YouTrack.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-users.html#get_all-User-method
        """
        return TypeAdapter(tuple[User, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path="/users",
                    fields=model_to_field_names(User),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_issue_links(
        self,
        issue_id: str,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[IssueLink]:
        """Read the list of links for the issue in YouTrack.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issues-issueID-links.html#get_all-IssueLink-method
        """
        return TypeAdapter(tuple[IssueLink, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/issues/{issue_id}/links",
                    fields=model_to_field_names(IssueLink),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_issue_link_types(
        self,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[IssueLinkType]:
        """Read the list of all available link types in in YouTrack.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-issueLinkTypes.html#get_all-IssueLinkType-method
        """
        return TypeAdapter(tuple[IssueLinkType, ...]).validate_python(
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
        return TypeAdapter(Issue).validate_python(
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

    def get_agiles(self, *, offset: Optional[int] = None, count: Optional[int] = None) -> Sequence[Agile]:
        """Get the list of all available agile boards in the system.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-agiles.html#get_all-Agile-method
        """
        return TypeAdapter(tuple[Agile, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path="/agiles",
                    fields=model_to_field_names(Agile),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_agile(self, *, agile_id: str) -> Agile:
        """Get settings of the specific agile board.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-agiles.html#get-Agile-method
        """
        return Agile.model_validate(
            self._get(
                url=self._build_url(
                    path=f"/agiles/{agile_id}",
                    fields=model_to_field_names(Agile),
                ),
            ),
        )

    def get_sprints(
        self,
        *,
        agile_id: str,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Sequence[Sprint]:
        """Get the list of all sprints of the agile board.

        https://www.jetbrains.com/help/youtrack/devportal/resource-api-agiles-agileID-sprints.html#get_all-Sprint-method
        """
        return TypeAdapter(tuple[Sprint, ...]).validate_python(
            self._get(
                url=self._build_url(
                    path=f"/agiles/{agile_id}/sprints",
                    fields=model_to_field_names(Sprint),
                    offset=offset,
                    count=count,
                ),
            ),
        )

    def get_sprint(self, *, agile_id: str, sprint_id: str) -> Sprint:
        """Get settings of the specific sprint of the agile board.

        https://www.jetbrains.com/help/youtrack/devportal/operations-api-agiles-agileID-sprints.html#get-Sprint-method
        """
        return Sprint.model_validate(
            self._get(
                url=self._build_url(
                    path=f"/agiles/{agile_id}/sprints/{sprint_id}",
                    fields=model_to_field_names(Sprint),
                ),
            ),
        )
