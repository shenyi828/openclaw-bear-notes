# Publishing guide for `bear-notes`

## 1. Set public git identity for this repo only

Use your main GitHub identity, but prefer GitHub's noreply email instead of a private mailbox.

```bash
git config user.name "YOUR_PUBLIC_GITHUB_NAME"
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
```

GitHub noreply format is usually one of these:

- `12345678+username@users.noreply.github.com`
- `username@users.noreply.github.com`

Check GitHub Settings → Emails.

## 2. Rewrite recent local commits to use the public identity

Because earlier commits used an auto-generated local identity, amend them before pushing publicly.

If only the latest commit needs correction:

```bash
git commit --amend --reset-author
```

If several recent commits need correction, interactive rebase them:

```bash
git rebase -i HEAD~3
```

Mark commits as `edit`, then for each stopped commit:

```bash
git commit --amend --no-edit --reset-author
git rebase --continue
```

## 3. Create a clean public repository

Suggested repo name:

```text
openclaw-bear-notes
```

## 4. Push to GitHub

After creating the empty repository on GitHub:

```bash
git remote add origin <YOUR_REPO_URL>
git push -u origin main
```

## 5. Configure GitHub repo page

- Add repo description from `REPO_METADATA.md`
- Add suggested topics
- Add initial release notes
- Optionally add a screenshot or short demo GIF

## 6. Optional cleanup before first push

- confirm no private file paths remain in README/examples/scripts
- confirm no personal note samples are included
- confirm LICENSE year/owner matches what you want public

## 7. Recommended first public positioning

Use `public beta` / `experimental` wording rather than implying perfect stability.
