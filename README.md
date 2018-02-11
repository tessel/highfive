Tessel highfive
===============

This is a fork of http://github.com/nrc/highfive designed to be a single
rebased commit over the original. It's adapted to run as a Dokku app.
See our [WWW guidelines](https://github.com/tessel/project/blob/master/WWW.md)
for more information on deploying.

```
git remote add dokku dokku@dokku.tessel.io:highfive
git push dokku master
```

To rebase:

```
git remote add nrc http://github.com/nrc/highfive
git rebase nrc master
```

---

Highfive
========

GitHub hooks to provide an encouraging atmosphere for new contributors

Install
=======

To install `highfive` you just need to execute the `setup.py` script or use
`pip` directly. Both commands have to be executed from the directory where the
`setup.py` script is located.

    $ python setup.py install

or

    $ pip install . # the dot is important ;)


Testing
=======

To run tests, make sure the test-requirements are installed by running:

    $ pip install -r test-requirements.txt


Once the dependencies are installed, you can run tests by executing:

    $ nosetests

Adding a Project
================

To make rust-highfive interact with a new repo, add a configuration file in
`highfive/configs`, with a filename of the form `reponame.json`.

It should look like:

```
{
    "groups":{
        "all": ["@username", "@otheruser"],
        "subteamname": ["@subteammember", "@username"]
    },
    "dirs":{
        "dirname":  ["subteamname", "@anotheruser"]
    },
    "contributing": "http://project.tld/contributing_guide.html",
    "expected_branch": "develop"
}   
```

The `groups` section allows you to alias lists of usernames. You should
specify at least one user in the group "all"; others are optional.

The `dirs` section is where you map directories of the repo to users or
groups who're eligible to review PRs affecting it. This section can be left
blank.

`contributing` specifies the contribution guide link in the message which
welcomes new contributors to the repository. If `contributing` is not
present, the [Rust contributing.md][rustcontrib] will be linked instead.

If PRs should be filed against a branch other than `master`, specify the
correct destination in the `expected_branch` field. If `expected_branch` is
left out, highfive will assume that PRs should be filed against `master`.
The bot posts a warning on any PR that targets an unexpected branch.

Enabling a Repo
---------------

Once the hooks for a repository are set up, visit the repo's webhook settings
page at `https://github.com/org/repo/settings/hooks`.

Create a new webhook, pointing at your highfive instance's location:

Payload URL: `http://99.88.777.666/highfive/newpr.py`
Content type: `application/x-www-form-urlencoded`
Leave the 'secret' field blank.
Let me select individual events: Issue comment, pull request
Check the box by 'Active'

[rustcontrib]: https://github.com/rust-lang/rust/blob/master/CONTRIBUTING.md
