## Remote Notebooks

This repository contains a python script `dg_notebook.py`, which when run, will connect to a remote server,
launch a notebook and then in the terminal setup port forwarding between your local host and that remote notebook. 

In order to use the script, there are a few python library requirements which should be installed.
You can install them with pip in whatever your default python environment is as:
    
    pip install -r requirements.txt

Next, you can either use the script `dg_notebook.py` directly however you want, as it gives you command line
options. Run the following command to open a description of these:

    python dg_notebook.py --help

Or, you can run the provided `add_new.py` script, which will walk you through generating a re-usable bash alias.

    python add_new.py

If you want different configurations, you can just run add new multiple times to generate those.
You can also go in and manually edit the output of add new in the .zshrc file with whatever
text editor you like.

In the end, the command should look something like this:
