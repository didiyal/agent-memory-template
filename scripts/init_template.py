# -*- coding: utf-8 -*-
"""init_template.py — 记忆机制模板初始化（生命周期第 1-2 步自动化）

用法（在本仓库克隆后的根目录运行）：
  python scripts/init_template.py --owner 刘迪龙
可选：
  --inject   初始化后自动把注入段写入检测到的 Agent 自动加载文件（默认询问/跳过时用 --yes）
  --yes      跳过确认

做什么：
  第 1 步 初始化：替换全库 {{ROOT}}（=本仓库根目录绝对路径）与【姓名】占位符。
  第 2 步 注入  ：探测 ~/.claude / ~/.codex / ~/.zcode，把注入段写入
                  CLAUDE.md / AGENTS.md（空则写入；有内容且未含"记忆总库"则追加；
                  已含则跳过）。原文件有内容时先备份 .bak-<时间戳>。
  第 3 步 记账  ：更新 registry 接入点状态；git commit "init: 记忆库初始化"。
第 3 步（共写演化）不需要脚本——规则见 README「多 Agent 共写演化」。
"""
import argparse, datetime, os, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True, help="用户姓名（替换【姓名】）")
    ap.add_argument("--inject", action="store_true", help="自动写入各 Agent 自动加载文件")
    ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    inject_block_path = os.path.join(root, "injection", "inject-universal.md")

    # ---- 第 1 步：初始化占位符 ----
    inject = open(inject_block_path, encoding="utf-8").read()
    n = 0
    for dirpath, dirs, files in os.walk(root):
        if ".git" in dirs:
            dirs.remove(".git")
        for fn in files:
            if not fn.endswith((".md", ".py")):
                continue
            p = os.path.join(dirpath, fn)
            t = open(p, encoding="utf-8").read()
            t2 = t.replace("{{ROOT}}", root).replace("【姓名】", a.owner)
            if t2 != t:
                open(p, "w", encoding="utf-8").write(t2)
                n += 1
    print(f"[init] 占位符替换：{n} 个文件（ROOT={root}，OWNER={a.owner}）")

    # ---- 第 2 步：注入各 Agent 自动加载层 ----
    targets = []
    home = os.path.expanduser("~")
    if os.path.isdir(os.path.join(home, ".claude")) or a.inject:
        targets.append(("Claude Code", os.path.join(home, ".claude", "CLAUDE.md")))
    if os.path.isdir(os.path.join(home, ".codex")) or a.inject:
        targets.append(("Codex", os.path.join(home, ".codex", "AGENTS.md")))
    if os.path.isdir(os.path.join(home, ".zcode")) or a.inject:
        targets.append(("ZCode", os.path.join(home, ".zcode", "AGENTS.md")))
    block = open(inject_block_path, encoding="utf-8").read().replace("{{ROOT}}", root).replace("【姓名】", a.owner)

    print("[inject] 将写入以下自动加载文件（已有内容先备份 .bak-%s）：" % stamp)
    for name, path in targets:
        print("   -", name, "->", path)
    if not a.yes and input("确认写入？[y/N] ").strip().lower() not in ("y", "yes"):
        print("[inject] 已跳过（之后可重跑：python scripts/init_template.py --owner %s --inject --yes）" % a.owner)
        targets = []

    results = []
    for name, path in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        old = ""
        if os.path.isfile(path):
            old = open(path, encoding="utf-8", errors="replace").read()
            if old.strip():
                open(path + f".bak-{stamp}", "w", encoding="utf-8").write(old)
        if "记忆总库" in old:
            results.append((name, path, "已含记忆总库段，跳过"))
            continue
        sep = "

" if old.strip() else ""
        open(path, "w", encoding="utf-8").write((old.rstrip() + sep if old.strip() else "") + block + "
")
        results.append((name, path, "已注入" + ("（原文件已备份）" if old.strip() else "")))
    for name, path, st in results:
        print(f"[inject] {name}: {st}")

    # ---- 第 3 步：registry 记账 + git commit ----
    reg = os.path.join(root, "registry.md")
    t = open(reg, encoding="utf-8").read()
    line = "- %s init：owner=%s；注入=%s" % (datetime.date.today().isoformat(), a.owner,
          "、".join(n for n, _, _ in results) if results else "未执行")
    t = t.rstrip() + "
" + line + "
"
    open(reg, "w", encoding="utf-8").write(t)
    os.system('git -C "%s" add -A' % root)
    os.system('git -C "%s" commit -m "init: 记忆库初始化（owner=%s）"' % (root, a.owner))
    print("[done] 生命周期 1-2 完成。第 3 步＝正常使用：任何 Agent 开会话即可增量更新记忆（规则见 README）。")

if __name__ == "__main__":
    main()
