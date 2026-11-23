# access-cm3-paper-1

A collaborative project to create and discuss figures for description and assessment paper(s) for [ACCESS-CM3](https://github.com/ACCESS-NRI/access-cm3-configs). Your help is welcome! 

To get started, see the _How it works_ section below.

## Experiment descriptions

Currently we welcome any feedback on the CM3 experiments listed in [this table](https://access-cm3-configs.readthedocs.io/Experiments/).

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

## For maintainers: running the notebooks and publishing with GitHub Actions

_Most contributors can skip this: it is for the few people who render and publish the figures website._

The **mkfigs** workflow (in the [Actions tab](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/actions/workflows/mkfigs.yml))
runs `notebooks/polished-python/mkfigs.sh` on Gadi and attaches a **preview** of the figures website to the run. Nothing goes
to Figshare until a second, separate approval. It does the same as running `mkfigs.sh` and `mkfigs-pushit`
by hand; the details and the one-off set-up are in
[access-model-mkfigs](https://github.com/ACCESS-NRI/access-model-mkfigs#running-from-github-actions).

Anyone with write access can start a run, but nothing happens on Gadi until one of the approvers of the
`mkfigs` environment approves it, and publishing needs a second person, from the `mkfigs-publish` environment
(both are listed under **Settings → Environments**). Runs only ever use branches of this repo, never forks.

### Starting a run

**Actions → mkfigs → Run workflow** opens a form. The first field, **mode**, says what to do:

| Mode | Use workflow from | What it does |
|---|---|---|
| `new experiment` | `main` | First run of an experiment: runs the notebooks, then can publish it |
| `update a published experiment` | `main` | Re-runs or adds **only the notebooks you list**, taken from `main`; everything else stays as published. Then can publish them as a new version |
| `preview a branch` | the branch to try, e.g. a PR's | Runs the listed notebooks from that branch on one or more experiments, to look at. **Never publishes** |

The other fields:

| Field | What to put |
|---|---|
| `ename` | The experiment name. It becomes the Figshare article title, the website pages and the `eval-<ename>` branch and tag. For a preview, one or more names, space-separated; an experiment that isn't published yet is written `NAME=/g/data/.../datastore.json` |
| `esm_file` | The experiment's datastore `.json` on Gadi. Needed for a new experiment; for an update, leave blank to use the one it was published with; not used for a preview |
| `notebooks` | Space-separated (e.g. `TOA_CRE`). For an update or a preview, exactly these run. For a new experiment, blank runs every notebook in `mkfigs.sh` |
| `parameters` | Optional extra [papermill parameters](https://papermill.readthedocs.io/en/latest/usage-parameterize.html) for every notebook in the run, space-separated `NAME=VALUE` (e.g. `dpi=150`). A notebook without that parameter ignores it. Blank means none for a new experiment, and the experiment's published ones for an update or preview. They are recorded in `mkfigs.sh` with the experiment, and shown in the run summary and on the preview page |
| `pick_up_jobs` | Tick only to pick up the jobs of an earlier run that stopped waiting (see below) |
| `mkfigs_version` | Which [access-model-mkfigs](https://github.com/ACCESS-NRI/access-model-mkfigs) (the code that runs the notebooks and builds the pages) to use. `pinned`, the default, keeps a published experiment consistent: an update or preview uses **the version the experiment was published with**; a new experiment uses the one in this branch's `external/access-model-mkfigs`. `latest release` or `master` (unreleased) use something newer, and an update then records the newer version on `eval-<ename>`. Experiments published before this workflow existed need `latest release`. The run's summary says which version ran |

From a terminal, the same thing is e.g.
`gh workflow run mkfigs -R ACCESS-Community-Hub/access-cm3-paper-1 -f mode="new experiment" -f ename=<name> -f esm_file=<path>`.

Once approved, the notebooks run as PBS jobs on Gadi (one job per notebook where this repo's
`access-model-mkfigs` supports it, otherwise one job for all). When they finish, the run's summary page links,
for each experiment:

* **the preview page**, which opens straight in the browser: the website's landing page and every figure and
  caption for the experiment. It is reduced: no rendered notebooks, links to other pages don't work, and the
  figures are compressed;
* **the whole website** as a zip, rendered notebooks included, with the two commands to view it locally;
* a table of which notebooks ran and which failed.

Both are kept for 10 days.

### Making the website for a new experiment

1. Start a run from `main` with mode `new experiment`, `esm_file` and `ename` filled in and `notebooks` left blank.
2. Once it is approved and finished, open the preview and check the figures.
3. If they look right, ask a `mkfigs-publish` approver to approve **publish**. That creates and publishes the
   Figshare article (this cannot be undone), then pushes the `eval-<ename>` branch and tag, from which Read the
   Docs builds the website. If something is wrong, reject it: nothing has been published.

### Adding to or re-running a published experiment

1. Start a run from `main` with mode `update a published experiment`, the experiment's `ename`, and in
   `notebooks` the ones to add or re-run. Leave `esm_file` blank to use the datastore it was published with.
2. The run starts from the experiment's published `eval-<ename>` branch and takes **only those notebooks** from
   `main`; everything else (including `mkfigs.sh`) stays as published. The earlier results are restored from
   Figshare, so the preview shows the whole experiment with the new results in it.
3. If it looks right, a `mkfigs-publish` approver approves **publish**: the new results are added to the same
   Figshare article as a new version, committed on top of `eval-<ename>`, and tagged with the next number.

If an updated notebook needs something else that only changed on `main` (a helper file, or a newer conda
module in `mkfigs.sh`), the run fails and shows it in the preview, before anything is published.

### Previewing a branch (e.g. a PR)

To see what a PR's notebooks produce before merging it:

1. The PR's branch has to be in this repo (contributors with write access already work this way). A PR from a
   fork isn't run: push its branch to this repo first, after reading it.
2. Start a run with **Use workflow from** set to the PR's branch, mode `preview a branch`, in `notebooks` the
   ones the PR adds or changes, and in `ename` the experiments to try them on, e.g.
   `cm3-run-27-07-2026-PD-control`. Each experiment gets its own job and its own preview page; a published one shows the
   whole experiment with the PR's notebooks re-run.
3. An approver approves the run. Approving runs the PR's code on Gadi under the workflow's NCI account, so
   approvers should read the PR first.
4. Link the preview pages in the PR review. Nothing is published.

### Trying a notebook on any run

To see what a notebook makes of a run (say one that has just finished) without logging in to Gadi: start a
run from `main` with mode `preview a branch`, `notebooks` set to the notebook (e.g. `TOA_CRE`), and in `ename`
a name for the run with its datastore, e.g. `my-test-run=/g/data/.../datastore.json`. The preview page and
the zip appear on the run as usual, and nothing is published. The workflow's NCI account needs read access to
the datastore's project.

### If a run stops waiting

GitHub stops a run after 6 hours, so the workflow stops waiting for the PBS jobs after 5. The jobs keep going on
Gadi: start the workflow again with the same `mode` and `ename`, on the same branch, with **pick_up_jobs** ticked,
and it picks them up instead of submitting again.
