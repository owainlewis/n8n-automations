#!/usr/bin/env python3

import json
import sys
import os
from pathlib import Path
import copy

def sanitize_blueprint(input_file, output_file):
    """
    Sanitize n8n workflow blueprint by removing credentials and sensitive data
    """
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Create a deep copy to avoid modifying the original
        sanitized = copy.deepcopy(data)
        
        # Remove sensitive credential data
        if 'nodes' in sanitized:
            for node in sanitized['nodes']:
                if 'credentials' in node:
                    # Replace credential IDs with placeholder values
                    for cred_type in node['credentials']:
                        if 'id' in node['credentials'][cred_type]:
                            node['credentials'][cred_type] = {
                                "id": "PLACEHOLDER_CREDENTIAL_ID",
                                "name": f"{cred_type} account"
                            }
                
                # Remove or sanitize sensitive parameters
                if 'parameters' in node:
                    # Remove specific sensitive fields
                    sensitive_fields = ['apiKey', 'token', 'password', 'secret', 'clientId', 'clientSecret']
                    for field in sensitive_fields:
                        if field in node['parameters']:
                            node['parameters'][field] = 'PLACEHOLDER_VALUE'
                    
                    # Handle nested objects like base/table references
                    if 'base' in node['parameters'] and isinstance(node['parameters']['base'], dict):
                        if 'value' in node['parameters']['base']:
                            node['parameters']['base']['value'] = 'PLACEHOLDER_BASE_ID'
                    
                    if 'table' in node['parameters'] and isinstance(node['parameters']['table'], dict):
                        if 'value' in node['parameters']['table']:
                            node['parameters']['table']['value'] = 'PLACEHOLDER_TABLE_ID'
        
        # Remove instance-specific metadata
        if 'meta' in sanitized:
            sanitized['meta'].pop('instanceId', None)
            sanitized['meta'].pop('templateCredsSetupCompleted', None)
        
        # Remove workflow ID for clean sharing
        sanitized.pop('id', None)
        
        # Remove version ID
        sanitized.pop('versionId', None)
        
        # Write sanitized version
        with open(output_file, 'w') as f:
            json.dump(sanitized, f, indent=2)
        
        print(f"Sanitized blueprint saved to: {output_file}")
        
        # Show what was sanitized
        original_size = os.path.getsize(input_file)
        sanitized_size = os.path.getsize(output_file)
        print(f"Original: {original_size} bytes, Sanitized: {sanitized_size} bytes")   
        return sanitized
        
    except Exception as error:
        print(f"Error sanitizing blueprint: {error}")
        sys.exit(1)

def main():
    """CLI usage"""
    if len(sys.argv) < 2:
        print('Usage: python sanitize_blueprint.py <input-file> [output-file]')
        print('Example: python sanitize_blueprint.py workflow.json blueprints/workflow-clean.json')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '-sanitized.json')
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = Path(output_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    sanitize_blueprint(input_file, output_file)

if __name__ == "__main__":
    main()