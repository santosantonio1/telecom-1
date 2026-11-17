# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

`spec.txt` is a summary (in Portuguese) of the lab assignment. `grupo01/` holds Group 01's deliverables: `grupo01_pluto.grc`, `grupo01_teste.grc`, `grupo01.py` and `LEIA-ME.md`. All user-facing text is in Portuguese.

`grupo02/` is a copy of `grupo01/` with "Grupo 01"/"Grupo 02", `grupo01`/`grupo02` and 904/920 swapped everywhere. When you change one group's files, make the same change in the other group's files, with those values swapped.

## Modem design (non-obvious lessons)

- Both `.grc` files share the same RX chain and the same two embedded Python blocks (`quadros_tx`, `quadros_rx`), with the code copied into each file. A change to one must be made in both.
- Use `constellation_dqpsk` with `map_bb([0,1,3,2])` after the differential decoder. Plain `constellation_qpsk` with differential coding does not decode.
- The payload is whitened (XOR with `np.random.default_rng(1)` bytes). Without whitening, the long runs of padding spaces cause data-dependent bit errors.
- The FLL band-edge loop bandwidth must be about 0.02. At 0.0628 the bit error rate is about 9 % even on an ideal channel.
- A frame is 544 bits at 250 kbit/s, which gives about 460 frames/s (the spec's target).

## Assignment (from spec.txt)

This is a telecom lab: two-way digital communication between two groups, each using an ADALM-PLUTO SDR, built with **GNU Radio 3.10**. It is due 25/11 on Moodle.

- **Frequencies:** Group 01 transmits on 904 MHz and receives on 920 MHz. Group 02 does the reverse, so both groups can transmit and receive at the same time. Both frequencies fall in Anatel's restricted-radiation bands (Ato nº 14.448/2017).
- **Files each group needs:**
  1. a `.grc` flowgraph for GNU Radio Companion that uses the Pluto;
  2. a test version that runs without a radio, with simulated noise and frequency offset;
  3. a script that runs from the terminal;
  4. a LEIA-ME (README) with step-by-step instructions, in Portuguese.
- **Acceptance criteria:**
  - Flowgraphs open and compile in GNU Radio 3.10 without errors.
  - The test version runs at about 460 frames/s with 0 lost frames.
  - Without a Pluto connected, the script exits with a clear error message that says what to check.
- **The report must show:** spectrum, constellation, eye diagram, received messages and packet loss rate, in both directions.

## Commands

- Simulated loopback, no radio: `python3 grupo01/grupo01.py --teste`. Add `QT_QPA_PLATFORM=offscreen` to run without opening a window.
- Run with the Pluto: `python3 grupo01/grupo01.py [--uri usb:X.Y.Z]`. This transmits over the air.
- Compile a flowgraph only: `grcc -o <dir> <file>.grc`. `grupo01.py` recompiles automatically when the `.grc` is newer than its `.py`.
- Check that the Pluto is reachable: `iio_info -s`
