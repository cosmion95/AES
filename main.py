import sbox_tables
import multiplication_tables

# plainText = "NU RUPETI LEMNUL"
# plainTextKey = "ATUNCI POTI FUGI"

plainText = "AM VAZUT DOI CAI"
plainTextKey = "NU CRED CA VEDEM"

keys = []
cipherText = []
plainTextHex = []

roundConstants = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

mixColMatrix = [["0x02", "0x03", "0x01", "0x01"],
                ["0x01", "0x02", "0x03", "0x01"],
                ["0x01", "0x01", "0x02", "0x03"],
                ["0x03", "0x01", "0x01", "0x02"]
                ]


#break key into 4 byte long words
byteCounter = 1
letters = []
for ch in plainTextKey:
    letters.append(hex(ord(ch)))
    if byteCounter%4 == 0:
        keys.append(letters)
        letters = []
    byteCounter += 1

#break plain text into 4 byte long words
byteCounter = 1
letters = []
for ch in plainText:
    letters.append(hex(ord(ch)))
    if byteCounter%4 == 0:
        cipherText.append(letters)
        plainTextHex.append(letters)
        letters = []
    byteCounter += 1

def rotateLeft(word, rotations):
    newWord = word.copy()
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
        newLetter = hex(sbox_tables.sbox[int(letter, 16)])
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
    return newWord

def xorWords(word1, word2):
    newWord = []
    for i in range(4):
        newWord.append(hex(int(word1[i], 16) ^ int(word2[i], 16)))
    return newWord

def getRoundKey(r, wordCounter):
    newWord = []
    if wordCounter%4 == 0:
        #use formula w(r) XOR g(w(r+3))
        wr = keys[wordCounter-4]
        gw = g(keys[wordCounter-1], r)
        for i in range(4):
            newWord.append(hex(int(wr[i], 16) ^ int(gw[i], 16)))
    else:
        for i in range(4):
            newWord.append(hex(int(keys[wordCounter-1][i], 16) ^ int(keys[wordCounter-4][i], 16)))
    keys.append(newWord)

def getRoundKeys(round):
    roundKeys = []
    currentRound = 0
    for i in range(44):
        roundKeys.append(keys[i])
        if (i+1)%4 == 0:
            if currentRound == round:
                return roundKeys
            currentRound += 1
            roundKeys = []
    return roundKeys

def addRoundKey(cipher, round):
    roundKeys = getRoundKeys(round)
    newCipher = []
    for i in range(4):
        newCipher.append(xorWords(cipher[i], roundKeys[i]))
    print("  4. Add round key")
    print("    Cipher: " + str(cipher))
    print("    Keys:   " + str(roundKeys))
    print("    Result: " + str(newCipher))
    return newCipher

def shiftRow(cipher, rowNumber, moves):
    tempVals = []
    newCipher = cipher
    for i in range(4):
        if i-moves < 0:
            tempVals.append((newCipher[i][rowNumber], i))
        else:
            newCipher[i-moves][rowNumber] = newCipher[i][rowNumber]
    for temp in tempVals:
        destination = temp[1] - moves + 4
        newCipher[destination][rowNumber] = temp[0]
    return newCipher

def shiftRows(cipher):
    newCipher = shiftRow(cipher, 1, 1)
    newCipher = shiftRow(newCipher, 2, 2)
    newCipher = shiftRow(newCipher, 3, 3)
    return newCipher

def multiplication(word1, word2):
    newWord = []
    for i in range(4):
        if int(word1[i], 16) == 1:
            newWord.append(word2[i])
        elif int(word2[i], 16) == 1:
            newWord.append(word1[i])
        elif int(word1[i], 16) == 0:
            newWord.append(word1[i])
        else:
            l1 = multiplication_tables.l[int(word1[i], 16)]
            l2 = multiplication_tables.l[int(word2[i], 16)]
            letter = l1 + l2
            if letter > 0xff:
                letter -= 0xff
            newWord.append(hex(multiplication_tables.e[letter]))
    return newWord

def xorWord(word):
    for i in range(4):
        if i == 0:
            letter = int(word[i], 16)
        else:
            letter = letter ^ int(word[i], 16)
    return hex(letter)

def mixColumns(cipher):
    newCipher = []
    for j in range(4):
        newWord = []
        for i in range(4):
            newWord.append(xorWord(multiplication(cipher[j], mixColMatrix[i])))
        newCipher.append(newWord)
    return newCipher

def encrypt(cipher, round):
    print("Round " + str(round))
    if round == 0:
        cipher = addRoundKey(cipher, round)
        return cipher
    else:
        # sub bytes
        newCipher = []
        for i in range(4):
            newCipher.append(subBytes(cipher[i]))
        print("  1. Sub bytes")
        print("    Cipher: " + str(cipher))
        print("    Result: " + str(newCipher))
        cipher = newCipher
        # shift rows
        print("  2. Shift rows")
        print("    Cipher: " + str(cipher))
        cipher = shiftRows(cipher)
        print("    Result: " + str(cipher))
        #mix columns
        if round != 10:
            print("  2. Mix columns")
            print("    Cipher: " + str(cipher))
            print("    Matrix: " + str(mixColMatrix))
            cipher = mixColumns(cipher)
            print("    Result: " + str(cipher))
        #add round key
        cipher = addRoundKey(cipher, round)
        return cipher


wordCounter = 4
for r in range(10):
    for w in range(4):
        getRoundKey(r, wordCounter)
        wordCounter += 1

print("\nPlain text: " + plainText)
print("Master key: " + plainTextKey)

print("Calculated round keys:")
counter = 0
for word in keys:
    print("    Word " + str(counter) + ".: " + str(word))
    counter += 1

print("\nStarting encryption...\n")

for i in range(11):
    cipherText = encrypt(cipherText, i)

finalCipher = ""
for word in cipherText:
    for letter in word:
        finalCipher += chr(int(letter, 16))

print("\nEncryption finished.\n")
print("Encrypted text: " + str(cipherText))




