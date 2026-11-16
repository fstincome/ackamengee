# Architecture rules

- Keep user-guide content in `src/content/user-guide.json` and use it for both the guide page and the prebuilt PDF so the two editions stay aligned.
- Serve the fixed user-guide PDF from `public/downloads/` through a same-origin download link; regenerate it with `scripts/generate-user-guide.py` when guide content changes to avoid browser PDF-generation dependencies.