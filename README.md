# Canis STR-seq allele_muts

# Description
This program uses short tandem repeat (STR/microsatellite) sequence data output from SatAnalyzer (seq2sat) and incorporates mutations found in the flanking and repeat regions into a consolidated allele call that considers length and mutations. It takes as input all the *_genotypes_mra_final.txt output files from SatAnalyzer, and outputs a list of alleles at each locus that have mutation codes appended that indicate mutations in the MRA, snpsFF, and/or snpsRF regions. 

# Key Features
Ouput includes:
* a list of original genotypes based on length (allele_len)
* a list of coded allele scores that represent the allele size with appended digits to indicate MRA, snpsFF and snpsRF mutation codes (allele_mut).
* a list of reference codes for specific mutations.
* allele_mut output can be used in downstream analyses as a way to include true alleleic diversity typically overlooked when homoplasy is present.

# Preparation
* To run the program, you need to have [Python](https://www.python.org/downloads/) installed.
* Refer to the conda-env.yaml file that describes the necessary packages to run this code. You can create an environment with "conda env create --file=conda-env.yaml" and then activate the environment with "conda activate allele_muts" 
* Unzipping the test data file will set the necessary folders up to run a test, but if you are using the script on your own data then you will need to:
  * Create a directory called "data"
  * Within "data" create the following directories:
  *    "input" - contains all the "*_genotypes_mra_final.txt" output files from SatAnalyzer
  *    "merged" - this folder will contain the input data merged into a single file that we can use for processing 
  *    "processed" - this folder will contain several intermediate processed files that can be used for error checking
  *    "output" - this folder will contain the final output files from the script

# Run a test
* Clone this repository to get the allele_muts.py file and the data.zip file.
* Ensure you have installed python and relevant dependencies.
* Unzip the data.zip file (e.g. `unzip data.zip`)
* Within the "data" folder there is the "input" folder with *_genotypes_mra_final.txt files for five samples as well as empty "merged" "processd" and "output" folders.
* To run a test, simply call python and the downloaded script with the following command in your terminal (e.g. terminal window on Mac, Powershell on Windows or bash shell on Linux) (`python allele_muts_v1.0.py`)
* Confirm that the output files were created in data/outputs
  * FinalOutput.csv
  * MutationCodes.csv
  * allele_mut_onerowperind.csv

# Getting Help
* Note that this repository is not routinely monitored. We have ensured that the test runs accurately and we encourage users to follow instructions carefully when using allele_muts.py on their own data. 

# Publication
Click the icon below to navigate to the publication on Zenodo
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15794713.svg)](https://doi.org/10.5281/zenodo.15794713)

# Citation
Rutledge LY and Rutledge GA (2025) ‘lrutledge107/allele_muts: v1.0.0’. Zenodo. doi: 10.5281/zenodo.15794713.
