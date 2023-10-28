# Exercise 5

def run_length_encode(data):
    encoded_data = bytearray()
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append(count)
            encoded_data.append(data[i - 1])
            count = 1

    encoded_data.append(count)
    encoded_data.append(data[-1])

    return bytes(encoded_data)


def run_length_decode(encoded_data):
    decoded_data = bytearray()
    i = 0

    while i < len(encoded_data):
        count = encoded_data[i]
        value = encoded_data[i + 1]
        decoded_data.extend([value] * count)
        i += 2

    return bytes(decoded_data)


# Example usage:
original_data = bytes([1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4])
encoded_data = run_length_encode(original_data)
decoded_data = run_length_decode(encoded_data)

print("Original Data:", original_data)
print("Encoded Data:", encoded_data)
print("Decoded Data:", decoded_data)

"The printed output is the following" \
"Original Data: b'\x01\x01\x01\x02\x02\x03\x03\x03\x03\x04\x04'" \
"Encoded Data: b'\x03\x01\x02\x02\x04\x03\x02\x04'" \
"Decoded Data: b'\x01\x01\x01\x02\x02\x03\x03\x03\x03\x04\x04'" \
"" \
"We can see how the encoded data represents first the number of" \
"equal bits that occur in succession (i.e 3 time x01 at the start" \
"and the decoded sequence is equal to the original one"
