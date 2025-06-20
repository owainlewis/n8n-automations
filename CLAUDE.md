# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains n8n automation workflows and scripts. n8n is a workflow automation platform that connects different services through visual node-based workflows.

## Key Components

- **run-n8n.sh**: Docker command to start n8n instance with persistent data storage
- **youtube-content-research/**: Contains YouTube research automation workflow
  - **youtube_research_assistant.json**: n8n workflow that analyzes YouTube channel performance by fetching channel data, video statistics, and storing results in Airtable

## Common Commands

### Running n8n
```bash
./run-n8n.sh
```
This starts n8n in Docker on port 5678 with persistent data volume.

### Accessing n8n
- Web interface: http://localhost:5678
- Data is persisted in Docker volume `n8n_data`

## Workflow Architecture

The YouTube Research Agent workflow follows this data flow:
1. **Manual/Schedule Trigger** → **Configuration** (sets VIDEO_COUNT=50)
2. **Get Channels** (from Airtable with Selected=1 filter)
3. **Get Channel** → **Get Videos** → **Get Video Statistics** (YouTube API calls)
4. **Last 3 Months** filter → **Add Entry** (upsert to Airtable Videos table)

Key integrations:
- YouTube OAuth2 API for channel and video data
- Airtable for data storage (Channels and Videos tables)
- Scheduled daily execution at 9 AM

## File Structure

- Workflow JSON files contain complete n8n workflow definitions including nodes, connections, credentials references, and configuration
- Shell scripts provide Docker runtime commands for the n8n platform