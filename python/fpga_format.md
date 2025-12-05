## Q1.15 Fixed-Point Number Format

In this project, all signal and filter processing on the FPGA is performed using **fixed-point arithmetic**, specifically the **Q1.15 format**. This format represents real numbers using a 16-bit signed integer, where the binary point is fixed between the **1st** and **2nd** bit from the left.

---

### Definition

A Q1.15 number allocates:

- **1 bit** for the sign and integer part  
- **15 bits** for the fractional part  

Total: **16 bits (int16)**.

In binary form:

S | I | FFFFFFFFFFFFFFF


- **S** = sign bit (0 = positive, 1 = negative)  
- **I** = integer bit (0 or 1)  
- **F** = 15 fractional bits  

This format can represent values in the range:

\[
-1.0 \leq x < +1.0
\]

with a resolution of:

\[
2^{-15} \approx 3.05 \times 10^{-5}
\]

---

### Why Q1.15 is Used

Floating-point computation is expensive on FPGA fabric, consuming more logic, power, and latency.  
In contrast, Q1.15:

- fits directly into **16-bit signed multipliers**  
- is efficient for FIR filtering and power calculations  
- provides **high precision** for biomedical signals  
- simplifies hardware implementation (shift instead of float-normalization)

Thus, Q1.15 gives an excellent balance of **accuracy** and **hardware efficiency**, making it ideal for EEG bandpower extraction.

---

### Float to Q1.15 Conversion

A floating-point coefficient \( b \) in the range \([-1, 1)\) is converted to Q1.15 using:

\[
b_{\text{Q15}} = \text{round}(b \times 2^{15})
\]

Example:

b = 0.5
Q15 = round(0.5 × 32768) = 16384


In hardware, the integer `16384` represents the real value **0.5**.

In the code:

```python
b_q = np.round(b * (2**15)).astype(np.int16)

### Multiplication in Q1.15

When two Q1.15 numbers are multiplied, the raw product has **30 fractional bits**  
(i.e., it becomes a **Q2.30** number).  
To return to Q1.15 format, the result must be shifted right by 15 bits:

\[
(a_{\text{Q15}} \times b_{\text{Q15}}) \gg 15
\]

This shifting ensures proper scaling and preserves numerical correctness.

---

### Relevance to This Project

In this EEG bandpower extraction system, the following elements operate using **Q1.15 fixed-point arithmetic**:

- input samples  
- FIR filter coefficients  
- FIR filter outputs  
- squaring operations  
- accumulation over 256 samples  

Using Q1.15 guarantees:

- **deterministic behavior** (no floating-point nondeterminism)  
- **efficient hardware mapping** to FPGA multipliers  
- **resource-friendly FIR implementation**  
- **accurate and stable power estimation** for biomedical signals  

---

