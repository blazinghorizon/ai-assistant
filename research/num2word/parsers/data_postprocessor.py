import uuid
import pandas as pd

path = 'data/'
filename = 'from_15-12-2019=test'
suffix = '.csv'
needed_cols = ['text']
columns = ['uuid', 'text']

data = pd.read_csv(path+filename+suffix)

output = []
for index, row in data.iterrows():
    cur = [str(uuid.uuid4())]
    for col in needed_cols:
        cur.append(row[col])

    output.append(cur)

df = pd.DataFrame(output, columns=columns)
df.to_csv(path+filename+'_post'+suffix, index=False)