# Gilded Rose starting position in Python

For exercise instructions see [top level README](../README.md)

Package dependencies are managed with uv. To install uv, run `brew install uv` on a mac and then use it to install 
python by running `uv install python 3.12`.

## Install the dependencies

```
uv sync
```

## Run the unit tests from the Command-Line

```
uv run test_gilded_rose.py
```

## Run the TextTest fixture from the Command-Line

For e.g. 10 days:

```
uv run texttest_fixture.py 10
```

You should make sure the command shown above works when you execute it in a terminal before trying to use TextTest (see below).


## Run the TextTest approval test that comes with this project

There are instructions in the [TextTest Readme](../texttests/README.md) for setting up TextTest. You will need to specify the Python executable and interpreter in [config.gr](../texttests/config.gr). Uncomment these lines:

    executable:${TEXTTEST_HOME}/python/texttest_fixture.py
    interpreter:python
