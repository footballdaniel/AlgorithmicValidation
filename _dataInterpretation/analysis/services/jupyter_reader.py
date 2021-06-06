import glob
from dataclasses import dataclass

import pandas as pd  # type: ignore


@dataclass
class JupyterReader:
    df_rater: pd.DataFrame = pd.DataFrame()
    df_algo: pd.DataFrame = pd.DataFrame()
    _df_merged: pd.DataFrame = pd.DataFrame()

    @property
    def df_merged(self) -> pd.DataFrame:
        return self._df_merged

    def load(self, algorithmic_files: str = "data/P*.txt", manual_rating_files: str = "data/data_Rater*.csv") -> None:
        self._load_from_files(algorithmic_files, manual_rating_files)
        self._to_long_format()
        self._merge()

    def _load_from_files(self, algorithmic_files: str, manual_rating_files: str) -> None:
        # Load data from algorithmic tracking
        raterFiles = glob.glob(algorithmic_files)
        df_algoFiles = (pd.read_csv(f, header=None) for f in raterFiles)
        df_algo = pd.concat(df_algoFiles, ignore_index=True, axis=0)

        # Load data from manual ratings
        raterFiles = glob.glob(manual_rating_files)
        df_raterFiles = (pd.read_csv(f, header=0) for f in raterFiles)
        self.df_rater = pd.concat(df_raterFiles, ignore_index=True)

    def _to_long_format(self) -> None:
        # Only take the last judgement of each rater
        self.df_rater.drop_duplicates(subset=['Rater', 'Frame', 'Trial'], keep='last', inplace=True)
        # Rename columns
        self.df_algo.columns = ["Trial", "Label", "1", "2", "3", "4", "5", "6", "VisiblePoints", "7", "8"]
        # Add frame number column
        self.df_algo["Frame"] = self.df_algo.groupby(['Trial']).cumcount()
        # Add column for rater
        self.df_algo['Rater'] = 'Algorithm'
        # Set data types
        self.df_algo["Trial"] = self.df_algo["Trial"].astype("string")
        self.df_algo["Frame"] = self.df_algo["Frame"].astype("string")
        self.df_algo["Label"] = self.df_algo["Label"].astype("string")
        self.df_rater["Frame"] = self.df_rater["Frame"].astype("string")
        self.df_rater["Trial"] = self.df_rater["Trial"].astype("string")
        self.df_rater["Label"] = self.df_rater["Label"].astype("string")
        # Rename the labels to match the AOI from the algorithmic approach
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("Nose", "Head")
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("Neck", "Chest")
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("LElbow", "Left arm")
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("RElbow", "Right arm")
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("RKnee", "Right leg")
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("LKnee", "Left leg")
        self.df_algo['Label'] = self.df_algo['Label'].str.replace("MidHip", "Pelvis")

    def _merge(self) -> None:
        # Merge data frames
        df = pd.concat(
            [self.df_algo, self.df_rater],
            join='outer',
            keys=['Trial', 'Frame', 'Rater', 'Label']
        ).reset_index(drop=True)
        # only keep rows where all ratings are available
        df = df.groupby(['Trial', 'Frame']).apply(self._filter_rowwise).reset_index(drop=True)
        df.ffill(inplace=True)
        df = df[['Trial', 'Label', 'VisiblePoints', 'Frame', 'Rater']]
        df.drop(columns=['VisiblePoints'], inplace=True)
        self.df_merged = df

    def _filter_rowwise(self, group: pd.DataFrame) -> pd.DataFrame:
        if group.shape[0] > 1:
            return group
