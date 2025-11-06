---
name: Issue template for adding a Figure to polished-python 
about: 
title: ''
labels: ''
assignees: ''

---

### Issue description

Please describe your Figure here.

### Check list

There's a lot of items but many of them take a few seconds to do.

For polished python commits:

- [ ] When creating the notebook the template was [used](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/notebooks/polished-python/00_template_notebook.ipynb). Specifically:
 - [ ] using ESM datastore ("cell 3? from the template" -- give it a name?)
 - [ ] using intake (not an open netcdf command)
 - [ ] check that comparison of CM3 vs CM2 is using the "recommended CM2" data source
- [ ] check if there are observations being read in, are they on a project that we can access.
- [ ] does it run, add it to mkfigs.sh and run it on a new branch as a script on ARE or submit it as a job (change user specific things)
 - [ ]  check that [figure creation guidelines](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1?tab=readme-ov-file#guidelines-for-creating-figures) have been followed (where practical) 
- [ ] When posting the Figure in the issue below, I have included:
 - [ ] `include path to notebook`
 - [ ] `the commit hash that created the Figure` 
 - [ ] `which CM3 simulation was analysed`
- [ ] added [authorship details](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/blob/main/CITATION.cff) to `CITATION.cff`

For [mega issue](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1):
- [ ] create issue for each evaluation diagnostic;
- [ ] add new issue as a sub-issue to [the mega issue](https://github.com/ACCESS-Community-Hub/access-cm3-paper-1/issues/1);
- [ ] check "ticked off" when person contributes script;
- [ ] create link on mega issue to relevant script (once created);
- [ ] Before the next `CM3 Dev-Eval Working group` meeting share in the related meeting post [here](https://forum.access-hive.org.au/t/cm3-dev-eval-working-group-meeting-minutes-2025/5393?u=cbull).
