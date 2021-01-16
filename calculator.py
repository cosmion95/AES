import sbox_tables
import multiplication_tables

roundConstants = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def rotateLeft(word, rotations):
    newWord = word
    for i in range(rotations):
        firstLetter = word[0]
        counter = 0
        for letter in word:
            if counter != 0:
                newWord[counter-1] = letter
            counter += 1
        newWord[3] = firstLetter
    return newWord

def subBytes(word):
    newWord = []
    for letter in word:
        newLetter = hex(sbox_tables.sbox[letter])
        newWord.append(newLetter)
    return newWord

def roundConstant(word, r):
    newWord = word
    newWord[0] = hex(int(word[0], 16) ^ roundConstants[r])
    return newWord


def g(word, r):
    newWord = rotateLeft(word, 1)
    newWord = subBytes(newWord)
    newWord = roundConstant(newWord, r)
    print(newWord)


def xorWords(word1, word2):
    newWord = []
    for i in range(4):
        newWord.append(hex(word1[i] ^ word2[i]))
    print(newWord)

def xorWord(word):
    for i in range(4):
        if i == 0:
            letter = int(word[i], 16)
        else:
            letter = letter ^ int(word[i], 16)
    return hex(letter)

def multiplication(word1, word2):
    newWord = []
    for i in range(4):
        if word1[i] == 1:
            newWord.append(hex(word2[i]))
        elif word2[i] == 1:
            newWord.append(hex(word1[i]))
        else:
            l1 = multiplication_tables.l[word1[i]]
            l2 = multiplication_tables.l[word2[i]]
            letter = l1 + l2
            if letter > 0xff:
                letter -= 0xff
            newWord.append(hex(multiplication_tables.e[letter]))
    return newWord


gw = "6215bf5b"

gword = []


lg = ""
for i in range(1, 9):
    lg += gw[i-1]
    if i%2 == 0:
        gword.append(int(lg, 16))
        lg = ""




w1 = "76d46b6b"

w2 = "01020301"

word1 = []
word2 = []

l1 = ""
l2 = ""
for i in range(1, 9):
    l1 += w1[i-1]
    l2 += w2[i-1]
    if i%2 == 0:
        word1.append(int(l1, 16))
        word2.append(int(l2, 16))
        l1 = ""
        l2 = ""


#xorWords(word1, word2)
#g(gword, 2)


#print(subBytes(word1))

#print(multiplication(word1, word2))
print(xorWord(multiplication(word1, word2)))