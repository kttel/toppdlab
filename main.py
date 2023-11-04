import time
from functools import wraps

LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ',
)

ENCODE_KEY = "yelyzaveta"


def time_counter(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        start_processing = time.time()
        method(self, *method_args, **method_kwargs)
        print("Total {} processing time = {:.3f} seconds"
              .format(method.__name__, time.time() - start_processing))
    return _impl


def encode(key, message):
    encodedMessageLst = []

    for i in range(len(message)):
        letter = message[i]
        if letter in LETTERS:
            encodLetter = LETTERS.index(letter) + LETTERS.index(key[i % len(key)])
            if encodLetter > len(LETTERS) - 1: 
                encodLetter -= len(LETTERS)
            encodedMessageLst.append(LETTERS[encodLetter])
        else:
            encodedMessageLst.append(letter)

    return "".join(encodedMessageLst)


def decode(key, message):
    decodedMessageLst = []

    for i in range(len(message)):
        letter = message[i]
        if letter in LETTERS:
            decodLetter = LETTERS.index(letter) - LETTERS.index(key[i % len(key)])
            if decodLetter < 0: 
                decodLetter += len(LETTERS)
            decodedMessageLst.append(LETTERS[decodLetter])
        else:
            decodedMessageLst.append(letter)
      
    return "".join(decodedMessageLst)


class Message:
    encryption_key = ENCODE_KEY
    def __init__(self, text, encryption_key=None):
        self.text = text
        self.encryption_key = encryption_key or Message.encryption_key

    @time_counter
    def encode(self):
        self.encoded_message = encode(self.encryption_key, self.text)
        print(f"\tEncoded text:\n{self.encoded_message}")

    @time_counter
    def decode(self):
        decodedMessage = decode(self.encryption_key, self.encoded_message)
        print(f"\tDecoded text:\n{decodedMessage}")


if __name__ == '__main__':
    with open("text.txt", encoding="utf-8") as f:
        retrieved_message = f.read()

    message = Message(retrieved_message)
    message.encode()
    message.decode()
