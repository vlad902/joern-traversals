joern-traversals
-------------

A collection of example [joern](https://github.com/fabsx00/joern) queries with unit tests. These queries are for the old version of joern that used neo4j and tinkerpop v2, for some examples using octopus (the new update of joern using tinkerpop3 on TitanDB) look [here](https://tsyrklevich.net/2016/10/31/notes-on-octopus-gremlin3/).

Run unit tests
--------------

Install dependencies with `pip install pyyaml`. To run tests:

    rm -rf testing/intermediates .queriesTestDB
    ./testing/parse.py testing/intermediates queries/*.yaml
    joern testing/intermediates -outdir .queriesTestDB

    # Start the DB with the correct path to ./.queriesTestDB
    ./testing/verify.py queries/*.yaml
