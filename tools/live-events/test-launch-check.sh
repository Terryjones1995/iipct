#!/usr/bin/env bash
# Tests the --launch refusal in tools/publish-preview.sh WITHOUT running that script: it takes the script's
# REAL_URL line and its live_events_check block (between the ">>> live_events_check" and "<<< live_events_check"
# markers), and runs that function on throwaway folders. Never shipped.
# usage (from the repo root): bash tools/live-events/test-launch-check.sh [<folder with a commit's files> ...]
set -uo pipefail
SCRIPT=tools/publish-preview.sh
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
eval "$(grep -m 1 '^REAL_URL=' "$SCRIPT")"
eval "$(sed -n '/^# >>> live_events_check/,/^# <<< live_events_check/p' "$SCRIPT")"
type live_events_check > /dev/null || { echo "FAIL: no live_events_check block in $SCRIPT"; exit 1; }
fails=0
site() {   # <name> <LIVE_SITE line or ""> <data-site on the pages or "" for no reader>
  local d="$TMP/$1"; mkdir -p "$d/tools/generator"
  [ -n "$2" ] && printf '%s\n' "$2" > "$d/tools/generator/lib.py"
  if [ -n "$3" ]; then
    printf '<p>x</p><script defer src="assets/js/live-events.js" data-site="%s"></script>\n' "$3" > "$d/index.html"
  else
    printf '<p>x</p>\n' > "$d/index.html"
  fi
}
expect() {   # <name> <0 = allowed | 1 = refused>
  local out rc; out="$(live_events_check "$TMP/$1" 2>&1)"; rc=$?
  if [ "$rc" = "$2" ]; then echo "ok    $1 -> $([ "$rc" = 0 ] && echo allowed || echo refused)${out:+: ${out%%$'\n'*}}"
  else echo "FAIL  $1 -> exit $rc, wanted $2: $out"; fails=$((fails + 1)); fi
}
site test-address 'LIVE_SITE = "https://taylordunning.ca"' 'https://taylordunning.ca';           expect test-address 1
site test-address-single-quotes "LIVE_SITE = 'https://taylordunning.ca'  # comment" '';           expect test-address-single-quotes 1
site off 'LIVE_SITE = ""' '';                                                                         expect off 0
site off-single-quotes "LIVE_SITE = ''  # off" '';                                                    expect off-single-quotes 0
site off-but-stale-pages 'LIVE_SITE = ""' 'https://taylordunning.ca';                              expect off-but-stale-pages 1
site real-address 'LIVE_SITE = "https://iipct.org"' 'https://iipct.org';                              expect real-address 1
site real-address-no-pages 'LIVE_SITE = "https://iipct.org"' '';                                      expect real-address-no-pages 1
site unreadable 'LIVE_SITE = os.environ["X"]' '';                                                     expect unreadable 1
site twice "$(printf 'LIVE_SITE = ""\nLIVE_SITE = "https://taylordunning.ca"')" '';               expect twice 1
site indented "$(printf 'if True:\n    LIVE_SITE = "https://taylordunning.ca"')" '';             expect indented 1
site before-the-feature '' '';                                                                        expect before-the-feature 0
site no-constant-but-reader '' 'https://taylordunning.ca';                                         expect no-constant-but-reader 1
# a page with the reader's attributes in the other order, a reader file with no page tag, a footer sign-in link alone
site swapped-attrs 'LIVE_SITE = ""' ''
printf '<script defer data-site="https://taylordunning.ca" src="assets/js/live-events.js"></script>\n' > "$TMP/swapped-attrs/index.html"
expect swapped-attrs 1
site js-file-only 'LIVE_SITE = ""' ''
mkdir -p "$TMP/js-file-only/assets/js"; printf 'x' > "$TMP/js-file-only/assets/js/live-events.js"
expect js-file-only 1
site sign-in-only 'LIVE_SITE = ""' ''
printf '<footer><a class="fl" href="https://taylordunning.ca/login">Sign in</a></footer>\n' > "$TMP/sign-in-only/about.html"
expect sign-in-only 1
for dir in "$@"; do   # real commits: name the expectation in the folder name (…-refused / …-allowed)
  case "$dir" in *-refused) want=1 ;; *-allowed) want=0 ;; *) echo "skip $dir (name it …-refused or …-allowed)"; continue ;; esac
  rm -rf "$TMP/commit"; cp -R "$dir" "$TMP/commit"; out="$(live_events_check "$TMP/commit" 2>&1)"; rc=$?
  if [ "$rc" = "$want" ]; then echo "ok    $(basename "$dir") -> exit $rc${out:+: ${out%%$'\n'*}}"; else echo "FAIL  $(basename "$dir") -> exit $rc: $out"; fails=$((fails + 1)); fi
done
# the ordinary test publish never calls the check: its only call sits behind the --launch flag
calls="$(grep -n 'live_events_check "' "$SCRIPT")"
if [ "$(printf '%s\n' "$calls" | wc -l)" = 1 ] && printf '%s\n' "$calls" | grep -q 'if \[ -n "\$LAUNCH" \]; then live_events_check'; then
  echo "ok    the check runs only with --launch: $calls"
else
  echo "FAIL  unexpected calls: $calls"; fails=$((fails + 1))
fi
bash -n "$SCRIPT" && echo "ok    bash -n $SCRIPT" || { echo "FAIL  bash -n"; fails=$((fails + 1)); }
echo "failures: $fails"
exit "$fails"
