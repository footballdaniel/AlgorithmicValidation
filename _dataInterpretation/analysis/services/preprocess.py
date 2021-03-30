from __future__ import annotations  # Fix to type hint class itself

from dataclasses import dataclass, field
from glob import glob
from typing import List

import pandas as pd  # type: ignore

from analysis.model.model import Dataset, NullDataset


@dataclass
class DataSerializer:
    _algorithmic_aoi: List[str] = field(default_factory=list)
    _algorithmic_trial: List[str] = field(default_factory=list)

    def load(self, algorithmic_data: str, rater_data: str) -> Dataset:
        self._load_algorithmic_data(algorithmic_data)
        self._load_rater_data(rater_data)

        dataset = NullDataset()
        return dataset

    def _load_algorithmic_data(self, file_pattern: str = "data/P*.txt") -> None:
        file_reader = AlgorithmicFileReader(file_pattern)
        file_reader.read()

        self._algorithmic_aoi = file_reader.aoi
        self._algorithmic_trial = file_reader.trial_id
        self._algorithmic_frame = file_reader.frame_id

    def _load_rater_data(self, file_pattern: str = "data/data_*.csv") -> None:
        pass
        a = 1


@dataclass
class RaterFileReader:
    file_path: str
    _trial_id: List[str] = field(default_factory=list)
    _rater_id: List[str] = field(default_factory=list)
    _aoi: List[str] = field(default_factory=list)
    _frame_id: List[int] = field(default_factory=list)

    @property
    def trial_id(self) -> List[str]:
        return self._trial_id

    @property
    def aoi(self) -> List[str]:
        return self._aoi

    @property
    def frame_id(self) -> List[int]:
        return self._frame_id

    @property
    def rater_id(self) -> List[str]:
        return ["Algorithm"] * len(self._frame_id)

    def read(self):
        file_list = sorted(glob(self.file_path))
        dataframe_list = (pd.read_csv(f, header=0, dtype=str) for f in file_list)
        dataframe = pd.concat(dataframe_list, ignore_index=True, axis=0)

        # self._trial_id = list(dataframe.iloc[:, 0])
        # self._aoi = list(dataframe.iloc[:, 1])
        # self._frame_id = dataframe.index
        self._trial_id = list(dataframe.iloc[:, 3])
        self._rater_id = list(dataframe.iloc[:, 2])
        self._aoi = list(dataframe.iloc[:, 1])
        self._frame_id = list(dataframe.iloc[:, 0].astype(int))


@dataclass
class AlgorithmicFileReader:
    file_path: str
    _trial_id: List[str] = field(default_factory=list)
    _aoi: List[str] = field(default_factory=list)
    _frame_id: List[int] = field(default_factory=list)

    @property
    def trial_id(self) -> List[str]:
        return self._trial_id

    @property
    def aoi(self) -> List[str]:
        return self._aoi

    @property
    def frame_id(self) -> List[int]:
        return self._frame_id

    @property
    def rater_id(self) -> List[str]:
        return ["Algorithm"] * len(self._frame_id)

    def read(self) -> None:
        file_list = sorted(glob(self.file_path))
        dataframe_list = (pd.read_csv(f, header=None, dtype=str) for f in file_list)
        dataframe = pd.concat(dataframe_list, ignore_index=False, axis=0)

        self._trial_id = list(dataframe.iloc[:, 0])
        self._aoi = list(dataframe.iloc[:, 1])
        self._frame_id = dataframe.index


class DataPreprocessor:
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
        else:
            return False
