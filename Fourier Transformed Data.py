#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt 

datafile = 'output_21cm_may_2.dat'
sample_rate = 2.048e6 # 2.048 MHz is the standard for a RTL-SDR file
num_sample = 1000000  # change this accodring to the requirement so for first plots i am taking it from a million samples


# To convert the raw binary data into 8 bit interger (uint8)

raw_data = np.fromfile(datafile,dtype =np.uint8, count= num_sample)
samples = raw_data.astype(np.float32)-127.5
iq = samples[::2] +1j* samples[1::2]
# the above line does 2 things, one it is taking all the even index and assigning it to the real part of the complex number and taking all the odd integer and assigning it to the complex part of the complex number, there are various reasons for this: * this allows the computer to distinguish between positive and negative, and this is how we can know if the hydrogen cloud is moving towards or away relative to the 1420.4MHz center. 
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

axs[0].plot(iq.real[:500],label = 'Real value') # only 500 values are being plotted 
axs[0].plot(iq.imag[:500],label = 'Imaginary')# only 500 values are being plotted 
axs[0].set_ylabel("amplitude")
axs[0].set_title("Time Domain plot")
axs[0].legend()

# Frequency Domain, this is where i have added the fourier transformation to the data points, NFFT is the  number of points in the fast fourier transformation which defines how many 'bins' your frequency range is divided into.
# This is giving me a resolution of 1KHz per bin as the Sample rate is 2.048e6 and the NFFT is set to 2048. THE WIDTH OF EACH FREQUENCY BIN IS GIVEN BY delta_f = SampleRate/ NFFT which is 2.048e6/2048.

axs[1].psd(iq, NFFT= 2048, Fs = sample_rate/1e6)# this is the code for the Fast Fourier Transformation and the NFFT is the bin size of the transformation, that is this helps in the resolution usually it is 1024 or 2049 or 4096, higher the value, greater the resolution. Fs is the sampling frequency, which is 2048 per seconds, that means it is taking 1024 on either side of the centered 1420.41 MHz. 
axs[1].set_title("Frequency Domain, After Fourier Transformation")
axs[1].set_xlabel("Frequency offset from center (MHz)")
axs[1].set_ylabel("Power(dB)")
axs[1].axvline(x=0, color='brown', linestyle=':', linewidth=2, alpha=0.8)
axs[1].legend(['Power Spectrum', 'Center Frequency (1420.41 MHz)'])

plt.tight_layout()
plt.savefig('first_plot4',dpi=300)
plt.show()
