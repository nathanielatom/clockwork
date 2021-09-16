# clockwork
Some basic utilities for modular arithmetic and directional statistics.

## Installation

In terminal, simply run:

    git clone https://github.com/nathanielatom/clockwork.git
    cd clockwork
    pip install .[docs,test]

Note if using zsh, remember to escape `[` with `\[`. Also use `--editable` for development.

## Usage

Import and run as follows:

    from clockwork.angle_calc import AngleCalc
    calc = AngleCalc()
    unwrapped_angle, first_angle, second_angle = 884, 25, 92 # degrees
    principal_angle = calc.boundTo180(unwrapped_angle)
    between = calc.isAngleBetween(first_angle, principal_angle, second_angle)
    print(f'The angle {principal_angle:g}º is{" " if between else " not "}between {first_angle}º and {second_angle}º!')

## Tests

Are run using [pytest](https://docs.pytest.org), in the root of the repo, simply run `pytest`.

## Docs

Actually let's make this TBD. The docstrings for each function can be accessed with `?` in ipython, for example `clockwork.utils.circular_mean?`.

Future:
Are built using [sphinx](https://sphinx-doc.org), in the root of the repo, simply run `make html`. Or `make clean` to delete.

## Continuous Integration

TBD with Github Actions.
