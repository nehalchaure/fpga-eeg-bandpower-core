import numpy as np
from scipy.signal import firwin,lfilter

#numpy----->math on arrays
#firwin---->design FIR filter
#lfilter--->apply FIR filter to the signal

#-------------------------------------
#1.BASIC SETTINGS
#-------------------------------------

FS=256           # SAMPLING FREQUENCY IN HERTZ (256 SAMPLES EVERY 1 SECOND)
N_TAPS=32        # NUMBER OF FIR FILTER COEFFICIENTS (FILTER LENGTH)
BAND=(8,30)      # FREQUENCY BAND CONSIDERED: 8-30 HZ (THIS IS WHERE ALPHA + BETA EEG RHYTHM LIES)
WIN_LEN=256      # NUMBER OF SAMPLES IN ONE WINDOW: 256 
SCALE=2**15      # SCALE FACTOR FOR Q15 FIXED POINTS (MAPS [-1,1) TO INT16)

#------------------------------------
#2.CREATING FAKE EEG SIGNALS
#------------------------------------

#Time axis:0,1/FS...........WIN_LEN-1/FS

t=np.arrange(WIN_LEN)/FS

# [0,1/256,2/256..........255/256]
# using np. means using a funcction from numpy library
# arrange() creates a list of evenly spaced numbers, so creates an array from 0 to win_len-1
# Create an array of time values for each sample:
# t = [0 seconds, 1/FS seconds, 2/FS seconds, ..., (WIN_LEN−1)/FS seconds].


# x= clean 10 Hz sin wave inside the band + small random noise

x=0.5*np.sin(2*np.pi*10*t) + 0.1*np.random.randn(WIN_LEN)


#------------------------------------------------------
#3. DESIGN A FLOATING-POINT FIR BAND-PASS FILTER
#------------------------------------------------------

# firwin is a SciPy function that creates FIR filters.
# firwin returns N_TAPS coefficients for an FIR filter.

# cutoff=[8,30], pass_zero=False -> band-pass between 8 and 30 Hz. [web:71][web:74][web:152]

b=firwin(
N_TAPS,[BAND[0],BAND[1]],pass_zero=False,fs=FS
)

#------------------------------------------------------
#4.QUANTIZE FILTER COEFFICIENTS TO Q15 (FOR FPGA)
#------------------------------------------------------

#Multiply by SCALE to move from float [-1,1) to integer range, then round and cast to 16-bit signed integers.

b_q = np.round(b * SCALE).astype(np.int16)

# -----------------------------
# 5. FILTER THE SIGNAL (FLOAT) AND COMPUTE BANDPOWER
# -----------------------------
# lfilter applies the FIR filter 'b' to signal 'x' to produce 'y'. [web:152]
y = lfilter(b, [1.0], x)

# Bandpower = mean of squared filtered samples over the window. [web:72][web:78]
power_float = np.mean(y ** 2)

# -----------------------------
# 6. QUANTIZE INPUT SAMPLES TO Q15 (FOR FPGA)
# -----------------------------
# Same idea as coefficients: map float samples into int16 range.
x_q = np.round(x * SCALE).astype(np.int16)

# -----------------------------
# 7. SAVE TEST VECTORS TO TEXT FILES
# -----------------------------
# These files will be read by your Verilog testbench later.
# fmt="%d" -> write numbers as integers in text form. [web:87][web:91][web:101][web:153]

np.savetxt("python/test_vectors/coeffs.txt", b_q, fmt="%d")       # Q15 filter coeffs
np.savetxt("python/test_vectors/samples.txt", x_q, fmt="%d")      # Q15 input samples
np.savetxt("python/test_vectors/golden.txt",
           np.array([power_float]), fmt="%.10f")                   # float reference power

print("Wrote coeffs.txt, samples.txt, golden.txt")
