@echo off
python -m pip install --upgrade pip
python -m pip install Cython
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer
python -m pip install kivy
python -m pip install pyrebase
exit