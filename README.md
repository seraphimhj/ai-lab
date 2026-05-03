# ai-lab

My personal lab for learning & tinkering with deep learning and LLMs.

## Layout

```
ai-lab/
├── notebooks/         Jupyter experiments I write
├── notes/             Markdown notes & reading logs
├── experiments/       Standalone scripts
├── scripts/
│   └── bootstrap.sh   Clone all 3rd-party repos listed in repos.txt
├── repos.txt          List of 3rd-party repos I reference (URLs only)
├── repos/             (gitignored) 3rd-party repos live here after bootstrap
├── data/              (gitignored) datasets, never committed
└── .venv/             (gitignored) uv-managed virtualenv
```

## Setup on a new machine

```bash
git clone <this-repo> ai-lab && cd ai-lab

# 1. Python env + deps
uv sync

# 2. Pull the 3rd-party repos I'm studying
bash scripts/bootstrap.sh

# 3. Launch Jupyter
uv run jupyter lab
```

## Daily workflow

- `uv add <pkg>`              add a dependency (updates pyproject.toml + uv.lock)
- `uv run python foo.py`      run under the project's venv
- `uv run jupyter lab`        launch Jupyter
- Add a new reference repo:   append URL to `repos.txt`, rerun `bootstrap.sh`

## Sync across machines

Only **my own** content is in git: notes, notebooks, scripts, dependency manifests.
Third-party repos are re-cloned from `repos.txt` on each machine. Datasets and
model weights are never committed; keep them local or fetch via a script.
