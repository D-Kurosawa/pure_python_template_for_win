"""Customize display of pandas.DataFrame"""
from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class Customs:
    min_rows: int = 40  # 最小表示行数
    max_rows: int = 200  # 最大表示行数
    max_columns: int = 100  # 最大表示列数
    width: int = 600  # 全体の最大表示幅
    max_colwidth: int = 50  # 列ごとの最大表示幅
    show_dimensions: bool = True  # 省略時の行数・列数表示
    colheader_justify: str = "right"  # 列名表示の右寄せ・左寄せ
    precision: int = 6  # 小数点以下の桁数
    float_format: Optional[int] = None  # 有効数字（有効桁数）


def custom(**kwargs):
    """Customize Pandas display"""
    obj = Customs(**kwargs)

    pd.options.display.min_rows = obj.min_rows
    pd.options.display.max_rows = obj.max_rows
    pd.options.display.max_columns = obj.max_columns
    pd.options.display.width = obj.width
    pd.options.display.show_dimensions = obj.show_dimensions


if __name__ == "__main__":
    pass
