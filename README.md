# allele_muts

# Description
This program uses sequenced short tandem repeat (STR/microsatellite) loci output from SatAnalyzer (seq2sat) and incorporates mutations found in the flanking and repeat regions into a consolidated allele call that considers length and mutations. It takes as input all the *_genotypes_mra_final.txt output files from SatAnalyzer, and outputs a list of alleles at each locus that have mutations in the MRA, snpsFF, and snpsRF regions. It also outputs a list of reference codes for those mutations. The final output includes a list of coded alleles scores that represent the allele size with appended digits to indicate MRA, snpsFF and snpsRF mutation codes. These genotypes can be used in downstream analyses as a way to include true alleleic diversity typically overlooked when homoplasy is present and scores are based on allele length alone.

# Key Features
