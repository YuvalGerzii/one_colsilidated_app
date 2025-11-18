# MCP Server Integration Guide

**Model Context Protocol** - Connect AI Assistants to Real Estate Data

---

## What is MCP?

The Model Context Protocol (MCP) is an open standard introduced by Anthropic in November 2024 that connects AI assistants (like Claude) to external data sources and tools.

**Benefits:**
- ✅ Standardized integration protocol
- ✅ Real-time data access
- ✅ No manual API key management
- ✅ Works with Claude Desktop, Claude Code, and other MCP clients
- ✅ Extensible tool framework

---

## Available Real Estate MCP Servers

### 1. Zillow MCP Server

**GitHub:** https://github.com/sap156/zillow-mcp-server
**Language:** Python + FastMCP
**Status:** Community-maintained
**License:** Open source

#### Features

**Tools:**
1. `search_properties` - Search Zillow by criteria
2. `get_property_details` - Get detailed property information
3. `get_zestimate` - Get Zillow's estimated value
4. `get_market_trends` - Market trends for location
5. `calculate_mortgage` - Mortgage payment calculator

#### Installation

```bash
# Clone repository
git clone https://github.com/sap156/zillow-mcp-server.git
cd zillow-mcp-server

# Install dependencies
pip install -r requirements.txt

# Or install FastMCP directly
pip install fastmcp
```

#### Configuration for Claude Desktop

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
**Location:** `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "zillow-real-estate": {
      "command": "python",
      "args": ["/path/to/zillow-mcp-server/server.py"]
    }
  }
}
```

#### Usage Examples

Once configured, you can ask Claude:

```
"Search for 3-bedroom houses in San Francisco under $1.5M"
"What's the Zestimate for 123 Main St, San Francisco, CA?"
"Show me market trends in Austin, TX for the last 6 months"
"Calculate mortgage for $800k home with 20% down at 6.5% interest"
```

---

### 2. BatchData Real Estate MCP Server

**Source:** PulseMCP Directory
**Purpose:** Batch processing real estate data
**Status:** Community server

#### Features
- Property listings management
- Market analytics processing
- Workflow automation
- Batch data operations

---

## Creating Your Own MCP Server

### Option 1: Python with FastMCP

**Installation:**
```bash
pip install fastmcp
```

**Example Server:**

```python
# real_estate_mcp_server.py
from fastmcp import FastMCP
import httpx

mcp = FastMCP("Real Estate Data Server")

@mcp.tool()
async def get_census_demographics(zip_code: str) -> dict:
    """
    Get demographic data from Census Bureau for a ZIP code

    Args:
        zip_code: 5-digit ZIP code
    """
    # No API key needed for basic Census data
    url = f"https://api.census.gov/data/2023/acs/acs5"
    params = {
        'get': 'NAME,B01003_001E,B19013_001E',  # Population, Income
        'for': f'zip code tabulation area:{zip_code}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    return {
        'zip_code': zip_code,
        'population': data[1][1] if len(data) > 1 else None,
        'median_income': data[1][2] if len(data) > 1 else None
    }


@mcp.tool()
async def get_hud_fair_market_rent(zip_code: str, year: int = 2024) -> dict:
    """
    Get HUD Fair Market Rents for a ZIP code

    Args:
        zip_code: 5-digit ZIP code
        year: Fiscal year (default 2024)
    """
    # Note: This would need HUD API implementation
    # For demo, return structure
    return {
        'zip_code': zip_code,
        'year': year,
        'efficiency': 1200,
        'one_bedroom': 1400,
        'two_bedroom': 1700,
        'three_bedroom': 2200,
        'four_bedroom': 2600
    }


@mcp.tool()
async def calculate_investment_metrics(
    purchase_price: float,
    monthly_rent: float,
    expenses: float,
    down_payment_percent: float = 20.0,
    interest_rate: float = 6.5
) -> dict:
    """
    Calculate real estate investment metrics

    Args:
        purchase_price: Property purchase price
        monthly_rent: Expected monthly rent
        expenses: Monthly expenses (taxes, insurance, HOA, etc.)
        down_payment_percent: Down payment percentage
        interest_rate: Annual interest rate
    """
    down_payment = purchase_price * (down_payment_percent / 100)
    loan_amount = purchase_price - down_payment

    # Monthly mortgage payment (P&I)
    monthly_rate = interest_rate / 100 / 12
    num_payments = 30 * 12
    monthly_payment = loan_amount * (
        monthly_rate * (1 + monthly_rate)**num_payments /
        ((1 + monthly_rate)**num_payments - 1)
    )

    # Cash flow
    monthly_cash_flow = monthly_rent - monthly_payment - expenses

    # Cap rate
    noi = (monthly_rent - expenses) * 12
    cap_rate = (noi / purchase_price) * 100

    # Cash on cash return
    annual_cash_flow = monthly_cash_flow * 12
    cash_on_cash = (annual_cash_flow / down_payment) * 100

    return {
        'purchase_price': purchase_price,
        'down_payment': down_payment,
        'loan_amount': loan_amount,
        'monthly_payment': monthly_payment,
        'monthly_cash_flow': monthly_cash_flow,
        'annual_cash_flow': annual_cash_flow,
        'noi': noi,
        'cap_rate': cap_rate,
        'cash_on_cash_return': cash_on_cash
    }


# Run server
if __name__ == "__main__":
    mcp.run()
```

**Run Server:**
```bash
python real_estate_mcp_server.py
```

---

### Option 2: TypeScript/JavaScript

**Installation:**
```bash
npm install @modelcontextprotocol/sdk
```

**Example Server:**

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "real-estate-data",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_property_value",
        description: "Get estimated property value",
        inputSchema: {
          type: "object",
          properties: {
            address: {
              type: "string",
              description: "Property address",
            },
          },
          required: ["address"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_property_value") {
    const address = request.params.arguments?.address;

    // Fetch property data (implement your logic)
    const value = await fetchPropertyValue(address);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(value, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

---

## Integrating MCP Server with Your Dashboard

### Backend Integration

Create an MCP client in your backend to communicate with MCP servers:

**File:** `/backend/app/integrations/mcp/client.py`

```python
import asyncio
import json
from typing import Dict, List, Any
from pathlib import Path


class MCPClient:
    """Client for communicating with MCP servers"""

    def __init__(self, server_config: Dict):
        """
        Initialize MCP client

        Args:
            server_config: Server configuration
                {
                    'command': 'python',
                    'args': ['/path/to/server.py']
                }
        """
        self.server_config = server_config
        self.process = None

    async def start_server(self):
        """Start MCP server process"""
        self.process = await asyncio.create_subprocess_exec(
            self.server_config['command'],
            *self.server_config['args'],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict:
        """
        Call a tool on the MCP server

        Args:
            tool_name: Name of tool to call
            arguments: Tool arguments

        Returns:
            Tool result
        """
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/call',
            'params': {
                'name': tool_name,
                'arguments': arguments
            }
        }

        # Send request
        request_json = json.dumps(request) + '\n'
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()

        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())

        return response.get('result', {})

    async def list_tools(self) -> List[Dict]:
        """List available tools from MCP server"""
        request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/list'
        }

        request_json = json.dumps(request) + '\n'
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()

        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())

        return response.get('result', {}).get('tools', [])

    async def close(self):
        """Close MCP server connection"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
```

### API Endpoint

**File:** `/backend/app/api/v1/endpoints/mcp.py`

```python
from fastapi import APIRouter, HTTPException
from app.integrations.mcp.client import MCPClient
from typing import Dict, Any

router = APIRouter()

# Server configurations
MCP_SERVERS = {
    'zillow': {
        'command': 'python',
        'args': ['/path/to/zillow-mcp-server/server.py']
    },
    'real-estate-data': {
        'command': 'python',
        'args': ['/path/to/real_estate_mcp_server.py']
    }
}


@router.post("/mcp/{server_name}/call")
async def call_mcp_tool(
    server_name: str,
    tool_name: str,
    arguments: Dict[str, Any]
):
    """Call a tool on an MCP server"""
    if server_name not in MCP_SERVERS:
        raise HTTPException(status_code=404, detail="Server not found")

    try:
        client = MCPClient(MCP_SERVERS[server_name])
        await client.start_server()

        result = await client.call_tool(tool_name, arguments)

        await client.close()

        return {
            'success': True,
            'server': server_name,
            'tool': tool_name,
            'result': result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mcp/{server_name}/tools")
async def list_mcp_tools(server_name: str):
    """List available tools from an MCP server"""
    if server_name not in MCP_SERVERS:
        raise HTTPException(status_code=404, detail="Server not found")

    try:
        client = MCPClient(MCP_SERVERS[server_name])
        await client.start_server()

        tools = await client.list_tools()

        await client.close()

        return {
            'success': True,
            'server': server_name,
            'tools': tools
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## MCP Server Discovery

### Official Directories

- **MCP Server Finder:** https://www.mcpserverfinder.com/
- **MCP Resource Hub:** https://mcpnodes.com/
- **GitHub Official:** https://github.com/modelcontextprotocol/servers

### Community Servers

Check these repositories for pre-built servers:
- PostgreSQL, MySQL, SQLite (database access)
- Google Drive, Slack, GitHub (productivity tools)
- Puppeteer (web scraping)
- File system access
- Search engines

---

## Benefits for Real Estate Dashboard

### 1. **Real-Time Data Access**
- Query Zillow without managing API keys
- Access market data on-demand
- No data staleness issues

### 2. **Standardized Interface**
- Same protocol for all data sources
- Easy to add new servers
- Consistent error handling

### 3. **AI-Powered Analysis**
- Claude can analyze property data
- Generate insights automatically
- Answer complex questions

### 4. **Extensibility**
- Create custom tools for your needs
- Integrate proprietary data
- Connect internal systems

---

## Best Practices

### Security

✅ **DO:**
- Validate all inputs from MCP tools
- Rate limit tool calls
- Log all MCP interactions
- Restrict server access to trusted sources

❌ **DON'T:**
- Expose sensitive credentials through MCP
- Allow arbitrary code execution
- Trust all community servers blindly

### Performance

✅ **DO:**
- Cache MCP responses when possible
- Use connection pooling
- Implement timeouts
- Monitor server health

❌ **DON'T:**
- Make synchronous MCP calls
- Start new server for each request
- Ignore resource limits

---

## Troubleshooting

### "Server not responding"

1. Check server is running: `ps aux | grep mcp`
2. Verify configuration path is correct
3. Check server logs for errors
4. Test server independently

### "Tool not found"

1. List available tools first
2. Verify tool name spelling
3. Check server version compatibility
4. Restart server and try again

### "Invalid arguments"

1. Check tool input schema
2. Validate argument types
3. Ensure required fields present
4. Review server documentation

---

## Example: Complete Integration

### 1. Create MCP Server

```bash
# Create server file
cat > /path/to/census_mcp_server.py << 'EOF'
from fastmcp import FastMCP

mcp = FastMCP("Census Data Server")

@mcp.tool()
async def get_demographics(zip_code: str) -> dict:
    # Implementation here
    pass

if __name__ == "__main__":
    mcp.run()
EOF
```

### 2. Configure Claude Desktop

```json
{
  "mcpServers": {
    "census": {
      "command": "python",
      "args": ["/path/to/census_mcp_server.py"]
    }
  }
}
```

### 3. Use in Dashboard

```python
# Backend endpoint
@router.get("/property/{address}/demographics")
async def get_property_demographics(address: str):
    client = MCPClient(MCP_SERVERS['census'])
    await client.start_server()

    # Extract ZIP from address
    zip_code = extract_zip(address)

    result = await client.call_tool(
        'get_demographics',
        {'zip_code': zip_code}
    )

    await client.close()

    return result
```

---

## Resources

- **MCP Documentation:** https://modelcontextprotocol.io/
- **FastMCP Documentation:** https://github.com/jlowin/fastmcp
- **Official Servers:** https://github.com/modelcontextprotocol/servers
- **Community Directory:** https://www.mcpserverfinder.com/

---

**Document Status:** Complete
**Last Updated:** 2025-11-09
**MCP Version:** 1.0
**Recommendation:** Start with Zillow MCP Server, then build custom servers for your specific needs
