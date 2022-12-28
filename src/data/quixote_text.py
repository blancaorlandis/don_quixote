import re
import pandas as pd

from src.functions.basics import get_module_path


class QX_Text():
    
    def __init__(self):
        self.module_path = get_module_path()
   
    
    def read_raw_quixote(self, part):
        '''
        Read the raw quixote texts files (part 1 or part 2)        
        > part (int): A number equal to 1 (first part) or 2 (second part)
        > output: text string
        '''
        main_path = get_module_path()
        path = main_path+'/data/raw/el_quixote_{}.txt'.format(part)
        return open(path, 'r', encoding='utf-8').read()
    
    
    def process_raw_quixote(self, part_list=[1,2], lower=True, keep_escape_character=False):
        '''
        Read and process the raw quixote texts files (part 1 or part 2).        
        > part (integer list): A list with the parts (1, 2 or both) needed to process
        > output: pandas dataframe
        '''
        dict_quixote = {}
        for p in part_list:
            raw_quixote = self.read_raw_quixote(part=p)
            if lower: raw_quixote = raw_quixote.lower()            
            # split by chapter
            #txt_clean_quixote = re.split("\n[Cc][Aa][Pp]í[Tt][Uu][Ll][Oo]\s\d+: ", raw_quixote)
            txt_clean_quixote = re.split("\nCapítulo\s\d+: ", raw_quixote, flags=re.IGNORECASE)
            # get chapter's title
            txt_clean_quixote = [ i.split('\n', 1) for i in txt_clean_quixote]

            if keep_escape_character:
                dict_translate= {'[':'', ']':''} # delete braket symbols ('[', ']')
            else:
                dict_translate= {'\n':'', '[':'', ']':''} # delete new line ('\n') and braket symbols ('[', ']')            
            txt_clean_quixote = [[j.translate(dict_translate) for j in i] for i in txt_clean_quixote]

            # get author and part title
            intro = txt_clean_quixote[0]
            # get chapter main corpus (skip the title text)
            txt_clean_quixote = txt_clean_quixote[1:]

            # create a dictionary and append
            if p==1: NPart='First'
            if p==2: NPart='Second'
            dict_clean_quixote_temp = { '{NPart}Part_ChapterNumber_{n}'.format(NPart=NPart, n=j+1):{'Part':p, 'ChapterNumber':j+1, 'ChapterName':i[0], 'ChapterCorpus':i[1]} for j, i in enumerate(txt_clean_quixote)}
            dict_quixote.update(dict_clean_quixote_temp)
            
        # from dictionary to pandas dataframe
        dataframe_quixote = pd.DataFrame.from_dict(dict_quixote).T
        
        return dict_quixote, dataframe_quixote