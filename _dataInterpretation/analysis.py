# All data analysis for the algorithmic validation
from analysis.services.preprocess import DataLoader

algorithmic_files = "analysis/tests/data/P*.txt"
rater_files = "analysis/tests/data/data_*.csv"

data = DataLoader().load(algorithmic_files, rater_files)



a = 1
