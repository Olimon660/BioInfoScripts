"""
Normally step 1 to align trimmed reads
e.g.
"""
import os
import sys
from tqdm import trange
from joblib import Parallel, delayed
import re

input_root = sys.argv[1]
output_root = sys.argv[2]
genome_dir = sys.argv[3]

subdirs = []
for subdir, dirs, files in os.walk(input_root):
    for file in files:
        subdirs.append(subdir)

subdirs = sorted(set(subdirs))
if not os.path.isdir(output_root):
    os.system(f'mkdir -p {output_root}')

def process(pair_dir):
    name = re.search(".*/(.*$)", pair_dir).group(1)

    print(
        (f'STAR --runThreadN 1 --genomeDir {genome_dir} --readFilesIn {pair_dir}/*gz '
         f'--outFileNamePrefix {os.path.join(output_root, name)} '
         f'--readFilesCommand zcat --outFileNamePrefix {output_root}/{name}_ --quantMode TranscriptomeSAM '
         '--outSAMtype BAM'))


Parallel(n_jobs=1)(delayed(process)(subdirs[i]) for i in trange(len(subdirs)))
