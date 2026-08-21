# VDS API Access Guide - Cloudflare & Porkbun

## Overview
This guide documents the correct API access methods for Cloudflare and Porkbun on the VDS.

## Porkbun API Access

### Correct API Endpoint
- **BASE URL**:  (NOT )
- **Domain List**: 

### Authentication Method
- **Headers** (recommended):
  
- **Body** (legacy):
  

### Current Credentials
- **API Key**: 
- **Secret Key**: 

### Usage Scripts
-  - Main export script for VDS
-  - Alternative domain listing script
-  - MacBook version (synced to VDS)

### Export Process


### Domain Opt-In Requirement
- All domains must be opted in for API access via Porkbun dashboard
- Enable Opt all domains into API access in Porkbun Domain Management

## Cloudflare API Access

### Authentication
- Uses Cloudflare API token (stored in environment variables or config)
- Standard Cloudflare API v4 endpoints

### Domain List
-  - Current list of Cloudflare domains (23,887 domains)
- Located in 

### Scripts
- Various ingest scripts for Cloudflare domain processing
-  - Ingestion logs

## Common Issues & Solutions

### 403 Forbidden Errors
- **Root Cause**: Wrong API base URL (using  instead of )
- **Fix**: Update URL to use  subdomain
- **Verification**: Response should be JSON, not HTML

### Empty Domain Lists
- **Root Cause**: Domains not opted in for API access
- **Fix**: Enable API access in Porkbun dashboard
- **Verification**: Check Porkbun API Access settings

## VDS Access from MacBook

### SSH Configuration
- **Config Host**:  (in )
- **IP**:  (via Tailscale: )
- **User**: 
- **Key**: 

### File Transfer


## MCP Server Alternative
Porkbun now offers an official MCP server:

This provides native tool access for Claude Desktop, Cursor, Cline, etc.

## Updates
- **2026-08-20**: Fixed API base URL from  to 
- **2026-08-20**: Updated API credentials to latest keys
- **2026-08-20**: Switched to header-based authentication
