#!/bin/bash
# Bring up the HERMES FREE LOCAL LANE on 127.0.0.1:11435 -> VDS ollama 100.64.0.2:11434
# This is what makes Hermes USE the free qwen3:8b-64k (config default) instead of
# silently falling back to paid deepseek/claude-sonnet-4 (the groundhog-day paying).
# Run once at boot / when port 11435 is closed:
#   bash free_lane.sh  (backgrounds itself)
set -e
LANE_PORT=11435
TARGET=100.64.0.2:11434

# Already up?
if (exec 3<>/dev/tcp/127.0.0.1/$LANE_PORT) 2>/dev/null; then
  echo "free lane already UP on 127.0.0.1:$LANE_PORT"
  exit 0
fi

echo "bringing up free lane 127.0.0.1:$LANE_PORT -> $TARGET"
# Use socat-tcp (forward without TLS, plain HTTP) so ollama /v1 works
# Prefer socat, else use a python-based TCP proxy
if command -v socat >/dev/null 2>&1; then
  nohup socat TCP-LISTEN:$LANE_PORT,reuseaddr,fork TCP:$TARGET \
    >> "$LOCALAPPDATA/hermes/logs/free_lane.log" 2>&1 &
else
  nohup python -c "
import socket,threading
def pipe(a,b):
    try:
        while True:
            d=a.recv(65536)
            if not d: break
            b.sendall(d)
    except Exception: pass
    finally:
        try:a.close()
        except:pass
        try:b.close()
        except:pass
def handle(c):
    try:
        r=socket.create_connection(('$TARGET'.rsplit(':',1)[0],int('$TARGET'.rsplit(':',1)[1])))
        threading.Thread(target=pipe,args=(c,r),daemon=True).start()
        pipe(r,c)
    except Exception as e:
        print('err',e)
        try:c.close()
        except:pass
s=socket.socket();s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('127.0.0.1',$LANE_PORT));s.listen(16)
print('free lane up on $LANE_PORT')
while True:
    c,a=s.accept();threading.Thread(target=handle,args=(c,),daemon=True).start()
" >> "$LOCALAPPDATA/hermes/logs/free_lane.log" 2>&1 &
fi
disown 2>/dev/null || true
sleep 2
if (exec 3<>/dev/tcp/127.0.0.1/$LANE_PORT) 2>/dev/null; then
  echo "FREE LANE UP on 127.0.0.1:$LANE_PORT -> $TARGET"
else
  echo "FAILED - check $LOCALAPPDATA/hermes/logs/free_lane.log"
  exit 1
fi
