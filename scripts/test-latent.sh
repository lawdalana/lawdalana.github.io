#!/usr/bin/env bash
set -euo pipefail

# Reuse the isolated browser tooling without adding repository node_modules.
latent_test_tools="${LATENT_TEST_DEPS:-${SLIDES_TEST_DEPS:-${XDG_CACHE_HOME:-$HOME/.cache}/lawdalana-slides-tests}}"
if ! NODE_PATH="$latent_test_tools/node_modules" node -e "require('liquidjs'); require('yaml'); require('sass'); require('playwright')" >/dev/null 2>&1; then
  npm install --prefix "$latent_test_tools" --no-audit --no-fund liquidjs@10.30.0 yaml@2.9.1 sass@1.105.1 playwright@1.63.0
fi
NODE_PATH="$latent_test_tools/node_modules" node --test tests/latent-reading.test.cjs
