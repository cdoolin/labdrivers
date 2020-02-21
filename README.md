# Labdrivers

A collection of Python scripts to help run experiments.  Written for use in [The Davis lab](https://sites.ualberta.ca/~jdavis/) at the University of Alberta in Edmonton, Canada.

The scripts were originally written for Python 2.7, so Python 3 support is not guaranteed.

## Instruments

Labdrivers includes scripts to talk to, amongst other:

- Attocube positioning stages via [ANC300 controller](https://www.attocube.com/en/products/nanopositioners/motion-controllers-overview/anc300) over RS232
- New Focus [Velocity TLB-6700](https://www.newport.com/f/velocity-wide-&-fine-tunable-lasers) series tunable lasers over USB
- New Focus Velocity TLB-6300 series tunable lasers over GPIB

## Installation

To use, install with pip.  An editable install is recommended so changes to the labdrivers module are automatically used by python without having to reinstall the module.  Do this with

```bash
pip install -e .
```

or the path to the labdrivers directory instead of "." if running from another directory.


