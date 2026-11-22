#!/usr/bin/env bash
# Publish the site to the gh-pages branch. GitHub Pages serves that branch as the test site:
#   https://terryjones1995.github.io/iipct/
#
# usage: tools/publish-preview.sh [--dry-run <dir>] [<commit>]      (commit defaults to HEAD)
#
# What it does
#   1. Takes the site files from <commit>: the pages (*.html at the top level), assets/ and .nojekyll.
#      tools/, README.md and everything else stay out of the published copy.
#   2. Adds <meta name="robots" content="noindex, nofollow"> to every page, so search engines keep the
#      test copy out of their results. The pages in the repo stay clean for the real launch.
#   3. Commits that as the next commit on gh-pages and pushes it. Nothing in your working folder changes.
#
# --dry-run <dir> writes the files to <dir> (it must be empty or not exist yet) and stops before committing.
set -euo pipefail

DRY=""
if [ "${1:-}" = "--dry-run" ]; then
  DRY="${2:?--dry-run needs a folder}"
  shift 2
fi
REF="${1:-HEAD}"
REMOTE="origin"
BRANCH="gh-pages"
ROBOTS='<meta name="robots" content="noindex, nofollow">'

cd "$(git rev-parse --show-toplevel)"
SHA="$(git rev-parse --verify "$REF^{commit}")"
SHORT="$(git rev-parse --short "$SHA")"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir "$TMP/all" "$TMP/site"

# 1. the site files of that commit (an allow-list: anything new in the repo stays private until it is added here)
git archive "$SHA" | tar -x -C "$TMP/all"
cp "$TMP"/all/*.html "$TMP/site/"
cp -R "$TMP/all/assets" "$TMP/site/assets"
: > "$TMP/site/.nojekyll"

# 2. keep the test copy out of search results
pages=0
for f in "$TMP"/site/*.html; do
  if grep -qi '<meta name="robots"' "$f"; then
    echo "error: $(basename "$f") already has a robots meta tag; publish expects clean pages" >&2
    exit 1
  fi
  awk -v tag="$ROBOTS" '{ print } /<meta name="viewport"/ && !done { print tag; done = 1 }' "$f" > "$f.tmp"
  mv "$f.tmp" "$f"
  if [ "$(grep -c -F "$ROBOTS" "$f")" != "1" ]; then
    echo "error: could not add the robots tag to $(basename "$f") (no viewport meta line?)" >&2
    exit 1
  fi
  pages=$((pages + 1))
done
[ "$pages" -gt 0 ] || { echo "error: no pages found in $SHORT" >&2; exit 1; }
[ -f "$TMP/site/index.html" ] || { echo "error: no index.html in $SHORT" >&2; exit 1; }

if [ -n "$DRY" ]; then
  if [ -e "$DRY" ] && [ -n "$(ls -A "$DRY" 2>/dev/null)" ]; then
    echo "error: $DRY is not empty" >&2
    exit 1
  fi
  mkdir -p "$DRY"
  cp -R "$TMP/site/." "$DRY/"
  echo "dry run: $pages pages from $SHORT written to $DRY (nothing committed or pushed)"
  exit 0
fi

# 3. commit on gh-pages without touching the working folder, then push
GIT_DIR_ABS="$(git rev-parse --absolute-git-dir)"
PARENT=""
if git fetch --quiet "$REMOTE" "$BRANCH" 2>/dev/null; then
  PARENT="$(git rev-parse --verify FETCH_HEAD)"
fi
TREE="$(cd "$TMP/site" && GIT_INDEX_FILE="$TMP/index" git --git-dir="$GIT_DIR_ABS" --work-tree="$TMP/site" add -A . \
        && GIT_INDEX_FILE="$TMP/index" git --git-dir="$GIT_DIR_ABS" write-tree)"
if [ -n "$PARENT" ] && [ "$(git rev-parse "$PARENT^{tree}")" = "$TREE" ]; then
  echo "gh-pages already matches $SHORT: nothing to publish"
  exit 0
fi
MSG="Publish test site from $SHORT"
if [ -n "$PARENT" ]; then
  COMMIT="$(git commit-tree "$TREE" -p "$PARENT" -m "$MSG")"
else
  COMMIT="$(git commit-tree "$TREE" -m "$MSG")"
fi
git push "$REMOTE" "$COMMIT:refs/heads/$BRANCH"
echo "published $pages pages from $SHORT to $BRANCH ($(git rev-parse --short "$COMMIT"))"
