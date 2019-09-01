#!/bin/bash

set -Eeuo pipefail

# Allow extended patterns and empty results
shopt -s extglob nullglob

BASE=$(dirname "$0")
HOME=${HOME:-${DOCUMENT_ROOT%/${DOCUMENT_ROOT#/home/*/}}}

# shellcheck source=/dev/null
[[ -f "$BASE/.env" ]] && source "$BASE"/.env 

LOGS=${LOGS:-$HOME/logs}

# Jump to clean URL if query is empty
if [[ "$QUERY_STRING" == 'g=' ]]
then
	echo "Location: ."
	echo
	exit
fi

# Strip param name
QUERY_STRING="${QUERY_STRING#g=}"

# Convert encoded glob pattern chars
QUERY_STRING="${QUERY_STRING//%3F/?}"
QUERY_STRING="${QUERY_STRING//%2B/+}"
QUERY_STRING="${QUERY_STRING//%40/@}"
QUERY_STRING="${QUERY_STRING//%21/!}"
QUERY_STRING="${QUERY_STRING//%5E/^}"
QUERY_STRING="${QUERY_STRING//%28/(}"
QUERY_STRING="${QUERY_STRING//%29/)}"
QUERY_STRING="${QUERY_STRING//%5B/[}"
QUERY_STRING="${QUERY_STRING//%5D/]}"
QUERY_STRING="${QUERY_STRING//%7C/|}"

# Sanitize Query to only allow chars in domains and glob patterns
QUERY_STRING=${QUERY_STRING//[^a-zA-Z0-9\-.*?+@!\^()\[\]|]/}

if [[ -z "$QUERY_STRING" ]]
then
	LOGGLOB='*'
	SEARCHVALUE=''
else
	LOGGLOB="$QUERY_STRING"
	SEARCHVALUE="$LOGGLOB"
fi

cat <<ENDHEADER
Content-type: text/html

<!doctype html>
<html>
<head>
<meta charset=utf-8>
<title>GoAccess-DH</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  font-family: sans-serif;
  background: #f0f0f0;
  max-width: 70em;
  margin: auto;
  text-align: center;
}

ul.site-list {
  list-style-type: none;
  padding-left: 0;

  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(12em, 1fr));
  grid-gap: 10px;
}

.site-list img { height: 48px; width: 48px; visibility: hidden; }

a { text-decoration: none; }
</style>
<script>
function loadfavicon(img, site) {
  var favicon = 'http://'+ site + '/favicon.ico';
  img.src = (img.src != favicon) ? favicon : 'siteicon.cgi?'+site;
  return true;
}
</script>
</head>
<body>
<h1>GoAccess-DH</h1>
<form>
  <input type="search" name="g" placeholder="filter pattern: *.net  blog.*"
  value="${SEARCHVALUE}">
</form>
<ul class="site-list">
ENDHEADER

function sites
{
	for LOGFILE in $LOGS/$LOGGLOB/http?(s)/access.log.$(date -I --date='-2 days')
	do
		[[ "$LOGFILE" =~ $LOGS/([^\/]+)/ ]]
		echo "${BASH_REMATCH[1]}"
	done
}

# 
function sitename {
	if [[ "$1" =~ ^xn\-\- ]]
	then
		python -c 'import sys; print sys.argv[1].decode("idna").encode("utf-8")' "$1"
	else
		echo "$1"
	fi
}

for SITE in $(sites | rev | sort -u | rev)
do

cat <<ENDITEM
<li>
  <a href="$SITE">
    <img alt src="http://$SITE/apple-touch-icon.png" 
         onload="this.style.visibility='visible'" onerror="loadfavicon(this, '$SITE')">
    <br>
    $(sitename "$SITE")
  </a>
</li>
ENDITEM

done

cat <<ENDFOOTER
</ul>
<p>
<a href="${LOGGLOB//\?/%3F}">
<img src="./siteicon.cgi?Z"><img src="./siteicon.cgi?A" style="margin-left: -75px;"><br>
All Sites: $LOGGLOB
</a>
</p>
</body>
</html>
ENDFOOTER
