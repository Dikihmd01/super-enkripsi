from ast import keyword
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import CryptoForm

alphabets = "ABCDEFGHIJKLMNOPQRSTU"

word_to_index = dict(zip(alphabets, range(len(alphabets))))
index_to_word = dict(zip(range(len(alphabets)), alphabets))

def generate_key(message, key):
    key  = list(key)
    if len(message) == len(key):
        return key
    else:
        for i in range(len(message) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt_vigenere(message, key):
    encrypted = ""
    message = message.upper()
    key = key.upper()
    split_message = [
        message[i : i + len(key)] for i in range(0, len(message), len(key))
    ]

    alpha_list = list(alphabets)

    for word in split_message:
        i = 0
        for letter in word:
            if letter in alpha_list:
                number = (word_to_index[letter] + word_to_index[key[i]]) % len(alphabets)
                encrypted += index_to_word[number]
                i += 1
            # else:
            #     encrypted += letter

    return encrypted


def decrypt_vigenere(cipher, key):
    decrypted = ""
    cipher = cipher.upper()
    key = key.upper()
    split_encrypted = [
        cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))
    ]
    alpha_list = list(alphabets)

    for word in split_encrypted:
        i = 0
        for letter in word:
            if letter in alpha_list:
                number = (word_to_index[letter] - word_to_index[key[i]]) % len(alphabets)
                decrypted += index_to_word[number]
                i += 1
            # else:
            #     decrypted += letter

    return decrypted

def encrypt_rail_fence(text, key):
    text = text.replace(" ", "")
    text = text.upper()
    r = [['\n' for i in range(len(text))] for j in range(key)]
    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down

        r[row][col] = text[i]
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    result = []

    for i in range(key):
        for j in range(len(text)):
            if r[i][j] != '\n':
                result.append(r[i][j])
    return("" . join(result))

def decrypt_rail_fence(cipher, key):
    r = [['\n' for i in range(len(cipher))] for j in range(key)] 
    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        r[row][col] = '*'
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if ((r[i][j] == '*') and
            (index < len(cipher))):
                r[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False
        if (r[row][col] != '*'):
            result.append(r[row][col]) 
            col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    return("".join(result))

# caesar cipher
# def encrypt_caesar(message, shift):
#     cipher = ""
#     message = message.upper()
#     for word in message:
#         if word in list(alphabets):
#             number = (word_to_index[word] + int(shift)) % len(word_to_index)
#             word = index_to_word[number]
#             cipher += word
#         else:
#             cipher += word
#     return cipher

# def decrypt_caesar(cipher, shift):
#     decrypted = ""
#     cipher = cipher.upper()
#     for word in cipher:
#         if word in list(alphabets):
#             number = (word_to_index[word] - shift) % len(word_to_index)
#             word = index_to_word[number]
#             decrypted += word
#         else:
#             decrypted += word
#     return decrypted

# def encrypt_rail_fence(message, rails):
#     message = message.upper()

def index(request):
    data = {}
    error_msg = False
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            
            message = request.POST['message'].upper().replace(" ", "")
            keyword = request.POST['key'].upper()
            key = generate_key(message, keyword)
            rails = request.POST['key_rf']
            
            if int(rails) < 2:
                rails = 2


            vigenere_encrypt_text = encrypt_vigenere(message, keyword)
            vigenere_decrypt_text = decrypt_vigenere(vigenere_encrypt_text, keyword)

            final_encrypt_text = encrypt_rail_fence(vigenere_encrypt_text, int(rails))
            final_decrypt_text1 = decrypt_rail_fence(final_encrypt_text, int(rails))
            final_decrypt_text2 = decrypt_vigenere(final_decrypt_text1, keyword)
            # form.cleaned_data()

            data = {
                'message': message,
                'keyword': keyword,
                'key': key,
                'shift': rails,
                'vigenere_encrypt_text': vigenere_encrypt_text,
                'vigenere_decrypt_text': vigenere_decrypt_text,
                'final_encrypt_text': final_encrypt_text,
                'final_decrypt_text1': final_decrypt_text1,
                'final_decrypt_text2': final_decrypt_text2,
                'error_msg': error_msg
            }
            form = CryptoForm()
    else:
        form = CryptoForm()
    
    data['form'] = form
        
    return render(request, 'cryptoapp/index.html', data)
