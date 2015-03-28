joern-traversals
-------------

A collection of example [joern](https://github.com/fabsx00/joern) queries with unit tests.

Run unit tests
--------------

Install dependencies with `pip install pyyaml`. To run tests:

    rm -rf testing/intermediates .queriesTestDB
    ./testing/parse.py testing/intermediates queries/*.yaml
    joern testing/intermediates -outdir .queriesTestDB

    # Start the DB with the correct path to ./.queriesTestDB
    ./testing/verify.py queries/*.yaml
