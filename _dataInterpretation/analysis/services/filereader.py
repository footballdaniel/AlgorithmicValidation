from collections import OrderedDict
from dataclasses import dataclass, field
from glob import glob
from typing import List

import pandas as pd  # type: ignore


@dataclass
class AlgorithmicFileReader:
    file_path: str
    _trial_id: List[str] = field(default_factory=list)
    _aoi: List[str] = field(default_factory=list)
    _frame_id: List[str] = field(default_factory=list)

    @property
    def trial_id(self) -> List[str]:
        return self._trial_id

    @property
    def aoi(self) -> List[str]:
        return self._aoi

    @property
    def frame_id(self) -> List[str]:
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
        self._frame_id = dataframe.index.map(str)

    def rename_aoi(self) -> None:
        self._aoi = [aoi.replace("Nose", "Head") for aoi in self._aoi]
        self._aoi = [aoi.replace("Neck", "Chest") for aoi in self._aoi]
        self._aoi = [aoi.replace("LElbow", "Left arm") for aoi in self._aoi]
        self._aoi = [aoi.replace("RElbow", "Right arm") for aoi in self._aoi]
        self._aoi = [aoi.replace("RKnee", "Right leg") for aoi in self._aoi]
        self._aoi = [aoi.replace("LKnee", "Left leg") for aoi in self._aoi]
        self._aoi = [aoi.replace("MidHip", "Pelvis") for aoi in self._aoi]

@dataclass
class RaterFileReader:
    file_path: str
    _trial_id: List[str] = field(default_factory=list)
    _rater_id: List[str] = field(default_factory=list)
    _aoi: List[str] = field(default_factory=list)
    _frame_id: List[str] = field(default_factory=list)

    @property
    def trial_id(self) -> List[str]:
        return self._trial_id

    @property
    def aoi(self) -> List[str]:
        return self._aoi

    @property
    def frame_id(self) -> List[str]:
        return self._frame_id

    @property
    def rater_id(self) -> List[str]:
        return self._rater_id

    def read(self) -> None:
        file_list = sorted(glob(self.file_path))
        dataframe_list = (pd.read_csv(f, header=0, dtype=str) for f in file_list)
        dataframe = pd.concat(dataframe_list, ignore_index=True, axis=0)
        self._trial_id = list(dataframe.iloc[:, 3])
        self._rater_id = list(dataframe.iloc[:, 2])
        self._aoi = list(dataframe.iloc[:, 1])
        self._frame_id = list(dataframe.iloc[:, 0])

    def drop_duplicate_ratings(self) -> None:
        frames_and_raters = zip(self.frame_id, self.rater_id)
        ordered_dict_with_corresponding_keys = list(OrderedDict.fromkeys(frames_and_raters))
        self._frame_id = [k[0] for k in ordered_dict_with_corresponding_keys]
        self._rater_id = [k[1] for k in ordered_dict_with_corresponding_keys]