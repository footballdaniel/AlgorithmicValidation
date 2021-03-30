# All data analysis for the algorithmic validation

from analysis.services.preprocess import DataPreprocessor

data = DataPreprocessor()
data.load(algorithmic_data="data/P*.txt", rater_data="data/data_Rater*.csv")
data.drop_duplicate_ratings(columns=["Rater", "Trial", "Frame"])
