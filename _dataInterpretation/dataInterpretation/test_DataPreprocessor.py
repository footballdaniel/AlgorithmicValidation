import pandas as pd

from dataInterpretation.preprocess import DataPreprocessor


def test_IsDuplicateFrameDiscarded():

    # Arange
    dp = DataPreprocessor()
    dp._rater_data = pd.DataFrame(
        {
            "Frame": [1, 2, 3, 3],  # Forth frame is duplicate and has to be deleted
            "Rater": [1, 1, 1, 1],
            "Label": ["Head", "Head", "Nose", "Nose"],
            "Trial": [1, 1, 1, 1],
        }
    )

    # Act
    dp.drop_duplicate_ratings(columns=["Rater", "Trial", "Frame"])

    # Assert
    assert dp._rater_data.shape[0] == 3


def test_NoDuplicatesToRemove():

    # Arange
    dp = DataPreprocessor()
    dp._rater_data = pd.DataFrame(
        {
            "Frame": [1, 2, 3, 4],
            "Label": ["Head", "Head", "Nose", "Nose"],
        }
    )

    # Act
    dp.drop_duplicate_ratings(columns=["Rater", "Trial", "Frame"])

    # Assert
    assert dp._rater_data.shape[0] == 4


def test_DuplicateFrameToRemove():

    # Arange
    dp = DataPreprocessor()
    dp._rater_data = pd.DataFrame(
        {
            "Frame": [1, 2, 3, 3],  # Forth frame is duplicate and has to be deleted
            "Rater": [1, 1, 1, 1],
            "Label": [
                "Head",
                "Head",
                "Head",
                "Nose",
            ],  # Label is no duplicate. Yet should still be deleted
            "Trial": [1, 1, 1, 1],
        }
    )

    # Act
    dp.drop_duplicate_ratings(columns=["Rater", "Trial", "Frame"])

    # Assert
    assert dp._rater_data.shape[0] == 3
