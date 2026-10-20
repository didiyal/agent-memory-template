# injection — 各工具自动加载注入段

通用注入段（写入各工具的自动加载文件，替换【】）＋ 每工具落地位置：
- Claude Code → ~/.claude/CLAUDE.md
- Codex → ~/.codex/AGENTS.md
- ZCode → ~/.zcode/AGENTS.md
- AutoClaw → 平台记忆卡（memory 条目）
自检：片段含 [mem-check] 指令——新会话首轮回显文件哈希前 8 位，未回显=未生效，不得假装已加载。
