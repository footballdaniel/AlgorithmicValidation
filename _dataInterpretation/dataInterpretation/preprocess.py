from __future__ import annotations  # Fix to type hint class itself

from glob import glob
from typing import List

import pandas as pd  # type: ignore


class DataPreprocessor(object):
    @property
    def algorithmic_data(self) -> pd.DataFrame:
        return self._algorithmic_data

    @property
    def rater_data(self) -> pd.DataFrame:
        return self._algorithmic_data

    def load(self, algorithmic_data: str, rater_data: str) -> None:
        self._load_algorithmic_data(algorithmic_data)
        self._load_rater_data(rater_data)

    def _load_algorithmic_data(self, data_path: str = "data/P*.txt") -> None:
        file_list = glob(data_path)
        dataframe_list = (pd.read_csv(f, header=None) for f in file_list)
        dataframe = pd.concat(dataframe_list, ignore_index=True, axis=0)
        self._algorithmic_data: pd.DataFrame = dataframe

    def _load_rater_data(self, data_path: str = "data/data_Rater*.csv") -> None:
        raterFiles = glob(data_path)
        dataframe_list = (pd.read_csv(f, header=0) for f in raterFiles)
        dataframe = pd.concat(dataframe_list, ignore_index=True)
        self._rater_data: pd.DataFrame = dataframe

    def drop_duplicate_ratings(self, columns: List[str] = []) -> DataPreprocessor:
        if self._columns_exist_in_dataframe(columns):
            self._rater_data = self._rater_data.drop_duplicates(
                keep="last", subset=columns
            )
        return self

    def _columns_exist_in_dataframe(self, columns: List[str]) -> bool:
        if set(columns).issubset(self._rater_data):
            return True

    def format(self) -> DataPreprocessor:
        pass

    def merge(self):
        pass
