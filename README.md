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
* To run the program, you need to have [Python](https://www.python.org/downloads/) installed.
* Refer to the conda-env.yaml file that describes the necessary packages to run this code. You can create an environment with "conda env creat --file=conda-env.yaml" and then activate the environment with "conda activate allele_muts" 
* Create a directory called "run_allele_muts" that includes an "input" directory that contains all the "*_genotypes_mra_final.txt" output files from SatAnalyzer.
* When you run the program from within the "run_allele_muts" directory, the program will create addtional directories:
    * merged/ - this folder contains the input data merged into a single file that we can use for processing
    * processed/ - this folder contains several intermediate processed files that can be used for error checking
    * output/ - this folder contains the final output of the script

# Run the program
To run the script simply call python and the downloaded script with the following command in your terminal window (Mac) or Powershell (Windows)

`python ./allele_muts`
