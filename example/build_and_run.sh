#!/usr/bin/env bash

# Change to script directory
cd "$(dirname "$0")"

# Create a virtual environment
python -m venv example_venv
. example_venv/bin/activate

# Install  cppumockify
pip install -e ..

# Build the example project
mkdir -p bld
cd bld
cmake ..
make

# Run the example test
./test_greetings


