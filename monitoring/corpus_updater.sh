#!/bin/bash
# Auto-update corpus with new domains
LOG_FILE='/root/zynthio/monitoring/corpus_update.log'
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting corpus update check..." >> $LOG_FILE

cd /root/zynthio/corpus
source venv/bin/activate

# Check for new domains in Porkbun export
if [ -f '/root/zynthio/corpus/porkbun_domains.txt' ]; then
    TOTAL_DOMAINS=$(wc -l < /root/zynthio/corpus/porkbun_domains.txt)
    echo "[$TIMESTAMP] Found $TOTAL_DOMAINS domains in Porkbun export" >> $LOG_FILE
fi

# Check for new domains in Cloudflare export
if [ -f '/root/zynthio/corpus/cloudflare_domains.txt' ]; then
    TOTAL_CF=$(wc -l < /root/zynthio/corpus/cloudflare_domains.txt)
    echo "[$TIMESTAMP] Found $TOTAL_CF domains in Cloudflare export" >> $LOG_FILE
fi

# Check current corpus size
if [ -f '/root/zynthio/corpus/corpus_FINAL_20260820.index' ]; then
    python3 -c "import faiss; index = faiss.read_index('corpus_FINAL_20260820.index'); print(f'Current corpus: {index.ntotal} documents')" >> $LOG_FILE
fi

echo "[$TIMESTAMP] Corpus update check complete" >> $LOG_FILE
