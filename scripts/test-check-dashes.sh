#!/usr/bin/env bash
#
# Proves that scripts/check-dashes.sh catches what it must, and only that, under a
# given bash, including the macOS /bin/bash (3.2), where the old script passed
# everything. Copied from 1212-Capital/app, plus .mdx and .txt cases:
#
#   bash scripts/test-check-dashes.sh
#   BASH_BIN=/bin/bash bash scripts/test-check-dashes.sh
#
# Each case runs the script in a throwaway git repository. Must fail, naming the file:
# an em dash, an en dash, an em dash in .mdx, an &mdash; entity, both dashes in one file, --quiet (exit 1,
# no output). Must pass: a clean tree, a dash under design/ or node_modules/ (excluded),
# a line carrying the allow marker.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASH_BIN="${BASH_BIN:-bash}"
EM="$(printf '\342\200\224')"
EN="$(printf '\342\200\223')"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "check-dashes self-test under $("$BASH_BIN" -c 'echo "bash $BASH_VERSION"')"

failures=0
n=0

# new_case: a fresh repository holding a copy of the script, in $d. Not called in a
# subshell, so each case gets its own directory.
new_case() {
  n=$((n + 1))
  d="$WORK/case-$n"
  mkdir -p "$d/scripts"
  cp "$HERE/check-dashes.sh" "$d/scripts/check-dashes.sh"
  git -C "$d" init -q
}

# run_case <dir> <expect: fail|pass> <name> [file the output must name] [script args]
run_case() {
  local dir="$1" expect="$2" name="$3" must_name="${4:-}"
  shift 4 || shift $#
  git -C "$dir" add -A -f
  local out code=0
  out="$(cd "$dir" && "$BASH_BIN" scripts/check-dashes.sh "$@" 2>&1)" || code=$?
  local ok=1
  if [ "$expect" = fail ]; then
    [ "$code" -eq 1 ] || ok=0
    if [ -n "$must_name" ] && ! printf '%s' "$out" | grep -qF -- "$must_name"; then ok=0; fi
  else
    [ "$code" -eq 0 ] || ok=0
  fi
  if [ "$ok" -eq 1 ]; then
    echo "ok   $name"
  else
    echo "FAIL $name (exit $code, expected to $expect)"
    printf '%s\n' "$out" | sed 's/^/     /'
    failures=$((failures + 1))
  fi
}

new_case; printf 'A title %s with an em dash\n' "$EM" > "$d/probe.md"
run_case "$d" fail "an em dash in a .md file fails" "probe.md"

new_case; printf 'const label = "1 %s 31 July";\n' "$EN" > "$d/probe.ts"
run_case "$d" fail "an en dash in a .ts file fails" "probe.ts"

new_case; printf '# A page %s in MDX\n' "$EM" > "$d/page.mdx"
run_case "$d" fail "an em dash in a .mdx page fails (this copy also reads .mdx, .mjs and .txt)" "page.mdx"

new_case; printf 'The firm %s summary\n' "$EN" > "$d/llms.txt"
run_case "$d" fail "an en dash in a .txt file fails" "llms.txt"

new_case; printf '<p>A &mdash; entity</p>\n' > "$d/probe.html"
run_case "$d" fail "an &mdash; entity in a .html file fails" "probe.html"

new_case; printf 'one %s\ntwo %s\n' "$EM" "$EN" > "$d/both.json"
run_case "$d" fail "an em dash and an en dash in one file fail, both listed" "2 em dash or en dash to remove"

new_case; printf 'quiet %s\n' "$EM" > "$d/quiet.md"
out="$(cd "$d" && git add -A && "$BASH_BIN" scripts/check-dashes.sh --quiet 2>&1)" && code=0 || code=$?
if [ "$code" -eq 1 ] && [ -z "$out" ]; then echo "ok   --quiet fails with no output"; else echo "FAIL --quiet (exit $code, output: $out)"; failures=$((failures + 1)); fi

new_case; printf 'A plain line - with a hyphen, and 1-31 July.\n' > "$d/clean.md"
run_case "$d" pass "a clean tree passes"

new_case; mkdir -p "$d/design" "$d/node_modules/pkg"
printf 'excluded %s\n' "$EM" > "$d/design/notes.md"; printf 'excluded %s\n' "$EN" > "$d/node_modules/pkg/index.js"
run_case "$d" pass "a dash under design/ or node_modules/ is excluded"

new_case; printf 'The character %s is banned. check-dashes:allow\n' "$EM" > "$d/about.md"
run_case "$d" pass "a line carrying the allow marker passes"

if [ "$failures" -ne 0 ]; then
  echo "$failures case(s) failed: scripts/check-dashes.sh does not do its job under $BASH_BIN"
  exit 1
fi
echo "all $n cases passed"
