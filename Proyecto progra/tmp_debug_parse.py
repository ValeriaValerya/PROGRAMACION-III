from pathlib import Path
import re
text = Path('Data/Malla_Curri.dzn').read_text(encoding='utf-8')
pattern = re.compile(r'creditos\s*=\s*\[(.*?)\];', re.S)
m = pattern.search(text)
if not m:
    print('no match')
    raise SystemExit(1)
g = m.group(1)
print('repr', repr(g[:200]))
parts = g.split(',')
print('part count', len(parts))
for i, part in enumerate(parts[:5]):
    print('part', i, repr(part))
print('last part repr', repr(parts[-1]))
print('all parts', [repr(part) for part in parts[:10]])
