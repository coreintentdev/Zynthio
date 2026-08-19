# Critical Disk Cleanup Plan - August 17, 2026

## Current Status: CRITICAL (91% disk usage)

### Disk Usage Analysis:
- Total: 174G
- Used: 158G (91%)
- Available: 17G (9%)

### Largest Directories:
1. /root/zynthio-tools: 41G (26% of used space)
2. /root/model_deploy: 8.9G (6%)
3. /root/heartlib: 7.6G (5%)
4. /root/voice-studio: 6.2G (4%)
5. /root/coreyai-pages: 5.5G (3%)
6. /root/sites: 4.0G (3%)
7. /root/llama.cpp: 1.1G (1%)
8. /root/google-cloud-sdk: 855M
9. /root/go: 713M
10. /root/git: 622M

### Immediate Cleanup Targets:

#### Priority 1: Safe Cleanup (Today)
- /root/_TO_DELETE: 357M (marked for deletion)
- Old logs in /var/log: Potential 1-2G
- Package cache: /var/cache/apt: Potential 500M-1G
- Temp files: /tmp: Variable

#### Priority 2: Archive/Move (This Week)
- /root/model_deploy: 8.9G (if not actively used)
- Old model files in /root/zynthio-tools
- Completed projects in /root/sites

#### Priority 3: Compress/Optimize (Next Week)
- /root/heartlib: 7.6G (compress if not actively used)
- /root/voice-studio: 6.2G (compress old audio files)
- /root/coreyai-pages: 5.5G (archive old versions)

## Cleanup Actions

### Immediate Actions (Today):
1. Remove /root/_TO_DELETE (357M)
2. Clean package cache (apt-get clean)
3. Clean old logs (logrotate)
4. Clean temp files

### Expected Recovery: 1-2G (brings disk to ~89%)

### This Week Actions:
1. Review /root/model_deploy for inactive models
2. Archive old zynthio-tools projects
3. Compress large media files
4. Move completed projects to backup storage

### Expected Recovery: 5-10G (brings disk to ~80-85%)

### Long-term Actions:
1. Implement automated log rotation
2. Set up disk usage alerts at 80%
3. Archive strategy for large projects
4. Consider storage expansion if needed

## Automation for Prevention

### Add to Health Monitor:
- Disk usage threshold: 80% (warning), 90% (critical)
- Automatic cleanup scripts
- Archive triggers for large directories
- Storage expansion recommendations

### Cron Jobs:
- Weekly disk cleanup
- Monthly archive review
- Quarterly storage planning

## Safety Considerations

### Before Deletion:
1. Verify directory contents
2. Check for active dependencies
3. Create backup if uncertain
4. Test deletion on non-critical items first

### Corey Approval Required:
- Any deletion > 1G
- Removal of active projects
- Archive location decisions
- Storage expansion purchases

## Implementation

### Phase 1: Safe Cleanup (Today)
1. Remove /root/_TO_DELETE (357M)
2. apt-get clean (~500M)
3. Log rotation cleanup (~500M)
4. Temp file cleanup (~200M)

### Phase 2: Review and Archive (Week 1)
1. Review each large directory with Corey
2. Identify inactive projects
3. Archive to backup storage
4. Compress media files

### Phase 3: Prevention (Ongoing)
1. Automated cleanup scripts
2. Disk usage monitoring
3. Archive automation
4. Storage planning

## Target Metrics

### Short-term (Today):
- Reduce to 89% disk usage
- Remove 1-2G of safe deletions

### Medium-term (Week 1):
- Reduce to 80-85% disk usage
- Archive 5-10G of inactive data

### Long-term (Month 1):
- Maintain < 80% disk usage
- Automated cleanup active
- Archive strategy established

## Status

**Current Disk Usage: 91% (CRITICAL)**
**Immediate Cleanup: READY TO EXECUTE**
**Corey Approval: REQUIRED for deletions > 1G**

The governance systems are operational, but disk space is critical. Safe cleanup can begin immediately, but large deletions require Corey approval.
