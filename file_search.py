import os
import pickle
import PySimpleGUI as sg
sg.ChangeLookAndFeel('Dark')


class Gui:
    def __init__(self):
        self.layout = [[sg.Text('Search Term', size=(10,1)), 
                        sg.Input(size=(45,1), focus=True), 
                        sg.Radio('Contains', group_id='choice'), 
                        sg.Radio('StartsWith', group_id='choice'), 
                        sg.Radio('EndsWith', group_id='choice')],
                       [sg.Text('Root Path', size=(10,1)), 
                        sg.Input('D:/', size=(45,1)), 
                        sg.FolderBrowse('Browse'), 
                        sg.Button('Re-Index', size=(10,1)), 
                        sg.Button('Search', size=(10,1), bind_return_key=True)],
                       [sg.Output(size=(100,30))] 
                      ]

        self.window = sg.Window('File Search Engine').Layout(self.layout)



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
            pickle.dump(self.file_index, f)


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


def test1():
    s = SearchEngine()
    s.create_new_index('F:/')
    s.search('White')

    print()
    print('>> There were {:,d} matches out of {:,d} records searched'.format(s.matches , s.records))
    print()
    print('>> This query produced the following matches:')
    for match in s.results:
        print('   ' + match)
    print()


def test2():
    g = Gui()
    g.window.Read()

#test1()

test2()