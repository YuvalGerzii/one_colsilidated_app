#!/bin/bash
# =============================================================================
# DEPENDENCY WAITING UTILITY
# =============================================================================
# Waits for service dependencies to be ready before starting
# Can be used as a docker entrypoint wrapper
# =============================================================================

set -e

TIMEOUT=${TIMEOUT:-120}
RETRY_INTERVAL=${RETRY_INTERVAL:-2}

usage() {
    echo "Usage: wait-for-deps.sh [options] -- command"
    echo ""
    echo "Options:"
    echo "  -h HOST:PORT    Wait for TCP connection (can be specified multiple times)"
    echo "  -u URL          Wait for HTTP endpoint (can be specified multiple times)"
    echo "  -t TIMEOUT      Timeout in seconds (default: 120)"
    echo "  -i INTERVAL     Retry interval in seconds (default: 2)"
    echo ""
    echo "Examples:"
    echo "  wait-for-deps.sh -h postgres:5432 -h redis:6379 -- python app.py"
    echo "  wait-for-deps.sh -u http://postgres:5432 -- npm start"
}

# Parse arguments
TCP_DEPS=()
HTTP_DEPS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -h)
            TCP_DEPS+=("$2")
            shift 2
            ;;
        -u)
            HTTP_DEPS+=("$2")
            shift 2
            ;;
        -t)
            TIMEOUT="$2"
            shift 2
            ;;
        -i)
            RETRY_INTERVAL="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

COMMAND="$@"

if [ -z "$COMMAND" ]; then
    echo "Error: No command specified"
    usage
    exit 1
fi

echo "⏳ Waiting for dependencies..."
echo "Timeout: ${TIMEOUT}s | Retry Interval: ${RETRY_INTERVAL}s"
echo ""

# Function to check TCP connection
check_tcp() {
    local host_port=$1
    local host=${host_port%:*}
    local port=${host_port#*:}

    timeout 1 bash -c "cat < /dev/null > /dev/tcp/$host/$port" 2>/dev/null
}

# Function to check HTTP endpoint
check_http() {
    local url=$1
    curl -sf --connect-timeout 1 "$url" > /dev/null 2>&1
}

# Wait for TCP dependencies
for dep in "${TCP_DEPS[@]}"; do
    echo "Waiting for $dep..."
    elapsed=0

    while ! check_tcp "$dep"; do
        elapsed=$((elapsed + RETRY_INTERVAL))

        if [ $elapsed -ge $TIMEOUT ]; then
            echo "✗ Timeout waiting for $dep"
            exit 1
        fi

        echo "  Still waiting... (${elapsed}s/${TIMEOUT}s)"
        sleep $RETRY_INTERVAL
    done

    echo "✓ $dep is ready"
done

# Wait for HTTP dependencies
for dep in "${HTTP_DEPS[@]}"; do
    echo "Waiting for $dep..."
    elapsed=0

    while ! check_http "$dep"; do
        elapsed=$((elapsed + RETRY_INTERVAL))

        if [ $elapsed -ge $TIMEOUT ]; then
            echo "✗ Timeout waiting for $dep"
            exit 1
        fi

        echo "  Still waiting... (${elapsed}s/${TIMEOUT}s)"
        sleep $RETRY_INTERVAL
    done

    echo "✓ $dep is ready"
done

echo ""
echo "✓ All dependencies are ready!"
echo "🚀 Starting: $COMMAND"
echo ""

# Execute the command
exec $COMMAND
