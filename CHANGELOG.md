# bear-notes changelog

## 2026-03-14

### New capabilities
- Added `create_or_append_note.py` as the main workflow entrypoint.
- Added `decide_note_action.py` for lightweight create/append routing.
- Added `suggest_title.py` for rough title suggestion.
- Added `recommend_tags.py` for lightweight tag recommendation.
- Added experimental `append_bear_note.py` for appending to existing Bear notes.
- Added public release materials: `README.md`, `LICENSE`, `REPO_METADATA.md`, `PUBLISHING.md`, `release-checklist.md`.

### Fixes
- Fixed AppleScript long-Chinese-note write failures by switching Bear create flow to URL + `open`.
- Fixed duplicate leading H1 in rendered markdown.
- Fixed duplicate leading tags in rendered markdown.
- Fixed Bear create flow to strip leading H1 and tags from note body before sending, preventing duplicate title/tag display inside Bear notes.

### Current limitations
- Append still relies on front-end UI automation and may be sensitive to UI/focus/language changes.
- Intelligent similarity-based append/new-note routing is not implemented yet.
- Title suggestion is still heuristic and needs further refinement.
