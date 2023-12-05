import pandas as pd
import uuid
import re
from number_extractor.extractor import NumberExtractor
from sentence_splitter.splitter import SyntaxAnalyzer

sa = SyntaxAnalyzer()
ne = NumberExtractor()

part_1 = pd.read_csv('data/lenta-ru-base.csv')
part_2 = pd.read_csv('data/from_15-12-2019.csv')

df = pd.concat(objs=[part_1, part_2])
df.reset_index()

df.to_csv('data/lenta-ru-full.csv', index=False)

columns = ['text_index', 'base_text', 'converted_text', 'was_changed']

for index, row in df.iterrows():
    text_id = str(uuid.uuid4())
    base_text = row['text']
    base_sentences = sa(base_text)
    if base_sentences is None:
        continue

    out = []
    for base_sen in base_sentences:
        try:
            converted_sen = ne.replace_groups(base_sen)
            was_changed = not (
                len(re.findall(r'\d', base_sen)) 
                == len(re.findall(r'\d', converted_sen))
            )
        except:
            converted_sen = base_sen
            was_changed = 0

        out.append([text_id, base_sen, converted_sen, was_changed])

out_df = pd.DataFrame(data=out, columns=columns)
out_df.to_csv('data/lenta-ru-processed.csv', index=False)
