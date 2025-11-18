#!/usr/bin/env python3
"""
Add metadata fields to all calculator CLI modules.
"""

import os
from pathlib import Path

# Define the metadata fields to add
METADATA_DEFAULT_INPUTS = {
    "tags": "",
    "purpose": "",
    "references": "",
    "notes": "",
}

METADATA_FORM_FIELDS = [
    {"name": "tags", "label": "Tags (comma-separated)", "type": "text", "section": "Metadata"},
    {"name": "purpose", "label": "Analysis Purpose", "type": "text", "section": "Metadata"},
    {"name": "references", "label": "References / Links", "type": "text", "section": "Metadata"},
    {"name": "notes", "label": "Additional Notes", "type": "textarea", "section": "Metadata"},
]

# List of CLI modules to update
CLI_MODULES = [
    "fix_and_flip_cli.py",
    "single_family_rental_cli.py",
    "small_multifamily_cli.py",
    "extended_multifamily_cli.py",
    "hotel_model_cli.py",
    "mixed_use_cli.py",
    "lease_analyzer_cli.py",
    "renovation_budget_cli.py",
]

def update_module(module_path):
    """Add metadata fields to a CLI module."""
    print(f"Updating {module_path.name}...")

    with open(module_path, 'r') as f:
        content = f.read()

    # Add metadata to DEFAULT_INPUTS
    if '"notes"' not in content and '"tags"' not in content:
        # Find DEFAULT_INPUTS dictionary
        import_idx = content.find('DEFAULT_INPUTS: Dict[str, Any] = {')
        if import_idx != -1:
            # Find the closing brace
            brace_count = 0
            in_dict = False
            close_idx = -1
            for i in range(import_idx, len(content)):
                if content[i] == '{':
                    in_dict = True
                    brace_count += 1
                elif content[i] == '}' and in_dict:
                    brace_count -= 1
                    if brace_count == 0:
                        close_idx = i
                        break

            if close_idx != -1:
                # Insert metadata fields before the closing brace
                insertion = '\n    "tags": "",\n    "purpose": "",\n    "references": "",\n    "notes": "",\n'
                content = content[:close_idx] + insertion + content[close_idx:]
                print(f"  ✓ Added metadata to DEFAULT_INPUTS")

    # Add metadata to FORM_FIELDS
    if not any(x in content for x in ['"tags"', '"purpose"', '"references"']):
        # Find FORM_FIELDS list
        fields_idx = content.find('FORM_FIELDS: List[Dict[str, Any]] = [')
        if fields_idx != -1:
            # Find the closing bracket
            bracket_count = 0
            in_list = False
            close_idx = -1
            for i in range(fields_idx, len(content)):
                if content[i] == '[':
                    in_list = True
                    bracket_count += 1
                elif content[i] == ']' and in_list:
                    bracket_count -= 1
                    if bracket_count == 0:
                        close_idx = i
                        break

            if close_idx != -1:
                # Insert metadata fields before the closing bracket
                insertion = '''    {"name": "tags", "label": "Tags (comma-separated)", "type": "text", "section": "Metadata"},
    {"name": "purpose", "label": "Analysis Purpose", "type": "text", "section": "Metadata"},
    {"name": "references", "label": "References / Links", "type": "text", "section": "Metadata"},
    {"name": "notes", "label": "Additional Notes", "type": "textarea", "section": "Metadata"},
'''
                content = content[:close_idx] + insertion + content[close_idx:]
                print(f"  ✓ Added metadata to FORM_FIELDS")

    # Write back
    with open(module_path, 'w') as f:
        f.write(content)

    print(f"  ✓ Updated {module_path.name}")

def main():
    backend_dir = Path(__file__).parent
    scripts_dir = backend_dir / "scripts" / "real_estate"

    print(f"Adding metadata fields to calculator modules...")
    print(f"Scripts directory: {scripts_dir}")

    for module_name in CLI_MODULES:
        module_path = scripts_dir / module_name
        if module_path.exists():
            try:
                update_module(module_path)
            except Exception as e:
                print(f"  ✗ Error updating {module_name}: {e}")
        else:
            print(f"  ⚠ Module not found: {module_name}")

    print("\n✓ Metadata fields added to all modules!")

if __name__ == "__main__":
    main()
