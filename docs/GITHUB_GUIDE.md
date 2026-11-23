# Publish to GitHub (first release)

1. Log in to GitHub and create a **new empty** repository, e.g. `pedagogical-triad-framework`, without pre-populating it with another README.
2. Open the extracted directory in VS Code. Run `python run.py analyze` and `python -m unittest discover -s tests -v`.
3. In Terminal, run:

```bash
git init
git add .
git commit -m "feat: initialize reproducible pedagogical triad research prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pedagogical-triad-framework.git
git push -u origin main
```

GitHub authentication may require a browser login, GitHub CLI or a credential manager. **Do not publish tokens or passwords.** Replace `YOUR_USERNAME` yourself. If `origin` already exists, review `git remote -v` rather than blindly repeating the command.

## Suggested next milestones

- Source-review log with report year/page/table and reproducible extraction scripts
- Qualified Bangla translation and cognitive interview protocol
- IRB-approved instrument pilot; real-data privacy workflow
- School-stratified and multilevel analysis with sensitivity checks
- A complete reproducible methods preprint and properly cited manuscript
