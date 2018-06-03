#!/usr/bin/env bash

# Change to script directory
cd "$(dirname "$0")"

# Create a virtual environment (when not in travis)
if [ -z "$TRAVIS" ]; then
    python -m venv example_venv
    . example_venv/bin/activate
fi

# Install  cppumockify
pip install -e ..

pip list

# Build the example project
mkdir -p bld
cd bld
cmake ..
make

# Run the example test
./test_greetings


