from __future__ import annotations

from typing import List, Dict

from analysis.services.filereader import AlgorithmicFileReader, RaterFileReader
from analysis.services.preprocess import DataMerger


# class TestAlgorithmicFileReader:
#     class TestRead:
#         def test_read_txt_data_from_several_files_concatenate_right_number_of_lines(self) -> None:
#             file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
#             file_reader.read()
#             assert len(file_reader.trial_id) == 5

#         def test_read_txt_data_from_several_files_aoi_length_is_same_as_trial_id_length(self) -> None:
#             file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
#             file_reader.read()
#             assert len(file_reader.trial_id) == len(file_reader.aoi)

#         def test_read_txt_data_from_several_files_frame_index_starts_at_0_for_each_file(self) -> None:
#             file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
#             file_reader.read()
#             expected = ["0", "1", "0", "1", "2"]
#             assert all([a == b for a, b in zip(file_reader.frame_id, expected)])

#         def test_raterid_should_return_list_of_string_with_length_of_data(self) -> None:
#             file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
#             file_reader._frame_id = ["0", "1", "2", "3", "4"]
#             assert len(file_reader.rater_id) == 5
#             assert file_reader.rater_id[0] == "Algorithm"

#     class TestRenameAOI:

#         def test_rename_items_in_aoi(self) -> None:
#             file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
#             file_reader._aoi = ["Nose"]
#             file_reader.rename_aoi()
#             assert file_reader.aoi == ["Head"]


# class TestRaterFileReader:
#     class TestRead:
#         def test_read_csv_data_from_several_files_concatenate_right_number_of_lines(self) -> None:
#             file_reader = RaterFileReader("analysis/tests/data/data_*.csv")
#             file_reader.read()
#             assert len(file_reader.trial_id) == 5

#         def test_read_csv_data_retrieve_frame_ids(self) -> None:
#             file_reader = RaterFileReader("analysis/tests/data/data_*.csv")
#             file_reader.read()
#             expected = ["175", "176", "175", "176", "177"]
#             assert all([a == b for a, b in zip(file_reader.frame_id, expected)])

#     class TestDropDuplicates:
#         def test_keep_last_value_when_frameid_and_raterid_the_same(self) -> None:
#             file_reader = RaterFileReader("analysis/tests/data/data_*.csv")
#             file_reader._frame_id = ["0", "1", "2", "0"]
#             file_reader._rater_id = ["rater1"] * 4
#             file_reader.drop_duplicate_ratings()
#             assert len(file_reader.frame_id) == 3

#         def test_keep_all_values_when_frameid_and_raterid_not_the_same_but_frameid_the_same(self) -> None:
#             file_reader = RaterFileReader("analysis/tests/data/data_*.csv")
#             file_reader._frame_id = ["0", "1", "2", "0"]
#             file_reader._rater_id = ["rater1", "rater1", "rater1", "rater2"]
#             file_reader.drop_duplicate_ratings()
#             assert len(file_reader.frame_id) == 4


# class Builder:
#     def data_deserializer(self) -> Builder:
#         return self

#     def with_algorithmic_data(self) -> Dict[str, List[str]]:
#         algorithmic_ratings = {
#             'aoi': ["Nose", "Nose"],
#             'trial_id': ["1", "1"],
#             'frame_id': ["1", "2"],
#             'rater_id': ["algorithm", "algorithm"]
#         }
#         return algorithmic_ratings

#     def with_rater_data(self) -> Dict[str, List[str]]:
#         manual_ratings = {
#             'aoi': ["Nose", "Nose"],
#             'trial_id': ["1", "1"],
#             'frame_id': ["1", "2"],
#             'rater_id': ["rater1", "rater1"]
#         }
#         return manual_ratings


# class TestDataMerger:
#     def test_concatenate_data_streams_results_in_long_dataframe(self) -> None:
#         algorithmic_data = Builder().data_deserializer().with_algorithmic_data()
#         rater_data = Builder().data_deserializer().with_rater_data()
#         merger = DataMerger(algorithmic_data)
#         merger.merge_with(rater_data)
#         merger.drop_missing_rows()
#         assert merger.pandas_dataframe.shape == (4, 4)
