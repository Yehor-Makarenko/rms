import numpy as np
import struct

def quantize(matrix, step=10):
    return np.floor((matrix + 256) / step).astype(np.uint16)

def dequantize(matrix, step=10):
    return (matrix.astype(np.float32) * step) - 256

def zigzag(matrix):
    rows, cols = matrix.shape
    zigzagged = []
    for sum_idx in range(rows + cols - 1):
        if sum_idx % 2 == 0:
            row = min(sum_idx, rows - 1)
            col = sum_idx - row
            while row >= 0 and col < cols:
                zigzagged.append(matrix[row, col])
                row -= 1
                col += 1
        else:
            col = min(sum_idx, cols - 1)
            row = sum_idx - col
            while col >= 0 and row < rows:
                zigzagged.append(matrix[row, col])
                row += 1
                col -= 1
    return np.array(zigzagged)

def inverse_zigzag(zigzagged, shape):
    rows, cols = shape
    matrix = np.zeros((rows, cols), dtype=np.uint16)
    idx = 0
    for sum_idx in range(rows + cols - 1):
        if sum_idx % 2 == 0:
            row = min(sum_idx, rows - 1)
            col = sum_idx - row
            while row >= 0 and col < cols:
                matrix[row, col] = zigzagged[idx]
                idx += 1
                row -= 1
                col += 1
        else:
            col = min(sum_idx, cols - 1)
            row = sum_idx - col
            while col >= 0 and row < rows:
                matrix[row, col] = zigzagged[idx]
                idx += 1
                row += 1
                col -= 1
    return matrix

def rle_encode(data):    
    encoded = []
    current_value = data[0]
    count = 1
    for i in range(1, len(data)):
        if data[i] == current_value:
            count += 1
        else:
            encoded.append((current_value, count))
            current_value = data[i]
            count = 1
    encoded.append((current_value, count))
    return encoded

def rle_decode(encoded):    
    flat = []
    for value, count in encoded:
        flat.extend([value] * count)
    return np.array(flat, dtype=np.uint16)

def encode_to_binary(matrix, file_path, quant_step=10):
    quantized = quantize(matrix, quant_step)
    zigzagged = zigzag(quantized)
    encoded_rle = rle_encode(zigzagged)

    with open(file_path, 'wb') as f:        
        f.write(struct.pack('ii', *quantized.shape))
        
        f.write(struct.pack('f', quant_step))
        
        for value, count in encoded_rle:
            f.write(struct.pack('HH', value, count))

def decode_from_binary(file_path):    
    with open(file_path, 'rb') as f:        
        rows, cols = struct.unpack('ii', f.read(8))
        
        quant_step = struct.unpack('f', f.read(4))[0]
        
        encoded_rle = []
        while True:
            data = f.read(4)
            if not data:
                break
            value, count = struct.unpack('HH', data)
            encoded_rle.append((value, count))
        
        zigzagged = rle_decode(encoded_rle)
        quantized = inverse_zigzag(zigzagged, (rows, cols))

    return dequantize(quantized, quant_step)
