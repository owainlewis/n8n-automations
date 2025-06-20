#!/usr/bin/env python3
"""
N8N Workflow Analyzer - Uses Claude Code to generate A2D2 format summaries
Usage: python analyze_workflow.py <workflow.json>
"""

import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_workflow.py <workflow.json>")
        print("Example: python analyze_workflow.py blueprints/youtube-research-clean.json")
        sys.exit(1)
    
    workflow_file = sys.argv[1]
    
    if not Path(workflow_file).exists():
        print(f"Error: File not found: {workflow_file}")
        sys.exit(1)
    
    print(f"To analyze the workflow, run this command in Claude Code:")
    print(f"claude --file .claude/analyze_n8n_workflow.claude 'Analyze this N8N workflow: {workflow_file}'")
    print("\nOr use the Task tool with the prompt from .claude/analyze_n8n_workflow.claude")

if __name__ == "__main__":
    main()