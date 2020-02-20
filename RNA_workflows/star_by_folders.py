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
    if os.path.exists(f"{output_root}/{name}_Aligned.out.bam"):
        return

    os.system(
        (f'STAR --runThreadN 4 --genomeDir {genome_dir} --readFilesIn {pair_dir}/*gz '
         f'--readFilesCommand zcat --outFileNamePrefix {output_root}/{name}_ --quantMode TranscriptomeSAM '
         '--outSAMtype BAM Unsorted'))


Parallel(n_jobs=2)(delayed(process)(subdirs[i]) for i in trange(len(subdirs)))
