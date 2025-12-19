from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Fungsi untuk dekripsi pesan
def decrypt_message_(encrypted_data, key, iv):
    # Menyiapkan cipher AES dengan mode CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Dekripsi data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    return decrypted_data.decode()
