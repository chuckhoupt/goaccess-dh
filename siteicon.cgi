#!/bin/bash

set -Eeuo pipefail

SITE="${QUERY_STRING^^}"

cat <<ENDSVG
Content-type: image/svg+xml

<svg version="1.1" baseProfile="full"
     width="48" height="48"
     xmlns="http://www.w3.org/2000/svg">

  <circle cx="24" cy="24" r="24" fill="gray" />

  <text x="24.5" y="34" font-size="28" font-family="sans-serif" text-anchor="middle" fill="white">${SITE:0:1}</text>

</svg>
ENDSVG
