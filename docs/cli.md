# `corsair`

CorSaiR v2.0.0 -- CSR map generator for HDL projects.

**Usage**:

```console
$ corsair [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --verbose`: Increase verbosity. Can be applied multiple times to increase even more. Default is WARNING level unless LOG_LEVEL environment variable is set.
* `-q, --quiet`: Decrease verbosity. Can be applied multiple times to decrease even more.Default is WARNING level unless LOG_LEVEL environment variable is set.
* `--no-color`: Disable color output. When not provided, color is enabled unless the NO_COLOR environment variable is set.
* `--no-rich`: Disable rich formatting. When not provided, rich formatting is enabled unless the TERM environment variable is set to &#x27;dumb&#x27; or &#x27;unknown&#x27;.
* `-l, --log PATH`: Log file to write to.
* `--help`: Show this message and exit.


        Pass --help or -h after any COMMAND to get additional help.

        Set NO_COLOR=1 environment variable to disable any color in output.

        Set TERM=dumb or TERM=unknown environment variable to enable plain text output.

**Commands**:

* `init`: Initialize a simple project.
* `build`: Build required targets according to the...
* `check`: Check integrity of Corsair input files...
* `schema`: Dump JSON schema for user input file.
* `version`: Print the application version.
* `test-logging`: Hidden command for testing logging...

## `corsair init`

Initialize a simple project.

**Usage**:

```console
$ corsair init [OPTIONS] [KIND]:[json|hjson|yaml]
```

**Arguments**:

* `[KIND]:[json|hjson|yaml]`: Template kind. Defines the format of the generated register map file.  [default: yaml]

**Options**:

* `-o, --output PATH`: Path to an output directory  [default: .]
* `--help`: Show this message and exit.

## `corsair build`

Build required targets according to the provided specification.

**Usage**:

```console
$ corsair build [OPTIONS] [TARGETS]...
```

**Arguments**:

* `[TARGETS]...`: Select targets to build. By default, all targets are built when empty.

**Options**:

* `-s, --spec PATH`: Path to a build specification file  [default: csrbuild.yaml]
* `-o, --output PATH`: Path to an output directory  [default: corsair-build]
* `--clean`: Clean the output directory before building.
* `--help`: Show this message and exit.

## `corsair check`

Check integrity of Corsair input files (build specifications or register maps).

**Usage**:

```console
$ corsair check [OPTIONS] [INPUT_PATHS]...
```

**Arguments**:

* `[INPUT_PATHS]...`: Path(s) to build/map file(s) to check. If omitted, checks all supported files in the current directory.

**Options**:

* `--help`: Show this message and exit.

## `corsair schema`

Dump JSON schema for user input file.

**Usage**:

```console
$ corsair schema [OPTIONS] KIND:{build|map}
```

**Arguments**:

* `KIND:{build|map}`: Schema kind.  [required]

**Options**:

* `--indent N`: Indentation level for JSON output. Single line form is used if not provided.
* `-o, --out PATH`: Path for output file. If not provided, then schema is printed to stdout.
* `--help`: Show this message and exit.

## `corsair version`

Print the application version.

**Usage**:

```console
$ corsair version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `corsair test-logging`

Hidden command for testing logging configuration.

**Usage**:

```console
$ corsair test-logging [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
