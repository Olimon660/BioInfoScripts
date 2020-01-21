"""
Normally step 0 to get trimmed reads
e.g. python ~/BioInfoScripts/RNA_workflows/trim_galore_by_folders.py . ~/processing_simoncai/hiPSC_download/trimmed_reads/
"""
import os
import sys
from tqdm import trange
from joblib import Parallel, delayed


input_root = sys.argv[1]
output_root = sys.argv[2]

subdirs = []
for subdir, dirs, files in os.walk(input_root):
    for file in files:
        subdirs.append(subdir)

subdirs = sorted(set(subdirs))


def process(pair_dir):
    os.system(f'trim_galore --paired --output_dir {os.path.join(output_root, pair_dir)} -j 4 {pair_dir}/*')


Parallel(n_jobs=5)(delayed(process)(subdirs[i]) for i in trange(len(subdirs)))
