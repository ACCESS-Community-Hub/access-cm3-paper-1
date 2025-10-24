# access-cm3-paper-1

A collaborative project to create and discuss figures for a description and assessment paper(s) for [ACCESS-CM3](https://github.com/ACCESS-NRI/access-cm3-configs). Your help is welcome! Please see `How it works` below to get started.

TL;DR
#TODO: add workflow example (and clean it up)
https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/19

## Experiment descriptions

Currently we welcome feedback on: 
 1. `/g/data/zv30/non-cmip/ACCESS-CM3/cm3-run-11-08-2025-25km-beta-om3-new-um-params/cm3-demo-datastore/cm3-demo-datastore.json` CM3 25km ocean which is a present day control with constant forcing (year numbers essentially meaningless). This run is not made from a released configuration/build so there is no guarantees of it being available or re-producible long-term! Ocean initial conditions are taken from a "cold start" in OM3 (i.e. WOA2023 January).
 2.  `/g/data/p73/archive/non-CMIP/ACCESS-CM2/cj877` CM2 25km present day control run for comparison. Again year numbers are meaningless but in this case start from 1. We recommend comparing the first N years of this run to CM3 runs to assess the spin-up.

## How it works

All community members (and ACCESS-NRI staff) can get write access to this repository (our preference over using forks). To get write access, you need to create an issue and request access, [please use this issue template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=add-user-request-to--access-cm3-1-repository-.md).

All aspects of the project are tracked through [issues](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues). Create an issue to represent each small task, _a single issue is used for each Figure_. Issues will develop to include discussion of analysis methods and figures associated with each task. [A mega-issue exists here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1) to track all the evaluation metrics. Feel free to add new Figure-issues as sub-issues.

To start contributing to the code, you have two options:
 1. Push your code changes to the `main` branch directly. 
 2. If you'd prefer your code changes to be reviewed, create a new branch directly in this repository, make your changes there, and then open a pull request from your branch into `main`. 

### Detailed instructions 

For option 1, follow the steps below but omit the branch steps (e.g., step 2 and 7)
For option 2, carry out all steps below 

 1. Clone this repository locally;
 2. Make a new branch with your name `git checkout -b username`;
 3. `cd` into `notebooks/polished-python/`;
 4. Copy the example notebook, and start hacking away (see `Notebooks` section below for the details);
 5. When ready to upload, run the commands:
    `git add <path to your notebook>`
    `git commit -m "A short decriptive message"`
    `git push -u REMOTE_NAME branch_name` (where `REMOTE_NAME` is the name of your GitHub remote, this defaults to `origin`)
 7. Make a PR on github to merge it into main (you can delete your branch at this point)
 8. Add your authorship details to the [citation file](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/CITATION.cff).

Note: You need to have write access to the repo. If you don't, please [request it](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=add-user-request-to--access-cm3-1-repository-.md).)


### Guidelines for creating Figures
 - Create an issue (one per figure) for the Figure you are looking to create. Add it as a sub-issue to [the mega-issue](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1).
 - When posting in the issue, **please include path to notebook and the commit hash that created the Figure**. The commit hash also gives run information, which you can include in the post for convenience.
 - Try to include a CM2 comparison!
 - Average over the last 10 years is also desirable.
 - Once you've created your Figure / uploaded your notebook, please tick off your assigned task in [the list](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1).
 - If it is not currently possible to complete the metric due to missing diagnostics, please note that in an issue [here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/2) so we can provide that output in future runs.

## Notebooks

Notebooks for figures should be in the [notebooks folder](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/tree/main/notebooks/polished-python/). When starting a new notebook, please use the template [here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/00_template_notebook.ipynb). 

To enable us to run all notebooks at once, *please include the following code snippet* (boilerplate) at the top of your notebook:
```python
#parameters

### USER EDIT start
esm_file='/g/data/zv30/non-cmip/ACCESS-CM3/cm3-run-11-08-2025-25km-beta-om3-new-um-params/cm3-demo-datastore/cm3-demo-datastore.json'
dpi=300
### USER EDIT stop

import os
from matplotlib import rcParams
%matplotlib inline
rcParams['figure.dpi']= dpi

plotfolder=f"/g/data/{os.environ['PROJECT']}/{os.environ['USER']}/access-om3-paper-figs/"
os.makedirs(plotfolder, exist_ok=True)

 # a similar cell under this means it's being run in batch
print("ESM datastore path: ",esm_file)
print("Plot folder path: ",plotfolder)
```

To enable notebooks to be easily re-run later with different experiments, it is important to use `esm_file` variable for the source data and save plots into the folder defined by the `plotfolder` variable, i.e., `plt.savefig(plotfolder+'exampleout.png')`. Please refer to [this example](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/00_template_notebook.ipynb):
```python
datastore = intake.open_esm_datastore(
    esm_file,
    columns_with_iterables=[
        "variable",
        "variable_long_name",
        "variable_standard_name",
        "variable_cell_methods",
        "variable_units"
    ]
)
```
This cell needs to have the tag `parameters`, copying this cell will copy the tag as well but [you can also set this on other cells](https://papermill.readthedocs.io/en/latest/usage-parameterize.html) should you wish to parameterise other parts of the notebook. This allows us to [pass in arguments externally using papermill](https://papermill.readthedocs.io/en/latest/usage-cli.html) (see [mkfigs.sh for details](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/mkfigs.sh))

Once you have finished your notebook, *please add the name of your notebook to the `array` variable* in [this notebook](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/mkfigs.sh). This allows us to run your new notebook as part of a suite of evaluation notebooks when assessing new simulations.

## Other options for scripts and notebooks

Note that in this directory `access-cm3-paper-1/notebooks`, there are three kinds of shared scripts/notebooks:
1. `polished-python`;
2. `sandbox-python`;
3. `non-python`.

In more detail:
 - `polished-python` contains scripts that have used the `access-cm3-paper-1/notebook/polished-python/00_template_notebook.ipynb` template as a starting point and have been added to the `access-cm3-paper-1/notebooks/polished-python/mkfigs.sh` script (most preferred); 
 - `sandbox-python` contains scripts that create evaluation using python, but are not using the above workflow;
 - `non-python` contains any kind of script that creates an evaluation figure.

#TODO: more words about the carrot for doing `polished-python`.
