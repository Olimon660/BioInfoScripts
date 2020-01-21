import pandas as pd
from tqdm import tqdm, trange
import os
import re
from joblib import Parallel, delayed

df = pd.read_csv("PRJEB14362.txt", sep='\t')
all_files = [x for run in df['fastq_ftp'].values for x in str(run).split(';')]

def download(fp):
    location = fp.replace('ftp.sra.ebi.ac.uk/vol1/fastq','/home/scai/das/Inbox/Embryology\ Unit/cuomo_hipsc')
    if location is not None and re.search("(.*)/E.*fastq.gz", location):
        location = re.search("(.*)/E.*fastq.gz", location).group(1)
    else:
        return
    os.system(f"wget -q -P {location} {fp}")

Parallel(n_jobs=20)(delayed(download)(all_files[i]) for i in trange(len(all_files)))