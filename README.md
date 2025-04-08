# allele_muts
Incorporates sequence mutations into microsatellite allele length calls.

# Details
This program uses sequenced microsatellite output from SatAnalyzer (seq2sat) and incorporates mutations found in the flanking and repeat regions into a 8 or 9 digit allele call. 
It is used to identify and code mutations found in sequences of short tandem repeat (STR) loci used in the Canis STRseq assay. It takes as input all the *_genotypes_mra_final.txt output files from SatAnalyzer, and outputs a list of alleles at each locus that have mutations in the MRA, snpsFF, and snpsRF regions. It also provides reference codes for those mutations. The final output includes a list of coded allele scores that represent the allele size with appended digits that represent MRA, snpsFF and snpsRF mutation codes. These scores can be used in downstream analyses as a way to include true alleleic diversity typically overlooked when homoplasy is present.
