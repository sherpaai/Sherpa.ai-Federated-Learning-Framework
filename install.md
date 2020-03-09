# Install

We are on prerelease stage so at the moment the PyPI repository 
doesn't contain the package. In the future install should be as easy as write "pip install shfl".

At the moment, the best option is install the package in editable mode, linking the package to the source code. 
From the main directory of the project you can write: 

```shell
pip -e install .
```

The project documentation is mainly autogenerated from pydocs. If you want to generate the documentation just go to
documentation directory and execute.


```shell
python autogen.py
```

The documentation is created using [MkDocs](https://www.mkdocs.org/). If you want to see the web version of the 
documentation you can serve after install it with in the documentation directory:

```shell
mkdocs serve
```