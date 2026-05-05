# importing the essential packages

import numpy as np 
import matplotlib.pyplot as plt

sample_rate = 2.4e6  # 2.4 MSPS(Mega samples per second)
center_frequency = 1420.4e6 # 1420.4 MHz

# converting the binary file to unsigned integer8
raw_data = np.fromfile('output_21cm_may_2.dat',dtype=np.uint8)

#Converting to the float datatype and shifting the offset as SRD data is centered at 127.5 Hz
samples = (raw_data.astype(np.float32)-127.5) /127.5

# converting it into I-Phase and Quadrature (I and Q respectively) as the data is stored alternative real and imaginary value of a complex number.

i_part = samples[0::2] # assigning the even index to the real part
q_part = samples[1::2] # assigning the odd index to the imaginary part

# creating a complex number using the i and q parts
complex_data = i_part + 1j * q_part


# Now creating a time domain series data to frequency Domain Series data using the FFT  (Fast Fourier Transformation), I found out this function in the numpy library which I shall try using for computation. 
fft_result = np.fft.fft(complex_data) # this is the code that performs the FFT onto the data.
fft_freqs = np.fft.fftfreq(len(complex_data), d=1/sample_rate) # this is the frequency 

# now we are supposed to shift the 0 frequency component to the center (1420MHz)
fft_result = np.fft.fftshift(fft_result)
fft_freqs = np.fft.fftshift(fft_freqs)

# calculating the power spectral density (PSD)
psd = 10 * np.log10(np.abs(fft_result)**2)

# Plotting the FFT transformed frequency Domain Series 
#plt.plot((fft_freqs + center_frequency) / 1e6, psd)
#plt.xlabel("Frequency (Hz)")
#plt.ylabel("Power (dB)")
#plt.savefig('plot5_1',dpi=300)
#plt.show()



# Assuming 'complex_data' is your array of 20,000,000 complex samples, we need to divide the total samples into fewer chunks to get better results
fft_size = 2048  # This defines your frequency resolution, change it according to the power of 2
# for instance if the total number is 60 and the fft_size is 4, then the total number of chunks we get will be 60/4 = 15 chunks

#  Determine how many full chunks we can make
num_chunks = len(complex_data) // fft_size

# now we will be reshaping the data into a 2D array (Matrix) 
# This creates 'num_chunks' rows, each with 'fft_size' samples-->(so there will be 15 rows totally with each containing 4 values)
reshaped_data = complex_data[:num_chunks * fft_size].reshape(num_chunks, fft_size)

#  Apply FFT to every row at once
# axis=1 tells NumPy to do the FFT across the rows
fft_matrix = np.fft.fft(reshaped_data, axis=1)
fft_matrix = np.fft.fftshift(fft_matrix, axes=1)

#  Calculate Power and then Average
# We take the absolute square to get power, then the mean across the rows (axis=0)
average_psd_linear = np.mean(np.abs(fft_matrix)**2, axis=0)

#  Convert the averaged result to Decibels (dB)
psd_dB = 10 * np.log10(average_psd_linear)

# Re-calculate your frequency axis for the smaller FFT size
fft_freqs = np.fft.fftshift(np.fft.fftfreq(fft_size, d=1/sample_rate))

# Plotting the smooth result
plt.plot((fft_freqs + center_frequency) / 1e6, psd_dB)
plt.title(f"Averaged Spectrum ({num_chunks} segments)")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (dB)")
plt.savefig('plot5_3',dpi=300)
plt.show()
