# FPGA Motor-Imagery EEG Bandpower Core
## Project Specification

**Title:** FPGA-based Single-Channel Motor-Imagery EEG Bandpower Feature Extraction  
**Date:** 4 Dec 2025  
**Target completion:** 25 Dec 2025  
**Platform:** Xilinx Vivado (simulation now), Basys 3 / Zynq UltraScale+ later

---

## 1. Goal
Design and simulate a single-channel FPGA core that computes 8–30 Hz bandpower from EEG windows (256 samples) using fixed-point DSP, with a Python golden model and Vivado synthesis, ready for later deployment on Basys 3 or Zynq UltraScale+.

Success by 25 Dec means:
- RTL matches Python golden model within ±5% on test data.  
- Design synthesizes in Vivado for a Basys 3 Artix-7 device with timing met at ≥50 MHz.  
- Repo has clean `/rtl`, `/python`, `/docs`, `/test_vectors` structure and basic docs.

---

## 2. Scope

**In scope (now):**
- 1 EEG channel, 8–30 Hz band.
- 32-tap FIR band-pass filter, 16-bit fixed-point coefficients.
- 256-sample windows, average power feature (optionally normalized).
- Verilog modules: `fir.v`, `power_accumulator.v`, `top_sim.v`.
- Python golden model: FIR design, quantization, power calculation, test-vector export.
- Testbenches for FIR, power, and full pipeline in simulation.
- Vivado project targeting Basys 3 part (XC7A35T) for synthesis only.

**Out of scope (later):**
- Physical board bring-up (Basys 3 / Zynq).
- Real-time UART streaming from PC to FPGA and back.
- Classifier on FPGA (stay Python-only if done at all).
- Multi-channel or multi-band extension.

---

## 3. Architecture

**Data path:**

- Input: 16-bit signed EEG samples (assume 256 Hz sampling).  
- FIR: 32-tap band-pass 8–30 Hz, coeffs in Q15 (16-bit).  
- FIR output: wider fixed-point (e.g., 24-bit) to preserve precision.  
- Power block: square FIR output, accumulate over 256 samples, scale back to 16-bit bandpower.  
- Output: 16-bit bandpower + `feature_valid` pulse at end of each window.

**Modules:**
- `fir.v` – streaming FIR filter, one sample per clock when `sample_valid` is high.  
- `power_accumulator.v` – squares, accumulates, divides (right shift), asserts `feature_valid`.  
- `top_sim.v` – connects FIR + power; used by testbench and simple file-based I/O.  

---


## 4. Deliverables

- `/python/golden_model.py` – FIR design, quantization, power, export test vectors.  
- `/python/verify.py` – compares RTL output vs golden.  
- `/python/test_vectors/{samples.txt,golden.txt,coeffs.txt}`.  
- `/rtl/{fir.v,power_accumulator.v,top_sim.v}`.  
- `/tests/{tb_fir.sv,tb_power.sv,tb_top_sim.sv}` (names flexible).  
- `vivado_project/` – project files, synth/timing reports.  
- `/docs/project_spec.md` – this file.  
- `README.md` – overview + how to run Python and simulations.

---

## 5. Future work (later)

- Add UART + constraints to run on Basys 3 when you have the board.  
- Extend to multiple bands (theta/alpha/beta) and multiple features per window.  
- Add a simple Python classifier (e.g., logistic regression) using these features.  
- Port core to Zynq UltraScale+ and connect to ARM PS for real-time demos.
