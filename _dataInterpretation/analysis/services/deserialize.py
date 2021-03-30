from typing import List, Dict

from analysis.model.model import NullDataset, Dataset


class DataDeserializer:
    def deserialize(self, inputs: Dict[str, List[str]]) -> Dataset:
        dataset = NullDataset()
        return dataset