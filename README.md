PySobokan 1.0
=============

A highly customizable sokoban implementation using Python's tkinter.



Requirements
============

Python 2+  
Tkinter



Usage
=====

1. Clone the repository.  
2. Run `python setup.py sdist` from the project directory to create a source distribution.  
3. Run `pip install --user pysokoban*.tar.gz` from the new `dist/` directory to install the package.  
4. Run `python -c "import pysokoban.sokoban as skb; skb.main()"` to play!


- **Or** simply run `python sokoban.py` from the project directory without installing the package.

To update the version:

1. Clone or pull the repository for the latest version.  
2. Recreate the source distribution using the steps above.  
3. Run `pip upgrade pysokoban*.tar.gz` from the `dist/` directory to upgrade the package.

To uninstall, run `pip uninstall pysokoban`.  
You can modify the graphics used by replacing the images in the images folder.
