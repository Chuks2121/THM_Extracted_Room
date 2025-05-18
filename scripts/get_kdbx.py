import base64

with open('Database1337', 'r') as file:
    encoded_data = file.read()

binary_data = base64.b64decode(encoded_data)
xor_key = b'B'
decrypted_data = bytearray(len(binary_data))

for i in range(len(binary_data)):
    decrypted_data[i] = binary_data[i] ^ xor_key[i % len(xor_key)]

with open('Database1337.kdbx', 'wb') as file:
    file.write(decrypted_data)

print("Decryption completed, saved to Database1337.kdbx")