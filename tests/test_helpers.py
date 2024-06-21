from http import HTTPStatus
from typing import Annotated, Literal, Optional, Sequence, Union
from unittest import TestCase

import requests_mock
from pydantic import Field

from tests.test_definitions import TEST_ISSUE, TEST_STATE_CUSTOM_FIELD
from youtrack_sdk import Client
from youtrack_sdk.entities import BaseModel
from youtrack_sdk.helpers import NonSingleValueError, exists, get_issue_custom_field, model_to_field_names


class SimpleModel(BaseModel):
    type: Literal["SimpleModel"] = Field(alias="$type", default="SimpleModel")
    id: Optional[int] = None
    short_name: Optional[str] = Field(alias="shortName", default=None)


class NestedModel(BaseModel):
    type: Literal["NestedModel"] = Field(alias="$type", default="NestedModel")
    value: Optional[SimpleModel] = None


class NestedUnionModel(BaseModel):
    type: Literal["NestedUnionModel"] = Field(alias="$type", default="NestedUnionModel")
    items: Optional[Sequence[NestedModel | SimpleModel | int]] = None
    entry: Optional[NestedModel | SimpleModel | int] = None


class TestModelToFieldNames(TestCase):
    def test_simple_model(self):
        self.assertEqual(
            "$type,id,shortName",
            model_to_field_names(SimpleModel),
        )

    def test_nested_model(self):
        self.assertEqual(
            "$type,value($type,id,shortName)",
            model_to_field_names(NestedModel),
        )

    def test_nested_union_model(self):
        self.assertEqual(
            "$type,"
            "items($type,value($type,id,shortName),id,shortName),"
            "entry($type,value($type,id,shortName),id,shortName)",
            model_to_field_names(NestedUnionModel),
        )

    def test_union_type(self):
        self.assertEqual(
            "$type,id,shortName,value($type,id,shortName)",
            model_to_field_names(SimpleModel | NestedModel),
        )
        self.assertEqual(
            "$type,id,shortName,value($type,id,shortName)",
            model_to_field_names(Union[SimpleModel | NestedModel]),
        )
        self.assertEqual(
            "$type,id,shortName,value($type,id,shortName)",
            model_to_field_names(Annotated[SimpleModel | NestedModel, Field(discriminator="type")]),
        )


class TestHelpers(TestCase):
    def setUp(self):
        self.client = Client(base_url="https://server", token="test")

    def test_get_issue_custom_field(self):
        self.assertEqual(
            get_issue_custom_field(issue=TEST_ISSUE, field_name="State"),
            TEST_STATE_CUSTOM_FIELD,
        )
        self.assertRaises(
            NonSingleValueError,
            get_issue_custom_field,
            issue=TEST_ISSUE,
            field_name="Unknown",
        )

    @requests_mock.Mocker()
    def test_issue_exists(self, m):
        m.register_uri(method="GET", url="https://server/api/issues/1", json={})
        self.assertTrue(exists(self.client.get_issue, issue_id="1"))

    @requests_mock.Mocker()
    def test_issue_not_found(self, m):
        m.register_uri(method="GET", url="https://server/api/issues/1", status_code=HTTPStatus.NOT_FOUND)
        self.assertFalse(exists(self.client.get_issue, issue_id="1"))
