# N8N Automations

A collection of n8n workflow blueprints for various automation tasks with business analysis and documentation tools.

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.6+ (for blueprint sanitization and analysis)
- Claude Code CLI (optional, for automated workflow analysis)

### Getting Started

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your actual credentials.

2. **Start n8n:**
   ```bash
   docker-compose up -d
   ```
   Access n8n at http://localhost:5678

3. **Enable tunnel for OAuth/Webhooks (optional):**
   Set `N8N_COMMAND=start --tunnel` in `.env` to enable n8n's built-in tunneling for OAuth callbacks and webhooks.

4. **Stop n8n:**
   ```bash
   docker-compose down
   ```

## Testing Workflows

### Import Workflow for Testing
1. Start n8n with `docker-compose up -d`
2. Navigate to http://localhost:5678
3. Go to Workflows → Import from File
4. Select your workflow JSON file
5. Configure credentials in n8n UI
6. Test the workflow

### Export Workflow from n8n
1. Open your workflow in n8n
2. Click the workflow menu (3 dots)
3. Select "Download"
4. Save to your project directory

## Workflow Analysis

### Generate Business Summaries
Automatically generate A2D2 (AI Automation Design Document) format business summaries for any N8N workflow:

```bash
# Using Claude Code (recommended)
claude --file .claude/analyze_n8n_workflow.claude "Analyze this workflow: blueprints/youtube-research-clean.json"

# Or use the helper script for guidance
python analyze_workflow.py blueprints/youtube-research-clean.json
```

The analysis generates comprehensive business documentation including:
- **Business Goal**: Problem being solved and target users
- **Workflow Steps**: Detailed process flow
- **Integrations**: External services and APIs used
- **Risk Assessment**: Failure modes and mitigation strategies
- **Business Value**: Time savings, ROI estimates, and impact metrics

## Sharing Workflows Safely

### Sanitize Before Sharing
Always sanitize workflows before sharing to remove credentials:

```bash
# Sanitize a single workflow
python sanitize_blueprint.py workflow.json blueprints/workflow-clean.json

# Or let it auto-name the output
python sanitize_blueprint.py workflow.json
```

The sanitization script:
- Removes credential IDs and replaces with placeholders
- Removes sensitive API keys, tokens, passwords
- Removes instance-specific metadata
- Removes workflow and version IDs
- Sanitizes database/table references

### What Gets Sanitized
- ✅ Credential IDs → `PLACEHOLDER_CREDENTIAL_ID`
- ✅ API keys, tokens, secrets → `PLACEHOLDER_VALUE`
- ✅ Airtable base/table IDs → `PLACEHOLDER_BASE_ID`/`PLACEHOLDER_TABLE_ID`
- ✅ Instance metadata and workflow IDs
- ✅ Version information

### Sharing Checklist
- [ ] Export workflow from n8n
- [ ] Run sanitization script
- [ ] Review sanitized file for any remaining sensitive data
- [ ] Share the sanitized version from `blueprints/` directory
- [ ] Include setup instructions for credentials needed

## Adding New Workflows

1. **Develop in n8n UI** with your real credentials
2. **Export** the working workflow
3. **Save** to appropriate directory (e.g., `project-name/workflow.json`)
4. **Sanitize** before sharing: `python sanitize_blueprint.py project-name/workflow.json blueprints/project-name-clean.json`
5. **Generate business documentation**: `claude --file .claude/analyze_n8n_workflow.claude "Analyze this workflow: blueprints/project-name-clean.json"`
6. **Document** any special setup requirements

## Security Notes

- Never commit `.env` file
- Always sanitize before sharing
- Review sanitized files manually
- Keep raw workflows in private directories
- Use environment variables for sensitive configuration