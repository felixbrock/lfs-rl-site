# lfs-rl-site instructions

This repo is the public GitHub Pages site for the lfs-rl environment
suite (https://felixbrock.github.io/lfs-rl-site/).

- Before ANY edit to index.html, read STYLE.md in this repo and follow
  it as a checklist, voice, conclusion-first order, claims discipline,
  visualization rules, design constraints, and the edit process.
- Deployment is the GitHub Actions workflow in
  .github/workflows/pages.yml, triggered on push to main. After every
  push, verify the run succeeded (gh run list) and that the LIVE page
  contains the change, deploy failures have silently stranded this
  site before. Transient 429 failures are fixed by gh run rerun.
- Every number on the page must trace to a committed results file in
  the private lfs-rl repo.
