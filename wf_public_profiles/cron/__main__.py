import sys

from .scheduler import Scheduler


def main():
    s = Scheduler()
    s.start()


if __name__ == "__main__":
    sys.exit(main())
