This repository contains a python script `dg_notebook.py`, which when run, will connect to a remote server, launch a notebook and then in the terminal setup port forwarding between your local host and that remote notebook. 

Warning: This isn't a fully developed library, more of a quick proof of concept, and right now will only work on mac or linux. 

In order to use the script, there are a few python library requiriments which should be installed.


Warning: This is a just a quick proof of concept.

This repo tried to simplify launching notebooks from a remote server.
It only works on mac / linux.

1. Make sure you install the python requirements.txt locally, with

    
    pip install -r requirements.txt

2. Run add_new.py, which will walk you through generating an alias
to add you zshrc file.

3. Or instead, you could just make the alias yourself, for example:


    alias dg_notebook="python /Users/shahn/PycharmProjects/remote_notebook/dg_notebook.py --username=sage.hahn --hostname=10.69.42.62 --key_filename=/Users/shahn/.ssh/dgx --password="

4. If you added an alias to zshrc, make sure to open a new terminal or source it, e.g.,


    source ~/.zshrc