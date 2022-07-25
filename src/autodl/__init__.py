from collections.abc import Sequence

# pylint: disable=import-outside-toplevel
def run_autodl():
    """Run autodl
    argv can be a sequence of strings normally supplied as arguments on the command line
    """
    from autodl.autodl import main

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
