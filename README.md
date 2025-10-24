# access-cm3-paper-1

A collaborative project to create and discuss figures for description and assessment paper(s) for [ACCESS-CM3](https://github.com/ACCESS-NRI/access-cm3-configs). Your help is welcome! Please see `How it works` [below](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/tree/18_improve_docs?tab=readme-ov-file#how-it-works) to get started.

## Experiment descriptions

Currently we welcome feedback on: 
 1. `/g/data/zv30/non-cmip/ACCESS-CM3/cm3-run-11-08-2025-25km-beta-om3-new-um-params/cm3-demo-datastore/cm3-demo-datastore.json`: CM3 25km ocean which is a present day control with constant forcing (year numbers are essentially meaningless). This run is not made from a released configuration/build so there is no guarantees of it being available or re-producible long-term! Ocean initial conditions are taken from a "cold start" in OM3 (i.e. WOA2023 January).
 2.  `/g/data/p73/archive/non-CMIP/ACCESS-CM2/cj877`: CM2 25km present day control run for comparison. Again year numbers are meaningless but in this case start from "1". We recommend comparing the first N years of this run to CM3 runs to assess the spin-up.

## How it works

All community members (and ACCESS-NRI staff) can get write access to this repository (our preference over using forks). To get write access, you need to create an issue and request access, [please use this issue template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=add-user-request-to--access-cm3-1-repository-.md).

All aspects of the project are tracked through [issues](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues). Create an issue to represent each small task, _a single issue is used for each Figure_. Issues will develop to include discussion of analysis methods and figures associated with each task. [A mega-issue exists here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1) to track all the evaluation metrics, evaluation metrics that are "ported" from OM3 evaluation are [tracked here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/5). Feel free to add new Figure-issues as sub-issues.

### Options for scripts and notebooks
We have 3 different levels of scripts to enable contributions from anyone, regardless of their language or workflow preference. Inside this directory `access-cm3-paper-1/notebooks`, there are three kinds of shared scripts/notebooks:
1. `polished-python`;
2. `sandbox-python`;
3. `non-python`.

In more detail:
 - `polished-python` contains scripts that have used the `access-cm3-paper-1/notebook/polished-python/00_template_notebook.ipynb` template as a starting point and have been added to the `access-cm3-paper-1/notebooks/polished-python/mkfigs.sh` script (most preferred); 
 - `sandbox-python` contains scripts that create evaluation using python, but are not using the above workflow;
 - `non-python` contains any kind of script that creates an evaluation figure.

### Getting started
To start contributing to the code, you have two options:
 1. Push your code changes to the `main` branch directly. 
 2. If you'd prefer your code changes to be reviewed, create a new branch directly in this repository, make your changes there, and then open a pull request from your branch into `main`. 

**For option 1**, follow the steps below but omit the branch steps (i.e. step 2 and 7).

**For option 2**, carry out all steps below. For more detailed instructions [see section below](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/tree/18_improve_docs?tab=readme-ov-file#how-to-set-up-a-local-copy-of-access-cm3-paper-1-repo-and-create-a-notebook-on-a-branch) _How to set up a local copy of `access-cm3-paper-1` repo and create a notebook on a branch_

 1. Clone the `access-cm3-paper-1` repository locally
 2. Make a new branch with your name `git checkout -b username`
 3. `cd` into `notebooks/polished-python/`
 4. Copy the example notebook, and start hacking away (see `Notebooks` section below for the details)
 5. When ready to upload, run the commands:
    `git add <path to your notebook>`
    `git commit -m "A short decriptive message"`
    `git push -u REMOTE_NAME branch_name` (where `REMOTE_NAME` is the name of your GitHub remote, this defaults to `origin`)
 7. Make a PR on github to merge it into main and delete your branch
 8. Add your authorship details to the [citation file](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/CITATION.cff).

_Note_: You need to have write access to the repo. If you don't, please [request it](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=add-user-request-to--access-cm3-1-repository-.md).

## Detailed instructions 
### How to set up a local copy of `access-cm3-paper-1` repo and create a notebook on a branch

1. Clone the `access-cm3-paper-1`git repository locally. Go to the directory on your local machine where you want to store the project, e.g., in your home directory or a subdirectory within it, such as `~/git/`:
```bash
    cd ~/git/
    git clone https://github.com/ACCESS-Community-Hub/access-cm3-paper-1.git
    cd ~/git/access-cm3-paper-1/notebooks/polished-python
```

2. Create a new branch called `YOUR-USERNAME` and switch to the current branch using the -b option:
```bash
git checkout -b YOUR-USERNAME
```
To list all branches (the `*` indicates the branch you're on) and print the name of the upstream branch:
```bash
git branch -vvl
```

3. Create `YOUR-NOTEBOOK.ipynb` by copying the template notebook `00_template_notebook.ipynb`:
```bash
cp 00_template_notebook.ipynb YOUR-NOTEBOOK.ipynb
```
The `git status` command displays information about the working directory (your local files), where you can see which changes have been staged, which haven’t, and which files aren’t being tracked by Git. 
```bash
git status
```

4. Add the new file to the staging area so it can be committed:
```bash
git add YOUR-NOTEBOOK.ipynb
```

Now, if you run `git status` again, you will see that your new file is staged to be committed:
```bash
git status 
```
You will also see the message *Changes to be committed:*, where the new file (to be committed) is written in green text.

5. Commit the new file and give a meaningful short commit message:
```bash
git commit -m "Created notebook for xx evaluation of CM3"
```

6. As your local `YOUR-USERNAME` branch has no Upstream branch to the remote repository, you need to set the Upstream branch in order to push your changes to the remote repository:
```bash
git push --set-upstream origin YOUR-USERNAME
```

_Note_: if you're not using SSH keys, you will be prompted for your GitHub username and password. 
If successful you should see the following output:
```bash
branch 'YOUR-USERNAME' set up to track 'origin/YOUR-USERNAME
```
Now you can see your active branch `YOUR-USERNAME` [here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/branches) on the remote git repository.

7. Create a (draft) pull request for `YOUR-USERNAME` on GitHub by following the prompts, which will appear here:
`https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/pulls`

You can also see the changes you've made so far here: 
`https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/commits/YOUR-USERNAME/`

The specifics of a commit can be found in the _Git hash_ (also referred to as a _commit hash_). This is a 40-character hexadecimal string unique identifier for every single commit in a Git repository, e.g., `b7a4f2c10903c989efe3694481c9325d2040ed2b`, which can be found here: 
`https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/commit/`

8. **Please include this Git hash** when sharing a Figure on your github issue as detailed next in the _Guidelines for Creating Figures_.


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

