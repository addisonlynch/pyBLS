.. _install:


*******
Install
*******

Dependencies
============

pyBLS relies on:

-  `requests <http://docs.python-requests.org>`__

For testing requirements, see `testing <testing.html>`__.

Installation
============

Latest stable release via pip (recommended):

.. code:: bash

    $ pip install pyBLS

Latest development version:

.. code:: bash

    $ pip install git+https://github.com/addisonlynch/pyBLS.git

or

.. code:: bash

     $ git clone https://github.com/addisonlynch/pyBLS.git
     $ cd pyBLS
     $ pip install .

**Note:**

The use of
`virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
is recommended as below:

.. code:: bash

    $ pip install virtualenv
    $ virtualenv env
    $ source env/bin/activate
