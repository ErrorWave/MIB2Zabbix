# MIB to Zabbix Template Converter

A user-friendly GUI application to convert SNMP MIB (Management Information Base) files into Zabbix monitoring templates.

## Features

- **Easy MIB Parsing**: Load and parse SNMP MIB files with automatic object extraction
- **Object Preview**: View all extracted MIB objects with their OIDs, syntax, and access types
- **Zabbix Template Generation**: Automatically convert MIB objects to Zabbix SNMP items
- **Customizable Templates**: Set template name, description, and group assignments
- **XML Export**: Generate standard Zabbix template XML files that can be imported directly

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

### Platform-Specific Installation

**Windows**: tkinter is included with Python installer

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-tk
```

**macOS**:
```bash
brew install python-tk@3.x  # Replace x with your Python version
```

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. No additional pip packages needed - uses only Python standard library!

## Usage

### Running the Application

From the application directory:
```bash
python main.py
```

### Step-by-Step Guide

1. **Select MIB File**
   - Click "Browse..." to select your .mib file
   - Click "Parse" to extract objects from the file

2. **Configure Template**
   - Template Name: Will auto-populate from filename
   - Description: Optional template description
   - Group Name: Zabbix host group (default: "Templates")

3. **Review Objects**
   - The preview pane shows all extracted MIB objects
   - Verify the parsing was successful

4. **Generate Template**
   - Click "Generate Zabbix Template"
   - Choose where to save the XML file
   - The template is ready to import into Zabbix!

## File Structure

```
mib2zabbix/
├── main.py                 # Main GUI application
├── mib_parser.py          # MIB file parsing module
├── zabbix_generator.py    # Zabbix template generation
├── requirements.txt       # Dependencies (none!)
└── README.md             # This file
```

## How It Works

### MIB Parser (`mib_parser.py`)
- Extracts module information from MIB headers
- Identifies OBJECT-TYPE definitions
- Parses OIDs, SYNTAX, ACCESS, and DESCRIPTION fields
- Handles both structured object definitions and standalone OID definitions

### Zabbix Generator (`zabbix_generator.py`)
- Converts MIB objects to Zabbix SNMP items
- Automatically determines Zabbix data types based on MIB syntax
- Generates valid Zabbix 5.0+ compatible XML templates
- Assigns proper item keys and update intervals

## Example

### Input MIB File
```
SNMPv2-MIB DEFINITIONS ::= BEGIN

sysDescr OBJECT-TYPE
    SYNTAX DisplayString
    MAX-ACCESS read-only
    DESCRIPTION "A textual description of the entity"
    ::= { system 1 }
```

### Generated Zabbix Template
The converter produces a standard Zabbix XML template with:
- SNMP items configured for each MIB object
- Proper OID mappings (e.g., `.1.3.6.1.2.1.1.1.0`)
- Data type assignments (Numeric, Text, etc.)
- Template grouping and organization

## Supported MIB Formats

- Standard SNMP MIB files (.mib, .txt)
- Both SMIv1 and SMIv2 syntax
- Modules with OBJECT IDENTIFIER definitions
- OBJECT-TYPE and OBJECT-GROUP constructs

## Zabbix Compatibility

- **Tested with**: Zabbix 5.0 and later
- **Template Format**: XML v5.0 standard
- **Item Type**: SNMP agent with configurable update intervals

## Limitations

- MIB parsing is simplified and uses regex patterns
- Complex macro substitutions and dependencies may need manual adjustment
- SNMP community strings and security settings must be configured in Zabbix manually
- Table entries and columnar objects need additional manual configuration

## Troubleshooting

### "No objects found"
- Verify the MIB file uses standard SNMP MIB syntax
- Check that OBJECT-TYPE or OBJECT IDENTIFIER definitions are present

### "Failed to parse MIB file"
- Ensure the file is a valid text-based MIB file
- Try opening the file in a text editor to verify it's readable

### Template won't import into Zabbix
- Check Zabbix version compatibility (5.0+)
- Verify you have permission to create templates
- Check Zabbix logs for import errors

## Future Enhancements

- [ ] Advanced MIB syntax parsing with semantic analysis
- [ ] SNMP walk simulation for testing
- [ ] Multiple MIB file merging
- [ ] Template validation against Zabbix API
- [ ] Direct Zabbix server import via API
- [ ] Support for MIB dependencies and imports
- [ ] Visual MIB object hierarchy tree

## License

MIT License - Feel free to use and modify for your needs

## Support

For issues or suggestions, please report them in the issue tracker or contact the development team.

## Contributing

Contributions are welcome! Please:
1. Test thoroughly with various MIB files
2. Document any new features
3. Follow existing code style
4. Test on multiple Python versions

## Technical Notes

### MIB Parsing Strategy
- Uses regex patterns to identify key MIB structures
- Extracts OID components from `::= { parent number }` syntax
- Determines data types from SYNTAX field content
- Preserves DESCRIPTION fields up to 200 characters

### Zabbix Template Structure
- Root: `<zabbix_export>` (v5.0)
- Contains: Groups, Templates, and Items
- Each item has SNMP OID, type, and update interval
- Follows Zabbix XML schema for v5.0+

## Version History

### v1.0.0 (2026-03-05)
- Initial release
- MIB parsing from files
- Zabbix template generation
- GUI application with file dialogs
- Support for basic SNMP objects
