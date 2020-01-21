# python scripts/ZNF827_and_GH1.py JFCF6_P12 HCP-AAVS1-CG02
import os, sys

sample = sys.argv[1]
vector = sys.argv[2]

BAM_PATH = "/home/scai/das/Process/Bioinformatics/tedwong/Sources/immortal_simon/bams"
REF_PATH = "/home/scai/das/Process/Bioinformatics/tedwong/Sources/immortal/vector_sequences"

if not os.path.exists(f"{BAM_PATH}/{sample}_GH1_1.fq"):

    cmd = f'samtools view -bh {BAM_PATH}/REALIGNED_RG_DEDUP_SORTED_HG19_{sample}.bam "chr17:61993000-61995500" > {BAM_PATH}/{sample}_GH1.bam'
    print(cmd)
    os.system(cmd)

    cmd = f"bam2fastq --force --strict -o {BAM_PATH}/{sample}_GH1#.fq {BAM_PATH}/{sample}_GH1.bam"
    print(cmd)
    os.system(cmd)

cmd = f"bwa mem -t 10 {REF_PATH}/{vector}.fa {BAM_PATH}/{sample}_GH1_1.fq {BAM_PATH}/{sample}_GH1_2.fq > {BAM_PATH}/{sample}_{vector}_GH1.sam"
print(cmd)
os.system(cmd)

cmd = f"java -Xmx32G -jar ~/tools/picard.jar SortSam INPUT={BAM_PATH}/{sample}_{vector}_GH1.sam OUTPUT={BAM_PATH}/{sample}_{vector}_GH1_sorted.sam SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT"
print(cmd)
os.system(cmd)

cmd = f"java -Xmx32G -jar ~/tools/picard.jar MarkDuplicates INPUT={BAM_PATH}/{sample}_{vector}_GH1_sorted.sam OUTPUT={BAM_PATH}/{sample}_{vector}_GH1_marked.bam ASSUME_SORTED=true VALIDATION_STRINGENCY=SILENT METRICS_FILE=metrics.txt"
print(cmd)
os.system(cmd)

cmd = f"samtools index {BAM_PATH}/{sample}_{vector}_GH1_marked.bam"
print(cmd)
os.system(cmd)

if os.path.exists(f"{BAM_PATH}/{sample}_{vector}_GH1_sorted.bam"):
    os.system(f"rm {BAM_PATH}/{sample}_{vector}_GH1_sorted.bam")
cmd = f"rm {BAM_PATH}/*.sam"
print(cmd)
os.system(cmd)

cmd = f"rm {BAM_PATH}/*.fq"
print(cmd)
os.system(cmd)