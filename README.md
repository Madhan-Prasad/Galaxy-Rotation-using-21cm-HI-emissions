# Galaxy-Rotation-using-21cm-HI-emissions

This is a project that I am doing under Prabu T at RRI as a part of my VSP studentship. We are essentially looking out for the 21cm HI emissions from the HI Clouds in the Galaxy arms and calculating it Doppler shift allows us decipher the Rotation of the Galaxy.
# introduction 
This project focuses on the detection and analysis of the 21cm hyperfine transition line of neutral hydrogen (HI) to map the rotation curve of the Milky Way Galaxy. Neutral hydrogen is the most abundant element in the Interstellar Medium (ISM) and emits radio waves at a rest frequency of 1420.405 MHz due to a "spin-flip" transition.
Because these radio waves penetrate interstellar dust, they allow us to observe the structure and velocity of the Galaxy in regions optically hidden from visible light. By measuring the Doppler shift of these emissions from different Galactic longitudes ($l$), we can derive the orbital velocities of hydrogen clouds and infer the presence of Dark Matter in the outer galactic disk.

# Hardware & Data Acquisition
The data was captured using a low-cost radio telescope setup consisting of:

Antenna: A custom-built horn antenna (often flare-extended for higher gain).  

Receiver Chain: Low Noise Amplifiers (LNA) and Bandpass Filters (BPF) optimized for the L-Band (1.4 GHz).  

SDR: An RTL-SDR (Blog V3 or NooElec) sampled at 2.4 MSPS (Mega Samples Per Second).  

Data Format: Raw IQ data stored in a binary .dat format as unsigned 8-bit integers (uint8).

# Methodology & Signal Processing

The raw binary data was processed using a custom Python-based pipeline to extract the faint HI signal from the noise floor:

A. Data Pre-processing

Type Casting: Converted raw uint8 bytes to float32.  
DC Offset Correction: Shifted the data by -127.5 to center the signal around zero.  
IQ Reconstruction: Interleaved the data into complex numbers ($I + jQ$) to preserve phase and frequency information.  

B. Spectral Analysis & Averaging

Fast Fourier Transform (FFT): Performed FFTs to move the signal from the time domain to the frequency domain.  
Vectorized Averaging: To increase the Signal-to-Noise Ratio (SNR), the data was segmented into thousands of chunks (e.g., 2048 samples each). 
The Power Spectral Density (PSD) of these segments was averaged to reduce thermal noise by a factor of $\sqrt{N}$.  
Logarithmic Conversion: Converted the linear power to Decibels (dB) for visualization.  

C. Baseline Correction

Instrumental Bandpass Removal: Modeled the "M-shaped" gain profile of the SDR using a 3rd-degree Polynomial Fit.  
Subtraction: Subtracted the baseline model from the averaged spectrum to isolate the 21cm emission "hump".

# Science GoalsPeak Detection: 
Identify the peak frequency ($f_{obs}$) of the HI emission line.  
Doppler Velocity: Calculate the line-of-sight radial velocity ($V_r$) using the Doppler formula.  
Rotation Curve Derivation: Apply the Velocity-Vector Method ($V_r = \frac{Measured}{\sin(90-l)}$) to correct for projection effects and determine the rotation speed of the Galaxy at specific radial distances. 
