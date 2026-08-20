# DEV DOMAINS COMPREHENSIVE PLAN — ALL OPTIONS
youlittledev.com + youlittle.dev with Option A + B + C combined

## DOMAINS
- **youlittledev.com** — Corey McIvor
- **youlittle.dev** — Corey McIvor
- **Current state**: Owned, not deployed
- **Registry**: Porkbun

## COMPREHENSIVE STRATEGY: A + B + C

### OPTION A: PORTFOLIO/SHOWCASE
**Purpose**: Showcase development work, AI projects, technical capabilities

**Implementation**:
- Landing page: "Building AI systems that actually work"
- Portfolio section: What works after 9-month groundhog day
- Technical blog: Lessons learned, what not to do
- Dev diary: Real progress, no plans only shipped artifacts

### OPTION B: DIRECT AI INTERFACE
**Purpose**: Direct interface to working AI tools (bypassing broken Hermes)

**Implementation**:
- Simple web form → direct ollama API call
- No "assistant" layer, just direct model access
- Clean, working, no groundhog day
- Scripts and examples for direct API usage

### OPTION C: SERVICE/PRODUCT OFFERING
**Purpose**: Monetize development services or products

**Implementation**:
- Service offering: "I build working AI systems"
- Product showcase: Any working tool or script
- Contact form: Direct email, no complex routing
- Pricing: Only for working results, no plans

## SITE STRUCTURE

### youlittledev.com (Main Site)
```
/ (landing)
  - Hero: "Building AI systems that actually work"
  - Anti-groundhog day manifesto
  - Portfolio: What works
  - Services: What I offer
  - Contact: Direct email

/portfolio
  - Working AI tools
  - Technical projects
  - Real deployments (not plans)

/services
  - "I build working AI systems"
  - "No groundhog day guarantee"
  - Pricing based on delivery

/blog
  - 9-month groundhog day lessons
  - What not to do with AI assistants
  - Direct API access tutorials
```

### youlittle.dev (Tool/Documentation)
```
/ (landing)
  - Hero: "Direct AI access, no broken assistants"
  - Quick start: How to use direct API
  - Tools: Available scripts

/tools/ollama-direct
  - Web form → direct ollama API
  - No assistant layer
  - Prompt → response

/docs
  - Direct API access tutorials
  - Script examples
  - Configuration guides

/scripts
  - Downloadable scripts
  - Python examples
  - Bash automation
```

## IMPLEMENTATION PHASES

### PHASE 1: INFRASTRUCTURE (1 day)
```bash
# 1. DNS Configuration
youlittledev.com A → 5.189.143.170
youlittle.dev A → 5.189.143.170
# Cloudflare SSL

# 2. Nginx Setup
server {
    listen 80;
    server_name youlittledev.com youlittle.dev;
    
    root /var/www/dev;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# 3. Basic Content
mkdir -p /var/www/dev/{youlittledev,youlittle}
# Simple "Under construction" pages
```

### PHASE 2: CORE FUNCTIONALITY (1 week)
```bash
# 1. Landing Pages
youlittledev.com: Portfolio + Services
youlittle.dev: Tools + Documentation

# 2. Direct AI Interface (youlittle.dev)
# Simple Flask app
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    response = requests.post('http://127.0.0.1:11434/api/generate', json={
        'model': 'zynthio-twin-7b:latest',
        'prompt': prompt
    })
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# 3. Service Pages
# Simple contact form → direct email
# Service descriptions based on what actually works
```

### PHASE 3: CONTENT BUILDING (ongoing)
```bash
# 1. Portfolio Content
- Document what actually works (local ollama, direct API)
- Before/after: Broken Hermes vs direct access
- Real deployments (not plans)

# 2. Documentation
- Direct API access tutorials
- Script examples
- Configuration guides

# 3. Service Content
- "No groundhog day guarantee"
- Pricing based on delivery
- Examples of working systems
```

## ANTI-GROUNDHOG DAY RULES

### RULE 1: NO PLANS WITHOUT SHIPPED ARTIFACTS
- No "coming soon" sections
- No "roadmap" pages
- Only ship what's real

### RULE 2: NO DOCUMENTATION OF THINGS THAT DON'T WORK
- No tutorials for broken systems
- No guides for abandoned projects
- Only document what works

### RULE 3: NO "ASSISTANT" LAYERS THAT BREAK
- Direct API access only
- No complex agent layers
- No interactive setup blockers

### RULE 4: ONLY SHIP WHEN COREY CAN USE IT
- Test everything before publishing
- Verify Corey can actually use it
- No "theoretical" features

### RULE 5: UPDATE ONLY WHEN SOMETHING REAL CHANGES
- No "content updates" without real progress
- No "site refreshes" without shipped artifacts
- Only update when something real ships

## SUCCESS METRICS

### PHASE 1 SUCCESS
- Domains resolve to VDS
- Basic pages load
- SSL works
- No groundhog day (pages say "building", not "coming soon")

### PHASE 2 SUCCESS
- Direct AI interface works
- Documentation is accurate
- Service pages are honest
- Contact form works

### PHASE 3 SUCCESS
- Portfolio shows real work
- Documentation reflects reality
- Services based on actual capabilities
- Updates only when real changes happen

## NEXT ACTIONS

### IMMEDIATE (today)
1. Zone domains on Cloudflare
2. Set up nginx on VDS
3. Create basic landing pages
4. Test DNS resolution

### SHORT TERM (this week)
1. Build direct AI interface
2. Create portfolio content
3. Write service descriptions
4. Set up contact form

### ONGOING
1. Add only real working tools
2. Document only what works
3. Update only when real changes
4. No groundhog day updates

## RISK MITIGATION

### RISK: Groundhog Day Returns
**Mitigation**: Anti-groundhog day rules, only ship what's real

### RISK: Overcomplication
**Mitigation**: Keep it simple, direct API access, no complex layers

### RISK: Broken Services
**Mitigation**: Test everything before publishing, remove if broken

### RISK: Content Stagnation
**Mitigation**: Update only when real changes happen, no fake updates

---
Comprehensive dev domains plan: 2026-08-20
Domains: youlittledev.com, youlittle.dev
Strategy: Option A (portfolio) + Option B (direct interface) + Option C (services)
Anti-groundhog day: Only ship what's real, no plans without artifacts
Next action: Phase 1 infrastructure (DNS + nginx + basic pages)