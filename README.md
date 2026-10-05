# Website Capture and HTML Editor

**An early Streamlit prototype for capturing a page's HTML, storing it in SQLite, and editing saved content.**

## What it demonstrates

- Fetching a page with Requests and parsing it with Beautiful Soup.
- Rewriting relative asset and navigation URLs into absolute URLs.
- Saving HTML snapshots and timestamps in SQLite.
- A Streamlit interface for browsing and editing captured pages.

This version uses HTTP fetching and HTML processing. It does not include an LLM workflow or rebuild a website's private backend. It is an earlier exploration alongside the [Website Fabricator prototype](https://github.com/ahsaan-10/AA---wc).

## Run the main interface

```bash
git clone https://github.com/ahsaan-10/Web-cloner.git
cd Web-cloner
python -m venv .venv
```

Activate the environment, then:

```bash
python -m pip install streamlit requests beautifulsoup4
python -m streamlit run app.py
```

The main application initializes its local `cloned_sites.db` table on startup. This entry point does not require a browser automation installation.

## Repository map

```text
app.py          Main capture and editing application
cms.py          Additional file in the original experiment
test_script.py  Supporting experiment script
*.db            Databases bundled with the original project
```

## Scope

Use this to demonstrate Python web tooling and simple persistence. JavaScript-rendered applications and authenticated flows are outside the main HTTP capture approach. Only capture sites you own or have permission to use. The bundled databases and earlier code drafts should be reviewed before presenting a cleaned source release.
