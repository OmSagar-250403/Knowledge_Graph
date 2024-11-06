import os
import math
import pandas as pd
from collections import defaultdict

punctuations = '''!()-[]{};:'"\,\n<>./?@#$%^&*_~'''

files = os.listdir('../actors and movies')
document_index = {}
for i in range(len(files)):
    document_index[str(i+1)] = files[i].replace(".json", "")

#print(document_index)
count = 1
Documents_dict = {}
vocab_dict = defaultdict(int)   
for fil in files:     
    f = pd.read_json('../actors and movies/' + str(fil))
    text = f['text'][0]
    #print(text)
    text = text.replace('\n', ' ')
    final_text = ""
    for char in text:
        if char not in punctuations:
            final_text = final_text + char
    list_text = final_text.split(" ")
    for word in list_text:
        vocab_dict[word] += 1
    Length_text = len(list_text)
    uniq_set = set(list_text)
    uniq_text = list(uniq_set)
    TF_dict = {}
    norm_doc = 0
    for words in uniq_text:
        list_temp = [list_text.count(words), list_text.count(words)/Length_text]
        TF_dict[words] = list_temp
        norm_doc = norm_doc + TF_dict[words][1]*TF_dict[words][1]
    norm_docc = math.sqrt(norm_doc)
    TF_dict["norm_doc" + str(count)] = norm_docc
    Documents_dict["doc" + str(count)] = TF_dict
    count = count + 1

freq_vocab = []
uniq_vocab = []
for word in vocab_dict.keys():
    if vocab_dict[word] > 10:
        freq_vocab.append(word)
    elif vocab_dict[word] == 1:
        uniq_vocab.append(word)

print("Enter your query: ")
query = input()
query = query.split(" ")
query_set = set(query)
query_list = list(query_set)

i = 0
Query_doc_freq = {}
Total_doc_freq = 0
while i < len(query_list):
    doc_freq = 0
    for j in range(1, len(Documents_dict) + 1):
        if query_list[i] in Documents_dict["doc" + str(j)].keys():
            doc_freq = doc_freq + 1
    Total_doc_freq = Total_doc_freq + doc_freq
    Query_doc_freq[query_list[i]] = doc_freq
    i = i + 1

if Total_doc_freq == 0:
    print("--------Query not found--------")
else:
    norm_q = 0
    for Keyss in Query_doc_freq:
        print(Keyss, "->", Query_doc_freq[Keyss], "->", Query_doc_freq[Keyss]/Total_doc_freq)
        Query_doc_freq[Keyss] = Query_doc_freq[Keyss]/Total_doc_freq
        norm_q = norm_q + Query_doc_freq[Keyss]*Query_doc_freq[Keyss]
    norm_qq = math.sqrt(norm_q)
    print("\n|| q || = ", norm_qq, "\n")

    Similarity_scores = {}
    i = 1
    while i <= len(Documents_dict):
        sim_temp = 0
        j = 0
        while j < len(query_list):
            if "doc" + str(i) in Documents_dict and query_list[j] in Documents_dict["doc" + str(i)].keys():
                sim_temp = sim_temp + Documents_dict["doc" + str(i)][query_list[j]][1]*Query_doc_freq[query_list[j]]
            j = j + 1
        if "doc" + str(i) in Documents_dict:
            denominator = norm_qq*Documents_dict["doc" + str(i)]["norm_doc" + str(i)]
            Similarity_scores["doc" + str(i)] = sim_temp/denominator
        i = i + 1

    print("Similarity scores:")
    print(Similarity_scores)
    print("\nRanking based on similarity scores: ")

    i = 1
    for a in sorted(Similarity_scores.items(), reverse=True, key = lambda x : x[1]):
        if a[1] != 0:
            print(document_index[a[0].replace("doc","")] + ".json is the Document" + "Ranked at " + str(i) + " With " + " Similarity Score :" + str(a[1]))
        i = i + 1  