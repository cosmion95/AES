import main
import sbox_tables

invMixColMatrix = [
                    ["0x0e", "0x0b", "0x0d", "0x09"],
                    ["0x09", "0x0e", "0x0b", "0x0d"],
                    ["0x0d", "0x09", "0x0e", "0x0b"],
                    ["0x0b", "0x0d", "0x09", "0x0e"]
                ]

def inverseSubBytes(word):
    newWord = []
    for letter in word:
        newLetter = hex(sbox_tables.sboxInv[int(letter, 16)])
        newWord.append(newLetter)
    return newWord

def inverseShiftRow(cipher, rowNumber, moves):
    tempVals = []
    newCipher = cipher
    for i in range(3, -1, -1):
        if i+moves > 3:
            tempVals.append((newCipher[i][rowNumber], i))
        else:
            newCipher[i+moves][rowNumber] = newCipher[i][rowNumber]
    for temp in tempVals:
        destination = temp[1] + moves - 4
        newCipher[destination][rowNumber] = temp[0]
    return newCipher

def inverseShiftRows(cipher):
    newCipher = inverseShiftRow(cipher, 1, 1)
    newCipher = inverseShiftRow(newCipher, 2, 2)
    newCipher = inverseShiftRow(newCipher, 3, 3)
    return newCipher

def inverseMixColumns(cipher):
    newCipher = []
    for j in range(4):
        newWord = []
        for i in range(4):
            newWord.append(main.xorWord(main.multiplication(cipher[j], invMixColMatrix[i])))
        newCipher.append(newWord)
    return newCipher

def decrypt(cipher, round):
    print("Round " + str(round))
    if round == 10:
        cipher = main.addRoundKey(cipher, round)
        return cipher
    else:
        # inverse shift rows
        print("  1. Inverse shift rows")
        print("    Cipher: " + str(cipher))
        cipher = inverseShiftRows(cipher)
        print("    Result: " + str(cipher))
        # sub bytes
        newCipher = []
        for i in range(4):
            newCipher.append(inverseSubBytes(cipher[i]))
        print("  2. Inverse sub bytes")
        print("    Cipher: " + str(cipher))
        print("    Result: " + str(newCipher))
        cipher = newCipher
        # add round key
        cipher = main.addRoundKey(cipher, round)
        #mix columns
        if round != 0:
            print("  4. Inverse mix columns")
            print("    Cipher: " + str(cipher))
            print("    Matrix: " + str(invMixColMatrix))
            cipher = inverseMixColumns(cipher)
            print("    Result: " + str(cipher))
        return cipher

decryptedCipher = main.cipherText

print("\n\nStarting decryption...\n")
for i in range(10, -1, -1):
    decryptedCipher = decrypt(decryptedCipher, i)

decryptedMessage = ""
success = True
for i in range(4):
    for j in range(4):
        if decryptedCipher[i][j] != main.plainTextHex[i][j]:
            success = False
        decryptedMessage += chr(int(decryptedCipher[i][j], 16))

print("\nDecryption finished.\n")
if success:
    print("Decryption successful.")
else:
    print("Decryption was unsuccessful.")

print("\nResults:\n")
print("    Plain text: " + main.plainText)
print("    Master key: " + main.plainTextKey)
print("\n    Plain HEX text:     " + str(main.plainTextHex))

print("\n    Encrypted HEX text: " + str(main.cipherText))
print("    Encrypted text: " + main.finalCipher)

print("\n    Decrypted HEX text:   " + str(decryptedCipher))
print("    Decrypted plain text: " + decryptedMessage)

