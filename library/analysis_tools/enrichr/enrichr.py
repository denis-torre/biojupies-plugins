#################################################################
#################################################################
############### DE 
#################################################################
#################################################################

#############################################
########## 1. Load libraries
#############################################
##### 1. General support #####
import requests
import json
import time
import pandas as pd
from IPython.display import display, Markdown
from plotly import tools
from plotly.offline import iplot
import plotly.graph_objs as go

##### 2. Other libraries #####


#######################################################
#######################################################
########## S1. Function
#######################################################
#######################################################

#############################################
########## 1. Run
#############################################

def get_genesets(signature_dataframe, signature_col, top_n=True, nr_genes=500):
	genesets = {}
	sorted_genes = signature_dataframe.sort_values(signature_col).index
	genesets['upregulated'] = sorted_genes[-500:]
	genesets['downregulated'] = sorted_genes[:500]
	return genesets

def submit_enrichr_geneset(geneset, label=''):
	ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/addList'
	genes_str = '\n'.join(geneset)
	payload = {
		'list': (None, genes_str),
		'description': (None, label)
	}
	response = requests.post(ENRICHR_URL, files=payload)
	if not response.ok:
		raise Exception('Error analyzing gene list')
	time.sleep(0.5)
	data = json.loads(response.text)
	return data

def run(signature, signature_label, geneset_size=500, sort_genes_by='t'):

	# Sort signature
	signature = signature.sort_values(sort_genes_by, ascending=False)

	# Get genesets
	genesets = {
		'upregulated': signature.index[:geneset_size],
		'downregulated': signature.index[-geneset_size:]
	}

	# Submit to Enrichr
	enrichr_ids = {geneset_label: submit_enrichr_geneset(geneset=geneset, label=signature_label+', '+geneset_label+', from BioJupies') for geneset_label, geneset in genesets.items()}
	enrichr_ids['signature_label'] = signature_label
	return enrichr_ids

#############################################
########## 2. Plot
#############################################

def plot(enrichr_results, plot_counter):
	display(Markdown('##### {signature_label} Signature:\n * Upregulated: https://maayanlab.cloud/Enrichr/enrich?dataset={upregulated[shortId]} \n * Downregulated: https://maayanlab.cloud/Enrichr/enrich?dataset={downregulated[shortId]}'.format(**enrichr_results)))

	# Figure Legend
	display(Markdown('** Table '+plot_counter('table')+' | Enrichr links. **The table displays links to Enrichr containing the results of enrichment analyses generated by analyzing the up-regulated and down-regulated genes from a differential expression analysis. By clicking on these links, users can interactively explore and download the enrichment results from the Enrichr website'.format(**locals())))

