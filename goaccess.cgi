#!/bin/bash

set -Eeuo pipefail

# Allow extended patterns and empty results
shopt -s extglob nullglob

BASE=$(dirname "$0")
HOME=${HOME:-${DOCUMENT_ROOT%/${DOCUMENT_ROOT#/home/*/}}}
PATH=$BASE/bin:$PATH

# shellcheck source=/dev/null
[[ -f "$BASE/.env" ]] && source "$BASE"/.env 

LOGS=${LOGS:-$HOME/logs}

SITEGLOB=${1:-$(basename "$SCRIPT_URL")}

# Sanitize glob to only allow chars in domains and glob patterns
SITEGLOB=${SITEGLOB//[^a-zA-Z0-9\-.*?+@!\^()\[\]|]/}

SITES=($LOGS/$SITEGLOB)

ALLLOGS=($LOGS/$SITEGLOB/http?(s)/access.log?(.2*))

# Calc log size, but note that it is compressed size.
set $(du -cb "${ALLLOGS[@]}" | tail -1)
LOGSIZE=$1

function vcombinelogs {
	for SITE in "${SITES[@]}"
	do
		VHOST=$(basename "$SITE")
		SITELOGS=($SITE/http?(s)/access.log?(.2*))
		zcat -f "${SITELOGS[@]}" | sed "s/^/$VHOST:0 /"
	done
}

OUTPUT=$(mktemp -t XXXXXXXXXX.html)

# GoAccess needs HOME defined
export HOME

vcombinelogs \
| goaccess - -o "$OUTPUT" --no-progress --log-format=VCOMBINED --no-global-config \
   --html-report-title="$SITEGLOB" --log-size="$LOGSIZE" --html-prefs='{"theme":"bright"}' \
   --agent-list --http-protocol=no --http-method=yes 

echo "Content-type: text/html"
echo ""
cat "$OUTPUT"
rm  "$OUTPUT"
