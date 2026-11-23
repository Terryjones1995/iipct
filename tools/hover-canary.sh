#!/usr/bin/env bash
# Canary for tools/hover-check.mjs: on a copy of the site, remove ONE hover rule from the stylesheet (the footer and
# dark-band links' colour, ".fl:hover, .dl:hover") and expect the check to go red, naming those links.
# usage: tools/hover-canary.sh <site-dir>      (run it through hof-heavy: it starts Chrome)
# Exit 0 = the check caught the missing rule; 1 = it did not (the check proves nothing); 2 = the canary could not run.
set -u
SITE=$(cd "${1:-.}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp -d /tmp/hover-canary-XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$SITE"/*.html "$TMP"/ && cp -r "$SITE/assets" "$TMP/assets" || exit 2
python3 -I - "$TMP/assets/css/site.css" <<'PY' || exit 2
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
rule = '  .fl:hover, .dl:hover {\n    color: #E3BE74 !important;\n  }\n'
n = s.count(rule)
if n != 1:
    sys.exit(f'canary: expected the rule once in the stylesheet, found it {n} times')
open(p, 'w', encoding='utf-8').write(s.replace(rule, ''))
print('canary: removed ".fl:hover, .dl:hover { color: #E3BE74 }" from a copy of the stylesheet')
PY
OUT=$(node "$HERE/hover-check.mjs" "$TMP" --pages index.html,contact.html --no-focus 2>&1); CODE=$?
echo "$OUT" | grep -E 'no hover change|controls without a hover change|AT [0-9]+px' | head -8
echo "$OUT" | grep -E '^ +[0-9]+x a\.fl' | head -4
if [ "$CODE" -eq 1 ] && echo "$OUT" | grep -qE '^ +[0-9]+x a\.fl'; then
  echo "CANARY OK: without the rule the check fails (exit $CODE) and names the footer links"
  exit 0
fi
echo "CANARY FAILED: the check exited $CODE without naming the footer links"
exit 1
