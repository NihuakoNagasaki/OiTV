import pymorphy2

word = '3,5'

if len(word) > 6:
    word=word[0:-2]
elif len(word) <= 6 and len(word) > 3:

    word=word[0:-1]

print(word)