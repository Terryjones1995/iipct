#!/usr/bin/env bash
# Publish the site to the gh-pages branch. GitHub Pages serves that branch as the test site:
#   https://terryjones1995.github.io/iipct/
#
# usage: tools/publish-preview.sh [--dry-run <dir>] [<commit>]      (commit defaults to HEAD)
#
# What it does
#   1. Takes the site files from <commit> (an allow-list): the pages (*.html at the top level), assets/,
#      sitemap.xml, robots.txt, the redirect pages at the old iipct.org addresses listed in
#      tools/redirects/redirect-pages.txt, and .nojekyll. tools/, README.md and everything else stay out.
#   2. Keeps the test copy out of search results: adds <meta name="robots" content="noindex, nofollow"> to every
#      page (the redirect pages already carry noindex) and replaces robots.txt with "Disallow: /".
#      The pages in the repo stay clean for the real launch.
#   3. Points the share tags of the test copy at the test address, so a pasted test link shows its preview card:
#      in the canonical link and the og:url, og:image and twitter:image tags (each on its own line in the head)
#      https://iipct.org/ becomes the test address. Nothing else in a page changes; the structured data and the
#      sitemap keep the real address.
#   4. Commits that as the next commit on gh-pages and pushes it. Nothing in your working folder changes.
#
# --dry-run <dir> writes the files to <dir> (it must be empty or not exist yet) and stops before committing.
# Check a dry run with: python3 -I tools/check-site.py <dir> --preview
set -euo pipefail

DRY=""
if [ "${1:-}" = "--dry-run" ]; then
  DRY="${2:?--dry-run needs a folder}"
  shift 2
fi
REF="${1:-HEAD}"
REMOTE="origin"
BRANCH="gh-pages"
PREVIEW_BASE="/iipct/"      # the path the test site is served under on GitHub Pages
ROBOTS='<meta name="robots" content="noindex, nofollow">'
REAL_URL="https://iipct.org/"                              # tools/generator/seo.py SITE_URL
PREVIEW_URL="https://terryjones1995.github.io/iipct/"      # the test site's address
MANIFEST="tools/redirects/redirect-pages.txt"

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
for f in sitemap.xml robots.txt; do
  [ -f "$TMP/all/$f" ] || { echo "error: no $f in $SHORT (run tools/generator/export_site.py)" >&2; exit 1; }
  cp "$TMP/all/$f" "$TMP/site/$f"
done
: > "$TMP/site/.nojekyll"
redirects=0
if [ -f "$TMP/all/$MANIFEST" ]; then
  while IFS= read -r rel; do
    case "$rel" in ''|'#'*) continue ;; esac
    if ! printf '%s\n' "$rel" | grep -qE '^([a-z0-9-]+/)+index\.html$'; then
      echo "error: unexpected path in $MANIFEST: $rel" >&2; exit 1
    fi
    [ -f "$TMP/all/$rel" ] || { echo "error: $MANIFEST lists $rel, which $SHORT does not have" >&2; exit 1; }
    if ! grep -q '<meta name="robots" content="noindex' "$TMP/all/$rel"; then
      echo "error: redirect page $rel has no noindex tag" >&2; exit 1
    fi
    mkdir -p "$TMP/site/$(dirname "$rel")"
    cp "$TMP/all/$rel" "$TMP/site/$rel"
    redirects=$((redirects + 1))
  done < "$TMP/all/$MANIFEST"
fi

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
printf '# Test copy of the IIPCT website: keep crawlers out. The real site is %s\nUser-agent: *\nDisallow: /\n' "$REAL_URL" \
  > "$TMP/site/robots.txt"

# 3. the share tags of the test copy point at the test address (line-targeted: only these four tags, only in the head)
TAGS='^(<link rel="canonical" href="|<meta property="og:(url|image)" content="|<meta name="twitter:image" content=")'
REAL_RE="${REAL_URL//./\\.}"
while IFS= read -r f; do
  sed -E -i "\#${TAGS}${REAL_RE}#s#${REAL_RE}#${PREVIEW_URL}#" "$f"
  if grep -qE "${TAGS}${REAL_RE}" "$f"; then
    echo "error: ${f#"$TMP/site/"}: a share tag still points at $REAL_URL" >&2; exit 1
  fi
  tagged="$(grep -cE "${TAGS}${PREVIEW_URL}" "$f" || true)"
  total="$({ grep -oF "$PREVIEW_URL" "$f" || true; } | wc -l)"
  if [ "$tagged" != "$total" ]; then
    echo "error: ${f#"$TMP/site/"}: the test address appears outside the four share tags" >&2; exit 1
  fi
done < <(find "$TMP/site" -name '*.html' -not -path "$TMP/site/assets/*")

# The "page not found" page is shown for ANY missing address, however deep (/iipct/contact-us/ for example), so its
# own links must not be relative. On the test site everything lives under /iipct/. (After the domain move the same
# rewrite uses "/" instead.) Links to other sites, mail, phone and in-page anchors are left alone.
if [ -f "$TMP/site/404.html" ]; then
  perl -pi -e 's{(href|src)="(?![a-z][a-z0-9+.-]*:|#|/)}{$1="'"$PREVIEW_BASE"'}g' "$TMP/site/404.html"
  if grep -qE '(href|src)="(assets/|[a-z0-9-]+\.html)' "$TMP/site/404.html"; then
    echo "error: 404.html still has relative links after the rewrite" >&2
    exit 1
  fi
fi

if [ -n "$DRY" ]; then
  if [ -e "$DRY" ] && [ -n "$(ls -A "$DRY" 2>/dev/null)" ]; then
    echo "error: $DRY is not empty" >&2
    exit 1
  fi
  mkdir -p "$DRY"
  cp -R "$TMP/site/." "$DRY/"
  echo "dry run: $pages pages and $redirects redirect pages from $SHORT written to $DRY (nothing committed or pushed)"
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
echo "published $pages pages and $redirects redirect pages from $SHORT to $BRANCH ($(git rev-parse --short "$COMMIT"))"
