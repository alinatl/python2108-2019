import urllib.request
import json

#скачиваем что надо на комп
def d_comp():
    login_list = ['alinatl', 'elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'gricolamz', 'lehkost', 'kylepjohnson', 'mikekestemont',
'demidovakatya', 'shwars', 'JelteF', 'timgraham', 'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
    str_login = ', '.join(login_list)
    login = ''
    while login not in login_list:
        login = input (str_login + '\n введите имя пользователя из списка: ')
        login = login.lower()
        if login not in login_list:
            print('вы ввели не то что нужно. попробуйте еще раз.')
    user = login
    token = "" # тут ваш токен
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)   
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')  
    data = json.loads(text)
    return data, user

# Распечатать список языков (language) выбранного пользователя
# и количество репозиториев, в котором они используются
def lang(data):
    list_a = []
    vse_lang = []
    print('\n выбраный юзер пользуется языками: ')
    for i in data:
        a = i['language']
        #print(a)
        if a == None:
            continue
        vse_lang.append(a)
        #print(vse_lang)
        if a not in list_a:
            list_a.append(a)
    str_lang = ', '.join(list_a)
    print(str_lang, '\n')
    c_lang_max = 0
    for word in list_a:
        u = vse_lang.count(word)
        print('язык ', word, 'количество репов в которых используется ', u)
    print('\n')

# распечатать список его репозиториев (name) и их описания (description)
def name(name):
    print('вот список его репозиториев с описанием:')
    for i in data:
        a = i['name']
        b = i['description']
        print(a, ' : ', b)

# считает кол-во репов у пользователя, и выдает пользователя с максимум
def count_rep(login_list):
    c_rep_max = 0
    login_max = ''
    for login in login_list:
        user = login
        token = "18ea6ae62c2666e9d72406bf5219a12194fe62f2" # тут ваш токен, скопированный с гитхаба
        url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)   
        response = urllib.request.urlopen(url) 
        text = response.read().decode('utf-8')  
        data = json.loads(text)
        c_rep = len(data)
        if c_rep > c_rep_max:
            c_rep_max = c_rep
            login_max = login
    print('у пользователя ', login_max, 'максимальное количество репов: ', c_rep_max, '\n')

# больше всего фоловеров
def fol_max(login_list):
    c_fol_max = 0
    login_max = ''
    for login in login_list:
        user = login
        token = "18ea6ae62c2666e9d72406bf5219a12194fe62f2" # тут ваш токен, скопированный с гитхаба
        url = url = f'https://api.github.com/users/%s/followers?access_token=%s' % (user, token)    
        response = urllib.request.urlopen(url) 
        text = response.read().decode('utf-8')  
        data = json.loads(text)
        c_fol = len(data)
        if c_fol > c_fol_max:
            c_fol_max = c_fol
            login_max = login
    print('у пользователя ', login_max, 'максимальное количество фолловеров: ', c_fol_max, '\n')

#самый популярный язык
def count_max_lang(login_list, lang):
    c_lang_max = 0
    login_max = ''
    vse_lang = []
    for login in login_list:
        user = login
        token = "18ea6ae62c2666e9d72406bf5219a12194fe62f2" # тут ваш токен, скопированный с гитхаба
        url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token)   
        response = urllib.request.urlopen(url) 
        text = response.read().decode('utf-8')  
        data = json.loads(text)
        for i in data:
            a = i['language']
            if a == None:
                continue
            vse_lang.append(a)
    qq = 0
    wordq = ''
    for word in vse_lang:
        q = vse_lang.count(word)
        if q > qq:
            wordq = word
            qq = q
    print ('самый популярный язык среди пользователей списка: ', wordq, qq, 'вхождений \n')


login_list = ['alinatl', 'elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'gricolamz', 'lehkost', 'kylepjohnson', 'mikekestemont',
'demidovakatya', 'shwars', 'JelteF', 'timgraham', 'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum']
data, user = d_comp()
print('\n вы выбрали пользователя:', user, '\n')
name = name(user)
lang = lang(data)
count_max_lang(login_list, lang)
count_rep(login_list)
fol = fol_max(login_list)


