from django.shortcuts import render
from .forms import CryptoForm

alphabets = "abcdefghijklmnopqrstuvwxyz "

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
    message = message.lower()
    key = key.lower()
    split_message = [
        message[i : i + len(key)] for i in range(0, len(message), len(key))
    ]

    for word in split_message:
        i = 0
        for letter in word:
            number = (word_to_index[letter] + word_to_index[key[i]]) % len(alphabets)
            encrypted += index_to_word[number]
            i += 1

    return encrypted


def decrypt_vigenere(cipher, key):
    decrypted = ""
    cipher = cipher.lower()
    key = key.lower()
    split_encrypted = [
        cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))
    ]

    for word in split_encrypted:
        i = 0
        for letter in word:
            number = (word_to_index[letter] - word_to_index[key[i]]) % len(alphabets)
            decrypted += index_to_word[number]
            i += 1

    return decrypted

# caesar cipher
def encrypt_caesar(message, shift=3):
    cipher = ""
    message = message.lower()
    for word in message:
        number = (word_to_index[word] + shift) % len(word_to_index)
        word = index_to_word[number]
        cipher += word
    
    return cipher

def decrypt_caesar(cipher, shift=3):
    decrypted = ""
    cipher = cipher.lower()
    for word in cipher:
        number = (word_to_index[word] - shift) % len(word_to_index)
        word = index_to_word[number]
        decrypted += word
    
    return decrypted

def index(request):
    data = {}
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            message = request.POST['message'].lower()
            keyword = request.POST['key'].lower()
            key = generate_key(message, keyword)
            vigenere_encrypt_text = encrypt_vigenere(message, keyword)
            vigenere_decrypt_text = decrypt_vigenere(vigenere_encrypt_text, keyword)

            final_encrypt_text = encrypt_caesar(vigenere_encrypt_text, shift=3)
            final_decrypt_text = decrypt_caesar(final_encrypt_text, shift=3)

            data = {
                'message': message,
                'keyword': keyword,
                'key': key,
                'vigenere_encrypt_text': vigenere_encrypt_text,
                'vigenere_decrypt_text': vigenere_decrypt_text,
                'final_encrypt_text': final_encrypt_text,
                'final_decrypt_text': final_decrypt_text
            }
    else:
        form = CryptoForm()
    
    data['form'] = form
        
    return render(request, 'cryptoapp/index.html', data)
