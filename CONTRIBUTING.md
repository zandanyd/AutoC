# Repo principles:

## Git

## Legal

We have tried to make it as easy as possible to make contributions. This applies to how we handle the legal aspects of contribution. We use the same approach - the Developer's Certificate of Origin 1.1 (DCO) - that the Linux® Kernel community uses to manage code contributions.

We simply ask that when submitting a patch for review, the developer must include a sign-off statement in the commit message.

Here is an example Signed-off-by line, which indicates that the submitter accepts the DCO:

Signed-off-by: John Doe <john.doe@example.com>
You can include this automatically when you commit a change to your local git repository using the following command:

git commit -s

### Commit
Always commit with a [good commit message](https://cbea.ms/git-commit/) and sign off:

Example:

```bash
git commit -s
```

### Push
Push into a new branch and open a PR.

Example:

```bash
git push origin master:<my-new-branch-name>
```

### Merge your PR to master
Use squash and merge to merge your PR to master.
