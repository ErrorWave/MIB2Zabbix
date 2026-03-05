# MIB to Zabbix Template Converter

A user-friendly GUI application to convert SNMP MIB (Management Information Base) files into Zabbix monitoring templates.

## Features

- **MIB Parsing** - Extract SNMP MIB objects with OIDs and metadata
- **Template Generation** - Convert to Zabbix SNMP items automatically
- **GUI Interface** - Browse files, preview objects, and generate templates
- **Zabbix Compatible** - Generate Zabbix 5.0+ compatible XML templates

## Requirements

- Python 3.6 or higher
- tkinter (`sudo apt-get install python3-tk` on Ubuntu/Debian, `brew install python-tk@3.x` on macOS)

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ and tkinter are installed
3. Run: `python main.py`

No additional pip dependencies required!

## Usage

1. **Load MIB File** - Click "Browse..." and select your .mib file, then click "Parse"
2. **Configure Template** - Set template name, description, and Zabbix group
3. **Review Objects** - Verify extracted MIB objects in the preview pane
4. **Generate** - Click "Generate Zabbix Template" and save the XML file

The template is ready to import directly into Zabbix!

## File Structure

- `main.py` - GUI application
- `mib_parser.py` - MIB file parsing
- `zabbix_generator.py` - Zabbix template generation

## How It Works

The MIB parser extracts OBJECT-TYPE definitions, OIDs, SYNTAX, and ACCESS fields. The Zabbix generator then converts these objects to SNMP items with appropriate data types and generates Zabbix 5.0+ compatible XML templates.

## Example

An example MIB OBJECT-TYPE definition:
```
sysDescr OBJECT-TYPE
    SYNTAX DisplayString
    MAX-ACCESS read-only
    DESCRIPTION "Entity description"
    ::= { system 1 }
```

Gets converted to a Zabbix SNMP item with proper OID mapping (e.g., `.1.3.6.1.2.1.1.1.0`), data type assignment, and template grouping.

## Limitations

- MIB parsing uses regex patterns (not full semantic analysis)
- Complex macros and dependencies may need manual adjustment
- SNMP credentials must be configured in Zabbix manually
- Table entries need additional configuration

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No objects found" | Verify MIB file has OBJECT-TYPE definitions |
| "Failed to parse MIB file" | Ensure file is valid text-based MIB format |
| Template won't import | Check Zabbix 5.0+ compatibility and permissions |

See [ISSUES.md](ISSUES.md) for planned features and enhancements.

## Contributing & Support

Contributions welcome! Please test thoroughly, document new features, follow code style, and test on multiple Python versions. For issues, use the issue tracker.

## License

MIT License - Use and modify freely for your needs

## Version History

### v1.0.0 (2026-03-05)
- Initial release with MIB parsing, Zabbix template generation, and GUI
