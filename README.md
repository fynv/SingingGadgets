SingingGadgets
================

This is an on-going refactor of [ScoreDraft](https://github.com/fynv/ScoreDraft) to address 2 weakness of ScoreDraft when considering it as a Python library:

* PyPi Compatibility 
* Low-level Interface Exposing.

This project is consisted of 2 packages: SingingGadgets and ScoreDraft.

* Package SingingGadgets provides low-level interfaces to the singing synthesis engine.
* Package ScoreDraft provides highevel interfaces similar to the project ScoreDraft, based on package SingingGadgets.

For more details on the design considerations, see:

[http://scoredraft.org/index.php/2018/05/27/introducing-singinggadgets/](http://scoredraft.org/index.php/2018/05/27/introducing-singinggadgets/)

## Building with CMake

SingingGadgets can be built and deployed to an arbitary local path with CMake.

Prerequisites:

* CMake 3.0+
* Python3
* CUDA (Optionally needed by the VoiceSampler module, can be disabled by setting "USE_CUDA" to false in /SingingGadgets/VoiceSampler/CMakeLists.txt)

You can simply run CMake to generate makefiles/project files for your system and build. 
You can set CMAKE_INSTALL_PREFIX to /Test so that the test scripts can find SingingGadgets.

## PyPi Style Building/Installing

SingingGadgets is compatible with Setuptools. To build and install PyPi locally, try:

	$ python3 setup.py build	
	$ python3 setup.py install

Prebuilt wheels are also available from https://pypi.org/. Lastest packages are:

	SingingGadgets-0.0.2-cp35-cp35m-manylinux1_x86_64.whl
	SingingGadgets-0.0.2-cp36-cp36m-manylinux1_x86_64.whl
	SingingGadgets-0.0.2-cp36-cp36m-win_amd64.whl
	SingingGadgets-0.0.2-cp36-cp36m-macosx_10_9_x86_64.whl

If you are using a compatible system, try:

	$ pip3 install SingingGadgets

### limitations

* PyPi style building currently doesn't support CUDA
* Because SingingGadgets contains a package called exactly ScoreDraft, it will likely conflict with the one in project ScoreDraft (https://github.com/fynv/ScoreDraft). If you are using both, please consider using the CMake building approach and deploy neither of them into your Python installation directory.

## Usage

See [http://scoredraft.org/index.php/2018/05/30/singinggadgets-how-to-use/](http://scoredraft.org/index.php/2018/05/30/singinggadgets-how-to-use/)

## License

pyTinySoundFont is available under the [MIT license](https://choosealicense.com/licenses/mit/).

