import re
p = "/root/zynthio/seamstress/master_seamstress.py"
src = open(p).read()
old = 'HOME / "Desktop" / "zynthio-tools", HOME / "zynthio-tools"'
new = 'HOME / "zynthio", HOME / "zynthio" / "desk", HOME / "zynthio" / "research", HOME / "zynthio" / "seamstress"'
assert old in src, "old path not found"
src = src.replace(old, new)
open(p, "w").write(src)
print("PATCHED: zynrip paths now -> /root/zynthio/*")
