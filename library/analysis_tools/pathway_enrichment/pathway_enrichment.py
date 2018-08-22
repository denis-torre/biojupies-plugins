#################################################################
#################################################################
############### Enrichment Analysis
#################################################################
#################################################################

#############################################
########## 1. Load libraries
#############################################
##### 1. General support #####
import pandas as pd
import os
import sys
from IPython.display import display, Markdown
import plotly.plotly as py

##### 2. Other libraries #####
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'core_scripts', 'shared', 'shared.py'))
import shared as s

#######################################################
#######################################################
########## S1. Function
#######################################################
#######################################################

#############################################
########## 1. Run
#############################################

def run(enrichr_results, signature_label, plot_type='interactive'):

	# Libraries
	libraries = {
		'KEGG_2016': 'KEGG Pathways',
		'WikiPathways_2016': 'WikiPathways',
		'Reactome_2016': 'Reactome Pathways'
	}

	# Get Enrichment Results
	enrichment_results = {geneset: s.get_enrichr_results(enrichr_results[geneset]['userListId'], gene_set_libraries=libraries, geneset=geneset) for geneset in ['upregulated', 'downregulated']}
	enrichment_results['signature_label'] = signature_label
	enrichment_results['plot_type'] = plot_type

	# Return
	return enrichment_results

#############################################
########## 2. Plot
#############################################

def plot(enrichment_results, plot_counter):

	# Create dataframe
	enrichment_dataframe = pd.concat([enrichment_results['upregulated'], enrichment_results['downregulated']])

	# Plot barcharts
	for gene_set_library in enrichment_dataframe['gene_set_library'].unique():
		s.plot_library_barchart(enrichment_results, gene_set_library, enrichment_results['signature_label'], 10, 300)

	# Download button
	results_txt = enrichment_dataframe.sort_values('pvalue').to_csv(sep='\t', index=False)
	s.download_button(results_txt, 'Download Results', 'pathway_enrichment_results.txt')

	# Figure legend
	display(Markdown('** Figure '+plot_counter()+' | Pathway Enrichment Analysis Results.** The figure contains interactive bar charts displaying the results of the pathway enrichment analysis generated using Enrichr. The x axis indicates the enrichment score for each term. Significant terms are highlighted in bold. Additional information about enrichment results is available by hovering over each bar. If you are experiencing issues visualizing the plot, please visit our <a href="https://amp.pharm.mssm.edu/biojupies/help#troubleshooting" target="_blank">Troubleshooting guide</a>.'.format(**locals())))
