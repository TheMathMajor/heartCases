#!/usr/bin/python
#heartCases_help.py
'''
heartCases is a medical language processing system for case reports 
involving cardiovascular disease (CVD).

This part of the system includes helper functions.

'''

import os, sys, urllib, urllib2

def find_citation_counts(pmids):
	#Given a list of PMIDs, return counts of PMC citation counts
	#(e.g., 150 documents have 0 citations, 20 documents have 1, etc.)
	#Also produces two files:
	#the raw output of the Pubmed search in XML 
	#and a file containing a PMID, its corresponding
	#citation count, and its publication, one per line.
	
	#This list may be long, so makes a POST to the History server first.
	
	counts = {} #Counts of citation counts
	counts_by_pmid = {} #Citation counts and pubs for each PMID 
						#(IDs are keys)

	baseURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	epost = "epost.fcgi"
	esummary = "esummary.fcgi?db=pubmed"
	esummary_options = "&usehistory=y&retmode=xml&version=2.0"
	
	outfiledir = "output"
	outfilename = "searched_documents.xml"
	countsfilename = "citation_counts.tsv"
	
	if not os.path.isdir(outfiledir):
		os.mkdir(outfiledir)
	os.chdir(outfiledir)
	
	if len(pmids) > 0:
		
		try:
			#POST using epost first, with all PMIDs
			idstring = ",".join(pmids)
			queryURL = baseURL + epost
			args = urllib.urlencode({"db":"pubmed","id":idstring})
			response = urllib2.urlopen(queryURL, args)
			
			response_text = (response.read()).splitlines()
			
			webenv_value = (response_text[3].strip())[8:-9]
			webenv = "&WebEnv=" + webenv_value
			querykey_value = (response_text[2].strip())[10:-11]
			querykey = "&query_key=" + querykey_value
			
			batch_size = 500
			
			i = 0
			while i <= len(pmids):
				retstart = "&retstart=" + str(i)
				retmax = "&retmax=" + str(i + batch_size)
				queryURL = baseURL + esummary + querykey + webenv \
							+ retstart + retmax + esummary_options
				
				response = urllib2.urlopen(queryURL)
				
				out_file = open(outfilename, "a+")
				chunk = 1048576
				while 1:
					data = (response.read(chunk)) #Read one Mb at a time
					out_file.write(data)
					if not data:
						break
					sys.stdout.flush()
					sys.stdout.write(".")
					
				i = i + batch_size
				
			#Now that the file is complete, parse it and get the counts
			out_file.seek(0)
			for line in out_file:
				if not line.strip():
					continue
				splitline = line.split("<")
				if splitline[1][0:19] == "DocumentSummary uid":
					this_pmid = str((splitline[1].split("\""))[1])
				if splitline[1][0:7] == "Source>":
					this_pub = str((splitline[1].split(">"))[1])
				if splitline[1][0:12] == "PmcRefCount>":
					this_count = str(splitline[1][12])
					counts_by_pmid[this_pmid] = (this_count, this_pub)
						
			out_file.close()
			
			#Get counts of counts
			#Write the counts to file, too
			with open(countsfilename, 'wb') as countsfile:
				for pmid in counts_by_pmid:
					count_num = counts_by_pmid[pmid][0]
					pub_name = counts_by_pmid[pmid][1]
					outstring = "%s\t%s\t%s\n" % (pmid, count_num, pub_name)
					countsfile.write(outstring)
					count_num_str = str(count_num)
					if count_num_str not in counts:
						counts[count_num_str] = 1
					else:
						counts[count_num_str] = counts[count_num_str] +1
			
			print("\nRetrieved citation counts for %s records." \
					% len(pmids))
		
		except urllib2.HTTPError as e:
			print("Couldn't complete PubMed search: %s" % e)
	
	else:
		print("No IDs provided to find citation counts for.")
	
	os.chdir("..")
	
	return counts, outfilename
