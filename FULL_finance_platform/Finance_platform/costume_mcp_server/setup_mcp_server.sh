#!/bin/bash
# ============================================================================
# MCP Financial Datasets Setup Script
# Portfolio Dashboard Automation
# ============================================================================

set -e  # Exit on error

echo "============================================================================"
echo "MCP Financial Datasets Server Setup"
echo "Portfolio Dashboard Integration"
echo "============================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# Step 1: Check Prerequisites
# ============================================================================
echo "Step 1: Checking prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}✗ Python version $PYTHON_VERSION is too old${NC}"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}⚠ PostgreSQL client not found in PATH${NC}"
    echo "  You'll need to manually run the database schema setup"
else
    echo -e "${GREEN}✓ PostgreSQL client found${NC}"
fi

# ============================================================================
# Step 2: Install UV
# ============================================================================
echo ""
echo "Step 2: Installing/checking UV package manager..."

if ! command -v uv &> /dev/null; then
    echo "Installing UV..."
    
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # macOS or Linux
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        echo -e "${YELLOW}Please install UV manually on Windows:${NC}"
        echo "curl -LsSf https://astral.sh/uv/install.ps1 | powershell"
        exit 1
    fi
    
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
else
    echo -e "${GREEN}✓ UV already installed${NC}"
fi

UV_PATH=$(which uv)
echo "UV path: $UV_PATH"

# ============================================================================
# Step 3: Clone MCP Server Repository
# ============================================================================
echo ""
echo "Step 3: Setting up MCP server..."

MCP_DIR="$HOME/mcp-financial-datasets"

if [ -d "$MCP_DIR" ]; then
    echo -e "${YELLOW}⚠ MCP directory already exists: $MCP_DIR${NC}"
    read -p "Do you want to delete and re-clone? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$MCP_DIR"
    else
        echo "Using existing directory..."
    fi
fi

if [ ! -d "$MCP_DIR" ]; then
    echo "Cloning MCP server repository..."
    git clone https://github.com/financial-datasets/mcp-server "$MCP_DIR"
    echo -e "${GREEN}✓ Repository cloned${NC}"
fi

cd "$MCP_DIR"

# ============================================================================
# Step 4: Install Dependencies
# ============================================================================
echo ""
echo "Step 4: Installing dependencies..."

# Create virtual environment
uv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install dependencies
uv add "mcp[cli]" httpx

echo -e "${GREEN}✓ Dependencies installed${NC}"

# ============================================================================
# Step 5: Configure API Key
# ============================================================================
echo ""
echo "Step 5: Configuring API key..."

if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
else
    echo "FINANCIAL_DATASETS_API_KEY=your-api-key-here" > .env
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

echo ""
echo -e "${YELLOW}IMPORTANT: Edit the .env file and add your API key:${NC}"
echo "  File location: $MCP_DIR/.env"
echo "  Get your API key from: https://www.financialdatasets.ai/"
echo ""
read -p "Press Enter after you've added your API key..."

# ============================================================================
# Step 6: Configure Claude Desktop
# ============================================================================
echo ""
echo "Step 6: Configuring Claude Desktop..."

# Determine config path
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    CONFIG_DIR="$HOME/.config/Claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
else
    # Windows (need to handle differently)
    echo -e "${YELLOW}Please manually configure Claude Desktop on Windows${NC}"
    echo "Config location: %APPDATA%\\Claude\\claude_desktop_config.json"
    exit 0
fi

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Create or update config file
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠ Config file already exists${NC}"
    echo "Backing up existing config..."
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
fi

# Generate config
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "financial-datasets": {
      "command": "$UV_PATH",
      "args": [
        "--directory",
        "$MCP_DIR",
        "run",
        "server.py"
      ]
    }
  }
}
EOF

echo -e "${GREEN}✓ Claude Desktop configured${NC}"
echo "  Config file: $CONFIG_FILE"

# ============================================================================
# Step 7: Test Installation
# ============================================================================
echo ""
echo "Step 7: Testing installation..."

# Test UV
echo "Testing UV..."
if $UV_PATH --version &> /dev/null; then
    echo -e "${GREEN}✓ UV works${NC}"
else
    echo -e "${RED}✗ UV test failed${NC}"
fi

# Test server.py exists
if [ -f "server.py" ]; then
    echo -e "${GREEN}✓ server.py found${NC}"
else
    echo -e "${RED}✗ server.py not found${NC}"
fi

# Test .env exists
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
else
    echo -e "${RED}✗ .env file not found${NC}"
fi

# ============================================================================
# Summary
# ============================================================================
echo ""
echo "============================================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "============================================================================"
echo ""
echo "Next Steps:"
echo "  1. Restart Claude Desktop"
echo "  2. Look for the hammer icon (🔨) in bottom right"
echo "  3. Test with: 'Get Apple's latest income statement'"
echo ""
echo "Integration Files Created:"
echo "  - Python Integration: mcp_market_data_integration.py"
echo "  - Database Schema: market_data_schema.sql"
echo "  - Integration Guide: MCP_INTEGRATION_GUIDE.md"
echo ""
echo "Database Setup:"
echo "  Run this command to set up database tables:"
echo "  psql -U your_username -d portfolio_dashboard -f market_data_schema.sql"
echo ""
echo "Troubleshooting:"
echo "  - MCP server location: $MCP_DIR"
echo "  - Claude config: $CONFIG_FILE"
echo "  - UV location: $UV_PATH"
echo ""
echo "For detailed documentation, see: MCP_INTEGRATION_GUIDE.md"
echo "============================================================================"
