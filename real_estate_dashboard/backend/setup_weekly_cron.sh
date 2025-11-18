#!/bin/bash
#
# Setup Weekly Economics Data Update Cron Job
#
# This script sets up a cron job to run weekly_economics_update.py
# every Sunday at 2:00 AM.
#
# Usage:
#   ./setup_weekly_cron.sh
#   ./setup_weekly_cron.sh --day Monday --time "03:00"
#   ./setup_weekly_cron.sh --remove  # Remove the cron job

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Defaults
DAY="Sunday"
TIME="02:00"
REMOVE=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/weekly_economics_update.py"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/weekly_economics_update.log"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --day)
            DAY="$2"
            shift 2
            ;;
        --time)
            TIME="$2"
            shift 2
            ;;
        --remove)
            REMOVE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --day DAY       Day of week (default: Sunday)"
            echo "  --time TIME     Time to run (default: 02:00)"
            echo "  --remove        Remove existing cron job"
            echo "  --help          Show this help"
            echo ""
            echo "Examples:"
            echo "  $0                                  # Run every Sunday at 2 AM"
            echo "  $0 --day Monday --time '03:00'      # Run every Monday at 3 AM"
            echo "  $0 --remove                         # Remove cron job"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Function to convert day name to cron day number
get_day_number() {
    case "$1" in
        Sunday) echo "0" ;;
        Monday) echo "1" ;;
        Tuesday) echo "2" ;;
        Wednesday) echo "3" ;;
        Thursday) echo "4" ;;
        Friday) echo "5" ;;
        Saturday) echo "6" ;;
        *) echo "0" ;;  # Default to Sunday
    esac
}

# Function to parse time
parse_time() {
    local time_str="$1"
    local hour=$(echo "$time_str" | cut -d':' -f1 | sed 's/^0*//')
    local minute=$(echo "$time_str" | cut -d':' -f2 | sed 's/^0*//')
    echo "$minute $hour"
}

# Remove existing cron job
remove_cron() {
    echo -e "${YELLOW}Removing existing weekly economics update cron job...${NC}"

    # Remove lines containing weekly_economics_update.py
    crontab -l 2>/dev/null | grep -v "weekly_economics_update.py" | crontab - 2>/dev/null || true

    echo -e "${GREEN}✓ Cron job removed${NC}"
    exit 0
}

# Check if remove flag is set
if [ "$REMOVE" = true ]; then
    remove_cron
fi

# Create logs directory
mkdir -p "$LOG_DIR"

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}Error: Script not found at $SCRIPT_PATH${NC}"
    exit 1
fi

# Make script executable
chmod +x "$SCRIPT_PATH"

# Get day number and time
DAY_NUM=$(get_day_number "$DAY")
TIME_PARTS=$(parse_time "$TIME")
MINUTE=$(echo "$TIME_PARTS" | cut -d' ' -f1)
HOUR=$(echo "$TIME_PARTS" | cut -d' ' -f2)

# Create cron job line
CRON_LINE="$MINUTE $HOUR * * $DAY_NUM cd $SCRIPT_DIR && /usr/bin/python3 $SCRIPT_PATH >> $LOG_FILE 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "weekly_economics_update.py"; then
    echo -e "${YELLOW}Existing cron job found. Removing it first...${NC}"
    crontab -l 2>/dev/null | grep -v "weekly_economics_update.py" | crontab - 2>/dev/null || true
fi

# Add new cron job
echo -e "${GREEN}Setting up weekly economics update cron job...${NC}"
echo ""
echo "Schedule: Every $DAY at $TIME"
echo "Script: $SCRIPT_PATH"
echo "Logs: $LOG_FILE"
echo ""

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo -e "${GREEN}✓ Cron job installed successfully!${NC}"
echo ""
echo "To verify, run: crontab -l"
echo "To view logs: tail -f $LOG_FILE"
echo "To remove: $0 --remove"
echo ""
echo -e "${YELLOW}Note: Make sure ECONOMICS_API_KEY is set in your .env file${NC}"
