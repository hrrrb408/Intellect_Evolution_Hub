# Intellect Evolution Hub - obsidian-second-brain

面向 Obsidian 的多工具通用第二大脑底座。

这个仓库是在 `eugeniughelbur/obsidian-second-brain` 的跨 CLI 命令系统基础上，融合 `claude-obsidian` 风格的 hot/index/log、manifest-aware ingest、query、锁、health、chunked BM25、rerank、claim extraction、contradiction review、patch proposals、Desktop adapter，以及 SINGULARITY/IEH stage-model 知识库结构后形成的增强版。

它的目标不是做一个只能服务某个 AI 工具的笔记模板，而是把同一个 Obsidian vault 变成 Claude Code、Codex CLI、Codex Desktop、Claude Desktop、Gemini CLI、OpenCode、Hermes 都能共同使用的知识操作系统。

## 目录

- [适合谁用](#适合谁用)
- [核心理念](#核心理念)
- [功能总览](#功能总览)
- [仓库结构](#仓库结构)
- [Vault 结构](#vault-结构)
- [安装前准备](#安装前准备)
- [快速开始](#快速开始)
- [从零安装](#从零安装)
- [配置环境变量](#配置环境变量)
- [初始化 vault](#初始化-vault)
- [多平台安装](#多平台安装)
- [核心工作流](#核心工作流)
- [命令参考](#命令参考)
- [路由、模式与 stage model](#路由模式与-stage-model)
- [PDF、OCR 与 source ingest](#pdfocr-与-source-ingest)
- [检索、BM25 与 rerank](#检索bm25-与-rerank)
- [安全写入策略](#安全写入策略)
- [验证与排障](#验证与排障)
- [升级、回滚与维护](#升级回滚与维护)
- [与上游项目的关系](#与上游项目的关系)

## 适合谁用

这个项目适合以下使用方式：

- 你把 Obsidian 当长期知识库，而不是临时对话缓存。
- 你同时使用多个 AI 工具，希望它们读写同一个 vault，而不是各自维护一份上下文。
- 你希望论文、文章、项目经验、商业想法、人生决策都能进入同一套可检索、可审计、可增长的结构。
- 你希望 AI 写入知识库时有 manifest、日志、锁、health、proposal、dry-run 和回滚意识。
- 你希望保留 source 原文，同时让 source 推动 concepts、entities、queries、MOCs 生长。

不适合的情况：

- 你只想要一个极简 Obsidian 模板。
- 你不希望 AI 工具写文件。
- 你不想维护任何本地脚本、环境变量或 adapter。
- 你要求所有写入完全自动化且不需要人工审查。

## 核心理念

### 一个 vault，多种 AI 工具

不同 AI 工具可以有不同入口，但必须遵守同一套 vault contract：

- 同一个 Obsidian vault。
- 同一套 AI-first note 规则。
- 同一套 source preservation 规则。
- 同一套 retrieval 顺序：`hot` -> `index` -> BM25/chunks -> durable notes。
- 同一套写入策略：默认保守、可审查、可回滚。

### Source 不是收藏品，而是知识生长材料

普通笔记系统容易变成文件堆。这个项目要求 source 至少进入以下路径之一：

1. 保留 raw source。
2. 生成 source-summary。
3. 抽取 claims、entities、concepts。
4. 发现 contradiction candidates。
5. 生成 patch proposals。
6. 更新 timeline/history。
7. 通过 fusion 进入 concept/query/entity/MOC 层。

### 默认安全，不自动污染知识库

系统可以生成很多 proposal 和 draft，但默认不强行应用：

- `fusion` 默认只生成 report 和 draft。
- `apply-proposals` 默认 dry-run。
- contradiction 永远是 review candidate，不自动改成最终结论。
- `--apply` 只应用安全 append 类更新。
- `--upgrade-scaffolds` 只升级被识别为旧 scaffold 的页面，不覆盖人工写过的 durable notes。

## 功能总览

当前能力：

- 59 个平台中立命令，统一从 `commands/` 编译到不同 AI 工具适配层。
- 支持 Claude Code、Codex CLI、Gemini CLI、OpenCode、Hermes build 输出。
- 支持 Codex Desktop 面向同一 vault 的 adapter 安装、检查与回滚。
- 支持 Claude Desktop 通过 MCP、filesystem 或项目说明使用同一 vault protocol。
- 支持 IEH/SINGULARITY stage model：`raw/`、`source-summaries/`、`concepts/`、`entities/`、`queries/`、`mocs/`、`maintenance/`。
- 支持 compound vault：`wiki/hot.md`、`wiki/index.md`、`wiki/log.md`、manifest、chunked BM25、health。
- 支持 PDF ingest、`pdftotext` 抽取、OCR fallback、抽取质量诊断。
- 支持 source claim extraction、contradiction candidates、timeline/history updater、patch proposal、safe apply。
- 支持 fusion draft workflow：从 source 生成可审查的中文优先 processed-note 草稿，并安全创建/升级 stage pages。
- 支持 configurable routing：按 domain/subdomain 自动路由 source、summary、concept、entity、query、MOC。
- 支持 Ollama rerank，可用时提升检索排序，不可用时自动退回 lexical/BM25。
- 支持 manifest repair，修复 runtime 绕过标准 ingest 后留下的账本缺口。
- 支持 Desktop adapter 检查与回滚，避免长期 drift。

## 仓库结构

```text
obsidian-second-brain/
|-- commands/                  # 59 个平台中立命令定义，是命令的唯一源头
|-- references/                # vault schema、write policy、retrieval、desktop adapter 等规范
|-- scripts/                   # 核心脚本、build、research、compound vault engine
|-- scripts/research/          # research/x/youtube/podcast/notebooklm 工具
|-- adapters/                  # claude-code/codex-cli/gemini-cli/opencode/hermes 适配层
|-- hooks/                     # Claude Code 与 Hermes lifecycle hook 示例
|-- integrations/              # MCP / Telegram journal 等可选集成
|-- examples/                  # 示例 vault
|-- tests/                     # pytest 测试
|-- architecture.md            # 架构说明
|-- SKILL.md                   # AI 工具加载的主技能说明
|-- README.md                  # 当前文档
|-- install.sh                 # Claude Code 传统安装脚本
|-- update.sh                  # 更新辅助脚本
|-- pyproject.toml             # Python 项目依赖
`-- uv.lock                    # uv 锁文件
```

关键原则：

- `commands/` 是命令源。
- `dist/` 是生成物，不要手改。
- `scripts/compound_vault.py` 是 compound vault 的确定性核心。
- `references/` 是 AI runtime 应遵守的规则层。
- `hooks/`、`integrations/`、`adapters/` 是平台接入层。

## Vault 结构

IEH/SINGULARITY mode 下，一个 vault 会被组织成：

```text
IEH/
|-- SCHEMA.md
|-- index.md
|-- log.md
|-- SOUL.md
|-- CRITICAL_FACTS.md
|-- _CLAUDE.md
|-- AGENTS.md
|-- CODEX-DESKTOP.md
|-- CLAUDE-DESKTOP.md
|-- HERMES.md
|-- raw/
|   |-- articles/<domain>/<subdomain>/
|   `-- papers/<domain>/<subdomain>/
|-- source-summaries/<domain>/<subdomain>/
|-- concepts/<domain>/<subdomain>/
|-- entities/<domain>/<subdomain>/
|-- queries/<domain>/<subdomain>/
|-- comparisons/<domain>/<subdomain>/
|-- mocs/<domain>/<subdomain>/
|-- maintenance/
|-- wiki/
|   |-- hot.md
|   |-- index.md
|   |-- log.md
|   |-- meta/
|   `-- resources/
|-- .vault-meta/
|   |-- compound-manifest.json
|   |-- desktop-install-manifest.json
|   |-- singularity-routes.json
|   |-- mode.json
|   |-- bm25/index.json
|   `-- chunks/
|-- .agents/                   # Codex Desktop / Agent Skills adapter
`-- .codex/                    # Codex Desktop local scripts/references
```

目录说明：

- `raw/` 保存原始材料的可追溯副本。PDF 原件通常放在 `raw/papers/`，抽取文本放在 `raw/articles/`。
- `source-summaries/` 是单 source 阅读脚手架，用于保留摘要、贡献、方法、证据和后续链接。
- `concepts/` 是可复用概念，不等同于单篇论文标题页。
- `entities/` 是人物、机构、工具、论文、数据集等稳定对象。
- `queries/` 是学习问题、研究问题和判断入口，适合承载综合性理解。
- `comparisons/` 是多 source 横向比较。
- `mocs/` 是领域导航，不承载长篇正文。
- `maintenance/` 放 vault-wide 维护文档、lint 规则、迁移记录。
- `wiki/hot.md` 是最近上下文缓存。
- `wiki/index.md` 是可读索引。
- `wiki/log.md` 是操作日志。
- `wiki/meta/` 放系统生成的 report、proposal 和 draft。
- `.vault-meta/` 放机器索引、manifest、route table、mode 和 chunks。

## 安装前准备

### 必需工具

- Git
- Bash 或 zsh
- Python 3.10+
- Obsidian

### 推荐工具

- `uv`：安装 Python 依赖更稳定。
- `pdftotext`：PDF 文本抽取。
- `pdftoppm`：OCR fallback 前的页面渲染。
- `tesseract`：OCR fallback。
- `ollama`：本地 embedding/rerank。

macOS 可参考：

```bash
brew install uv poppler tesseract ollama
```

Linux 可用系统包管理器安装：

```bash
sudo apt-get install poppler-utils tesseract-ocr
```

### Python 依赖

推荐：

```bash
uv sync
```

如果不用 `uv`：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

## 快速开始

假设：

- 仓库路径：`/path/to/obsidian-second-brain`
- Vault 路径：`/path/to/IEH`

推荐先从内置模板创建一个干净 IEH vault。这个模板和本项目实际使用的 compound/stage-model 结构一致，但不包含任何私人材料：

```bash
cd /path/to/obsidian-second-brain
cp -R examples/ieh-vault-template "$OBSIDIAN_VAULT_PATH"
```

如果 `$OBSIDIAN_VAULT_PATH` 还没有设置，可以先设置：

```bash
cd /path/to/obsidian-second-brain
export OBSIDIAN_VAULT_PATH="/path/to/IEH"
cp -R examples/ieh-vault-template "$OBSIDIAN_VAULT_PATH"
```

然后初始化 runtime：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" init
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --json
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
```

`init` 默认就是 IEH 模板，会写入 `.vault-meta/ieh-template.json`，并在没有既有 mode 时设置为 `singularity`。只有维护旧 obsidian-second-brain vault 时才使用 `init --template generic`。

之后再 ingest 第一份材料：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" ingest /path/to/source.pdf
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" query "这篇材料的核心观点是什么？" --refresh
```

如果你不想复制模板，也可以直接对空目录初始化：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" init
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
```

如果要在 Codex Desktop 使用：

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --json
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --check --json
```

如果要在 Claude Code 使用：

```bash
bash scripts/build.sh --platform claude-code
mkdir -p ~/.claude/skills ~/.claude/commands
ln -sfn "$(pwd)/dist/claude-code" ~/.claude/skills/obsidian-second-brain
ln -sfn "$(pwd)/dist/claude-code/commands/"*.md ~/.claude/commands/
```

重启对应 AI 工具后使用 `/obsidian-*` 命令。

## 从零安装

### 1. 克隆仓库

```bash
git clone https://github.com/hrrrb408/Intellect_Evolution_Hub.git
cd Intellect_Evolution_Hub/obsidian-second-brain
```

如果你已经在 Claude Code skills 目录中使用：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/hrrrb408/Intellect_Evolution_Hub.git ~/.claude/skills/Intellect_Evolution_Hub
cd ~/.claude/skills/Intellect_Evolution_Hub/obsidian-second-brain
```

### 2. 安装依赖

```bash
uv sync
```

或：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

### 3. 创建或选择 Obsidian vault

推荐从 IEH 模板创建新 vault：

```bash
export OBSIDIAN_VAULT_PATH="$HOME/Obsidian/IEH"
cp -R examples/ieh-vault-template "$OBSIDIAN_VAULT_PATH"
```

这个模板位于：

```text
examples/ieh-vault-template/
```

它包含 IEH 的 stage-model 目录、runtime 手册、路由表、Obsidian starter config 和 `.gitignore`，但不包含私人资料、PDF、generated chunks、`.codex/`、`.agents/` 或 `.git/`。

也可以使用已有 vault，但建议先备份。对已有 vault 初始化时，runtime 会追加必要结构，但不会自动把旧 PARA/生活模板迁移成 IEH stage model。

### 4. 设置 vault 路径

```bash
export OBSIDIAN_VAULT_PATH="$HOME/Obsidian/IEH"
```

长期使用建议写入 shell 配置：

```bash
echo 'export OBSIDIAN_VAULT_PATH="$HOME/Obsidian/IEH"' >> ~/.zshrc
```

### 5. 初始化 vault

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" init
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --json
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" index
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" chunks
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" hot
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
```

### 6. 打开 Obsidian

在 Obsidian 中打开 `$OBSIDIAN_VAULT_PATH`。

建议先阅读：

- `SCHEMA.md`
- `_CLAUDE.md`
- `AGENTS.md`
- `DESKTOP-ADAPTERS.md`
- `index.md`
- `wiki/hot.md`
- `wiki/index.md`

## 配置环境变量

### 最小配置

```bash
export OBSIDIAN_VAULT_PATH="/path/to/IEH"
```

`compound_vault.py` 的 `--vault` 参数优先级高于环境变量。如果不传 `--vault`，会使用：

1. `OBSIDIAN_VAULT_PATH`
2. 当前工作目录

### Research 工具配置

复制 `.env.example`：

```bash
mkdir -p ~/.config/obsidian-second-brain
cp .env.example ~/.config/obsidian-second-brain/.env
chmod 600 ~/.config/obsidian-second-brain/.env
```

常用变量：

```bash
OBSIDIAN_VAULT_PATH=
XAI_API_KEY=
PERPLEXITY_API_KEY=
GEMINI_API_KEY=
YOUTUBE_API_KEY=
GROK_MODEL=grok-4
PERPLEXITY_RESEARCH_MODEL=sonar-pro
PERPLEXITY_DEEP_MODEL=sonar-deep-research
NOTEBOOKLM_MODEL=gemini-2.5-flash
```

没有 API key 时，部分 research 命令会不可用或降级；vault 本地 ingest/query/health 不依赖这些 key。

### Ollama rerank 配置

默认：

```bash
OLLAMA_URL=http://127.0.0.1:11434
COMPOUND_OLLAMA_MODEL=nomic-embed-text
COMPOUND_OLLAMA_TIMEOUT_SEC=3
```

安装模型：

```bash
ollama pull nomic-embed-text
```

查询时使用：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" query "问题" --rerank auto
```

安全说明：

- 默认只建议使用本机 Ollama。
- 如果 `OLLAMA_URL` 指向远程端点，query chunks 会发送到该端点。
- 只有明确理解数据边界时才使用远程 rerank。

## 初始化 vault

### init

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" init
```

创建或更新：

- `wiki/hot.md`
- `wiki/index.md`
- `wiki/log.md`
- `.vault-meta/`
- 基础 scaffold

### mode

查看：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" mode get
```

设置：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" mode set singularity
```

常见 mode：

- `generic`：通用 Obsidian wiki。
- `para`：偏 PARA/项目管理。
- `singularity`：IEH/SINGULARITY stage model，适合多领域知识库。

### index / chunks / hot

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" index
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" chunks
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" hot
```

用途：

- `index`：重建 `wiki/index.md` 和 `wiki/meta/index.json`。
- `chunks`：重建 `.vault-meta/chunks/` 和 `.vault-meta/bm25/index.json`。
- `hot`：刷新 `wiki/hot.md`。

## 多平台安装

### 构建所有平台

```bash
bash scripts/build.sh
```

构建单个平台：

```bash
bash scripts/build.sh --platform claude-code
bash scripts/build.sh --platform codex-cli
bash scripts/build.sh --platform gemini-cli
bash scripts/build.sh --platform opencode
bash scripts/build.sh --platform hermes
```

输出：

```text
dist/claude-code/
dist/codex-cli/
dist/gemini-cli/
dist/opencode/
dist/hermes/
```

不要手改 `dist/`。需要改命令时修改 `commands/`，然后重新 build。

### Claude Code

方式一：使用传统安装脚本。

```bash
./install.sh
```

方式二：使用 build 输出。

```bash
bash scripts/build.sh --platform claude-code
mkdir -p ~/.claude/skills ~/.claude/commands
ln -sfn "$(pwd)/dist/claude-code" ~/.claude/skills/obsidian-second-brain
ln -sfn "$(pwd)/dist/claude-code/commands/"*.md ~/.claude/commands/
```

重启 Claude Code 后使用：

- `/obsidian-init`
- `/obsidian-compound-init`
- `/obsidian-compound-ingest`
- `/obsidian-query`
- `/obsidian-compound-health`
- `/obsidian-fusion`

Claude Code hooks：

- `hooks/obsidian-bg-agent.sh`
- `hooks/postcompact.hook.example.json`
- `hooks/validate-ai-first.sh`
- `hooks/validate-ai-first.hook.yaml`

这些 hook 是 opt-in。安装前先阅读 hook 文件和 `references/compound-write-policy.md`。

### Codex CLI

```bash
bash scripts/build.sh --platform codex-cli
```

将 `dist/codex-cli` 按你的 Codex CLI skills/agents 目录规则安装。该 adapter 会输出：

- `AGENTS.md`
- `.agents/skills/`
- scripts
- references

### Codex Desktop

Codex Desktop 推荐直接把 adapter 文件装进目标 vault：

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --json
```

安装后 vault 中会出现：

```text
AGENTS.md
.agents/skills/
.codex/scripts/compound_vault.py
.codex/references/desktop-adapters.md
DESKTOP-ADAPTERS.md
.vault-meta/desktop-install-manifest.json
```

检查：

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --check --json
```

回滚：

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --rollback --json
```

使用原则：

- Codex Desktop 打开 vault 根目录。
- 会话里先读 `AGENTS.md`、`CODEX-DESKTOP.md`、`DESKTOP-ADAPTERS.md`。
- 对 PDF/附件 ingest，优先调用 `.codex/scripts/compound_vault.py ingest`。
- 不要先手工写 `raw/`、`source-summaries/`、`concepts/`、`queries/`，除非是在标准 ingest 之后做人工增强。

### Gemini CLI

```bash
bash scripts/build.sh --platform gemini-cli
```

输出会包含 Gemini CLI 所需的命令和说明文件。安装方式取决于你的 Gemini CLI 本地配置。核心原则仍然是：让 Gemini 读取同一个 vault，并遵守 `references/` 中的写入规则。

### OpenCode

```bash
bash scripts/build.sh --platform opencode
```

输出会包含 OpenCode 可读取的 adapter 结构。安装后让 OpenCode 打开同一个 vault 或同一个项目工作区。

### Hermes

构建：

```bash
bash scripts/build.sh --platform hermes
```

输出：

```text
dist/hermes/skills/
dist/hermes/optional-skills/
dist/hermes/references/
dist/hermes/scripts/
dist/hermes/hooks/
dist/hermes/HOOKS.md
dist/hermes/INSTALL.md
```

手动安装 skills：

```bash
mkdir -p ~/.hermes/skills/obsidian-second-brain
cp -R dist/hermes/skills/. ~/.hermes/skills/obsidian-second-brain/
```

如果你的 Hermes 版本按 category 读取，也可以安装到：

```bash
mkdir -p ~/.hermes/skills/note-taking/obsidian-second-brain
cp -R dist/hermes/skills/. ~/.hermes/skills/note-taking/obsidian-second-brain/
```

安装 optional scheduled skills：

```bash
mkdir -p ~/.hermes/optional-skills
cp -R dist/hermes/optional-skills/. ~/.hermes/optional-skills/
```

Hook 安装参考：

```bash
mkdir -p ~/.hermes/agent-hooks
cp dist/hermes/hooks/obsidian-hermes-session-end.sh ~/.hermes/agent-hooks/
chmod +x ~/.hermes/agent-hooks/obsidian-hermes-session-end.sh
```

必须设置：

```bash
export OBSIDIAN_VAULT_PATH="/path/to/IEH"
export OBSIDIAN_HERMES_HOOK_ENABLED=1
export OBSIDIAN_HERMES_CONSOLIDATE_CMD="$HOME/.hermes/agent-hooks/obsidian-hermes-consolidate.sh"
```

建议同时写入 Hermes 的 `.env` 或 launchd/systemd 配置，让 gateway 进程也能读到这些变量。

检查：

```bash
hermes hooks doctor
hermes cron list
```

Scheduled agents：

- `obsidian-morning`
- `obsidian-nightly`
- `obsidian-weekly`
- `obsidian-health-check`

这些是 opt-in。确认 prompt 和写入规则后再启用。

### Claude Desktop

Claude Desktop 不直接运行 Claude Code slash commands。推荐接入方式：

1. 将 Claude Desktop 项目或 MCP 指向同一个 Obsidian vault。
2. 使用 filesystem/MCP/Obsidian MCP 访问 vault 文件。
3. 把 `_CLAUDE.md`、`AGENTS.md`、`CLAUDE-DESKTOP.md`、`DESKTOP-ADAPTERS.md` 作为项目说明。
4. 如有 shell 工具，则直接调用 `.codex/scripts/compound_vault.py` 或仓库内 `scripts/compound_vault.py`。

核心原则：Claude Desktop 是同一个 vault protocol 的客户端，不是另一个 fork。

## 核心工作流

### 新材料进入知识库

标准流程：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" ingest /path/to/source.pdf
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" query "这份材料讲了什么？" --refresh
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
```

人工审查路径：

1. 看 `wiki/meta/source-claims-latest.json`。
2. 看 `wiki/meta/contradictions-latest.json`。
3. 看 `wiki/meta/patch-proposals-latest.md`。
4. 运行 `apply-proposals` dry-run。
5. 确认安全后加 `--apply`。
6. 运行 `fusion` 生成 stage-model 草稿。
7. 确认后运行 `fusion --apply`。
8. 如已有旧 scaffold，再运行 `fusion --apply --upgrade-scaffolds`。
9. 最后运行 `health --json`。

### 日常查询

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" query "我的问题" --refresh --rerank auto
```

建议 AI runtime 的回答顺序：

1. 先读 `wiki/hot.md`。
2. 不够再读 `wiki/index.md`。
3. 仍不够再跑 query。
4. 回答时引用 source-summary、concept、query、raw source。
5. 如果发现缺口，新建或更新 query page。

### 论文/导师方向分析

推荐路径：

1. 将导师论文 PDF ingest 到 vault。
2. 每篇论文生成 source-summary。
3. 用 fusion 生成 concepts、entities、queries、MOC。
4. 在 queries 中形成研究方向判断。
5. 用 contradictions 检查论文之间是否存在方法或结论冲突。
6. 用 MOC 维护导师研究方向地图。
7. 用 query 检索验证新页面能被找回。

### 项目经验沉淀

建议把项目经验写成：

- `source-summaries/`：一次项目复盘、一次事故、一次技术调研。
- `concepts/`：可复用技术概念或模式。
- `entities/`：项目、系统、服务、客户、团队、工具。
- `queries/`：可反复追问的问题，例如“这个系统的核心瓶颈是什么？”
- `mocs/`：某个长期方向的导航页。

### 每日维护

建议最小日常：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" hot
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
```

建议每周：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" index
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" chunks
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
```

## 命令参考

### compound_vault.py

全局：

```bash
python3 scripts/compound_vault.py --vault /path/to/vault <command> [options]
```

子命令：

| Command | 作用 |
|---|---|
| `init` | 创建 compound vault scaffold |
| `index` | 重建 `wiki/index.md` 与 `wiki/meta/index.json` |
| `hot` | 刷新 `wiki/hot.md` |
| `ingest` | ingest 本地文件或 URL，默认执行 distribute、rewrite plan、claim analysis |
| `manifest-repair` | 扫描已有 stage files，补修 manifest |
| `query` | 运行 hot/index/BM25/rerank 检索 |
| `health` | 运行 vault health/lint |
| `chunks` | 重建 chunks 与 BM25 index |
| `fusion` | 生成或应用 stage-model source fusion |
| `apply-proposals` | dry-run 或应用安全 patch proposals |
| `mode` | 查看、设置或预览 methodology mode |
| `routes` | 查看、测试或新增 routing rules |
| `log` | 向 `wiki/log.md` 追加日志 |

### 59 个 slash commands

Vault：

- `/obsidian-save`
- `/obsidian-daily`
- `/obsidian-log`
- `/obsidian-task`
- `/obsidian-person`
- `/obsidian-capture`
- `/obsidian-find`
- `/obsidian-recap`
- `/obsidian-board`
- `/obsidian-project`
- `/obsidian-projects`
- `/obsidian-recurring`
- `/obsidian-world`
- `/obsidian-hot`
- `/obsidian-query`
- `/obsidian-compound-save`
- `/obsidian-agenda`
- `/obsidian-calendar`
- `/obsidian-meeting`
- `/obsidian-schedule`

Thinking：

- `/obsidian-challenge`
- `/obsidian-emerge`
- `/obsidian-connect`
- `/obsidian-graduate`
- `/obsidian-decide`
- `/obsidian-adr`
- `/obsidian-reconcile`
- `/obsidian-review`
- `/obsidian-synthesize`
- `/obsidian-learn`
- `/obsidian-panel`
- `/idea-discovery`
- `/vault-deep-synthesis`

Research：

- `/research`
- `/research-deep`
- `/notebooklm`
- `/x-read`
- `/x-pulse`
- `/youtube`
- `/podcast`
- `/obsidian-ingest`
- `/obsidian-compound-ingest`

Meta：

- `/obsidian-init`
- `/obsidian-health`
- `/obsidian-export`
- `/obsidian-visualize`
- `/obsidian-architect`
- `/obsidian-compound-init`
- `/obsidian-compound-health`
- `/obsidian-compound-chunks`
- `/obsidian-manifest-repair`
- `/obsidian-apply-proposals`
- `/obsidian-fusion`
- `/obsidian-routes`
- `/obsidian-mode`
- `/obsidian-desktop-setup`
- `/obsidian-desktop-install`
- `/create-command`

## 路由、模式与 stage model

### 查看路由

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" routes list
```

### 测试路由

```bash
python3 scripts/compound_vault.py \
  --vault "$OBSIDIAN_VAULT_PATH" \
  routes test "Test-Time Adaptation Survey" \
  --text "CLIP domain shift adaptation robust classification"
```

### 新增路由

```bash
python3 scripts/compound_vault.py \
  --vault "$OBSIDIAN_VAULT_PATH" \
  routes add engineering ai-engineering "clip,test-time adaptation,domain shift,robustness"
```

路由表位置：

```text
.vault-meta/singularity-routes.json
```

Stage model 写入原则：

- source 先进入 `raw/` 与 manifest。
- summary 写入 `source-summaries/`。
- 概念进入 `concepts/`。
- 人物/机构/工具/论文/数据集进入 `entities/`。
- 综合问题进入 `queries/`。
- 领域导航进入 `mocs/`。
- 不确定内容先进入 `wiki/meta/` proposal/draft。

## PDF、OCR 与 source ingest

### PDF ingest

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" ingest /path/to/paper.pdf
```

系统会尝试：

1. 保留 PDF 原件。
2. 使用 `pdftotext` 抽取正文。
3. 判断文本质量。
4. 如需要，尝试 `pdftoppm` + `tesseract` OCR fallback。
5. 写入 `raw/articles/...`。
6. 写入 `source-summaries/...`。
7. 生成 claims、contradictions、patch proposals、rewrite plan。
8. 刷新 index/hot/chunks。

缺工具时不会编造结果。health 会报告：

- extraction status
- page count if available
- text length
- OCR required
- missing OCR tools

### URL 或文本 source

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" ingest https://example.com/article
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" ingest /path/to/article.md
```

### Manifest repair

正常情况下，任何 PDF/附件 ingest 都应该先走 manifest-aware 入口：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" ingest /path/to/source.pdf
```

如果某个 Desktop/agent 会话已经手工创建了 `raw/papers`、`raw/articles` 和 `source-summaries`，但没有写入 `.vault-meta/compound-manifest.json`，用 manifest repair 修复机器账本。

Dry-run：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --json
```

Apply：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --apply --json
```

如果 source 已经登记进 manifest，但后续生成的 `concepts/`、`entities/`、`mocs/`、`queries/` 没有回写到 `distributed.entities` / `distributed.concepts`，使用：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --repair-distributed --json
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --repair-distributed --apply --json
```

这只会补账本反链，不会改写 durable notes。

## 检索、BM25 与 rerank

### 查询

```bash
python3 scripts/compound_vault.py \
  --vault "$OBSIDIAN_VAULT_PATH" \
  query "这个项目的核心设计是什么？" \
  --refresh \
  --rerank auto
```

检索顺序：

1. `wiki/hot.md`
2. `wiki/index.md`
3. `.vault-meta/chunks/`
4. `.vault-meta/bm25/index.json`
5. optional Ollama rerank

### Rerank 模式

```bash
--rerank auto
--rerank lexical
--rerank ollama
--rerank none
```

建议：

- 默认用 `auto`。
- 没有 Ollama 时会退回 lexical/BM25。
- 对敏感 vault，不要把 `OLLAMA_URL` 指向远程服务。

### 重建检索索引

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" index
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" chunks
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" hot
```

## 安全写入策略

项目有意避免几类危险行为：

- 不自动删除 notes。
- 不自动覆盖人工 durable notes。
- 不把 contradiction 自动改成最终结论。
- 不把单篇 source 的 claim 直接提升为领域共识。
- 不在 PDF 抽取失败时编造摘要。
- 不把 generated report 当成最终知识。

### Fusion

默认只生成 draft/report：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" fusion raw/articles/engineering/ai-engineering/example.md
```

真正写入：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" fusion raw/articles/engineering/ai-engineering/example.md --apply
```

升级旧 scaffold：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" fusion raw/articles/engineering/ai-engineering/example.md --apply --upgrade-scaffolds
```

### Patch proposals

默认 dry-run：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" apply-proposals
```

应用安全 proposal：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" apply-proposals --apply
```

只自动应用：

- `append_evidence`
- `append_timeline`

不自动应用：

- contradiction review
- destructive rewrite
- broad refactor

## 验证与排障

### 基础验证

```bash
python3 -m pytest -q
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
bash scripts/build.sh --platform claude-code
bash scripts/build.sh --platform codex-cli
bash scripts/build.sh --platform gemini-cli
bash scripts/build.sh --platform opencode
bash scripts/build.sh --platform hermes
git diff --check
```

### Desktop adapter 验证

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --check --json
```

应至少存在：

- `AGENTS.md`
- `.agents/skills`
- `.codex/scripts/compound_vault.py`
- `.codex/references/desktop-adapters.md`
- `DESKTOP-ADAPTERS.md`

### Hermes 验证

```bash
hermes hooks doctor
hermes cron list
```

如果 cron list 显示 gateway 未运行，检查你的 Hermes gateway 服务、launchd/systemd 配置和日志。

### 常见问题

#### ingest 后 manifest 没记录

原因通常是 runtime 绕过了标准入口，直接手工写了 `raw/` 或 `source-summaries/`。

修复：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --json
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --apply --json
```

#### query 找不到新材料

先重建：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" index
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" chunks
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" hot
```

再查询：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" query "关键词" --refresh
```

#### PDF 抽取为空

检查：

```bash
which pdftotext
which pdftoppm
which tesseract
```

如果是扫描版 PDF，需要 OCR 工具。

#### Codex Desktop 看不到 skill

检查：

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --check --json
```

确认 Codex Desktop 打开的目录是 vault 根目录，而不是 vault 的上级目录。

#### Claude Code 看不到 slash commands

检查：

```bash
ls ~/.claude/commands/obsidian-query.md
ls ~/.claude/skills/obsidian-second-brain
```

重新 build 并 symlink：

```bash
bash scripts/build.sh --platform claude-code
ln -sfn "$(pwd)/dist/claude-code" ~/.claude/skills/obsidian-second-brain
ln -sfn "$(pwd)/dist/claude-code/commands/"*.md ~/.claude/commands/
```

重启 Claude Code。

## 升级、回滚与维护

### 更新仓库

```bash
git pull
uv sync
bash scripts/build.sh
```

如果使用 Codex Desktop：

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --json
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --check --json
```

如果使用 Claude Code：

```bash
bash scripts/build.sh --platform claude-code
ln -sfn "$(pwd)/dist/claude-code" ~/.claude/skills/obsidian-second-brain
ln -sfn "$(pwd)/dist/claude-code/commands/"*.md ~/.claude/commands/
```

### 回滚 Desktop adapter

```bash
python3 scripts/install_desktop.py "$OBSIDIAN_VAULT_PATH" --rollback --json
```

### Vault 建议 git 管理

推荐给 vault 初始化独立 git 仓库：

```bash
cd "$OBSIDIAN_VAULT_PATH"
git init
```

建议 `.gitignore` 忽略：

```gitignore
.DS_Store
._*
.obsidian/workspace*.json
.obsidian/cache/
.trash/
.agents/
.codex/
.vault-meta/chunks/
.vault-meta/bm25/
wiki/meta/
raw/papers/**/*.pdf
*.tmp
*.bak
```

说明：

- PDF 原件可能很大，不建议直接纳入 vault git。
- `raw/articles/`、`source-summaries/`、`concepts/`、`entities/`、`queries/`、`mocs/` 建议纳入版本管理。
- `.vault-meta/compound-manifest.json` 建议纳入版本管理，因为它是 source 账本。
- `.vault-meta/chunks/` 和 BM25 index 可再生成，通常不纳入 git。

### Health 质量门

`health --json` 不只是链接检查。IEH 模板下还会检查：

- 是否有 `.vault-meta/ieh-template.json`。
- 当前 mode 是否为 `singularity`。
- raw PDF 是否按内容 hash 重复。
- processed 页面是否错误地写在 `concepts/*.md`、`entities/*.md`、`mocs/*.md`、`queries/*.md` 顶层。
- manifest 是否缺少 distributed concept/entity 反链。
- 最新 `rewrite-plan`、`source-claims`、`contradictions`、`patch-proposals` 审计产物是否存在。
- vault 是否已有 git baseline。

### 定期维护

建议每周运行：

```bash
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" health --json
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" manifest-repair --json
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" index
python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" chunks
```

## 与上游项目的关系

本项目保留并扩展了 `obsidian-second-brain` 的核心优点：

- 单一命令源。
- 多 CLI adapter。
- Obsidian AI-first vault。
- research / thinking / vault / meta 命令体系。

同时新增了面向 IEH 的能力：

- compound vault engine
- SINGULARITY stage model
- Desktop adapter installer
- PDF/OCR ingest
- manifest/delta
- chunked BM25
- Ollama rerank
- source claim extraction
- contradiction detector
- timeline/history updater
- patch proposals
- fusion draft workflow
- configurable routing
- manifest repair
- safer Desktop runtime rules

## 当前边界

仍然需要按你的环境手动配置的部分：

- Claude Desktop MCP 或 filesystem/project instructions。
- ChatGPT bridge。
- Hermes gateway 服务细节。
- 远程 embedding/rerank 服务。
- 个人 API keys。
- 大规模迁移时的人工审查策略。

代码质量仍可继续增强的部分：

- `scripts/compound_vault.py` 内部分函数仍偏长。
- 某些 research/integration 模块仍有宽泛异常捕获。
- hooks、adapters、integrations 的测试覆盖还可以继续补。

## License

MIT. See [LICENSE](LICENSE).
