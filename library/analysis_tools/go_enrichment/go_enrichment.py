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

def run(enrichr_results, signature_label, plot_type='interactive', go_version='2018', sort_results_by='pvalue'):

	# Libraries
	go_version = str(go_version)
	libraries = {
		'GO_Biological_Process_'+go_version: 'Gene Ontology Biological Process ('+go_version+' version)',
		'GO_Molecular_Function_'+go_version: 'Gene Ontology Molecular Function ('+go_version+' version)',
		'GO_Cellular_Component_'+go_version: 'Gene Ontology Cellular Component ('+go_version+' version)'
	}

	# Get Enrichment Results
	enrichment_results = {geneset: s.get_enrichr_results(enrichr_results[geneset]['userListId'], gene_set_libraries=libraries, geneset=geneset) for geneset in ['upregulated', 'downregulated']}
	enrichment_results['signature_label'] = signature_label
	enrichment_results['plot_type'] = plot_type
	enrichment_results['sort_results_by'] = sort_results_by

	# Return
	return enrichment_results

#############################################
########## 2. Plot
#############################################

def plot(enrichment_results, plot_counter):
	
	# Create dataframe
	enrichment_dataframe = pd.concat([enrichment_results['upregulated'], enrichment_results['downregulated']])

	# Plot barcharts
	libraries = enrichment_dataframe['gene_set_library'].unique()
	if len(libraries):

		# Barcharts
		for gene_set_library in libraries:
			s.plot_library_barchart(enrichment_results, gene_set_library, enrichment_results['signature_label'], enrichment_results['sort_results_by']) # 10 300

		# Download button
		results_txt = enrichment_dataframe.sort_values('pvalue').to_csv(sep='\t', index=False)
		s.download_button(results_txt, 'Download Results', 'go_enrichment_results.txt')

		# Figure legend
		display(Markdown('** Figure '+plot_counter()+' | Gene Ontology Enrichment Analysis Results. **The figure contains interactive bar charts displaying the results of the Gene Ontology enrichment analysis generated using Enrichr. The x axis indicates the -log10(P-value) for each term. Significant terms are highlighted in bold. Additional information about enrichment results is available by hovering over each bar.  If you are experiencing issues visualizing the plot, please visit our <a href="https://maayanlab.cloud/biojupies/help#troubleshooting" target="_blank">Troubleshooting guide</a>.'.format(**locals())))
	else:
		display(Markdown('### No enrichment results were found.\n This is likely due to the fact that the gene identifiers were not recognized by Enrichr. Please note that Enrichr currently only supports HGNC gene symbols (https://www.genenames.org/). If your dataset uses other gene identifier systems, such as Ensembl IDs or Entrez IDs, consider converting them to HGNC. Automated gene identifier conversion is currently under development.'))

