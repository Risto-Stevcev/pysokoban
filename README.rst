PySokoban
=========

| A highly customizable sokoban implementation using Python's tkinter.
| View the package in the PyPI repository_ for documentation and an easy Win32 installation.

Requirements
============

| Python 2+
| Tkinter

Usage
=====

**Installing it using pip:**

#. Run ``pip install --user pysokoban``

#. Run ``pysokoban`` to
   play!


**Installing it from the Git repository:**

#. Clone the repository.

#. Run ``python setup.py sdist`` from the project directory to create a
   source distribution.

#. Run ``pip install --user pysokoban*.tar.gz`` from the new ``dist/``
   directory to install the package.

#. Run ``pysokoban`` or ``python -c "import pysokoban.sokoban as skb; skb.main()"`` to
   play!

-  **Or** just run ``python sokoban.py`` from the project directory
   without installing the package.

To update the version:

#. Clone or pull the repository for the latest version.

#. Recreate the source distribution using the steps above.

#. Run ``pip upgrade pysokoban*.tar.gz`` from the ``dist/`` directory to
   upgrade the package.

| To uninstall, run ``pip uninstall pysokoban``.
| You can modify the graphics used by replacing the images in the images folder.

.. _repository: https://pypi.python.org/pypi/pysokoban/ 
