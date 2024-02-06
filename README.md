# CETKiller

A very simple script that removes Intel CET instructions from ELF executables.

The main reason for me to make this was that some x86 simulators, like multi2sim, will not decode these instructions correctly. Unfortunately, you cannot just stop GCC from emitting them, given that they are baked into all precompiled libraries on Linux, including glibc. The only solution I came up qith was to build stuff statically, and then remove replace all the CET instructions with NOPs in the final executable.

This script does just that.

See removecet.py for usage.