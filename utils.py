import numpy as np
from itertools import product


def generate_strings(charset, length):
    return np.array([list(comb) for comb in product(charset, repeat=length)])


def generate_trivial_code(joker, length, score):
    jokers = generate_strings(charset=[joker], length=length)
    zeros = [np.zeros(length, dtype=int) for i in range(score - 1)]
    return np.vstack([jokers] + zeros)


def distance(string1, string2):
    return sum(
        char1 != char2 and 
        char1 in (1, 2) and
        char2 in (1, 2)
        for char1, char2 in zip(string1, string2))


def k_neighborly(string1, string2, k):
    return True if 0 <= distance(string1, string2) <= k else False


def replace_joker(string, index):
    string1 = [1 if i == index else value for i, value in enumerate(string)]
    string2 = [2 if i == index else value for i, value in enumerate(string)]
    return string1, string2


def remove_string(code, string):
    return np.delete(
        code,
        np.where((code == string).all(axis=1))[0][0],
        axis=0)