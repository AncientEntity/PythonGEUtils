try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='PythonGEUtils',
      version='0.1',
      description='Python Game Engine',
      author='Ancient Entity',
      author_email='',
      url='https://github.com/AncientEntity/PythonGEUtils',
      packages=['PythonGEUtils','PythonGEUtils.images','PythonGEUtils.helpful'],
      install_requires=['pygame'],
      package_data={'PythonGEUtils.images': ['*']},
      include_package_data=True,
     )
