from __future__ import annotations  # Fix to type hint class itself

from dataclasses import dataclass, field
from typing import List, Dict, Any, cast

import pandas as pd  # type: ignore

from analysis.services.filereader import AlgorithmicFileReader, RaterFileReader


@dataclass
class DataLoader:
    _algorithmic_ratings: Dict[str, List[str]] = field(default_factory=dict)
    _manual_ratings: Dict[str, List[str]] = field(default_factory=dict)
    _merged_data: Dict[str, List[str]] = field(default_factory=dict)

    def load(self, algorithmic_data: str, rater_data: str) -> Dict[str, List[str]]:
        self._load_algorithmic_data(algorithmic_data)
        self._load_rater_data(rater_data)
        self._merge_data()
        return self._merged_data

    def _load_algorithmic_data(self, file_pattern: str = "data/P*.txt") -> None:
        file_reader = AlgorithmicFileReader(file_pattern)
        file_reader.read()
        file_reader.rename_aoi()
        self._algorithmic_ratings = {
            'aoi': file_reader.aoi,
            'trial_id': file_reader.trial_id,
            'frame_id': file_reader.frame_id,
            'rater_id': file_reader.rater_id
        }

    def _load_rater_data(self, file_pattern: str = "data/data_*.csv") -> None:
        file_reader = RaterFileReader(file_pattern)
        file_reader.read()
        file_reader.drop_duplicate_ratings()
        self._manual_ratings = {
            'aoi': file_reader.aoi,
            'trial_id': file_reader.trial_id,
            'frame_id': file_reader.frame_id,
            'rater_id': file_reader.rater_id
        }

    def _merge_data(self) -> None:
        merger = DataMerger(self._algorithmic_ratings)
        merger.merge_with(self._manual_ratings)
        merger.drop_missing_rows()
        self._merged_data = merger.data_dict


@dataclass
class DataMerger:
    data_stream: Dict[str, List[str]]
    merged_data: Dict[str, List[str]] = field(default_factory=dict)

    @property
    def pandas_dataframe(self) -> pd.DataFrame:
        return self._merged_data

    @property
    def data_dict(self) -> Dict[str, List[str]]:
        merged_dict = cast(Dict[str, List[str]], self._merged_data)
        return merged_dict

    def merge_with(self, to_be_merged: Dict[str, List[str]]) -> None:
        df_algo = pd.DataFrame(self.data_stream)
        df_rater = pd.DataFrame(to_be_merged)

        df = pd.concat(
            [df_algo, df_rater],
            join='outer',
            keys=['trial_id', 'frame_id', 'rater_id', 'aoi']).reset_index(drop=True)

        self._merged_data = df

    def drop_missing_rows(self) -> None:
        df = self._merged_data.groupby(['trial_id', 'frame_id']).apply(self._filterRows).reset_index(drop=True)
        df.ffill(inplace=True)
        self._merged_data = df

    def _filterRows(self, group: pd.DataFrame) -> pd.DataFrame:
        if group.shape[0] > 1:
            return group
