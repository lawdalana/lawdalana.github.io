#!/usr/bin/env bash
set -euo pipefail

# Isolated test tooling; no frontend npm build or repository node_modules.
slides_test_tools="${SLIDES_TEST_DEPS:-${XDG_CACHE_HOME:-$HOME/.cache}/lawdalana-slides-tests}"
if ! NODE_PATH="$slides_test_tools/node_modules" node -e "require('liquidjs'); require('yaml'); require('sass'); require('playwright'); require('v8-to-istanbul')" >/dev/null 2>&1; then
  npm install --prefix "$slides_test_tools" --no-audit --no-fund liquidjs@10.30.0 yaml@2.9.1 sass@1.105.1 playwright@1.63.0 v8-to-istanbul@9.3.0
fi
NODE_PATH="$slides_test_tools/node_modules" node --test tests/slides-dropdown.test.cjs
