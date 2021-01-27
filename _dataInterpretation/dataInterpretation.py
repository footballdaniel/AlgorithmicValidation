# All data analysis for the algorithmic validation

from dataInterpretation.analysis import RatingAgreement
from dataInterpretation.preprocess import DataPreprocessor

data = DataPreprocessor()
data.load(algorithmic_data="data/P*.txt", rater_data="data/data_Rater*.csv")
data.drop_duplicate_ratings(columns=["Rater", "Trial", "Frame"])
data.format()

# Left off at formatting dropt duplicates done.
data.merge()


RatingAgreement().load_data(data)
