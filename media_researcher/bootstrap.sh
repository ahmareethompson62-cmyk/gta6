#!/bin/bash
# Fetch/update the gta-deep-dive tools (media_researcher + preserved YouTube editor code) into $HOME/gta-deep-dive-tools.
# Read access works for the public repo without attaching it. Pushing plans / running workflows needs the repo attached with write access
# (mcp__claude-code-remote__add_repo owner=ahmareethompson62-cmyk repo=gta6 access=push, then clone that repo and pass --repo-dir).
set -e
T=${GDD_TOOLS:-$HOME/gta-deep-dive-tools}
if [ -d "$T/.git" ]; then git -C "$T" pull -q --ff-only; else git clone -q --depth 1 https://github.com/ahmareethompson62-cmyk/gta6 "$T"; fi
pip install -q pillow requests 2>/dev/null || pip install -q --break-system-packages pillow requests
echo "tools ready: $T"; ls "$T/media_researcher" | tr '\n' ' '; echo
