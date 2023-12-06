import pandas as pd
from tqdm import tqdm
import re
from number_extractor.extractor import NumberExtractor
from sentence_splitter.splitter import SyntaxAnalyzer

sa = SyntaxAnalyzer()
ne = NumberExtractor()

part_1 = pd.read_csv('data/lenta-ru-news_post.csv')
part_2 = pd.read_csv('data/from_15-12-2019_post.csv')
part_3 = pd.read_csv('data/literature_6084.csv')

df = pd.concat(objs=[part_1, part_2, part_3])
df.reset_index()

columns = ['text_index', 'base_text', 'converted_text', 'was_changed']

out = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        text_id = row['uuid']
        base_text = row['text']
        base_sentences = sa(base_text)
        if base_sentences is None:
            continue

        for base_sen in base_sentences:
            try:
                converted_sen = ne.replace_groups(base_sen)
                was_changed = int(not (
                    len(re.findall(r'\d', base_sen)) 
                    == len(re.findall(r'\d', converted_sen))
                ))
            except:
                converted_sen = base_sen
                was_changed = 0

            out.append([text_id, base_sen, converted_sen, was_changed])
    except:
        if 'uuid' in df.columns:
            print(f'ERROR: uuid={row["uuid"]}')

out_df = pd.DataFrame(data=out, columns=columns)
out_df.to_csv('data/num2word_dataset.csv', index=False)
