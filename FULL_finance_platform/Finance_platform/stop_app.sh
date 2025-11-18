#!/bin/bash

#######################################################################
# Portfolio Dashboard - Stop Script
#######################################################################
#
# Quick script to stop all Portfolio Dashboard services
#
#######################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

./start_app.sh --stop
