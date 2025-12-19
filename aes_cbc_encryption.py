from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import string

# Fungsi untuk enkripsi pesan
def encrypt_message_(plain_text, key, iv):
    # Menyiapkan cipher AES dengan mode CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Menambahkan padding ke pesan agar panjangnya kelipatan 16 byte
    padded_data = pad(plain_text.encode(), AES.block_size)
    
    # Enkripsi data
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data  # Mengembalikan ciphertext dalam bentuk biner

# Fungsi untuk mengonversi ciphertext biner menjadi string dengan karakter printable
def binary_to_printable_string(binary_data):
    """
    Mengonversi setiap byte dari ciphertext biner menjadi karakter printable.
    Panjang output akan sama dengan panjang ciphertext asli (termasuk padding).
    
    Args:
        binary_data: Ciphertext dalam bentuk bytes
    
    Returns:
        String dengan panjang sama dengan ciphertext (dalam byte)
    """
    printable_chars = string.ascii_letters + string.digits + string.punctuation + " "  # Karakter printable
    result = []
    
    # Memetakan setiap byte ciphertext ke karakter printable
    for byte in binary_data:
        # Memastikan byte menjadi angka dalam rentang panjang karakter printable
        mapped_char = printable_chars[byte % len(printable_chars)]
        result.append(mapped_char)
    
    # Mengembalikan string lengkap sesuai ukuran ciphertext asli
    return ''.join(result)

# Fungsi untuk mengonversi data ke representasi bitstream
def data_to_bitstream(data):
    return ''.join(format(byte, '08b') for byte in data)

# Fungsi untuk mengubah 1 bit pada plaintext (untuk pengujian difusi)
def flip_one_bit(plain_text, bit_position=None):
    """
    Mengubah satu bit pada plaintext untuk pengujian avalanche effect.
    Jika bit_position tidak ditentukan, bit terakhir akan diubah.
    """
    # Konversi plaintext ke bytes
    text_bytes = bytearray(plain_text.encode())
    
    if bit_position is None:
        # Ubah bit terakhir dari byte terakhir
        text_bytes[-1] ^= 1  # XOR dengan 1 untuk flip bit terakhir
    else:
        # Ubah bit pada posisi tertentu
        byte_index = bit_position // 8
        bit_index = bit_position % 8
        if byte_index < len(text_bytes):
            text_bytes[byte_index] ^= (1 << bit_index)
    
    return text_bytes.decode('latin-1')
