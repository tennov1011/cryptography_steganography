from aes_cbc_encryption import data_to_bitstream

# Fungsi untuk menghitung Avalanche Effect (Difusi)
def calculate_avalanche_effect(ciphertext_a, ciphertext_b):
    """
    Mengukur avalanche effect dengan menghitung persentase bit yang berbeda
    antara dua ciphertext yang dihasilkan dari plaintext yang hanya berbeda 1 bit.
    
    Avalanche Effect (%) = (Jumlah bit yang berbeda) / (Total bit) × 100%
    """
    # Konversi ciphertext ke bitstream
    bitstream_a = data_to_bitstream(ciphertext_a)
    bitstream_b = data_to_bitstream(ciphertext_b)
    
    # Pastikan panjang bitstream sama
    if len(bitstream_a) != len(bitstream_b):
        raise ValueError("Panjang ciphertext harus sama")
    
    # Hitung jumlah bit yang berbeda (operasi XOR manual)
    different_bits = sum(bit_a != bit_b for bit_a, bit_b in zip(bitstream_a, bitstream_b))
    
    # Hitung total bit
    total_bits = len(bitstream_a)
    
    # Hitung persentase avalanche effect
    avalanche_percentage = (different_bits / total_bits) * 100
    
    return different_bits, total_bits, avalanche_percentage

# Fungsi untuk mengukur konfusi (melalui distribusi karakter)
def calculate_confusion(ciphertext):
    """
    Mengukur konfusi dengan menganalisis distribusi bit pada ciphertext.
    Konfusi yang baik ditunjukkan dengan distribusi bit '0' dan '1' yang seimbang (~50%).
    """
    bitstream = data_to_bitstream(ciphertext)
    
    # Hitung jumlah bit '1' dan '0'
    ones_count = bitstream.count('1')
    zeros_count = bitstream.count('0')
    total_bits = len(bitstream)
    
    # Hitung persentase
    ones_percentage = (ones_count / total_bits) * 100
    zeros_percentage = (zeros_count / total_bits) * 100
    
    # Hitung deviasi dari distribusi ideal (50%-50%)
    balance_score = 100 - abs(50 - ones_percentage)
    
    return ones_count, zeros_count, ones_percentage, zeros_percentage, balance_score
