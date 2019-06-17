import re
import random
import gensim
from flask import url_for, render_template
from flask import request, redirect
from flask import Flask
from gensim.models import word2vec
from pymystem3 import Mystem

def get_s_and_v_dictionaries(string, string_lem):
    nouns_dict = {}
    verbs_dict = {}
    try:
        for dictionary, dictionary_lem in zip(mystem.analyze(string),
                                              mystem.analyze(string_lem)):
            try:
                word = dictionary['text'] + '_' + dictionary['analysis'][0]['gr'][:1]
                word_lem = dictionary_lem['text'] + '_' + dictionary_lem['analysis'][0]['gr'][:1]
                if word[-1] == 'S' and word_lem[-1] == 'S':
                    nouns_dict[word_lem] = word
                if word[-1] == 'V' and word_lem[-1] == 'V':
                    verbs_dict[word_lem] = word
            except KeyError:
                continue
            except  IndexError:
                continue
        return nouns_dict, verbs_dict
    except BrokenPipeError:
        print('Something went wrong')

def get_answer(message):
    pfrase = message
    pfrase = pfrase.lower()
    pfrase = pfrase.replace(',','').replace('.', '').replace('?', '').replace('!', '').replace('—','').replace(';', '').replace(':', '').replace('»', '').replace('«', '').replace(')','').replace('(','')

    #лемматизирую текст
    lemma1 = mystem.lemmatize(pfrase)
    lemma1 = ''.join(lemma1)[:-1]

    #pfrase, lemma1
    s_dict, v_dict = get_s_and_v_dictionaries(pfrase, lemma1)
    nouns, verbs = list(s_dict.keys()), list(v_dict.keys())


    nodes_list_n = []
    nodes_list_v = []
    for word in nouns:
        if word in model:
            for i in model.most_similar(positive=[word], topn = 30):
                if i[1]  >= 0.5:
                    nodes_list_n.append(i[0])
            #print(nodes_list_n)

    for word in verbs:
        if word in model:
            for i in model.most_similar(positive=[word], topn = 30):
                if i[1]  >= 0.5:
                    nodes_list_v.append(i[0])
            #print(nodes_list_v)


    order_1 = []
    order_2 = []
    order_3 = []
    order_4 = []
    order_5 = []

    for i in nouns:
        for j in verbs:
            if i in d_list and j in d_list:            
                with open ('data/pogovorki.txt',
                           'r', encoding = 'utf-8') as p:
                    for line in p:
                        if d[i] in line and d[j] in line:
                            order_1.append(line)

    for i in nouns:
        for j in verbs:
            if i in d_list or j in d_list:            
                with open ('data/pogovorki.txt',
                           'r', encoding = 'utf-8') as p:
                    for line in p:
                        try:
                            if d[i] in line or d[j] in line:
                                order_2.append(line)
                        except KeyError:
                            continue

    for i in nodes_list_n:
        for j in nodes_list_v:
            if i in d_list and j in d_list:            
                with open ('data/pogovorki.txt',
                           'r', encoding = 'utf-8') as p:
                    for line in p:
                        if d[i] in line and d[j] in line:
                            order_3.append(line)

    for i in nodes_list_n:
        for j in nodes_list_v:
            if i in d_list or j in d_list:            
                with open ('data/pogovorki.txt',
                           'r', encoding = 'utf-8') as p:
                    for line in p:
                        try:
                            if d[i] in line or d[j] in line:
                                order_4.append(line)
                        except KeyError:
                            continue                            
                            
    for i in nodes_list_n, nodes_list_v, nouns, verbs:
        for j in i:
            if j in d_list:            
                with open ('data/pogovorki.txt',
                           'r', encoding = 'utf-8') as p:
                    for line in p:
                        if d[j] in line:
                            order_5.append(line)  

    answer = 'Мне Вам нечего ответить.'

    for order in [order_1, order_2, order_3, order_4, order_5]:
        if len(order) != 0:
            answer = random.choice(order)
            break
    
    return answer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/answer', methods=['POST'])
def answer():
    if request.method == 'POST':
        message = request.form['message']
        answer = get_answer(message)
        return render_template('answer.html', answer=answer)
    else:
        return 'error'

if __name__ == '__main__':
    mystem = Mystem()

    m = 'data/ruscorpora_mystem_cbow_300_2_2015.bin.gz'

    model = gensim.models.KeyedVectors.\
        load_word2vec_format(m, binary=True)

    with open ('data/pogovorki_lemma.txt', 'r', encoding = 'utf-8') as f:
        file = f.read()
        file = file.replace('=', '_')

    words_s = re.findall(r'[а-яА-ЯёЁ]+\{[а-яА-ЯёЁ]+_[S]', file)

    words_v = re.findall(r'[а-яА-ЯёЁ]+\{[а-яА-ЯёЁ]+_[V]', file)

    d = {}
    d_X = {}
    words_s = str(words_s)
    words_s = words_s.replace("'", '').replace("[", '').replace("]", '').replace(' ', '')
    words_s = words_s.replace("{", ' ')
    words_ss = words_s.replace("_S", '').replace("_V", '')
    #print(words_s)
    rusult_s = re.split(r',', words_s)
    rusult_ss = re.split(r',', words_ss)
    #print(rusult_ss)


    words_v = str(words_v)
    words_v = words_v.replace("'", '').replace("[", '').replace("]", '').replace(' ', '')
    words_v = words_v.replace("{", ' ')
    #print(words_v)
    words_vv = words_v.replace("_S", '').replace("_V", '')
    rusult_v = re.split(r',', words_v)
    rusult_vv = re.split(r',', words_vv)


    for i in rusult_v:
        #print(i)
        rusult1 = re.split(' ', i)
        d[str(rusult1[1])] = str(rusult1[0])
        #print(rusult1[0])
    #d['мыло_S']
    d_list = d.keys()
    #print(d_list)

    #print(rusult)

    for i in rusult_s:
        #print(i)
        rusult1 = re.split(' ', i)
        d[str(rusult1[1])] = str(rusult1[0])
        #print(rusult1[0])

    for i in rusult_vv:
        #print(i)
        rusult1v = re.split(' ', i)
        d_X[str(rusult1v[1])] = str(rusult1v[0])
        #print(rusult1[0])
    #d['мыло_S']
    d_list_X = d_X.keys()
    #print(d_list)

    #print(rusult)

    for i in rusult_ss:
        #print(i)
        rusult1s = re.split(' ', i)
        d_X[str(rusult1s[1])] = str(rusult1s[0])
    #d_X['мыло']
    d_list_X = d_X.keys()
    #print(d_list_X)

    
    
    app.run(debug=False)

