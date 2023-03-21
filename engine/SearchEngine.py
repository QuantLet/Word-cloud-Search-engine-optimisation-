from nltk import PorterStemmer

from pdf.PDFManager import PDFManager
from indexers.IndexDriver import IndexDriver


class SearchEngine:
    def __init__(self, search_driver: IndexDriver):
        self.search_driver = search_driver
        self.ps = PorterStemmer()
        self.stopwords_list = {"i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this",'that',"that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't", "udcurlymod", "nvcpinkrddstratxbcbtsburstdgbdogeltcardrgntlskpascxrpbtcetcethomniscdashdcrfctgnonmrdynam", "btcomnigntclambbrdgbsclsknmrblitzltcethbtsfctdogestratsteembtcddmdbtmgroup", "vydytiyzjjhrtncozhjtzv", "vbuptqjymgcq", "leiowsmcwqueca", "uicgnihcgj", "hfd", "honxnk", "latexit", "latexit", "sha", "base", "nqu", "xkgewckhjywtkfomismnzuo", "aaab" ,"nicbzbnswmxeizn", "rr", "ainsqucoqt", "mvjbfsb", "vjm", "wbm", "gjcuupt", "ciwdfvpp", "vplvtn", "aoslgyd", "zsjmgynbjfx", "tfwnza", "rbwdt", "yaacqanbwp", "kromocsn", "gnwuzphegrwj", "vbuptqjymgcq", "ljtte", "douzi", "leqf", "xcueavcjx", "eikvzwqslao", "pbr", "yyy", "acirytnzldfnixzhkxycs", "bcfl", "uljw", "divlsnlzm", "vydytiyzjjhrtncozhjtzv", "vglzllvmmaslj", "jmeju", "kwdwjvkwcinxc", "urocdv", "latexit", "null", "until"}
        pass

    def index(self, courselet_id, pdf_url, title, author):
        word_cloud, data, duration = PDFManager(pdf_url).get_search_data()
        indexed = self.search_driver.index("courselets", courselet_id, data, word_cloud, title, author)
        if indexed:
            return True, {"id": courselet_id, "word_cloud": word_cloud, "search_data": data, "duration": duration}
        else:
            return False, None

    def search(self, query):
        results = self.search_driver.search("courselets", self.stem_query(query))
        return results['hits']

    def stem_query(self, query):
        """
        Trimming input search terms to be used for the occurrence matrix.
        The output is a generalized stemmed input form ready for checking and a count of terms for the ngram_range.
        """

        # splitting the phrase by pieces
        search_term = query.split(' ')

        # cleaning stopwords
        search_term = [i for i in search_term if i not in self.stopwords_list]

        # stem the words
        search_term = [self.ps.stem(i) for i in search_term]

        return ' '.join(search_term)
