
class Gene:
    def __init__(self, ncbiproteinid, ncbigeneid, uniprotid, symbol, name, organism, aa_len, sequence):
        self.ncbiproteinid = ncbiproteinid
        self.ncbigeneid = ncbigeneid
        self.uniprotid = uniprotid
        self.symbol = symbol
        self.name = name
        self.organism = organism
        self.aa_len = aa_len
        self.sequence = sequence

    '''    # here is where we add a row to the spreadsheet
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
    def get_row(self):
        row = [self.ncbiproteinid , self.ncbigeneid , self.uniprotid , self.symbol , self.name, \
               self.organism , str(self.aa_len),self.sequence]
        rowstr = ""
        for element in row:
            elementstr  = " ".join(element.split())
            rowstr = rowstr + "\t" + elementstr
        return rowstr[1:] #remove initial tab