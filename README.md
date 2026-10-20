# Agent Memory Template — 跨 Agent 记忆总库模板

> 用途：为任何「一人 + 一台机器 + 多个 AI 工具」的环境，一键搭建跨 Agent 共享的记忆总库。
> 本模板 = 【OWNER】的记忆机制抽象（2026-10-20 从 D:\AgentMemory + 两套 llm-wiki + 轻量契约型实践提炼）。
> 自举入口：任何新 Agent 接管本库时，第一件事 = 通读本文件。

## 一、设计原则（12 条，实践验证）

1. 唯一自举入口（本文件）；2. 纯 Markdown + 文件夹 + Git，零私有格式；3. 判定四问落位；
4. 失效不删除（_archive + superseded_by + log 仅追加）；5. 矛盾不覆盖（review_needed）；
6. frontmatter 最小集（owner/domain/type/created/updated/verified_at/source）；
7. 机器事实带 verified_at，超 30 天先核验再执行；8. Git commit = 同步单元，镜像只增量永不回灌；
9. 注入指针段进各 Agent 自动加载文件；10. lint 定期（清单制）；11. 冷启动验收（新会话答对 N 题）；
12. 项目层用轻量契约型（project-lite/PROJECT-CONTRACT.md，"改文件=改行为"）。

## 二、目录结构

```text
{{ROOT}}\
├── README.md                ← 宪法（本文件，唯一入口）
├── registry.md              ← 域+项目区注册表（派生缓存，可重建）
├── log.md                   ← 变更日志（仅追加，一行一事）
├── people\                  ← 人的域（一人一目录：profile/experiences/style/preferences）
├── machine\                 ← 机器域（system/known-pitfalls/automation-inventory，verified_at 强制）
├── shared\                  ← 共享方法论与调研
├── lint\                    ← 体检报告（按 lint-checklist.md）
├── project-lite\            ← 项目层【轻量契约型】模板（PROJECT-CONTRACT.md）
├── injection\               ← 各 AI 工具自动加载注入段（Claude Code/Codex/ZCode/AutoClaw）
└── docs\                    ← 设计说明与决策记录
```

## 三、判定四问（新事实写到哪）

1. 换个项目还为真吗（人的事实/经历/风格/偏好）→ people\<人>\
2. 只在本项目为真吗 → 留该项目（轻量契约型），本表 registry 登记
3. 关于机器/软件/自动化 → machine\
4. 高频变化 → 留项目域；个人域只收慢变事实
附：关于另一个人的 → 写他的域，这边只留指针。

## 四、注入（让总库进入各工具的自动加载）

把 injection\ 下对应片段，写入各工具的自动加载文件：
- Claude Code → ~/.claude/CLAUDE.md
- Codex → ~/.codex/AGENTS.md
- ZCode → ~/.zcode/AGENTS.md
- AutoClaw → 平台记忆卡（memory 条目）
验证：新会话首轮回显 [mem-check] 哈希（片段内含自检指令）。

## 五、裁剪指南（三种形态）

| 形态 | 何时用 | 取哪些件 |
|---|---|---|
| 总库型（本模板全量） | 一人多机多工具 | 全部 |
| 项目 llm-wiki 型 | 单项目深度知识（可另建 wiki/） | SCHEMA 思想 + wiki 四类页 + index |
| 项目轻量契约型 | 普通项目/定时任务 | project-lite/PROJECT-CONTRACT.md 一个文件即可 |

## 六、使用生命周期（三步）

> 这是本模板的标准用法：拉取 → 初始化 → 注入 → 多 Agent 共写演化。

### 第 1 步 · 拉取
`git clone <远程仓库>` 到本机任意位置（克隆后的目录就是记忆库根目录 {{ROOT}}）。

### 第 2 步 · 初始化＋注入（脚本自动化）
```bash
python scripts/init_template.py --owner 你的姓名 --inject --yes
```
- 初始化：替换全库 {{ROOT}}／【姓名】占位符；
- 注入：探测本机的 Claude Code／Codex／ZCode，把总库注入段写入各自的自动加载文件（已有内容先备份 .bak-时间戳）；
- 更新 registry 接入点状态并 git commit。
- AutoClaw：把 inject-universal.md 内容存为平台记忆卡。

### 第 3 步 · 多 Agent 共写演化（无需脚本，规则如下）
为什么注入到每个 Agent 的自动加载层？——**这样无论用哪个 Agent，只要开启会话，都自动带着记忆、也都能增量修改记忆**。演化规则：

1. **谁改谁提交**：任何 Agent 修改记忆文件后，当场 `git commit`（commit 信息带写入者身份）；
2. **只增量，不重写**：改文件＝锚定 Edit 小改；重写/删除前旧版进 _archive 并记 log；
3. **落位走判定四问**（README §三）：个人事实进 people，项目事实进该项目（轻量契约），机器事实进 machine；
4. **log 追加一行**：每次有意义的变更（里程碑/纠错/新页面）在 log.md 追加一行；
5. **冲突**：同一文件两个 Agent 都改了——后 commit 者负责合并，以 git 为准；
6. **平台记忆卡（AutoClaw）**：作为应急层与总库双写（重要纠错两边同步），日常增量以总库为准；
7. **lint 兜底**：定期跑 lint-checklist.md，漂移会被抓出来。

## 七、验收

新机器 git clone 后，新 Agent 只凭本 README 能答对冷启动问题（人 3 题/机器 3 题/项目 3 题）= 合格。
