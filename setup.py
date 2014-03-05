from setuptools import setup, find_packages

setup(
    name='pysokoban',
    version='1.0',
    license='BSD',
    author='Risto Stevcev',
    author_email='risto1@gmail.com',
    url='https://github.com/Risto-Stevcev/pysokoban',
    long_description="README.rst",
    packages=find_packages(),
    include_package_data=True,
    package_data={'' : ['*.gif']},
    description="A highly customizable sokoban implementation using Python's tkinter.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Games/Entertainment :: Puzzle Games',
        ],
)

