# access-cm3-paper-1

A collaborative project to create and discuss figures for description and assessment paper(s) for [ACCESS-CM3](https://github.com/ACCESS-NRI/access-cm3-configs). Your help is welcome! 

To get started, see the _How it works_ section below.

## ACCESS-OM3 Submodule

This repository includes the [access-om3-paper-1](https://github.com/ACCESS-Community-Hub/access-om3-paper-1) evaluation repository as a Git submodule. This allows scripts and analysis developed for ACCESS-OM3 to be shared and reused in ACCESS-CM3 evaluation.

### What is a Git Submodule?

A Git submodule allows you to keep a Git repository as a subdirectory of another Git repository. In this case, the OM3 evaluation repository is embedded within the CM3 repository, enabling shared analysis tools while maintaining separate development workflows for each project.

### Working with the Submodule

**Initial clone (first time setup):**

If you're cloning this repository for the first time and want to include the OM3 submodule, use:
```bash
git clone --recurse-submodules https://github.com/ACCESS-Community-Hub/access-cm3-paper-1.git
```

If you've already cloned the repository without the submodule, initialize it with:
```bash
git submodule update --init --recursive
```

**Updating the submodule:**

The submodule points to a specific commit in the OM3 repository. To update it to the latest version:
```bash
cd access-om3-paper-1
git pull origin main
cd ..
git add access-om3-paper-1
git commit -m "Update OM3 submodule to latest version"
```

**Note:** Changes made inside the `access-om3-paper-1/` directory should typically be committed to the OM3 repository separately. The CM3 repository only tracks which commit of OM3 it references.

## Experiment descriptions

Currently we welcome feedback on: 
 * `/g/data/zv30/non-cmip/ACCESS-CM3/cm3-run-11-08-2025-25km-beta-om3-new-um-params/cm3-demo-datastore/cm3-demo-datastore.json`: CM3 25km ocean which is a present day control with constant forcing (year numbers are essentially meaningless). This run is not made from a released configuration/build so there is no guarantees of it being available or re-producible long-term. Ocean initial conditions are taken from a "cold start" in ACCESS-OM3 (e.g., WOA2023 January).
 * `/g/data/p73/archive/non-CMIP/ACCESS-CM2/cj877`: CM2 25km present day control run for comparison. Again year numbers are meaningless but in this case start from "1". We recommend comparing the first N years of this run to ACCESS-CM3 runs to assess the spin-up.

## How it works

All community members (and ACCESS-NRI staff) can get write access to this repository (our preference over using forks). To get write access, you need to create an issue requesting access using [this template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=add-user-request-to--access-cm3-1-repository-.md).

All aspects of the project are tracked through [issues](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues), where each small task is captured in a separate issue, i.e., a single issue for each Figure. Issues will develop to include discussion of analysis methods and figures associated with each task. 

The [mega-issue](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1) is used to track all evaluation metrics. Additionally, [evaluation metrics "ported" from OM3 evaluation are tracked seperately here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/5). 

Please use sub-issues of the [mega-issue](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1) for creating new Figures and follow the checklist in the [issue template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=fig-issue-template.md).

### Options for scripts/notebooks
There are 3 different levels of scripts/notebooks to enable anyone to contribute, regardless of their language or workflow preference. These reside within the `access-cm3-paper-1/notebooks`directory:
1. `polished-python`contains scripts that have used the `access-cm3-paper-1/notebook/polished-python/00_template_notebook.ipynb` [template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/00_template_notebook.ipynb) as a starting point and have followed the checklist in the [issue template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=fig-issue-template.md), which includes adding the new script to `access-cm3-paper-1/notebooks/polished-python/mkfigs.sh`; 
2. `sandbox-python`contains scripts that create evaluation using python, but are not using the above workflow;
3. `non-python` contains any kind of script that creates an evaluation figure. 

### How to copy the `access-cm3-paper-1` repo and create a notebook 
To start contributing to the code, you have can either:
 * Push your code changes to the `main` branch directly (i.e., follow the steps below, _omitting_ the branch steps), or
 * Create a new branch directly in this repository, make your changes there, and then open a pull request from your branch into `main` to request review (i.e., carry out _all_ steps below.

 1. Clone the `access-cm3-paper-1` repository locally.
    Go to the directory on your local machine where you want to store the project, e.g., in your home directory or a subdirectory, such as `~/git/`:
    ```bash
    cd ~/git/
    git clone https://github.com/ACCESS-Community-Hub/access-cm3-paper-1.git
    cd ~/git/access-cm3-paper-1/notebooks/polished-python
    ```

2. Make a new branch called `YOUR-USERNAME` and switch to the current branch using the -b option:
   ```bash
   git checkout -b YOUR-USERNAME
   ```
   To list all branches (the `*` indicates the branch you're on) and print the name of the upstream branch, type `git branch -vvl`.

3. Change into `notebooks/polished-python/` directory
   ```bash
   cd notebooks/polished-python/
   ```

4. Copy the [example notebook](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/00_template_notebook.ipynb) as `YOUR-NOTEBOOK.ipynb` and start hacking away. See _Notebooks_ section below for more details.
   ```bash
   cp 00_template_notebook.ipynb YOUR-NOTEBOOK.ipynb
   ```
   The `git status` command displays information about the working directory (your local files), where you can see which changes have been staged, which haven’t, and which files aren’t being tracked by Git. 

5. Add the new file to the staging area so it can be committed:
   ```bash
   git add YOUR-NOTEBOOK.ipynb
   ```
   If you type `git status`, you will see a _Changes to be committed_ message indicating your new `YOUR-NOTEBOOK.ipynb` is now staged for commit. 

6. Commit the new file and give a meaningful short message:
   ```bash
   git commit -m "Notebook for xx evaluation of ACCESS-CM3"
   ```

7. As your local `YOUR-USERNAME` branch has no Upstream branch to the remote repository, you need to set the Upstream branch in order to push your changes to the remote repository:
   ```bash
   git push --set-upstream origin YOUR-USERNAME
   ```
   _Note:_ For the `git push --set-upstream origin <branch-name>` command to successfully push to a remote repository, you need to have an authentication mechanism with that remote. It is recommended to use [SSH keys for authentication with Git](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

   If successful you should see a _branch 'YOUR-USERNAME' set up to track 'origin/YOUR-USERNAME_ message.
   
   Now you can see your active branch `YOUR-USERNAME` in the [list of branches](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/branches) in the remote repository.

8. Create a [_New pull request_](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/pulls) for `YOUR-USERNAME` branch on the remote repository and follow the prompts.

   You can also see the changes you've made so far: `https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/commits/YOUR-USERNAME/`

   Once this pull request has been reviewed and merged into main, you can delete your branch on the remote repository.

9. _Include the Git hash_ when sharing a Figure on your github issue as detailed next in the _Guidelines for Creating Figures_.
    
   The specifics of a commit can be found in the _Git hash_ (also known as a _commit hash_). This is a 40-character hexadecimal string unique identifier for every single commit in a Git repository, e.g., `b7a4f2c10903c989efe3694481c9325d2040ed2b`, which can be found [here](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/commit/main).
    
10. _Add your authorship details_ to the [citation file](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/CITATION.cff). You will need to have write access to the repo - if you don't, please [request it](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/new?template=add-user-request-to--access-cm3-1-repository-.md).

11. If `polished-python` (i.e., follows the template), add your notebook to the `array` variable in `access-cm3-paper-1/notebooks/polished-python/mkfigs.sh` and test that it runs. For more details, see _Notebooks_ section below.

### Guidelines for Creating Figures
 - Create an issue for the Figure you are looking to create (i.e., one issue per figure).
 - Add it as a sub-issue to [the mega-issue](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1).
 - When posting in the issue, **please include path to notebook and the commit hash that created the Figure**. The commit hash also gives run information, which you can also include in the issue. If possible:
 - include a CM2 comparison;
 - Average over the last 10 years;
 - Once you've created your Figure and uploaded your notebook, please tick off your assigned task in the [mega-issue list](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1).
 - If it's not currently possible to complete the metric due to missing diagnostics, please note that in the [Missing diagnostics to do analysis](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/2) issue so we can provide that output in future runs.

## Notebooks

* Notebooks for figures should be in the [polished-python folder](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/tree/main/notebooks/polished-python/). 

* When starting a new notebook, please use [this template](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/00_template_notebook.ipynb). 

* To enable all notebooks to be run at once, **please include the following code snippet at the top of your notebook**:
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

   plotfolder=f"/g/data/{os.environ['PROJECT']}/{os.environ['USER']}/access-cm3-paper-figs/"
   os.makedirs(plotfolder, exist_ok=True)

    # a similar cell under this means it's being run in batch
   print("ESM datastore path: ",esm_file)
   print("Plot folder path: ",plotfolder)
   ```
   This cell needs to have the tag `parameters`. Copying this cell will copy the tag as well, but you can also [set this on other cells](https://papermill.readthedocs.io/en/latest/usage-parameterize.html) should you wish to parameterise other parts of the notebook. This allows us to [pass in arguments externally using papermill](https://papermill.readthedocs.io/en/latest/usage-cli.html) as detailed in [mkfigs.sh](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/mkfigs.sh).

* To enable notebooks to be re-run with different experiments, it's important to use the `esm_file` variable for the source data and save plots in the folder defined by the `plotfolder` variable, e.g., `plt.savefig(plotfolder+'exampleout.png')`. Please refer to [this example notebook](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/00_template_notebook.ipynb).
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

* Once you have finished your notebook, **please add the name of your notebook to the `array` variable** in the [mkfigs.sh notebook](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/mkfigs.sh). This allows us to run your notebook as part of a suite of evaluation notebooks when assessing new simulations.

