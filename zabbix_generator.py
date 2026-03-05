"""
Zabbix Template Generator
Converts MIB objects to Zabbix template format (XML)
"""

from datetime import datetime
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom
from mib_parser import MIBObject


class ZabbixTemplateGenerator:
    """Generates Zabbix templates from MIB objects"""
    
    def __init__(self, template_name: str, template_description: str = ""):
        self.template_name = template_name
        self.template_description = template_description
        self.items: List[Dict] = []
        self.groups: List[str] = []
    
    def add_mib_objects(self, mib_objects: List[MIBObject]) -> None:
        """
        Add MIB objects as Zabbix items
        
        Args:
            mib_objects: List of MIBObject instances
        """
        for obj in mib_objects:
            self.add_item(
                name=obj.name,
                snmp_oid=f".1{obj.oid}",  # Convert to numeric OID
                description=obj.description,
                item_type="SNMP agent",
                data_type=self._determine_data_type(obj.syntax)
            )
    
    def add_item(self, name: str, snmp_oid: str, description: str = "", 
                 item_type: str = "SNMP agent", data_type: str = "Text",
                 units: str = "", update_interval: str = "300") -> None:
        """
        Add an item to the template
        
        Args:
            name: Item name
            snmp_oid: SNMP OID
            description: Item description
            item_type: Type of Zabbix item
            data_type: Data type (Numeric, Text, etc.)
            units: Units of measurement
            update_interval: Update interval in seconds
        """
        item = {
            'name': name,
            'snmp_oid': snmp_oid,
            'description': description,
            'type': item_type,
            'data_type': data_type,
            'units': units,
            'update_interval': update_interval
        }
        self.items.append(item)
    
    def add_group(self, group_name: str) -> None:
        """Add a host group"""
        if group_name not in self.groups:
            self.groups.append(group_name)
    
    def _determine_data_type(self, syntax: str) -> str:
        """Determine Zabbix data type based on MIB syntax"""
        syntax_upper = syntax.upper()
        
        if 'INTEGER' in syntax_upper:
            return 'Numeric (integer)'
        elif 'OCTET' in syntax_upper or 'STRING' in syntax_upper:
            return 'Text'
        elif 'OBJECT' in syntax_upper and 'IDENTIFIER' in syntax_upper:
            return 'Text'
        elif 'BITS' in syntax_upper:
            return 'Text'
        elif 'GAUGE' in syntax_upper or 'COUNTER' in syntax_upper:
            return 'Numeric (unsigned)'
        else:
            return 'Text'
    
    def generate_xml(self) -> str:
        """
        Generate Zabbix template XML
        
        Returns:
            XML string representing the template
        """
        # Create root element
        zabbix_export = ET.Element('zabbix_export')
        zabbix_export.set('version', '5.0')
        zabbix_export.set('xmlns', 'http://www.zabbix.com/export/5.0')
        
        # Add date
        date_elem = ET.SubElement(zabbix_export, 'date')
        date_elem.text = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Add groups
        groups_elem = ET.SubElement(zabbix_export, 'groups')
        for group in self.groups or ['Templates']:
            group_elem = ET.SubElement(groups_elem, 'group')
            name_elem = ET.SubElement(group_elem, 'name')
            name_elem.text = group
        
        # Add template
        templates_elem = ET.SubElement(zabbix_export, 'templates')
        template_elem = ET.SubElement(templates_elem, 'template')
        
        # Template metadata
        template_name_elem = ET.SubElement(template_elem, 'template')
        template_name_elem.text = self.template_name
        
        name_elem = ET.SubElement(template_elem, 'name')
        name_elem.text = self.template_name
        
        description_elem = ET.SubElement(template_elem, 'description')
        description_elem.text = self.template_description or f"Template created from MIB file: {self.template_name}"
        
        groups_ref = ET.SubElement(template_elem, 'groups')
        for group in self.groups or ['Templates']:
            group_ref = ET.SubElement(groups_ref, 'group')
            name_ref = ET.SubElement(group_ref, 'name')
            name_ref.text = group
        
        # Add items
        items_elem = ET.SubElement(template_elem, 'items')
        item_id = 1
        
        for item in self.items:
            item_elem = ET.SubElement(items_elem, 'item')
            item_elem.set('uuid', self._generate_uuid(item_id))
            
            # Item properties
            self._add_element(item_elem, 'name', item['name'])
            self._add_element(item_elem, 'type', 'SNMP_AGENT')
            self._add_element(item_elem, 'snmp_oid', item['snmp_oid'])
            self._add_element(item_elem, 'key', f"snmp.{item['name']}")
            self._add_element(item_elem, 'delay', item['update_interval'])
            self._add_element(item_elem, 'value_type', self._get_value_type(item['data_type']))
            self._add_element(item_elem, 'description', item['description'] or item['name'])
            
            if item['units']:
                self._add_element(item_elem, 'units', item['units'])
            
            item_id += 1
        
        # Pretty print XML
        xml_string = minidom.parseString(ET.tostring(zabbix_export)).toprettyxml(indent="  ")
        
        # Remove the XML declaration line and extra blank lines
        lines = xml_string.split('\n')[1:]  # Skip XML declaration
        xml_string = '\n'.join([line for line in lines if line.strip()])
        
        return xml_string
    
    def _add_element(self, parent: ET.Element, tag: str, text: str) -> ET.Element:
        """Helper to add a text element"""
        elem = ET.SubElement(parent, tag)
        if text:
            elem.text = str(text)
        return elem
    
    def _get_value_type(self, data_type: str) -> str:
        """Convert data type to Zabbix value type"""
        if 'integer' in data_type.lower():
            return 'NUMERIC'
        else:
            return 'TEXT'
    
    def _generate_uuid(self, item_id: int) -> str:
        """Generate a simple UUID-like identifier"""
        # Simple deterministic UUID generation based on item ID
        import hashlib
        hash_obj = hashlib.md5(f"mib-{item_id}".encode())
        hex_dig = hash_obj.hexdigest()
        # Format as UUID: 8-4-4-4-12
        return f"{hex_dig[:8]}-{hex_dig[8:12]}-{hex_dig[12:16]}-{hex_dig[16:20]}-{hex_dig[20:32]}"
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save the template to an XML file
        
        Args:
            file_path: Path where to save the template
        """
        xml_content = self.generate_xml()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)


def create_template_from_mib(mib_objects: List[MIBObject], 
                             template_name: str,
                             template_description: str = "",
                             group_name: str = "Templates") -> ZabbixTemplateGenerator:
    """
    Convenience function to create a Zabbix template from MIB objects
    
    Args:
        mib_objects: List of MIBObject instances
        template_name: Name of the Zabbix template
        template_description: Description of the template
        group_name: Zabbix group for the template
        
    Returns:
        ZabbixTemplateGenerator instance
    """
    generator = ZabbixTemplateGenerator(template_name, template_description)
    generator.add_group(group_name)
    generator.add_mib_objects(mib_objects)
    return generator
