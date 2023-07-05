from typing import Literal, Optional, Sequence, Union
from unittest import TestCase

from pydantic.v1 import Field

from youtrack_sdk.entities import BaseModel
from youtrack_sdk.helpers import model_to_field_names


class SimpleModel(BaseModel):
    type: Literal["SimpleModel"] = Field(alias="$type", default="SimpleModel")
    id: Optional[int]
    short_name: Optional[str] = Field(alias="shortName")


class NestedModel(BaseModel):
    type: Literal["NestedModel"] = Field(alias="$type", default="NestedModel")
    value: Optional[SimpleModel]


class NestedUnionModel(BaseModel):
    type: Literal["NestedUnionModel"] = Field(alias="$type", default="NestedUnionModel")
    items: Optional[Sequence[NestedModel | SimpleModel | int]]
    entry: Optional[NestedModel | SimpleModel | int]


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
