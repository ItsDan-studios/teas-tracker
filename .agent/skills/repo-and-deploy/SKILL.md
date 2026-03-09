---
name: repo-and-deploy
description: Create a GitHub repository and deploy the project to Vercel. Handles git commit, GitHub repo creation, Vercel deployment, build error fixes, and returns both live links.
---
# repo-and-deploy

End-to-end skill for publishing a local project: commit all changes, create a GitHub repo, deploy to Vercel, fix any build issues, and share both links in chat.

## Prerequisites

Check that both CLIs are installed and authenticated:

```bash
gh auth status
vercel --version
```

If GitHub CLI is not installed:

**macOS:**
```bash
brew install gh && gh auth login
```

**Windows:**
```powershell
winget install GitHub.cli
gh auth login
```

If Vercel CLI is not installed:

```bash
npm install -g vercel
vercel login
```

---

## How to Use This Skill

When the user asks to "create a repo and deploy" or "push to GitHub and Vercel", follow these steps in order.

---

### Step 1: Check Git Status

```bash
git status
```

Review what is staged, modified, deleted, or untracked. Do NOT blindly stage everything — exclude:
- Temp files (`*.~tmp`, `*.log`)
- Sensitive files (`.env`, credentials)
- Unused assets that are not referenced in code

---

### Step 2: Stage and Commit

Stage relevant files explicitly (prefer named files over `git add .`):

```bash
git add src/ public/images/<used-images> .gitignore package-lock.json
```

Then commit:

```bash
git commit -m "$(cat <<'EOF'
<Short summary of changes>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

### Step 3: Create GitHub Repo and Push

```bash
gh repo create <repo-name> --public --source=. --remote=origin --push
```

- Use `--public` unless the user specifies private
- This creates the repo, sets `origin`, and pushes in one command
- Note the GitHub URL from the output

---

### Step 4: Deploy to Vercel

```bash
vercel --yes
```

- `--yes` accepts all auto-detected settings (framework, build command, output dir)
- Vercel auto-detects Vite, Next.js, CRA, etc.
- Note both the preview URL and the aliased production URL from the output

**Vercel automatically connects to GitHub**, so all future pushes to `master`/`main` will trigger redeployments.

---

### Step 5: Check for Build Warnings or Errors

Read the build output carefully. Common issues to fix immediately:

| Issue | Fix |
|---|---|
| CSS `@import` order warning | Move third-party `@import` (Google Fonts, etc.) **before** `@import "tailwindcss"` |
| Missing image files | Replace broken `src` references with available images |
| Unused import errors | Remove the unused import from the file |
| TypeScript type errors | Resolve type mismatches before redeploying |

After fixing, commit and push to trigger an automatic redeploy:

```bash
git add <fixed-file>
git commit -m "Fix <issue description>"
git push
```

---

### Step 6: Share Links in Chat

After a clean build, output both links to the user:

```
- GitHub: https://github.com/<username>/<repo-name>
- Vercel:  https://<repo-name>.vercel.app
```

---

## Example Workflow

**User:** "create repo and deploy"

### Step 1: Check status
```bash
git status
# → modified: src/, untracked: public/images/unsplash*.jpg
```

### Step 2: Stage and commit
```bash
git add src/ public/images/unsplash1.jpg public/images/unsplash2.jpg .gitignore
git commit -m "Initial redesign: text logo, services plans, marquee testimonials"
```

### Step 3: Create repo and push
```bash
gh repo create chairezlandscape --public --source=. --remote=origin --push
# → https://github.com/ItsDan-studios/chairezlandscape
```

### Step 4: Deploy
```bash
vercel --yes
# → Production: https://chairezlandscape.vercel.app
```

### Step 5: Fix build warning
Build output showed CSS `@import` order warning. Fix in `src/index.css`:
- Move `@import url('https://fonts.googleapis.com/...')` above `@import "tailwindcss"`
- Commit and push → Vercel auto-redeploys

### Step 6: Share links
```
- GitHub: https://github.com/ItsDan-studios/chairezlandscape
- Vercel:  https://chairezlandscape.vercel.app
```

---

## Common Rules

### Git
- Never use `git add .` or `git add -A` — stage files explicitly
- Never commit `.env`, credentials, or temp files (`*.~tmp`)
- Never force push unless user explicitly asks
- Always write a meaningful commit message

### GitHub
- Default to `--public` unless told otherwise
- One command creates repo + sets remote + pushes: `gh repo create ... --source=. --remote=origin --push`

### Vercel
- Always use `vercel --yes` to skip interactive prompts
- Vercel connects to GitHub automatically — no manual webhook setup needed
- Future pushes to `master`/`main` auto-deploy — tell the user this

### Build Fixes
- Fix all warnings before declaring the deployment done
- Push fixes and confirm the redeploy is clean
- Do not leave `[PLACEHOLDER]` content as a blocker — note it but don't fail the deploy
