## CubeSail Beacon Decoder

CubeSail is a technology demonstration by CU Aerospace which shows the
viability of solar sail propulsion for deep space missions. It was built
and is operated by students at the University of Illinois at Urbana-Champaign
through the Satellite Development, or SatDev student organization.

Interested in decoding beacons for us? Here's what you need to know:


Frequency: 437305kHz

Modulation: GFSK (GR3UH scrambling)

Bandwidth: 15kHz

Callsign: WI2XVF

Link Layer: AX.25/HDLC

Baud Rate: 9600

TLE:

    cubesail_temp
    1 99999U 18350.31100694 .00048519 00000-0 21968-2 0 00004
    2 99999 085.0351 178.2861 0013006 291.7248 120.7146 15.20874873000012

The decoder, `decoder.py` can be run using Python 3. It will guide you through
the data entry process.


## Usage

1) Download Python for your machine if you don't already have it. Linux users,
get it through your distribution's repositories. If you plan to do more than this
one project with Python, I'd recommend installing [Anaconda](https://www.anaconda.com/downloads)

2) Download git for your machine, and get the script using:

`git clone https://github.com/ijustlovemath/cubesail-decoder.git`

Alternatively, visit the GitHub link and download the script in a zip file.

3) Run the decoder in Python

`python3 decoder.py`
