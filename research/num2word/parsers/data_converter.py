import pandas as pd
from number_extractor.extractor import NumberExtractor
from sentence_splitter.splitter import SyntaxAnalyzer

sa = SyntaxAnalyzer()

part_1 = pd.read_csv('data/lenta-ru-base.csv')
part_2 = pd.read_csv('data/from_15-12-2019.csv')

df = pd.concat(objs=[part_1, part_2])
df.reset_index()

for index, row in df.iterrows():
    ...