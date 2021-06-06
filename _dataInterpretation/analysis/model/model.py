from dataclasses import dataclass, field
from enum import Enum
from typing import List


class AOI(Enum):
    NECK = "Neck"


@dataclass
class Rating:
    name: str
    aoi: AOI


@dataclass
class Frame:
    rater: List[Rating]


@dataclass
class Trial:
    frames: List[Frame]


@dataclass
class Dataset:
    trials: List[Trial]


@dataclass
class NullDataset(Dataset):
    trials: List[Trial] = field(default_factory=list)
