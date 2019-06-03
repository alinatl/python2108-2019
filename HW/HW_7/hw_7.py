#pip install networkx
#pip install --upgrade networkx
#pip show networkx

import re
import gensim
import logging
import pandas as pd
import urllib.request
from gensim.models import word2vec
import matplotlib.pyplot as plt
from matplotlib import style
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community.centrality import girvan_newman

urllib.request.urlretrieve("http://rusvectores.org/static/" + 
                           "models/rusvectores2/ruscorpora" + 
                           "_mystem_cbow_300_2_2015.bin.gz",
                           "ruscorpora_mystem_cbow_300_2_" + 
                           "2015.bin.gz")

m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'

if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.\
        load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.\
        load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)

def inp_W():
    words = str(input('введите 1 слово.чтобы ' + 
                      'закончить сеанс нажмите 0 '))
    words = words.lower()

    words = words + '_S'
    wordlist = []
    wordlist.append(words)
    gra = []
    G = nx.Graph()
    nodes_list = []


    for word in wordlist:

        if word in model:
            #print(word)
            # смотрим на вектор слова (его размерность 300,
            # смотрим на первые 10 чисел)
            #print(model[word][:10])
            # выдаем 20 ближайших соседей слова:
            for i in model.most_similar(positive=[word],
                                        topn = 10):
                if i[1]  >= 0.5 and re.findall(r'\w_S',
                                               i[0]):
                    gra.append(i[0])
                    nodes_list.append(i[0])

                    #print(i)
                    for val in gra:

                        #print(val[0], val[1])

                        G.add_node(val)
                        # соединаем слово и 
                        # три его соседа связями
                        G.add_edge(words, val)
                        #print([n for n in G.neighbors(val[0])])
                    #print('узлы', G.nodes())
                    #print('ребра', G.edges())

                # слово + коэффициент косинусной близости
                #print(i[0], i[1])
                #print('\n')
            return '1', nodes_list, gra, words, G
                
        else:
            # Увы!
            print('Увы, слова "%s" нет в модели!' % word)
            return '2', nodes_list, gra, words, G

    #print('nodes_list', nodes_list)
    #print(gra)

def sosedi(nodes_list, G):
    node_list = []
    #print(nodes_list)

    for word in nodes_list:
        list_n = []
        if word in model:
            #print(word)
            # смотрим на вектор слова (его размерность 300,
            #                          смотрим на первые 10 чисел)
            #print(model[word][:10])

            # выдаем 20 ближайших соседей слова:
            for i in model.most_similar(positive=[word], topn = 20):
                #print(i)
                if i[1]  >= 0.5 and re.findall(r'\w_S', i[0]):
                    words = word
                    G.add_node(i[0])
                    # соединаем слово и три его соседа связями
                    G.add_edge(words, i[0])
                    #print('words-word', word)
            #list_n.append(i[0])
            #print('list_n', list_n)
            #print('ребра', G.edges())
            #print('\n')

            #node_list.append(list_n)
            #print('node_list', node_list)
            #return node_list
        else:
            # Увы!
            print('Увы, слова "%s" нет в модели!' % word) 

   # print('узлы', G.nodes())
   # print('ребра', G.edges())
   # list1, list2, list3 = node_list           
   # print(list1, list2, list3)
   
def deg(G):
    deg = nx.degree_centrality(G)
    print('далее список слов в порядке убывания показателя',
          'degree_centrality')
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        print (nodeid) 
    return deg

def clos(G):
    clos = nx.closeness_centrality(G, u=None,
                                       distance=None)
    print('далее список слов в порядке убывания показателя',
          'closeness_centrality')
    for nodei in sorted(clos, key=clos.get, reverse=True):
        print(nodei)
def bet(G):
    bet = nx.betweenness_centrality(G, k=None,
                                    normalized=True,
                                    weight=None,
                                    endpoints=False,
                                    seed=None)
    print('далее список слов в порядке убывания показателя',
          'betweenness_centrality')
    for node in sorted(bet, key=bet.get, reverse=True):
        print(node)
    return bet

def eig(G):
    eig = nx.eigenvector_centrality(G, max_iter=100, tol=1e-06,
                                    nstart=None, weight=None)
    print('далее список слов в порядке убывания показателя',
          'eigenvector_centrality')
    for nod in sorted(eig, key=eig.get, reverse=True):
        print(nod)
    return eig

def dia(G):
    print('Диаметр графа, самый длинный путь' + 
          'от одной вершины до другой: ',
          nx.diameter(G))

    print('Коэффициент ассортативности (насколько вся сеть',
          ' завязана на основных "хабах": )',
          nx.degree_pearson_correlation_coefficient(G))

    print('Плотность графа, отношение рёбер и узлов: ',
          nx.density(G))

    print('вот какой коэффициент у нашего графа: ',
          nx.average_clustering(G))
    #print(nx.transitivity(G))

    return clos

def nodecolor(G):
    import networkx as nx
    from networkx.algorithms import community
    communities_generator = girvan_newman(G)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    #sorted(map(sorted, next_level_communities))
    next_level_communities = list(next_level_communities)
    a1, a2, a3 = next_level_communities
    a1 = list(a1) 
    a2 = list(a2) 
    a3 = list(a3)
    #print( a1, a2 ,a3)
    return a1, a2, a3

def color(i, G):
    next_level_communities = nodecolor(G)
    next_level_communities = list(next_level_communities)
    a1, a2, a3 = next_level_communities
    a1 = list(a1) 
    a2 = list(a2) 
    a3 = list(a3)
    if i in a1:
        return 'red'
    elif i in a2:
        return 'yellow'
    elif i in a3:
        return 'blue'
#color('барбос_S')

def size(word, G):
    deg = nx.degree_centrality(G)
    k = deg[word]
    #print(k)
    if k <= 0.03:
        return 90
    elif k > 0.03 and k < 0.06:
        return 150
    else:
        return 220

#size('барбос_S', G)

def word(G):
    for word in G.nodes:
        li = []
        li.append(i)
    return word, li

def paint(G, color, size, li):
    style.use('ggplot') 
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist = li,
                           node_color = color(word, G),
                           node_size = size(word, deg(G)))

def main():
    a, nodes_list, gra, words, G = inp_W()
    while words != '0_S':
        if a == '1':
            sosedi(nodes_list, G)
            #print('узлы', G.nodes())
            #print('ребра', G.edges())
            deg == deg(G)
            clos == clos(G)
            bet == bet(G)
            eig == eig(G)
            dia(G)
            a1, a2, a3 = nodecolor(G)
            style.use('ggplot') 
            pos=nx.spring_layout(G)
            for i in G.nodes:
                #print('i', i)
                li = []
                li.append(i)
                nx.draw_networkx_nodes(G, pos, nodelist= li,
                                       node_color=color(i, G),
                                       node_size=size(i, G))
            nx.draw_networkx_edges(G, pos, edge_color='yellow')
            nx.draw_networkx_labels(G, pos,  font_size=15,
                                    font_family='Arial')
            plt.axis('off')
            print ('параметры визуализации:')
            print (' цвет узла показывает к какому сообществу относится слово')
            print (' размер узла показывает насколько большой показатель degree_centrality')
            print ('я строила граф для слова собака. граф разбит на сообщества по следующему принципу:')
            print ('синим цветом - выделены "домашние животные, красным - дикие, а желтым - породы собак"')
            print('число узлов: ', G.number_of_nodes())
            print('число ребер: ', G.number_of_edges())
            plt.show()

            #list1, list2, list3 = node_list           
            #print(list1, list2, list3)


            a, nodes_list, gra, words, G = inp_W()
        elif a == '2':
            print('try again')
            a, nodes_list, gra, words, G = inp_W()


main()


