from __future__ import annotations  # Fix to type hint class itself

from dataclasses import dataclass, field
from glob import glob
from typing import List, Union, Dict

import pandas as pd  # type: ignore

from analysis.model.model import Dataset, NullDataset
from analysis.services.filereader import AlgorithmicFileReader, RaterFileReader


@dataclass
class DataSerializer:
    _algorithmic_aoi: List[str] = field(default_factory=list)
    _algorithmic_trial_id: List[str] = field(default_factory=list)
    _algorithmic_frame_id: List[str] = field(default_factory=list)
    _rater_aoi: List[str] = field(default_factory=list)
    _rater_trial_id: List[str] = field(default_factory=list)
    _rater_frame_id: List[str] = field(default_factory=list)

    def load(self, algorithmic_data: str, rater_data: str) -> Dataset:
        self._load_algorithmic_data(algorithmic_data)
        self._load_rater_data(rater_data)

        dataset = NullDataset()
        return dataset

    def _load_algorithmic_data(self, file_pattern: str = "data/P*.txt") -> None:
        file_reader = AlgorithmicFileReader(file_pattern)
        file_reader.read()

        self._algorithmic_aoi = file_reader.aoi
        self._algorithmic_trial_id = file_reader.trial_id
        self._algorithmic_frame_id = file_reader.frame_id

    def _load_rater_data(self, file_pattern: str = "data/data_*.csv") -> None:
        file_reader = RaterFileReader(file_pattern)
        file_reader.read()
        file_reader.drop_duplicate_ratings()

        self._rater_aoi = file_reader.aoi
        self._rater_trial_id = file_reader.trial_id
        self._rater_frame_id = file_reader.frame_id

    def _merge_data(self) -> Any:
        merger = DataMerger(self)
        # merged_data = merger.merge_rater_and_algorithm_data()


@dataclass
class DataMerger:
    _loader: DataSerializer

    # def merge_rater_and_algorithm_data(self) -> Dict[str, Union[str, int]]:
    #     pass