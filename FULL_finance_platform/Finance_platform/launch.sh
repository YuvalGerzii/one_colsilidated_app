#!/usr/bin/env bash
# =============================================================================
# Portfolio Dashboard - Smart Launcher
# =============================================================================
# Automatically detects environment and launches appropriate startup script
# =============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🚀 Portfolio Dashboard Launcher${NC}"
echo ""

# Check if running in Claude Code/AI environment
if [ -n "$CLAUDE_CODE" ] || [ -n "$AI_ENV" ] || [ "$1" == "--claude" ]; then
    echo -e "${GREEN}Detected Claude Code environment${NC}"
    echo -e "${YELLOW}Using optimized startup script...${NC}"
    exec "$SCRIPT_DIR/start_claude_code.sh"
else
    echo -e "${GREEN}Using standard startup script...${NC}"
    exec "$SCRIPT_DIR/start_app.sh" "$@"
fi
