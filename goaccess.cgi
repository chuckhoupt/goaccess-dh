#!/bin/bash

set -Eeuo pipefail

# Allow extended patterns and empty results
shopt -s extglob nullglob

BASE=$(dirname "$0")
HOME=${HOME:-${DOCUMENT_ROOT%/"${DOCUMENT_ROOT#/home/*/}"}}
PATH=$BASE/bin:$PATH

# shellcheck source=/dev/null
[[ -f "$BASE/.env" ]] && source "$BASE"/.env 

LOGS=${LOGS:-$HOME/logs}

SITEGLOB=${1:-$(basename "$SCRIPT_URL")}

# Sanitize glob to only allow chars in domains and glob patterns
SITEGLOB=${SITEGLOB//[^a-zA-Z0-9\-.*?+@!\^()\[\]|]/}

readarray -t SITES < <(find "$LOGS"/$SITEGLOB/http?(s)/access.log -mtime -4 -exec dirname {} \;)

# Calc log size, but note that it is compressed size.
ALLLOGS=( ${SITES[@]/%//access.log?(.2*)} )
LOGSIZE=$(du --total --byte "${ALLLOGS[@]}" | tail -1 | cut --fields=1)

function vcombinelogs {
	for SITE in "${SITES[@]}"
	do
		VHOST=$(basename $(dirname "$SITE"))
		SITELOGS=("$SITE"/access.log?(.2*))
		zcat -f "${SITELOGS[@]}" | sed "s/^/$VHOST:0 /"
	done
}

echo "Content-type: text/html"
echo ""

vcombinelogs \
  | goaccess - -o html --no-progress --no-global-config \
   --date-format='%d/%b/%Y' --time-format='%H:%M:%S' \
   --log-format='%v:%^ %h %^ %e [%d:%t %^] "%r" %s %b "%R" "%u"' \
   --html-report-title="$SITEGLOB" --log-size="$LOGSIZE" --html-prefs='{"theme":"bright"}' \
   --unknowns-as-crawlers \
   ${GEOIP:-} \
   --agent-list --http-protocol=no --http-method=yes --ignore-panel=KEYPHRASES \
   --all-static-files --real-os
