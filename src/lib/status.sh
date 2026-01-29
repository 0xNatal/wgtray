#!/bin/bash
# List active WireGuard interfaces

wg show interfaces 2>/dev/null | tr ' ' '\n' | grep -v '^$'