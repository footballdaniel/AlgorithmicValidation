from analysis.services.preprocess import AlgorithmicFileReader, RaterFileReader


class TestAlgorithmicFileReader:
    def test_read_txt_data_from_several_files_concatenate_right_number_of_lines(self) -> None:
        file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
        file_reader.read()
        assert len(file_reader.trial_id) == 5

    def test_read_txt_data_from_several_files_aoi_length_is_same_as_trial_id_length(self) -> None:
        file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
        file_reader.read()
        assert len(file_reader.trial_id) == len(file_reader.aoi)

    def test_read_txt_data_from_several_files_frame_index_starts_at_0_for_each_file(self) -> None:
        file_reader = AlgorithmicFileReader("analysis/tests/data/P*.txt")
        file_reader.read()
        expected = [0, 1, 2, 0, 1]
        assert all([a == b for a, b in zip(file_reader.frame_id, expected)])


class TestRaterFileReader:
    def test_read_csv_data_from_several_files_concatenate_right_number_of_lines(self) -> None:
        file_reader = RaterFileReader()
