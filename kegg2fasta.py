#!/usr/bin/env python

import urllib
import urllib.request

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


website = "http://www.kegg.jp"


# maybe given an id like abc1234 the output files by default are abc1234.txt and abc1234.fasta
def main():
    parser = argparse.ArgumentParser(description='Read pathway from KEGG and generate order sheet and fasta',
                                     epilog='Sample call: kegg2fasta hsa00120',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('keggid', help='kegg pathway kegggeneid')
    args = parser.parse_args()

    print_file = True

    kegggeneid_urls = keggpathway2genes(args.keggid)
    #fp_spreadsheet = open(spreadsheetfile, 'w')
    #fp_fasta = open(fastafile, 'w')
    c=kegggeneid_urls.keys()
    from gene import Gene
    import time
    genes = []
    start_time = time.time()
    for kegggeneid in kegggeneid_urls.keys():
        kegggeneurl=kegggeneid_urls[kegggeneid]

        (ncbiproteinid_url, ncbigeneid_url, uniprotid_url, aa_len, sequence) = kegggene2xref(kegggeneurl)
        (symbol, name, organism) = getfromncbigene(ncbigeneid_url)
        #(aa_len, sequence) = getfromncbiprotein(ncbiproteinid_url)
        gene = Gene(ncbiproteinid_url[1],ncbigeneid_url[1], uniprotid_url[1], symbol, name, organism, aa_len, sequence)
        genes.append(gene)
        print("Time since start is: " + str(time.time()-start_time) + " seconds" )

    if print_file:
        extension = ".tsv"
        import datetime
        #format similar to pathway-hsa00120_2017-02-28_14:30:14
        filepath = 'output/pathway-'+args.keggid+" " + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        file = open(filepath + extension, 'w')
        file.write("ncbiproteinid	ncbigeneid	uniprotid	symbol	name	organism	aa_len	sequence\n")
        for gene in genes:
            file.write(gene.get_row()+"\n")
        file.close()
    else:
        print(gene.get_row())
    print("Finished in "+str(time.time()-start_time)+" seconds")



#    kegggeneid_url = keggpathway2genes(args.keggid)
def keggpathway2genes(keggid):
    #http://www.kegg.jp/dbget-bin/www_bget?pathway+hsa00120
    url = website+"/dbget-bin/www_bget?pathway+"+keggid
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r,"html.parser")
    ths = soup.find_all('th')
    kegggeneid_url = {}
    for th in ths:
        th_nobr = th.nobr
        if th_nobr.string.lower().strip() == "gene": #is the header cell for the Gene row
            tr = th.parent #should be the tr that contains the th and the td contains a table of the genes
            geneinfo = tr.select("td table tr")
            for geneinfopart in geneinfo:
                 #only gives the links in the first column (which is the gene code). The 2nd column is the unneeded gene description
                genecode = geneinfopart.contents[0]
                for link in genecode.select("a"):
                    kegggeneid_url[link.string] = website+link['href']
    return kegggeneid_url

#(ncbiproteinid_url, ncbigeneid_url, uniprotid_url) = kegggene2xref(kegggeneid_list)
def kegggene2xref(kegggene_url):
    r = urllib.request.urlopen(kegggene_url).read()
    soup = BeautifulSoup(r,"html.parser")
    ths = soup.find_all('th')
    ncbiproteinid_url = None
    ncbigeneid_url = None
    uniprotid_url = None
    aa_len = None
    sequence = None
    for th in ths:
        th_nobr = th.nobr
        if th_nobr.string.lower().strip() == "other dbs": #is the header cell for the Other DBs row
            tr = th.parent #should be the tr that contains the th and the td contains a table of the genes
            otherdbinfo = tr.select("td > div > div") #gives a series of divs
            # within the tr, there are a series of divs. The odd number divs are the left column (titles)
            # and the even number divs are the right column (links & code)
            infoToRead = ""
            for div in otherdbinfo:
                if infoToRead:
                    link = div.a['href']
                    id = div.a.string
                    if infoToRead == "protein":
                        ncbiproteinid_url= (link, id)
                    elif infoToRead == "gene":
                        ncbigeneid_url= (link, id)
                    elif infoToRead == "uniprot":
                        uniprotid_url= (link, id)
                    infoToRead = ""
                #if something is prepared, then it cannot simulateneously be a title for the next one
                if div.string != None and div.string.strip() == "NCBI-ProteinID:":
                    infoToRead = "protein"
                elif div.string != None and div.string.strip() == "NCBI-GeneID:":
                    infoToRead = "gene"
                elif div.string != None and div.string.strip() == "UniProt:":
                    infoToRead = "uniprot"
        elif th_nobr.string.lower().strip() == "aa seq":
            tr = th.parent
            aaseq_cell = tr.select("td")[0] #gives a series of divs
            from bs4.element import NavigableString
            from bs4.element import Tag
            for child in aaseq_cell.contents:
                if type(child) is NavigableString:
                    a = child.strip()
                    if len(child.strip()) > 0:
                        if " aa" in child:
                            aa_lenstr = " ".join(child.string.split()).replace(" aa","")
                            aa_len = int(aa_lenstr)
                        else:
                            sequence = child.string.strip()
                #bs4.element.Tag. The two <a> (which are unnecessary) as well as the <br> we want will get past the first part of the logical statement
                elif type(child) is Tag and child.name == "br":
                    sequence = "".join(str(child).replace("<br>","").replace("</br>","").split())


    return (ncbiproteinid_url, ncbigeneid_url, uniprotid_url, aa_len, sequence)

#returns (symbol, name, organism) = getfromncbigene(ncbigeneid_url)
def getfromncbigene(ncbigeneid_url):
    #http://www.kegg.jp/dbget-bin/www_bget?pathway+hsa00120
    r = urllib.request.urlopen(ncbigeneid_url[0]).read()
    soup = BeautifulSoup(r,"html.parser")
    #dt tag on the left, dd tag on the right

    #go to summaryDl
    summaryDl = soup.find(id="summaryDl")
    summaryDlChildren = summaryDl.contents
    foundSymbol = False
    foundName = False
    foundOrganism = False
    symbol = None
    name = None
    organism = None
    from bs4.element import Tag
    for summaryDlChild in summaryDlChildren:
        if type(summaryDlChild) is not Tag:
            continue
        if foundSymbol:
            symbol = summaryDlChild.contents[0]
            foundSymbol = False
        if foundName:
            name = summaryDlChild.contents[0]
            foundName = False
        if foundOrganism: #will be a link
            organism_children = summaryDlChild.contents
            for child in organism_children:
                if type(child) is Tag:
                    organism = child.string
                    break
            foundOrganism = False
        title = summaryDlChild.contents[0].string.lower().strip()
        title = " ".join(title.split())
        if title == "official symbol":
            foundSymbol = True
        elif title == "official full name":
            foundName = True
        elif title == "organism":
            foundOrganism = True

    return (symbol, name, organism)

#(aa_len, sequence) = getfromncbiprotein(ncbiproteinid_url)


if __name__ == "__main__":
    main()
