#!/bin/sh
# The full check, one recipe for contributors and for CI, so there is no second one to drift (SE1/O3).
# The interpreter is chosen the way `se` chooses it: python3 where it exists, else python.
set -e
cd "$(dirname "$0")/.."
py=$(command -v python3 2>/dev/null || command -v python)
"$py" -I tools/check.py
"$py" -I tools/since.py --check
"$py" se.py --self
"$py" -I tools/test_se.py
"$py" -I tools/test_check.py
