# allele_muts

# Description
This program uses short tandem repeat (STR/microsatellite) sequence data output from SatAnalyzer (seq2sat) and incorporates mutations found in the flanking and repeat regions into a consolidated allele call that considers length and mutations. It takes as input all the *_genotypes_mra_final.txt output files from SatAnalyzer, and outputs a list of alleles at each locus that have mutation codes appended that incidate mutations in the MRA, snpsFF, and/or snpsRF regions. 

# Key Features
Ouput includes:
* a list of original genotypes based on length (allele_len)
* a list of coded alleles scores that represent the allele size with appended digits to indicate MRA, snpsFF and snpsRF mutation codes (allele_mut).
* a list of reference codes for specific mutations.
* allele_mut output can be used in downstream analyses as a way to include true alleleic diversity typically overlooked when homoplasy is present and scores are based on allele length alone.

# Getting Started
To run the program, you need to have [Python](https://www.python.org/downloads/) installed.

# Project Layout
The project is organized as follows

doc/
contains documentation of various sorts
collab.txt -this file is used to keep track of tasks, work completed and general collaboration between the team members
data/
input/
this folder contains the actual input data that is never touched by our processing
this folder will be checked into git
merged/
this folder contains the input data merged into a single file that we can use for processing
since this file is created from our processing and can easily be reproduced, it will not be checked into git (ie it is in .gitignore)
processed/
this folder contains several intermediate processed files that can be used for error checking
since this file is created from our processing and can easily be reproduced, it will not be checked into git (ie it is in .gitignore)
output/
this folder contains the final output of our system
since we may want to keep track of changes as our system evolves, this folder is checked in.
temp/
this folder contains temp files that need to be shared between team members but will evebtually be deleted

conda-env.yaml
this yaml file describes the necessary packages to run these notebooks.
you can create an environment using conda env create --file=conda-env.yaml
and then activate the environment using conda activate Canis-STR-seq
