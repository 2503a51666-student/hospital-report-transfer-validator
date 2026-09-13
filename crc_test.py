def calculate_crc(data, generator):
    data = list(data)
    generator = list(generator)

    # Append zeros according to generator degree
    data.extend(['0'] * (len(generator) - 1))

    for i in range(len(data) - len(generator) + 1):
        if data[i] == '1':
            for j in range(len(generator)):
                data[i + j] = str(
                    int(data[i + j]) ^ int(generator[j])
                )

    # Last bits are the CRC remainder
    crc = ''.join(data[-(len(generator) - 1):])

    return crc


# Test CRC-4
data = "1101011011"
generator = "10011"

crc = calculate_crc(data, generator)

print("Dataword :", data)
print("Generator:", generator)
print("CRC-4    :", crc)
print("Codeword :", data + crc)


def verify_crc(codeword, generator):
    remainder = calculate_crc(codeword, generator)
    return remainder == "0" * (len(generator) - 1)

def text_to_binary(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

# CRC-4 Test
data = "1101011011"
generator = "10011"

crc4 = calculate_crc(data, generator)

print("----- CRC-4 -----")
print("Dataword :", data)
print("Generator:", generator)
print("CRC-4    :", crc4)
print("Codeword :", data + crc4)


# CRC-8 Test
data = "1101011011"
generator = "100000111"

crc8 = calculate_crc(data, generator)

print("\n----- CRC-8 -----")
print("Dataword :", data)
print("Generator:", generator)
print("CRC-8    :", crc8)
print("Codeword :", data + crc8)

# CRC-8 Text Test
text = "HELLO"
generator = "100000111"

binary_text = text_to_binary(text)
crc = calculate_crc(binary_text, generator)

print("\n----- CRC-8 TEXT -----")
print("Text     :", text)
print("Binary   :", binary_text)
print("CRC-8    :", crc)
print("Codeword :", binary_text + crc)


# Hospital Report File CRC Test
file_path = "synthetic_hospital_lab_report.xlsx"

with open(file_path, "rb") as file:
    file_data = file.read()

file_binary = ''.join(format(byte, '08b') for byte in file_data)

generator = "100000111"

file_crc = calculate_crc(file_binary, generator)

print("\n----- HOSPITAL REPORT CRC -----")
print("File     :", file_path)
print("File Size:", len(file_data), "bytes")
print("CRC-8    :", file_crc)


# Hospital Report Verification
received_data = file_data

received_binary = ''.join(
    format(byte, '08b') for byte in received_data
)

received_crc = calculate_crc(received_binary, generator)

print("\n----- RECEIVER VERIFICATION -----")
print("Sender CRC  :", file_crc)
print("Receiver CRC:", received_crc)

if file_crc == received_crc:
    print("Status      : VALID - No error detected")
else:
    print("Status      : CORRUPTED - Error detected")


# Simulate corruption during transfer
corrupted_data = bytearray(file_data)

# Flip one bit in the received data
corrupted_data[100] ^= 1

corrupted_binary = ''.join(
    format(byte, '08b') for byte in corrupted_data
)

corrupted_crc = calculate_crc(corrupted_binary, generator)

print("\n----- CORRUPTED REPORT TEST -----")
print("Sender CRC  :", file_crc)
print("Received CRC:", corrupted_crc)

if file_crc == corrupted_crc:
    print("Status      : VALID - No error detected")
else:
    print("Status      : CORRUPTED - Error detected")