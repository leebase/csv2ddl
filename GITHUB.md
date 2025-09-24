# Publishing to GitHub and Enabling CI

This guide walks through creating a GitHub repository, pushing the existing project, and activating GitHub Actions so the off-by-default `ci.yml` workflow starts running.

## 1. Create the Repository on GitHub
1. Sign in at https://github.com and click **New repository**.
2. Choose an organization or your personal account, then set the repository name (e.g., `csv2ddl`).
3. Leave the repository empty—do not initialize with a README, .gitignore, or license (we already have those).
4. Pick visibility (public or private) and click **Create repository**. GitHub shows you the remote URL to use.

## 2. Add a Git Remote Locally
Run these commands from your project root on the machine that has the canonical `.git` history:
```bash
git remote add origin https://github.com/leebase/csv2ddl.git
```
If you fork the project, swap the URL for your fork. Verify:
```bash
git remote -v
```
You should see `origin` listed twice (fetch/push).

## 3. Push the Existing History
Push the current branch to GitHub (here we assume `main`):
```bash
git push -u origin main
```
`-u` sets `origin/main` as the upstream, so future `git push` or `git pull` commands know which branch to target.

## 4. Confirm GitHub Actions Trigger
After the push, navigate to the repository on GitHub. A yellow dot or green check next to the latest commit indicates the workflow started. To inspect:
1. Click the **Actions** tab.
2. Select the `CI` workflow run. You’ll see steps like “Checkout,” “Set up Python,” “Install dependencies,” and “Run tests.”

## 5. Update the README Badge
Once the workflow succeeds, the badge in `README.md` should point at your repository. For this project it is already set to:
```markdown
![CI](https://github.com/leebase/csv2ddl/actions/workflows/ci.yml/badge.svg)
```
Adjust the path if you are working from a fork.

## 6. Future Development Workflow
- Make changes locally, commit, and push to `main` (or feature branches).
- GitHub Actions automatically runs `ci.yml`; watch the Actions tab if a run fails.
- Open pull requests when collaborating; the workflow status appears on PRs to help reviewers.

That’s all—once the remote is set and the first push completes, the CI pipeline runs on every update automatically.
