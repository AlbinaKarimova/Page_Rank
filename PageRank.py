import pandas as pd
import numpy as np
from string import ascii_uppercase

#!!!!!! НАДО СКОПИРОВАТЬ ЗАНОВО СВОЙ ВАРИАНТ ФАЙЛА И СДЕЛАТЬ РАЗДЕЛЕНИЕ СТРОК
file = "links.csv"
data = pd.read_csv(file)
S_from = data['from']
S_to = data['to']

gamma = 0.02

L = {} # множество сайтов, на которых есть ссылки на сайт S_i
for _, row in data.iterrows():
    L.setdefault(row['from'], set()) # Добавляем ключ в словарь, если он еще не существует
                                     # 2-параметр: в качестве значения будет множество
    L[row['from']].add(row['to'])

count_L = {key: len(value) for key, value in L.items()} # Количество элементов для каждого ключа в множестве L(S_i)

# Индикаторная функция
def indicator(j, L_S_i):
    return 1 if j in L_S_i else 0

# Вывод словаря
def show_dict(p):
    for keys, values in p.items():
        print(keys)
        print(values)

# Считаем по формуле элементы для матрицы перехода (Матрица пока - это словарь)
def find_P_2(p):
    N = len(L)
    i = 0
    for let_1 in ascii_uppercase:
        if let_1 == 'L':
            break
        else:
            keys = L.keys()
            L_S_i = L[list(keys)[i]]
            for let_2 in list(keys):
                p[let_1].append((1 - N * gamma) * indicator(let_2, L_S_i) / count_L[f'{list(keys)[i]}'] + gamma)
        i += 1
    return p

# Создаем матрицу перехода пока в виде словаря
P = {}
for let in ascii_uppercase:
    if let == 'L':
        break
    else:
        P[let] = []

# Преобразуем словарь матрицыц перехода в обычную матрицу для дальнейшей работы с ней
def convert_to_arr(p):
    n = len(p)
    P = [0] * n

    for i in range(n):
        P[i] = [0] * n

    for i in range(n):
        str = list(p.values())[i]

        for j in range(len(str)):
            P[i][j] = str[j]

    return P

# Вывод матрицы
def show_arr(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            print(arr[i][j], end=" ")
        print()

P_dict = find_P_2(P)
P_matr = convert_to_arr(P_dict)
#show_arr(P) # ОКОНЧАТЕЛЬНЫЙ ВИД МАТРИЦЫ ПЕРЕХОДА

# Умножение матриц
for i in range(10):
    P_matr = np.dot(P_matr, P_matr)

l = P_matr[0] # Предельное распределение
print()
print(f"Предельное распределение: {l}")

links = list(P_dict.keys())
dict_links = {}
for i in range(len(l)):
    dict_links[links[i]] = round(l[i], 9)
    print(f"Сайт {links[i]}, метрики их 'важности': {round(l[i], 9)}")

dict_links = dict(sorted(dict_links.items(), key=lambda x:x[1], reverse=True))
print(f"Отсортрованные сайты в порядке убывания их 'важности': {list(dict_links.keys())}")
