#!/usr/bin/env python

import urllib

import argparse
from bs4 import BeautifulSoup
'''import os
import fnmatch
import math

import numpy as np
from scipy import interpolate
from scipy import stats as spstats
from scipy.stats import poisson as poisson
from scipy.special import gammaln as gammaln

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm '''

import logging
logging.basicConfig(format='%(levelname)s %(name)s.%(funcName)s: %(message)s')
logger = logging.getLogger('kegg2fasta')
logger.setLevel(logging.INFO)


# maybe given an id like abc1234 the output files by default are abc1234.txt and abc1234.fasta
def main():
    parser = argparse.ArgumentParser(description='Read pathway from KEGG and generate order sheet and fasta',
                                     epilog='Sample call: kegg2fasta hsa00120',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('keggid', help='kegg pathway id')
    args = parser.parse_args()

    kegggeneid_list = keggpathway2genes(args.keggid)
    print(kegggeneid_list)
    '''fp_spreadsheet = open(spreadsheetfile, 'w')
    fp_fasta = open(fastafile, 'w')
    for id in kegggeneid_list:
        (ncbiproteinid, ncbigeneid, uniprotid) = kegggene2xref(kegggeneid_list)
        (symbol, name, organism) = getfromncbigene(ncbigeneid)
        (aa_len, sequence) = getfromncbiprotein(ncbiproteinid)
        # here is where we add a row to the spreadsheet
        # here is where we add a record to the fasta file
        # boundary cases to be careful about:
        # what do you do when there are 0 records
        # what do you do when there are >1 record
        # do something reasonable to keep the info
        # spreadsheet should be plain text, tab delimited
        # ALWAYS check any text field for a tab. Some jokers slip tabs into gene names
        # some gene names and symbols have special characters that can screw you up, so check.
        # things like greek characters, subscripts and superscripts
        # gene names often have quotes and commas. this is why we never use csv
        # xlsx format is a pain
        # but you will probably us some crappy spreadsheet software to look at the output
        # be careful that you don't change gene names into dates.

        # the important thing is what to do when there are multiple splice variants listed
        # one reasonable thing is to provide the sequence for the first splice variant or isoform
        # and provide other identifiers
        # for nbci, try to take the .1 version

        # another reasonable thing would be to provide each splice variant as a separate row and fasta entry

        # probably the behavior should be a command-line option

        # if you can find a biopython method to do anything, use it
        # i know the first person who wrote seqio
    '''

#    kegggeneid_list = keggpathway2genes(args.keggid)
def keggpathway2genes(keggid):
    #http://www.kegg.jp/dbget-bin/www_bget?pathway+hsa00120
    url = "http://www.kegg.jp/dbget-bin/www_bget?pathway+"+keggid
    import urllib.request
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r,"html.parser")
    ths = soup.find_all('th')
    kegggeneid_list = []
    for th in ths:
        th_nobr = th.nobr
        if th_nobr.string == "Gene": #is the header cell for the gene row
            tr = th.parent #should be the tr that contains the th and the td contains a table of the genes
            geneinfo = tr.select("td table tr")
            for geneinfopart in geneinfo:
                 #only gives the links in the first column (which is the gene code). The 2nd column is the unneeded gene description
                genecode = geneinfopart.contents[0]
                for link in genecode.select("a"):
                    kegggeneid_list.append(link.string)
    return kegggeneid_list

#(ncbiproteinid, ncbigeneid, uniprotid) = kegggene2xref(kegggeneid_list)
#def kegggene2xref(kegggeneid_list):



if __name__ == "__main__":
    main()
