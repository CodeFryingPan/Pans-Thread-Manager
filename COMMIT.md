# How to properly commit to Pan's Kitchen?

We will lock the main from bring pushed right away and only allow pull requests. 

Requirements for Pull Requests:
    1. Github Account
    2. Create Branch
    3. Pull Request
    4. Approval

## Github Account

Please create your github account through [here](https://github.com/signup) .

## Create Branch

### Naming the branch

We will have 3 different branch types:
    1. Feature (Adding a new feature)
    2. Update (Removing/Cleanups/Update to a previous feature)
    3. Fix (Fixing a bug)

Name the branches according like this:
```
username/type/what-you-are-doing
```

Here are some examples:
```
tamphilip/feature/adding-upvotes

tamphilip/update/cleaning-up-integration-tests

tamphilip/fix/fixing-routes-to-discord
```

### Create your branch with your command and checkout!

```bash

git checkout -b "tamphilip/feature/updating-commit-read-me"

```

This will automatically create your branch and checkout and now you're ready to work on your feature/update/fix.

## Pull Request

### Pushing your code to Github

Once you are ready to push you can git add everything you've changed (Or specify what files) and then git push your branch to Github.

Add everything:
```bash

git commit . ; git push

```

To specify:
```bash

git commit <directory/files> ; git push

```

It'll ask you to set upstream and then follow the steps to do set the remote.

Don't forget to pull everything from the main branch first and then merge

```bash

git pull 
git merge 

```

Once this is done feel free to make your pull request

## Making the pull request

[Make your pull request here](https://github.com/CodeFryingPan/Pans-News-Feed-Bot/compare)

Update the description according to the template and you're ready for approval.

Now wait for approval and make updates if necessary asked to and merge when you can!