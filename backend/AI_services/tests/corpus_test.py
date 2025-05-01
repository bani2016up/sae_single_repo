import pathlib
import os
import textwrap

from backend.AI_services.ai_services.corpus_tools.cleaning import *

os.chdir('../../../data')

path = './The-Cambridge-History-of-Russia-vol.txt'
init_path = ".".join(path.split(".")[:-1])
raw_text = pathlib.Path(path).read_text(encoding='utf-8', errors='ignore')

paragraphs = clean_and_paragraphize(raw_text)
numbered_paragraphs = [f"{idx}\t{para}" for idx, para in enumerate(paragraphs, start=1)]

clean_path = pathlib.Path(f'{init_path}-clean.txt')
with open(clean_path, 'w', encoding='utf-8') as fh:
    fh.write('\n\n'.join(numbered_paragraphs))

print(f"Raw length: {len(raw_text):,} characters")
print(f"Cleaned paragraphs: {len(paragraphs):,}\n")

for num_para in numbered_paragraphs[:10]:
    idx, para = num_para.split('\t', 1)
    print(f"--- Paragraph {idx} ---")
    print(textwrap.fill(para, width=100))
    print()
