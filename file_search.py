import os
import pickle

class SearchEngine:
    def __init__(self):
        self.file_index = []
        self.results = []
        self.matches = 0
        self.records = 0

    def create_new_index(self, root_path):
        #Create a new index and save to a file
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]  #'if files' filters out empty file list

        #Save to file
        with open('file_index.pkl' , 'wb') as f:    #Open as 'write binary'
            pickle.dump(self.file, f)


    def load_existing_index(self):
        #Load existing index
        try:
            with open('file_index.pkl','rb') as f:  #Open as 'read binary'
                self.file_index = pickle.load(f)
        except:                                     #In case file doesn't exist
            self.file_index = []


    def search(self, term, search_type = 'contains'):
        #Search for term based on search type
        
        #Reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0

        #Perform search
        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if ((search_type == 'contains' and term.lower() in file.lower()) or
                    (search_type == 'startswith' and file.lower().startswith(term.lower())) or
                    (search_type == 'endswith' and file.lower().endswith(term.lower()))):
                    
                    result = path.replace('\\' , '/') + '/' + file
                    self.results.append(result)
                    self.matches += 1
                else:
                    continue

        #Save search results
        with open('search_results.txt','w') as f:
            for row in self.results:
                f.write(row + '\n')


