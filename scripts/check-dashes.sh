#!/usr/bin/env bash
#
# No em dashes. No en dashes. Nowhere a person or an agent reads.
#
# This is a brand rule, not a style preference, so it is a build failure rather
# than a reminder. The check lives in one script so it cannot drift: grep
# flavours differ between machines (ugrep treats \| as a literal, BSD grep has
# no -P), and both of those silently report CLEAN on a file full of dashes.
#
#   bash scripts/check-dashes.sh            list every offending line
#   bash scripts/check-dashes.sh --quiet    exit code only
#
# Copied from 1212-Capital/app. Here it also reads .mdx, .mjs and .txt.
#
# Scanned extensions: .md .mdx .ts .tsx .js .jsx .mjs .json .css .sql .yml .yaml .html .txt
# Excluded: node_modules, .next, dist, build, .git, and every file under design/
# because design/ holds the binary 1212.pen, which cannot be read as text.
#
# Runs from the repo root and from CI. Exit 1 when anything is found, so it can
# gate a merge.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Built from escapes on purpose: this file must not itself contain a literal em
# dash or en dash, or it would be the first thing it flags. The UTF-8 bytes come
# from printf octal escapes, which every bash reads the same way: $'\u2014' is
# not expanded by bash 3.2 (the /bin/bash of macOS), and with it the pattern
# never matched and the script said Clean on anything.
# scripts/test-check-dashes.sh proves it on the bash that runs it.
EM="$(printf '\342\200\224')"
EN="$(printf '\342\200\223')"
ENTITY_MDASH='&mdash;'
ENTITY_NDASH='&ndash;'
PATTERN="${EM}|${EN}|${ENTITY_MDASH}|${ENTITY_NDASH}"

# Escape hatch for a line that is legitimately *about* the characters rather
# than containing one in copy. Exact marker, so a real dash cannot hide behind a
# vague exemption.
ALLOW='check-dashes:allow'

QUIET=0
if [ "${1:-}" = "--quiet" ]; then
  QUIET=1
fi

EXTS="md mdx ts tsx js jsx mjs json css sql yml yaml html txt"

# Tracked files inside a git checkout (the CI case) and a filesystem walk
# otherwise, so the script still works before the first commit.
collect() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local globs=()
    local e
    for e in $EXTS; do
      globs+=("*.${e}")
    done
    git ls-files -- "${globs[@]}"
  else
    local args=()
    local first=1
    local e
    for e in $EXTS; do
      if [ "$first" -eq 1 ]; then
        args+=( -name "*.${e}" )
        first=0
      else
        args+=( -o -name "*.${e}" )
      fi
    done
    find . -type f \( "${args[@]}" \)
  fi
}

# Generated and dependency trees, plus all of design/.
excluded() {
  case "$1" in
    node_modules/*|*/node_modules/*) return 0 ;;
    .next/*|*/.next/*) return 0 ;;
    dist/*|*/dist/*) return 0 ;;
    build/*|*/build/*) return 0 ;;
    .git/*|*/.git/*) return 0 ;;
    design/*|*/design/*) return 0 ;;
  esac
  return 1
}

found=()
while IFS= read -r file; do
  [ -n "$file" ] || continue
  [ -f "$file" ] || continue
  if excluded "$file"; then
    continue
  fi
  hits="$(grep -nE -- "$PATTERN" "$file" 2>/dev/null | grep -vF -- "$ALLOW" || true)"
  [ -n "$hits" ] || continue
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    lineno="${hit%%:*}"
    text="${hit#*:}"
    text="${text#:}"
    found+=("${file}:${lineno}|${text:0:140}")
  done <<< "$hits"
done < <(collect | sed 's|^\./||' | sort -u)

if [ "${#found[@]}" -eq 0 ]; then
  if [ "$QUIET" -eq 0 ]; then
    echo "No em dashes or en dashes. Clean."
  fi
  exit 0
fi

if [ "$QUIET" -eq 0 ]; then
  echo "${#found[@]} em dash or en dash to remove:"
  echo
  for entry in "${found[@]}"; do
    printf '  %s\n    %s\n' "${entry%%|*}" "${entry#*|}"
  done
  echo
  echo "Rewrite the sentence: a colon, a comma, parentheses, or two sentences."
  echo 'Do not substitute " - " every time; that is the same tell in a new shape.'
fi

exit 1
