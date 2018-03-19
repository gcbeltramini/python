# IPython history

All history of your Jupyter notebooks and IPython is registered in the file `${HOME}/.ipython/profile_<name>/history.sqlite` (http://ipython.readthedocs.io/en/stable/interactive/reference.html?highlight=sqlite#search-command-history):

This is how you can use the magic command `%history`: http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-history

To query the database, check the Jupyter notebook `IPython-history.ipynb`.

One can also use [DBeaver](https://dbeaver.jkiss.org):
* File --> New --> DBeaver --> Database Connection --> SQLite
    * `Path`: /Users/<your-username>/.ipython/profile_default/history.sqlite
    * `User name`: empty
    * `Password`: empty
    * `Next` --> `Connection name`: IPython history
    * Leave the default options for all the rest
