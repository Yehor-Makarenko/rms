import os
os.environ['TCL_LIBRARY'] = r"C:\Users\makye\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\makye\AppData\Local\Programs\Python\Python313\tcl\tk8.6"
import numpy as np
import cv2
import pywt
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from PIL import Image
from encode_decode import encode_to_binary, decode_from_binary
import pickle

img = cv2.imread('lena_gray.bmp', cv2.IMREAD_GRAYSCALE)

height, width = img.shape

def dct_compress(image, block_size=8):
    height, width = image.shape
    compressed_image = np.zeros_like(image, dtype=float)
    
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = image[i:i+block_size, j:j+block_size]
            
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            
            compressed_image[i:i+block_size, j:j+block_size] = dct_block

    return compressed_image

def dct_reconstruct(compressed_image, block_size=8):
    height, width = compressed_image.shape
    reconstructed = np.zeros_like(compressed_image)
    
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = compressed_image[i:i+block_size, j:j+block_size]
            
            idct_block = idct(idct(block.T, norm='ortho').T, norm='ortho')
            
            reconstructed[i:i+block_size, j:j+block_size] = idct_block

    return reconstructed

def dwt_compress(img, wavelet='haar'):
    coeffs = pywt.dwt2(img, wavelet)
    cA, (cH, cV, cD) = coeffs
    coeff_matrix = np.block([[cA, cH], [cV, cD]])
    
    return coeff_matrix

def dwt_reconstruct(coeffs, wavelet='haar'):
    cA = coeffs[:256, :256]
    cH = coeffs[:256, 256:]
    cV = coeffs[256:, :256]
    cD = coeffs[256:, 256:]
    return pywt.idwt2((cA, (cH, cV, cD)), wavelet)

def psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return 100
    return 10 * np.log10((255 ** 2) / mse)

compressed_dct = dct_compress(img)
encoded = encode_to_binary(compressed_dct, "test.dctimg", 30)
decoded = decode_from_binary("test.dctimg")

reconstructed_dct = dct_reconstruct(decoded)
reconstructed_dct_uint8 = np.round(reconstructed_dct).astype(np.uint8)

compressed_dwt = dwt_compress(img)
encoded = encode_to_binary(compressed_dwt, "test.dwtimg", 30)
decoded = decode_from_binary("test.dwtimg")

reconstructed_dwt = dwt_reconstruct(decoded)
reconstructed_dwt_uint8 = np.round(reconstructed_dwt).astype(np.uint8)

dct_psnr = psnr(img, reconstructed_dct_uint8)
dwt_psnr = psnr(img, reconstructed_dwt_uint8)

print(f"PSNR для DCT: {dct_psnr} dB")
print(f"PSNR для DWT: {dwt_psnr} dB")

Image.fromarray(reconstructed_dct_uint8).save('dct_result.bmp')
Image.fromarray(reconstructed_dwt_uint8).save('wavelet_result.bmp')

plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title("Оригінал")

plt.subplot(1, 3, 2)
plt.imshow(reconstructed_dct_uint8, cmap='gray')
plt.title("Відновлене DCT")

plt.subplot(1, 3, 3)
plt.imshow(reconstructed_dwt_uint8, cmap='gray')
plt.title("Відновлене DWT")

plt.show()
