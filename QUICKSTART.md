# Quick Start Guide

## Setup (First Time)

### Windows
1. Ensure Python 3.6+ is installed (download from python.org)
2. Navigate to the mib2zabbix directory
3. Run: `python main.py`
   OR: Double-click `run.bat`

### Linux/macOS
1. Ensure Python 3.6+ and tkinter are installed
2. Navigate to the mib2zabbix directory
3. Make the script executable: `chmod +x run.sh`
4. Run: `./run.sh` or `python3 main.py`

## First Conversion

1. **Launch the Application**
   - Windows: Double-click `run.bat`
   - Linux/Mac: Run `./run.sh`

2. **Load a MIB File**
   - Click "Browse..." in the "Step 1" section
   - Select a .mib file (try `example.mib` to test)
   - Click "Parse" button

3. **Configure Your Template**
   - Template Name: Auto-populated from filename
   - Description: Add optional description
   - Group Name: Leave as "Templates" or customize

4. **Review the Objects**
   - Check the table below to verify parsing worked
   - You should see MIB object names, OIDs, syntax types

5. **Generate Template**
   - Click "Generate Zabbix Template"
   - Choose where to save the XML file
   - Success message will show the file location

6. **Import into Zabbix**
   - Go to Zabbix Frontend
   - Navigate to Templates section
   - Use "Import" function
   - Select the generated XML file
   - Complete the import wizard

## Testing with Example MIB

The package includes `example.mib` which contains sample SNMP objects:
- System description and information
- Interface statistics (counters and octets)
- Perfect for testing the converter

## Troubleshooting

**"Python is not installed"**
- Download Python from https://www.python.org
- Make sure to check "Add Python to PATH" during installation

**"tkinter not found"**
- Windows: Reinstall Python and select tkinter in the installation
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- macOS: `brew install python-tk@3.x`

**"No objects found when parsing"**
- Verify the MIB file has OBJECT-TYPE definitions
- Check that the file is a valid text MIB
- Try the example.mib file first

## Next Steps

1. Test with your own MIB files
2. Customize template names and descriptions
3. Adjust OID update intervals in the generated XML if needed
4. Configure SNMP community strings in Zabbix

## Getting Help

- Check README.md for detailed documentation
- Review the generated XML files to understand the format
- Consult Zabbix documentation for template import issues
