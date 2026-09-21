#!/usr/bin/env python3
"""Build Fake Trap revision 3 with clean motive and shortened checks board."""

import sys

from build_fake_trap_v1 import main


if __name__ == "__main__":
    sys.argv.insert(1, "--revision-v3")
    main()
