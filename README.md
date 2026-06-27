# Intellect Evolution Hub - obsidian-second-brain

面向 Obsidian 的多工具通用第二大脑底座。

这个仓库是在 `eugeniughelbur/obsidian-second-brain` 的跨 CLI 命令系统基础上，融合 `claude-obsidian` 风格的 hot/index/log、query、ingest、锁、health、BM25 检索、claim extraction、contradiction review、patch proposals、Desktop adapter，以及 SINGULARITY/IEH stage-model 知识库结构后形成的增强版。

它的目标不是做一个只能服务某个 AI 工具的笔记模板，而是把同一个 Obsidian vault 变成 Claude Code、Codex CLI、Codex Desktop、Claude Desktop、Gemini CLI、OpenCode、Hermes 都能共同使用的知识操作系统。

## 当前状态

- 59 个命令，统一从 `commands/` 生成到不同 AI 工具适配层。
- 支持 Claude Code、Codex CLI、Gemini CLI、OpenCode、Hermes build 输出。
- 支持 Codex Desktop / Claude Desktop 面向同一 vault 的 adapter 安装、检查与回滚。
- 支持 IEH/SINGULARITY stage model：`raw/`、`source-summaries/`、`concepts/`、`entities/`、`queries/`、`mocs/`、`maintenance/`。
- 支持 compound vault：`wiki/hot.md`、`wiki/index.md`、`wiki/log.md`、manifest、chunked BM25、rerank、health。
- 支持 PDF ingest、`pdftotext` 抽取、OCR fallback、抽取质量诊断。
- 支持 source claim extraction、contradiction candidates、timeline/history updater、patch proposal、safe apply。
- 支持 fusion draft workflow：从 source 生成可审查的中文优先 processed-note 草稿，并安全创建/升级 stage pages。

## 设计目标

### 1. 一个 vault，多种 AI 工具

不同工具可以有不同入口，但必须遵守同一套 vault contract：

- 同一个 Obsidian vault。
- 同一套 AI-first note 规则。
- 同一套 source preservation 规则。
- 同一套 retrieval 顺序：`hot` -> `index` -> BM25/chunks -> durable notes。
- 同一套写入策略：默认保守、可审查、可回滚，不自动覆盖人工笔记。

### 2. 源材料不是被收藏，而是推动知识库生长

普通笔记系统容易变成文件堆。这个项目的 ingest 流程要求每个 source 至少进入以下路径之一：

1. 保留 raw source。
2. 生成 source-summary。
3. 抽取 claims、entities、concepts。
4. 发现 contradictions。
5. 生成 patch proposals。
6. 更新 timeline/history。
7. 通过 fusion 进入 concept/query/entity/MOC 层。

### 3. 默认安全，不自动污染知识库

系统可以生成很多 proposal 和 draft，但默认不强行应用：

- `fusion` 默认只生成 report 和 draft。
- `apply-proposals` 默认 dry-run。
- `review_contradiction` 永远要求人工确认。
- `--apply` 只应用安全 append 类更新。
- `--upgrade-scaffolds` 只升级被识别为旧 scaffold 的页面，不覆盖人工写过的 durable notes。

## 仓库结构

```text
obsidian-second-brain/
|-- commands/                  # 59 个平台中立命令定义
|-- references/                # vault schema、write policy、retrieval、desktop adapter 等规范
|-- scripts/                   # 核心脚本、build、research、compound vault engine
|-- scripts/research/          # research/x/youtube/podcast/notebooklm 工具
|-- adapters/                  # claude-code/codex-cli/gemini-cli/opencode/hermes 适配层
|-- hooks/                     # Claude Code hooks
|-- integrations/              # MCP / Telegram journal 等可选集成
|-- examples/                  # 示例 vault
|-- tests/                     # pytest 测试
|-- architecture.md            # 架构说明
|-- SKILL.md                   # AI 工具加载的主技能说明
|-- README.md                  # 当前文档
```

## Vault 结构

IEH/SINGULARITY mode 下，一个 vault 会被组织成：

```text
IEH/
|-- SCHEMA.md
|-- index.md
|-- log.md
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
|   `-- meta/
`-- .vault-meta/
    |-- compound-manifest.json
    |-- singularity-routes.json
    |-- bm25/index.json
    `-- chunks/
```

其中：

- `raw/` 保存原始材料的可追溯副本。
- `source-summaries/` 是单 source 阅读脚手架。
- `concepts/` 是可复用概念。
- `entities/` 是人物、机构、工具、论文、数据集等稳定对象。
- `queries/` 是学习问题、研究问题和判断入口。
- `mocs/` 是领域导航，不承载长篇正文。
- `maintenance/` 放 vault-wide 维护文档。
- `wiki/meta/` 放系统生成的 report、proposal 和 draft。
- `.vault-meta/` 放机器索引、manifest、route table 和 chunks。

## 核心命令

### 初始化与模式

```bash
python3 scripts/compound_vault.py --vault /path/to/IEH init
python3 scripts/compound_vault.py --vault /path/to/IEH mode set singularity
python3 scripts/compound_vault.py --vault /path/to/IEH routes list
```

对应 slash commands：

- `/obsidian-compound-init`
- `/obsidian-mode`
- `/obsidian-routes`

### Ingest

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  ingest /path/to/source.pdf
```

会执行：

- raw source preservation
- PDF text extraction
- OCR fallback if needed
- source-summary generation
- source claim extraction
- contradiction detection
- patch proposal generation
- rewrite plan generation
- index/hot/chunk refresh

对应 slash command：

- `/obsidian-compound-ingest`

### Query

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
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

对应 slash commands：

- `/obsidian-query`
- `/obsidian-hot`
- `/obsidian-compound-chunks`

### Fusion

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  fusion raw/articles/engineering/ai-engineering/example.md
```

默认只生成：

- `wiki/meta/fusion-proposals-latest.json`
- `wiki/meta/fusion-proposals-latest.md`
- `wiki/meta/fusion-drafts-latest.json`
- `wiki/meta/fusion-drafts-latest.md`

真正写入：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  fusion raw/articles/engineering/ai-engineering/example.md \
  --apply
```

升级旧 scaffold：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  fusion raw/articles/engineering/ai-engineering/example.md \
  --apply \
  --upgrade-scaffolds
```

安全规则：

- 不加 `--apply` 不改 durable pages。
- `--apply` 只创建缺失页面。
- `--upgrade-scaffolds` 只替换旧 fusion scaffold。
- 人工写过的 durable note 不覆盖。

对应 slash command：

- `/obsidian-fusion`

### Patch proposals

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  apply-proposals
```

默认 dry-run。

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  apply-proposals \
  --apply
```

只自动应用安全 proposal 类型：

- `append_evidence`
- `append_timeline`

不自动应用：

- contradiction review
- destructive rewrite
- broad refactor

对应 slash command：

- `/obsidian-apply-proposals`

### Manifest repair

正常 ingest 必须先走 manifest-aware 入口：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  ingest /path/to/source.pdf
```

如果某个 Desktop/agent 会话已经手工创建了 `raw/papers`、`raw/articles`
和 `source-summaries`，但没有写入 `.vault-meta/compound-manifest.json`，
用 manifest repair 修复机器账本。

Dry-run：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  manifest-repair --json
```

Apply：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  manifest-repair --apply --json
```

对应 slash command：

- `/obsidian-manifest-repair`

### Health

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  health --json
```

检查：

- dead links
- orphan pages
- missing frontmatter
- missing `ai-first`
- duplicate titles
- generated index staleness
- manifest source coverage
- manifest untracked stage sources
- PDF extraction issues

对应 slash commands：

- `/obsidian-compound-health`
- `/obsidian-health`

## Desktop 适配

### Codex Desktop

构建并安装到 vault：

```bash
bash scripts/build.sh --platform codex-cli
python3 scripts/install_desktop.py /path/to/IEH --json
```

安装后 vault 中会出现：

```text
AGENTS.md
.agents/skills/
.codex/scripts/compound_vault.py
.codex/references/
DESKTOP-ADAPTERS.md
.vault-meta/desktop-install-manifest.json
```

检查：

```bash
python3 scripts/install_desktop.py /path/to/IEH --check --json
```

回滚：

```bash
python3 scripts/install_desktop.py /path/to/IEH --rollback --json
```

对应 slash command：

- `/obsidian-desktop-install`

### Claude Desktop

Claude Desktop 不直接运行 Claude Code slash commands。推荐方式：

1. 将 Claude Desktop 指向同一个 Obsidian vault。
2. 使用 filesystem/MCP/Obsidian MCP 访问 vault。
3. 把 `_CLAUDE.md`、`AGENTS.md`、`DESKTOP-ADAPTERS.md` 作为项目说明。
4. 如有 shell 工具，则直接调用 `.codex/scripts/compound_vault.py`。

核心原则：Desktop app 是同一个 vault protocol 的客户端，不是另一个 fork。

## 多平台 build

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

`commands/` 是唯一命令源。不要手改 `dist/`。

## 59 个命令

### Vault

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

### Thinking

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

### Research

- `/research`
- `/research-deep`
- `/notebooklm`
- `/x-read`
- `/x-pulse`
- `/youtube`
- `/podcast`
- `/obsidian-ingest`
- `/obsidian-compound-ingest`

### Meta

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

## 推荐工作流

### 新材料进入知识库

1. 把 PDF、文章、网页导出、课程笔记等交给 `/obsidian-compound-ingest`。
2. 看 `wiki/meta/source-claims-latest.json`。
3. 看 `wiki/meta/contradictions-latest.json`。
4. 看 `wiki/meta/patch-proposals-latest.md`。
5. 运行 `/obsidian-apply-proposals` dry-run。
6. 确认安全后加 `--apply`。
7. 运行 `/obsidian-fusion` 生成 stage-model 草稿。
8. 确认后运行 `/obsidian-fusion --apply`。
9. 如已有旧 scaffold，再运行 `/obsidian-fusion --apply --upgrade-scaffolds`。
10. 如果某个 runtime 绕过了 `/obsidian-compound-ingest` 而手工写入 stage files，运行 `/obsidian-manifest-repair` dry-run，再按需 `--apply`。
11. 最后运行 `/obsidian-compound-health`。

### 日常查询

1. 先读 `wiki/hot.md`。
2. 不够再读 `wiki/index.md`。
3. 仍不够再跑 `/obsidian-query <question>`。
4. 回答时引用 source-summary、concept、query、raw source。
5. 如果发现缺口，新建或更新 query page。

### 导师/论文方向分析

推荐路径：

1. 将导师论文 PDF ingest 到 IEH vault。
2. 每篇论文生成 source-summary。
3. 用 fusion 生成 concepts、entities、queries、MOC。
4. 在 queries 中形成研究方向判断。
5. 用 contradictions 检查论文之间是否存在方法或结论冲突。
6. 用 MOC 维护导师研究方向地图。

## 路由规则

路由表在：

```text
.vault-meta/singularity-routes.json
```

查看：

```bash
python3 scripts/compound_vault.py --vault /path/to/IEH routes list
```

测试：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  routes test "Test-Time Adaptation Survey" \
  --text "CLIP domain shift adaptation robust classification"
```

新增规则：

```bash
python3 scripts/compound_vault.py \
  --vault /path/to/IEH \
  routes add engineering ai-engineering "clip,test-time adaptation,domain shift,robustness"
```

## PDF 与 OCR

PDF ingest 优先使用：

- `pdftotext`

如果文本不足，会尝试：

- `pdftoppm`
- `tesseract`

缺工具不会伪造结果。health 会报告：

- extraction status
- page count if available
- text length
- OCR required
- missing OCR tools

## Rerank

`query` 支持：

```bash
--rerank auto
```

如果本机有 Ollama 或可用 rerank 环境，就使用 rerank；否则退回 BM25 排序，不阻断查询。

## 安全边界

这个项目有意避免几类危险行为：

- 不自动删除 notes。
- 不自动覆盖人工 durable notes。
- 不把 contradiction 自动改成最终结论。
- 不把单篇 source 的 claim 直接提升为领域共识。
- 不在 PDF 抽取失败时编造摘要。
- 不把 generated report 当成最终知识。

## 本地验证

```bash
python3 -m pytest tests/test_smoke.py tests/test_compound_vault.py tests/test_desktop_install.py -q
python3 scripts/compound_vault.py --vault /path/to/IEH health --json
bash scripts/build.sh --platform codex-cli
bash scripts/build.sh --platform claude-code
bash scripts/build.sh --platform gemini-cli
bash scripts/build.sh --platform opencode
bash scripts/build.sh --platform hermes
git diff --check
```

## 环境变量

常用：

```bash
export OBSIDIAN_VAULT_PATH="/path/to/IEH"
```

研究相关可选：

```bash
export PERPLEXITY_API_KEY="..."
export XAI_API_KEY="..."
export GOOGLE_API_KEY="..."
```

没有这些 key 时，部分 research 命令会使用免费公开源或降级路径。

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

## License

本仓库沿用上游 MIT License。详见 `LICENSE`。

## 建议原则

把它当成知识管理底座，而不是一次性脚本。

每次 ingest 后，都应该让 vault 发生可追溯的结构化变化：source 被保留，summary 被生成，concept/query/entity 被更新，MOC 能导航，health 能通过。这样知识库才会随着材料增长而变聪明，而不是只变大。
