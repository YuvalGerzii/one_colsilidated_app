#!/bin/bash
#
# Run all country update scripts
#
# Usage: ./run_all.sh
# With delay: ./run_all.sh 5  # 5 second delay between countries

DELAY=${1:-2}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running all country updates with ${DELAY}s delay between countries..."
echo ""

echo "Updating Australia..."
python3 "$SCRIPT_DIR/update_australia.py"
sleep $DELAY
echo ""
echo "Updating Brazil..."
python3 "$SCRIPT_DIR/update_brazil.py"
sleep $DELAY
echo ""
echo "Updating Canada..."
python3 "$SCRIPT_DIR/update_canada.py"
sleep $DELAY
echo ""
echo "Updating China..."
python3 "$SCRIPT_DIR/update_china.py"
sleep $DELAY
echo ""
echo "Updating Euro Area..."
python3 "$SCRIPT_DIR/update_euro_area.py"
sleep $DELAY
echo ""
echo "Updating France..."
python3 "$SCRIPT_DIR/update_france.py"
sleep $DELAY
echo ""
echo "Updating Germany..."
python3 "$SCRIPT_DIR/update_germany.py"
sleep $DELAY
echo ""
echo "Updating India..."
python3 "$SCRIPT_DIR/update_india.py"
sleep $DELAY
echo ""
echo "Updating Indonesia..."
python3 "$SCRIPT_DIR/update_indonesia.py"
sleep $DELAY
echo ""
echo "Updating Italy..."
python3 "$SCRIPT_DIR/update_italy.py"
sleep $DELAY
echo ""
echo "Updating Japan..."
python3 "$SCRIPT_DIR/update_japan.py"
sleep $DELAY
echo ""
echo "Updating Mexico..."
python3 "$SCRIPT_DIR/update_mexico.py"
sleep $DELAY
echo ""
echo "Updating Netherlands..."
python3 "$SCRIPT_DIR/update_netherlands.py"
sleep $DELAY
echo ""
echo "Updating Poland..."
python3 "$SCRIPT_DIR/update_poland.py"
sleep $DELAY
echo ""
echo "Updating Russia..."
python3 "$SCRIPT_DIR/update_russia.py"
sleep $DELAY
echo ""
echo "Updating Saudi Arabia..."
python3 "$SCRIPT_DIR/update_saudi_arabia.py"
sleep $DELAY
echo ""
echo "Updating South Korea..."
python3 "$SCRIPT_DIR/update_south_korea.py"
sleep $DELAY
echo ""
echo "Updating Spain..."
python3 "$SCRIPT_DIR/update_spain.py"
sleep $DELAY
echo ""
echo "Updating Switzerland..."
python3 "$SCRIPT_DIR/update_switzerland.py"
sleep $DELAY
echo ""
echo "Updating Taiwan..."
python3 "$SCRIPT_DIR/update_taiwan.py"
sleep $DELAY
echo ""
echo "Updating Turkey..."
python3 "$SCRIPT_DIR/update_turkey.py"
sleep $DELAY
echo ""
echo "Updating United Kingdom..."
python3 "$SCRIPT_DIR/update_united_kingdom.py"
sleep $DELAY
echo ""
echo "Updating United States..."
python3 "$SCRIPT_DIR/update_united_states.py"
sleep $DELAY
echo ""

echo "All country updates completed!"
