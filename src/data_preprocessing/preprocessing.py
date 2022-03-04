from string import punctuation







class Preprocessing():
    
    '''

        This class does the normal preprocessing like deleting the numbers, punctuations and stopwords, as well as two specific 
        preprocessing such as deleting english words and the place and date of the news text- which comes at the start of the 
        news text, and the name of the journalist occurring at the last of the text.


    '''
    def __init__(self, save_in="", output=False):
        '''
            save_in = the place where you save the file (if given) 
            output = print the processed text to console
            save_output = save the processed text to a file
        '''
        self.save_in = save_in
        self.output = output
        
        
    
    
    
    
    
    
    
    def delEngWords(self, filename="", text="", next=False):
        ''' 
            filename = give the filename where the text is in
            or give the value to text\
            next = there is a next step that needs the processed text of this step
        '''
        processed_text = ""
        # print(filename)
        if not text :
            with open(filename, encoding="utf-8") as fp:
                raw_text = fp.read()
        else: raw_text = text
        for letters in raw_text:
                if not ((letters <= 'z' and letters >= 'a') or ( letters >= 'A' and letters <= 'Z')):
                    processed_text += letters
        if self.save_in:
            with open(self.save_in, 'w', encoding='utf-8') as wp:
                
                    wp.write(processed_text)
        if self.output: print(processed_text)                      

                        
        
                 
        if next:
            return processed_text       






            
    def delNumbers(self, filename="", text="", next = False):
        nepali_no = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']
        processed_text = ""
        if not text :
            with open(filename, encoding="utf-8") as fp:
                raw_text = fp.read()
        else: raw_text = text
        for letters in raw_text:
            if letters not in nepali_no and not (letters >= '0' and letters <= '9'):
                processed_text += letters
        if self.save_in:
            
            with open(self.save_in, 'w', encoding= "utf-8") as wp:
                wp.write(processed_text)
                        
        if self.output:
            print(processed_text)           
        if next:
            return processed_text      
                    
                    
                    
                    
                    
                    
    def delPnctuatn(self, filename="", text="", next=False, punctuation=punctuation):
        punctuation = list(punctuation)
        punctuation.append('।')
        punctuation.append('’')
        punctuation.append('‘')
        punctuation.append('–')
        punctuation.append(' ः')
        
        
        processed_text = ""
        if not text :
            with open(filename, encoding="utf-8") as fp:
                raw_text = fp.read()
        else: raw_text = text
        for letters in raw_text:
            if letters not in punctuation:
                processed_text += letters
        if self.save_in:
            with open(self.save_in, 'w', encoding= "utf-8") as wp:
                wp.write(processed_text)
        if self.output:
            print(processed_text)

        if next:
            return processed_text
    
    
    
    
    
    def delStopwords(self, filename = '', text = '', next = False):
        processed_text = []
        with open('./stopwords.txt',encoding="utf8") as sw:
        # with open('./stopwords.txt',encoding="utf8") as sw: for windows os
            stopwords = (sw.read()).split()
        
        if not text:
            with open(filename) as fp:
                raw_text = fp.read()
        else:
            raw_text = text
        
        raw_text = raw_text.split()
        for letters in raw_text:
            if letters not in stopwords:
                processed_text.append(letters)
        
        processed_text = ' '.join(processed_text)
        if self.save_in:
            with open(self.save_in, 'w', encoding='Utf-8') as wp:
                wp.write(processed_text)
        if self.output:
            print(processed_text, end= ' ')
        
        if next:
            return processed_text
    
    
    



