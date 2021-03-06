import inspect
from dataclasses import asdict

import pandas as pd
import pytest

from project_name.mypkg import pddisplay


@pytest.fixture()
def my_custom():
    obj = pd.options.display
    pddisplay.custom()

    customs = inspect.getmembers(obj)
    return {cst[0]: cst[1] for cst in customs}


def test_min_rows(my_custom):
    key = "min_rows"
    assert my_custom[key] == asdict(pddisplay.Customs())[key]


def test_max_rows(my_custom):
    key = "max_rows"
    assert my_custom[key] == asdict(pddisplay.Customs())[key]


def test_max_columns(my_custom):
    key = "max_columns"
    assert my_custom[key] == asdict(pddisplay.Customs())[key]


def test_width(my_custom):
    key = "width"
    assert my_custom[key] == asdict(pddisplay.Customs())[key]


def test_show_dimensions(my_custom):
    key = "show_dimensions"
    assert my_custom[key] == asdict(pddisplay.Customs())[key]


if __name__ == "__main__":
    pytest.main()
