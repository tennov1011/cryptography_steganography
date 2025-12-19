from Crypto.Random import get_random_bytes
from aes_cbc_encryption import encrypt_message_, binary_to_printable_string, data_to_bitstream, flip_one_bit
from aes_cbc_decryption import decrypt_message_
from avalanche_effect import calculate_avalanche_effect, calculate_confusion

# Fungsi utama untuk demonstrasi enkripsi dan dekripsi
def main():
    # Kunci AES 128-bit (16 byte) dan IV 128-bit (16 byte)
    key = get_random_bytes(16)  # Kunci acak untuk AES
    iv = get_random_bytes(16)   # IV acak untuk AES
    
    # Meminta input plaintext dari pengguna
    plain_text = input("Masukkan pesan yang ingin dienkripsi: ")
    
    print("\nOriginal message:", plain_text)
    
    # Enkripsi pesan
    encrypted_data = encrypt_message_(plain_text, key, iv)
    print("\nEncrypted message (binary):", encrypted_data)
    
    print("\nInitial Vector:", iv)
    
    # Mengonversi ciphertext biner ke string printable
    encrypted_string = binary_to_printable_string(encrypted_data)
    print("\nEncrypted message (string):", encrypted_string)
    print("(Panjang ciphertext string: {} byte)".format(len(encrypted_string)))
    
    # Dekripsi pesan
    decrypted_message = decrypt_message_(encrypted_data, key, iv)
    print("\nDecrypted message:", decrypted_message)
    
    # ==================== PENGUKURAN DIFUSI (AVALANCHE EFFECT) ====================
    print("\n" + "="*70)
    print("PENGUKURAN DIFUSI - AVALANCHE EFFECT")
    print("="*70)
    
    # Buat plaintext kedua dengan 1 bit berbeda
    plain_text_modified = flip_one_bit(plain_text)
    
    print(f"\nPlaintext A (Original): {plain_text}")
    print(f"Plaintext B (1 bit diubah): {plain_text_modified}")
    
    # Enkripsi plaintext yang telah dimodifikasi dengan key dan IV yang sama
    encrypted_data_modified = encrypt_message_(plain_text_modified, key, iv)
    
    # Tampilkan ciphertext dalam bitstream
    bitstream_original = data_to_bitstream(encrypted_data)
    bitstream_modified = data_to_bitstream(encrypted_data_modified)
    iv_bitstream = data_to_bitstream(iv)
    
    print(f"\nCiphertext A (bitstream): {bitstream_original[:64]}... (Total: {len(bitstream_original)} bits)")
    print(f"Ciphertext B (bitstream): {bitstream_modified[:64]}... (Total: {len(bitstream_modified)} bits)")
    print(f"Initialization Vector (IV) (bitstream): {iv_bitstream[:64]}... (Total: {len(iv_bitstream)} bits)")
    
    # Hitung Avalanche Effect
    diff_bits, total_bits, avalanche_percent = calculate_avalanche_effect(encrypted_data, encrypted_data_modified)
    
    print(f"\nHasil Pengukuran Avalanche Effect:")
    print(f"  - Jumlah bit yang berbeda: {diff_bits}")
    print(f"  - Total bit pada ciphertext: {total_bits}")
    print(f"  - Avalanche Effect: {avalanche_percent:.2f}%")
    
    # Evaluasi hasil
    if avalanche_percent >= 45 and avalanche_percent <= 55:
        print(f"  - Evaluasi: SANGAT BAIK (mendekati ideal 50%)")
    elif avalanche_percent >= 40 and avalanche_percent <= 60:
        print(f"  - Evaluasi: BAIK (distribusi difusi memadai)")
    else:
        print(f"  - Evaluasi: PERLU PERBAIKAN (kurang optimal)")
    
    # ==================== PENGUKURAN KONFUSI ====================
    print("\n" + "="*70)
    print("PENGUKURAN KONFUSI - DISTRIBUSI BIT")
    print("="*70)
    
    # Hitung konfusi pada ciphertext original
    ones, zeros, ones_pct, zeros_pct, balance = calculate_confusion(encrypted_data)
    
    print(f"\nAnalisis Distribusi Bit pada Ciphertext:")
    print(f"  - Jumlah bit '1': {ones} ({ones_pct:.2f}%)")
    print(f"  - Jumlah bit '0': {zeros} ({zeros_pct:.2f}%)")
    print(f"  - Balance Score: {balance:.2f}% (100% = distribusi sempurna)")
    
    # Evaluasi konfusi
    if balance >= 95:
        print(f"  - Evaluasi: SANGAT BAIK (distribusi sangat seimbang)")
    elif balance >= 90:
        print(f"  - Evaluasi: BAIK (distribusi seimbang)")
    else:
        print(f"  - Evaluasi: CUKUP (masih dalam batas toleransi)")
    
    print("\n" + "="*70)
    
    # Menampilkan bitstream dari ciphertext dan IV
    encrypted_bitstream = data_to_bitstream(encrypted_data)
    iv_bitstream = data_to_bitstream(iv)
    
    print("\nCiphertext as bitstream:", len(encrypted_bitstream))
    print("Initialization Vector (IV) as bitstream:", len(iv_bitstream))
    
    # Menghitung total bitstream
    total_bitstream = len(encrypted_bitstream) + len(iv_bitstream)
    print("\nTotal bitstream (ciphertext + IV):", total_bitstream, "bits")
    
    print("\n" + "="*70)
    print("RINGKASAN UKURAN DATA")
    print("="*70)
    print("Panjang plaintext:           {} karakter ({} byte = {} bit)".format(
        len(plain_text), len(plain_text), len(plain_text) * 8))
    print("Panjang ciphertext (biner):  {} byte = {} bit".format(
        len(encrypted_data), len(encrypted_data) * 8))
    print("Panjang ciphertext (string): {} karakter ({} byte)".format(
        len(encrypted_string), len(encrypted_string)))
    print("Overhead padding:            {} byte".format(
        len(encrypted_data) - len(plain_text)))
    print("="*70)

if __name__ == "__main__":
    main()
