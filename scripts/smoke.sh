#!/usr/bin/env bash
# 轻量冒烟：结构检查；无 Key 时不做真实 Embedding 调用
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() { echo "✗ $1" >&2; exit 1; }
ok() { echo "✓ $1"; }

command -v python3 >/dev/null || fail "需要 python3"
[[ -f app.py && -f main.py && -f ingest.py ]] || fail "缺少主脚本"
[[ -f requirements.txt ]] || fail "缺少 requirements.txt"
[[ -f .env.example ]] || fail "缺少 .env.example"
[[ -d docs ]] || fail "缺少 docs/"
ok "核心文件齐全"

# 确保 .env 未被跟踪
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  fail ".env 仍被 git 跟踪，请先 git rm --cached .env"
fi
ok ".env 未跟踪"

python3 - <<'PY'
from pathlib import Path
req = Path("requirements.txt").read_text().lower()
for pkg in ("openai", "faiss", "dotenv", "streamlit"):
    assert pkg in req, pkg
print("requirements ok")
PY
ok "requirements 含关键包"

# 语法检查（不 import 重依赖）
python3 -m py_compile app.py main.py ingest.py
ok "py_compile 通过"

echo ""
echo "smoke: ok"
echo "提示：完整问答需配置 .env 中 OPENAI_API_KEY 后运行 ingest.py / streamlit run app.py"
