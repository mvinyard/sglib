
# _sgRNA_Library.py

__module_name__ = "_sgRNA_Library.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# import packages #
# --------------- #
import pandas as pd
import seq_toolkit
import pandas as pd


# local imports #
# ------------- #
from ._gene_annotation_functions._Gene import _Gene
from ._gene_annotation_functions._return_gene_body_bounds import _return_gene_body_bounds
from ._gene_annotation_functions._print_exon_statistics import _print_exon_statistics

from ._guide_id_functions._return_guides_in_regions import _return_guides_in_regions
from ._guide_id_functions._annotate_protospacer_position import _annotate_protospacer_position
from ._guide_id_functions._guide_df_to_stranded_bed import _guide_df_to_stranded_bed
from ._guide_id_functions._plot_guide_distribution import _plot_guide_distribution

from ._fetch_noncoding_region_sequence import _fetch_noncoding_region_sequence

class _sgRNA_Library:
    
    def __init__(self, reference_directory):
        
        """"""
        
        self.GTF, self.ref_genome_path = seq_toolkit.parse_reference(reference_directory)
        self._feature_key = "feature"
            
    def from_gene(self, gene, gene_feature="exon", reverse_strand=False):
        
        """Build a set of regions based on an input gene name"""
        
        self.gene_name = gene
        self.gene_feature = gene_feature
        self.Gene = _Gene(self.GTF, self.ref_genome_path)
        self.Gene.fetch(gene, gene_feature, reverse_strand)
        self.sequence = self.Gene.sequence
        self.formatted_feature_df = self.Gene.formatted_feature_df
        self.gene_start, self.gene_end = _return_gene_body_bounds(self.Gene.gene_df)
        self.global_start = self.gene_start
        self.region_specification = gene_feature
        self.feature = gene_feature
        self.df = self.Gene.merged_feature_df
        self.chromosome = self.Gene.gene_df["seqname"].unique()[0]
        self.region_sequences = {}
        self.region_sequences["chr22"] = self.Gene.sequence
        
        return _print_exon_statistics(self.formatted_feature_df)
        
<<<<<<< HEAD
    def from_regions(self, df, start_key="Start", end_key="End"):        
=======
    def from_regions(self, df, start_key="Start", end_key="End", feature="peak", target_name="noncoding"):
        
>>>>>>> 1d6c9fe20ff9853b6074c4918221d24e1c90f274
        """
        Use a pre-built set of regions as input. 
        
        Parameters:
        -----------
        df
            type: pandas.DataFrame
            
        Returns:
        --------
        
        Notes:
        ------
        """
<<<<<<< HEAD
        self.start_key = start_key
        self.end_key = end_key
        self.feature = "noncoding"
=======
        

#         self.formatted_df = df
#         self.global_start = df.sort_values(coordinate_keys[1])[coordinate_keys[1]].min()

        self._start_key = start_key
        self._end_key = end_key
        self._feature = feature
        self._target_name = target_name
>>>>>>> 1d6c9fe20ff9853b6074c4918221d24e1c90f274
        
        
        self.df = df
        self.region_sequences = _fetch_noncoding_region_sequence(self.df, self.ref_genome_path)
<<<<<<< HEAD
    
    def PAM_scan(self, PAM="NGG", extend_region=0, out_prefix="", return_guides=False, plot=False):
=======

        
    def PAM_scan(self, PAM="NGG", extend_region=0, out_prefix="", return_guides=False,):
>>>>>>> 1d6c9fe20ff9853b6074c4918221d24e1c90f274
        
        """
        Parameters:
        -----------
        PAM
            CRISPR-Cas9 Protospacer Adjacent Motif sequence (though any motif would work!)
            default: "NGG"
            type: str
           
        extend_region
            number of nucleotides by which regions of interest should be extended. 
            type: int
            default: 0

        region_column
            prefix to the boundary indication columns. followed by ".start" and ".end"
            type: str
            default: "gene_feature"
    
        return_guides
            Boolean indicator if the resulting guide_df should be returned (in-memory subclass by default)
            default: False
            type: bool


        Returns:
        --------
        guide_df (or None by default)
        
        Notes:
        ------
        df.loc[df[region_column] == region_specification]
        """
        
        self.TargetDict = {}
        list_of_guide_dfs = []
        for chromosome, sequence in self.region_sequences.items():
            
            chrom_df = self.df.loc[self.df["Chromosome"] == chromosome]
            start = chrom_df.Start.astype(int).min()
            end = chrom_df.End.astype(int).max()
            
            region = "_".join([chromosome, str(start), str(end)])
            self.TargetDict[region] = {}
            
            self.TargetDict[region]["target_df"] = int_df =  _return_guides_in_regions(sequence,
                                                                 df=chrom_df,
                                                                 PAM=PAM,
                                                                 global_start=start,
                                                                 region_extension=extend_region,
                                                                )         

            self.TargetDict[region]["guide_df"] = _annotate_protospacer_position(self.TargetDict[region]["target_df"])
            self.TargetDict[region]["guide_df"]["feature"] = self._feature
            list_of_guide_dfs.append(self.TargetDict[region]["guide_df"])
            
        self.sgRNA_df = pd.concat(list_of_guide_dfs).reset_index(drop=True)
        _guide_df_to_stranded_bed(self.sgRNA_df, 
                                  self._target_name,
                                  self._feature,
                                  out_prefix)
<<<<<<< HEAD
        if plot:
            _plot_guide_distribution(self.sgRNA_df, feature=self._feature_key)
            
        self.sgRNA_df.to_excel("./{}.{}.{}.sgRNAs.xlsx".format(region, self.feature, PAM), index=False)
=======
#         _plot_guide_distribution(self.sgRNA_df, feature=self._feature)
            
        self.sgRNA_df.to_excel("./{}.{}.{}.sgRNAs.xlsx".format(region, self._feature, PAM), index=False)
>>>>>>> 1d6c9fe20ff9853b6074c4918221d24e1c90f274
        if return_guides:
            return self.TargetDict