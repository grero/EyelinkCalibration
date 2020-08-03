from setuptools import setup

setup(name="EyelinkCalibration",
      version="0.1.0",
      packages=["EyelinkCalibration"],
      package_data={"EyelinkCalibration": ["EyelinkCalibration/main_gui.ui"]},
      include_package_data=True,
      data_files=["EyelinkCalibration/main_gui.ui"],
      entry_points={"gui_scripts": ["EyelinkCalibration = EyelinkCalibration.main_gui:main"
                                   ]
                   },
      install_requires=["PyQt5",
                        "pylink",
                        "pyserial",
                        "psychopy",
                        "pyglet==1.3.2"],
      dependency_links=["https://github.com/grero/pylinkwrapper/tarball/master"],
      )
