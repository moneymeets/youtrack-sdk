# YouTrack REST API Client

A client library for accessing YouTrack REST API.

## Usage

```python
from datetime import date
from youtrack_sdk import Client
from youtrack_sdk.entities import (
    DateIssueCustomField,
    EnumBundleElement,
    Issue,
    IssueTag,
    Project,
    SingleEnumIssueCustomField,
    SingleUserIssueCustomField,
    StateBundleElement,
    StateIssueCustomField,
    User,
)

client = Client(base_url="https://dummy.myjetbrains.com/youtrack", token="dummy")
result = client.create_issue(
    issue=Issue(
        project=Project(id="0-0"),
        summary="Created from YouTrack SDK",
        description="Description **text**.",
        tags=[
            IssueTag(id="6-0"),
        ],
        custom_fields=[
            StateIssueCustomField(
                name="State",
                value=StateBundleElement(
                    name="In Progress",
                ),
            ),
            SingleUserIssueCustomField(
                name="Assignee",
                value=User(
                    ring_id="00000000-a31c-4174-bb27-abd3387df67a",
                ),
            ),
            SingleEnumIssueCustomField(
                name="Type",
                value=EnumBundleElement(
                    name="Bug",
                ),
            ),
            DateIssueCustomField(
                name="Due Date",
                value=date(2005, 12, 31),
            ),
        ],
    ),
)
```
