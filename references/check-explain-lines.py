#!/usr/bin/env python3
"""核对互动式代码阅读文档：每个代码块的实际行数 vs LINE_EXPLAIN 解释键数。
用法: python check-explain-lines.py guide.html
输出: 每块 ✓/✗，全部对齐才算通过。行号错位是逐行解释最常见的 bug，必跑。"""
import io, re, sys, html as html_mod

path = sys.argv[1] if len(sys.argv) > 1 else "guide.html"
src = io.open(path, encoding='utf-8').read()

# 1. 每个 pre.code 的实际行数（去掉 HTML 标签、解码实体后按 \n 数）
pres = re.findall(r'<pre class="code">(.*?)</pre>', src, flags=re.S)
real_lines = [len(html_mod.unescape(re.sub(r'<[^>]+>', '', p)).split('\n')) for p in pres]

# 2. LINE_EXPLAIN 各块键数（只匹配行首的 "N:"，避免解释文本里的 "数字:" 误匹配）
m = re.search(r"var LINE_EXPLAIN = \{(.*?)\n\};", src, flags=re.S)
if not m:
    sys.exit("未找到 LINE_EXPLAIN")
body = m.group(1)
names = re.findall(r"'cb-[a-z]+':\{", body)

if len(names) != len(real_lines):
    print(f"警告: 代码块 {len(real_lines)} 个 vs 解释块 {len(names)} 个")

all_ok = True
print(f"{'块名':14s} {'实际行数':>6s} {'解释键数':>6s}  结果")
for name, rl in zip(names, real_lines):
    key = name[1:-3]
    b = re.search(r"'" + key + r"':\{([^}]*)\}", body, flags=re.S)
    keys = [int(k) for k in re.findall(r"^\s*(\d+):", b.group(1), flags=re.M)]
    ok = keys == list(range(1, rl + 1))
    if not ok:
        all_ok = False
    print(f"{key:14s} {rl:6d} {len(keys):6d}  {'✓' if ok else '✗ 错位!'}")

# 3. 顺带检查：代码块可见文本里有没有 HTML 标签残留（高亮引擎被污染的症状）
q = chr(34)
bad = sum(1 for p in pres if 'class' + q + '=' in html_mod.unescape(re.sub(r'<[^>]+>', '', p)))
if bad:
    print(f"警告: {bad} 个代码块可见文本含 class= 残留（高亮引擎有 bug）")
    all_ok = False

print(">>> 全部对齐" if all_ok else ">>> 仍有问题，修完再交付")
sys.exit(0 if all_ok else 1)
