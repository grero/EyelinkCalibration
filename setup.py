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
      )
