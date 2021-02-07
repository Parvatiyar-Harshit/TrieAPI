from django.shortcuts import render
from django.http  import HttpResponse


import json
import csv


class TrieNode(): 
    def __init__(self): 
          
        # Initialising one node for trie 
        self.children = {} 
        self.last = False
  
class Trie(): 
    def __init__(self): 
          
        # Initialising the trie structure. 
        self.root = TrieNode() 
        self.word_list = [] 
  
    def formTrie(self, keys): 
          
        # Forms a trie structure with the given set of strings
        for key in keys: 
            self.insert(key) # inserting one key to the trie. 
  
    def insert(self, key): 
          
        # Inserts a key into trie if it does not exist already. 
         
        node = self.root 
  
        for a in list(key): 
            if not node.children.get(a): 
                node.children[a] = TrieNode() 
  
            node = node.children[a] 
  
        node.last = True
  
    def search(self, key): 
          
        # Searches the given key in trie for a full match  
        node = self.root 
        found = True
  
        for a in list(key): 
            if not node.children.get(a): 
                found = False
                break
  
            node = node.children[a] 
  
        return node and node.last and found
    def suggestionsRec(self, node, word): 
          
        # Method to recursively traverse the trie 
        # and return a whole word.  
        if node.last: 
            self.word_list.append(word) 
  
        for a,n in node.children.items(): 
            self.suggestionsRec(n, word + a) 
  
    def printAutoSuggestions(self, key): 
          
        # Returns all the words in the trie whose common 
        # prefix is the given key thus listing out all  
        # the suggestions for autocomplete. 
        node = self.root 
        not_found = False
        temp_word = '' 
  
        for a in list(key): 
            if not node.children.get(a): 
                not_found = True
                break
  
            temp_word += a 
            node = node.children[a]

        if node.last and not node.children: 
            return [temp_word]
        else:
            self.suggestionsRec(node, temp_word)
            return self.word_list
#function to sort  based on string length
def Sorting(lst): 
    lst.sort(key=len) 
    return lst
#function to reverse an array
def Reverse(lst): 
    return [ele for ele in reversed(lst)]
# function to get unique values 
def unique(list1):
     
  
    # intilize a null list for names and scores
    unique_list = []
    rank_list = [] 
      
    # traverse for all elements 
    for x in range(len(list1)): 
        # check if exists in unique_list or not 
        if list1[x] not in unique_list: 
            unique_list.append(list1[x])
   
    #make json output
    arr_len = len(unique_list)      
    unique_json_list = []
    for u in range(len(unique_list)):
        unique_json_list.append({"name":unique_list[u] ,"score":arr_len-u})
    # return json output 
    return unique_json_list
 # Create your views here.
def index(request):
 response = json.dumps([{}])
 return HttpResponse(response,content_type='text/json')

def main_func(request, query):
 #initialize empty result array
 res_array = []
 temp_word = ''
 obj = Trie()
 query = query.lower()
 
 #implement TRIE data structure on data from csv file
 with open('C:/Users/Harshit Parvatiyar/Desktop/casamelhorsubmission/baby-names.csv') as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     for row in csv_reader:
         if (line_count>0):
             name = row[1]
             name = name.lower()
             obj.insert(name)
             line_count += 1
         else:
             line_count +=1

 #if query size is greater than 3 then loop through the query and find all similar names 
 if (len(query)>=3):
    for i in query:
        
        temp_word = temp_word+i
        temp_array = obj.printAutoSuggestions(temp_word)
        temp_array = Reverse(temp_array)
        res_array = temp_array+res_array
 
 res_array = unique(res_array)
 
 
  



      


 if request.method == 'GET':
  try:
   response = json.dumps(res_array)
  except:
   response = json.dumps([{'error':'No Query Possible'}])
 return HttpResponse(response,content_type='text/json')
