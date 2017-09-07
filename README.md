# heartCases
A medical language processing system for case reports involving cardiovascular disease.

(Work in progress.)

This system includes several different modules.

## heartCases_read.py

This part of the system is intended for parsing MEDLINE format files and specifically isolating those relevant to cardiovascular disease (CVD).

This script attempts to expand on existing MeSH annotations by performing tag classification with MeSH terms and adding terms to records where appropriate. These terms can optionally include just those used to search records (e.g., if only terms related to heart disease are provided, a classifier will be trained only to add those terms when missing.)
Similar approaches have been employed by [Huang et al. (2011) JAMIA.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3168302/) (Huang et al. used a k-nearest neighbors approach to get related articles and their highest-ranking MeSH terms. They achieved ~71% recall on average.)

Both previously present and newly added annotations are used to further annotate records with relevant ICD-10 disease codes.

A separate classifier is then used to determine medically-relevant content within abstracts, including demographic details, symptoms, and lab values, among other features.

Matching abstracts are labeled as part of a NER system. Labels may be visualized using the BRAT environment (http://brat.nlplab.org/).

### Requirements 
Requires the following packages. All packaged may be installed using *pip*.
* [bokeh](http://bokeh.pydata.org)
* [numpy](http://www.numpy.org/) *
* [nltk](http://www.nltk.org/)
* [scikit-learn](http://scikit-learn.org/stable/)
* [scipy](https://www.scipy.org/) *
* [tqdm](https://pypi.python.org/pypi/tqdm).  

*Note that numpy and scipy can be difficult to set up in some environments (e.g. Windows) so using a system like [Anaconda](https://www.continuum.io/downloads) may help. Or, find directions and Windows binaries for [scipy here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy) and for [numpy here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy).

Uses the Disease Ontology project database; see
http://www.disease-ontology.org/ or [Kibbe et al. (2015) NAR.](https://www.ncbi.nlm.nih.gov/pubmed/25348409)

Uses the [2017 MeSH Data Files provided by the NIH NLM](https://www.nlm.nih.gov/mesh/filelist.html).
These files are used without modification.

Uses the [2017 SPECIALIST Lexicon](https://lexsrv3.nlm.nih.gov/Specialist/Summary/lexicon.html).
See SPECIALIST.txt for terms and conditions regarding the use of the SPECIALIST NLP tools (don't worry, they're short).

The three data sets listed above are downloaded if not present locally.

### Usage
Run as:
`python heartCases_read.py`

Run with the `-h` option to see additional arguments.

#### Input
Text files containing literature references in MEDLINE format.
Files to process should be placed in the "input" folder - create this folder in the same location as the heartCases modules if it does not exist.

Alternatively, provide the input file as an argument:
  `--inputfile INPUT_FILE_NAME`

where INPUT_FILE_NAME is a text file containing one or more documents in MEDLINE format.

Input may also be provided as a text file of PubMed IDs, with one ID per line, using the argument:
  `--pmids INPUT_FILE_OF_PMIDS`


#### Output
Outputs are saved to the "output" folder at the end of each run.
These include three files containing the name of the input
(or "medline_entries_" if more than one input file is provided)
appended with the number of documents contained in the output
and one of the following:
* _out.txt - all documents provided in the input file(s) which
	match the given seach space (in this case, cardiovascular disease)
	with additional MeSH terms and ICD-10 annotations, where possible.
* _plots.html - Bokeh plots of document counts and properties.
* _raw_ne.txt - all document titles, PMIDs, and the raw dictionary
	of abstract text and NER labels (labels include entity types and locations).

Output of labeled abstracts is also provided in BRAT-compatible format in the "brat" folder within "output". Each abstract text is provided as [PMID].txt, while annotations are provided in [PMID].ann. The corresponding annotation.conf and visual.conf files are also generated.

Named entities used for abstract labeling are written to the file NE_dump.tsv.

Citation counts, if requested using the argument `--citation_counts TRUE`, are provided in citation_counts.tsv (as one record per line, including PMID, PMC citation count, and publication name) and in searched_documents.xml (including the raw XML record source of citation counts, as provided by PubMed).

## heartCases_learn.py

Work in progress.



# caseReportClassification
A medical language processing system that classifies case reports into single or multiple patient categories using their abstracts and MeSH terms.

## caseReport_classify.py

This system is intended to classify whether or not a case report is about a single patient or multiple patients.

### Usage
Run as:
`python caseReport_classify.py`

Run with the `-h` option to see additional arguments.

#### Input
This program can take 3 types of inputs:
- Run the program as `python caseReport_classify.py --folder FOLDERNAME` if using a folder containing MEDLINE files as input (see `example_FOLDER_format` for reference).
- Run the program as `python caseReport_classify.py --pmids PMIDS` if using a .txt file of PubMed IDs as input (see `example_PMIDS_format.txt` for reference).
- Run the program as `python caseReport_classify.py --medline MEDLINE` if using .txt file containing MEDLINE files as input (see `example_MEDLINE_format.txt` for reference).
The files must be in the same location as caseReport_classify.py

#### Output
The results will be stored as a tab separated .txt file called `Classification_Results.txt` containing the PubMed IDs as the first column and single/multiple as the second column.



# labValueExtraction
A medical language processing system that parses through full texts of case reports, retrieves the lab values, and finds the entity being measured by each lab value.

## extractLabValue.py

Running this file extracts the lab values of the passed in XML files of case reports and stores the results in `Lab Values.txt`.

### Usage
##### IMPORTANT!!! First UNZIP the files in the `word_embedding.syn1neg.zip` and `word_embedding.wv.syn0.zip` from the folder `files_to_be_loaded` and store them in the folder `files_to_be_loaded` as their own indepedent .npy files.

Run as:
`python extractLabValue.py --extract FOLDERNAME`

Run with the '-h' option to see additional arguments.

#### Input
- You will need a folder containing XML formatted full texts of case reports (see `example_FOLDERNAME_format` for reference).  Once you have the folder stored in the same location as `extractLabValue.py`, run `python extractLabValue.py --folder FOLDERNAME`

#### Output
The results will be stored in `Lab Values.txt` with double new line separating the results for each case report in the following format:

PMID: ########  
lab value:	LAB VALUE  
measured:	ENTITY  
lab value:	LAB VALUE  
measured:	ENTITY  
lab value:	LAB VALUE  
measured:	ENTITY  
...