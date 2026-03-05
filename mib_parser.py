"""
MIB Parser Module
Parses MIB files and extracts OID information
"""

import re
from typing import Dict, List, Tuple, Optional


class MIBObject:
    """Represents a single MIB object"""
    
    def __init__(self, name: str, oid: str, syntax: str = "", access: str = "", description: str = ""):
        self.name = name
        self.oid = oid
        self.syntax = syntax
        self.access = access
        self.description = description
    
    def __repr__(self):
        return f"MIBObject(name={self.name}, oid={self.oid})"


class MIBParser:
    """Parses MIB files to extract OID information"""
    
    def __init__(self):
        self.objects: List[MIBObject] = []
        self.module_name = ""
        self.module_id = ""
    
    def parse_file(self, file_path: str) -> Tuple[str, List[MIBObject]]:
        """
        Parse a MIB file and extract objects
        
        Args:
            file_path: Path to the MIB file
            
        Returns:
            Tuple of (module_name, list of MIBObjects)
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self._parse_module_header(content)
            self._parse_objects(content)
            
            return self.module_name, self.objects
        
        except Exception as e:
            raise Exception(f"Error parsing MIB file: {str(e)}")
    
    def _parse_module_header(self, content: str) -> None:
        """Extract module name and ID"""
        # Look for MODULE-IDENTITY or module definition
        module_match = re.search(r'(\w+)\s+MODULE-IDENTITY', content)
        if module_match:
            self.module_name = module_match.group(1)
        else:
            # Try alternate format
            module_match = re.search(r'(\w+)\s+DEFINITIONS', content)
            if module_match:
                self.module_name = module_match.group(1)
    
    def _parse_objects(self, content: str) -> None:
        """Extract MIB objects from content"""
        self.objects = []
        
        # Pattern to match object definitions
        # Looks for: NAME OBJECT-TYPE SYNTAX ... ACCESS ... ::= { parent number }
        pattern = r'(\w+)\s+OBJECT-TYPE\s+.*?::=\s*\{[^}]*\}'
        
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            obj_block = match.group(0)
            obj_name = match.group(1)
            
            # Extract OID
            oid = self._extract_oid(obj_block)
            
            # Extract SYNTAX
            syntax = self._extract_field(obj_block, 'SYNTAX')
            
            # Extract ACCESS/MAX-ACCESS
            access = self._extract_field(obj_block, '(?:MAX-)?ACCESS')
            
            # Extract DESCRIPTION
            description = self._extract_description(obj_block)
            
            if oid:  # Only add if we found an OID
                obj = MIBObject(obj_name, oid, syntax, access, description)
                self.objects.append(obj)
        
        # Also parse standalone OID definitions
        self._parse_standalone_oids(content)
    
    def _extract_oid(self, text: str) -> str:
        """Extract OID from object definition"""
        # Look for ::= { identifier number } or ::= { identifier number number }
        oid_match = re.search(r'::=\s*\{\s*([a-zA-Z0-9\s]+)\s*\}', text)
        if oid_match:
            oid_parts = oid_match.group(1).split()
            return '.'.join(oid_parts)
        return ""
    
    def _extract_field(self, text: str, field_name: str) -> str:
        """Extract a field value from object definition"""
        pattern = rf'{field_name}\s+([^\n]+?)(?=\n|$|[A-Z\-]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_description(self, text: str) -> str:
        """Extract DESCRIPTION field"""
        desc_match = re.search(r'DESCRIPTION\s+"([^"]*)"', text, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            # Clean up the description
            desc = re.sub(r'\s+', ' ', desc)
            return desc[:200]  # Limit to 200 chars
        return ""
    
    def _parse_standalone_oids(self, content: str) -> None:
        """Parse standalone OID definitions not in OBJECT-TYPE blocks"""
        # Pattern: NAME OBJECT IDENTIFIER ::= { parent number }
        pattern = r'(\w+)\s+OBJECT\s+IDENTIFIER\s+::=\s*\{\s*([a-zA-Z0-9\s]+)\s*\}'
        
        matches = re.finditer(pattern, content)
        for match in matches:
            obj_name = match.group(1)
            oid = match.group(2)
            
            # Check if not already in our list
            if not any(obj.name == obj_name for obj in self.objects):
                obj = MIBObject(obj_name, oid)
                self.objects.append(obj)


def parse_mib_file(file_path: str) -> Tuple[str, List[MIBObject]]:
    """
    Convenience function to parse a MIB file
    
    Args:
        file_path: Path to the MIB file
        
    Returns:
        Tuple of (module_name, list of MIBObjects)
    """
    parser = MIBParser()
    return parser.parse_file(file_path)
