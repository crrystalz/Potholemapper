from setuptools import setup
  
setup(
    name='Potholemapper',
    version='0.1',
    description='',
    author='Rrishi Anand',
    author_email='lichupatnaik@gmail.com',
    packages=['Potholemapper'],
    install_requires=[
        'ultralytics',
        'mapillary_tools',
        'exifread'
    ],
)