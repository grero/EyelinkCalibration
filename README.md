# Installation

First, create a fresh environment.

```sh
conda create -y -n eyelink python=3.6
source activate eyelink
pip install git+https://github.com/grero/pylinkwrapper
```

Prior to installing the package, the pylink package should be copied from the Eyelink directory to the site-packages directory of the `eyelink` environment.
On a macOS, this could be

```sh
cp -r  /Applications/Eyelink/pylink/pylink3.6 ~/anaconda/envs/eyelink/lib/python3.6/site-packages/pylink
```

Then, we can go ahead and install the package using pip:

```python
pip install git+https://github.com/grero/EyelinkCalibration
```

## Usage

After the installation step, the `EyelinkCalibration` app should be added to your system and you should be able to automatically run it. On macOS, simply type in `EyelinkCalibration` from the command line, making sure that you are in the `eyelink` environment.
