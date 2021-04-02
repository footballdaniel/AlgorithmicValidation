# All data analysis for the algorithmic validation
from analysis.services.jupyter_reader import JupyterReader
from analysis.services.preprocess import DataLoader

algorithmic_files = "analysis/tests/data/P*.txt"
rater_files = "analysis/tests/data/data_*.csv"

# Load with TDD approach (Merging is still incompletely happening)
data = DataLoader().load(algorithmic_files, rater_files)

# Load with Jupyter approach
reader = JupyterReader()
reader.load(algorithmic_files, rater_files)
data = reader.df_merged

a = 1
