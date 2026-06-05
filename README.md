# MarkItDown Skill

[English](#english) | [中文](#中文)

---

## English

MarkItDown Skill is an Agent Skill for Codex, Claude Code, and other `SKILL.md`-compatible coding agents. It wraps Microsoft [MarkItDown](https://github.com/microsoft/markitdown) so agents can reliably convert documents, office files, web pages, media, archives, and URLs into Markdown for LLM workflows.

### What It Does

- Converts files and URLs to Markdown using the upstream `markitdown` Python package.
- Supports common MarkItDown source types: PDF, Word, PowerPoint, Excel, images, audio, HTML, CSV, JSON, XML, ZIP archives, YouTube URLs, EPub, and other formats supported by the installed MarkItDown version.
- Provides a reusable wrapper script for single-file conversion, batch conversion, recursive directory conversion, URL conversion, local-only safe conversion, output naming, and overwrite control.
- Supports MarkItDown plugins, including OCR-style workflows when suitable plugins are installed.
- Supports LLM image descriptions through an OpenAI-compatible client.
- Supports Azure Document Intelligence and Azure Content Understanding for higher-quality layout extraction, OCR, multimodal conversion, and structured field extraction.
- Includes safety guidance for untrusted files, remote URLs, plugins, and prompt-injection risks in converted documents.

### Where You Can Use It

- **Codex personal skill**: `~/.codex/skills/markitdown-skill/SKILL.md`
- **Claude Code personal skill**: `~/.claude/skills/markitdown-skill/SKILL.md`
- **Claude Code project skill**: `<project>/.claude/skills/markitdown-skill/SKILL.md`
- **Agent Skills-compatible tools**: any tool that discovers a folder containing `SKILL.md`
- **Direct script usage**: run `scripts/markitdown_convert.py` from any shell with Python and MarkItDown installed

### Install

Clone this repository into a personal skill directory.

Codex:

```bash
git clone https://github.com/Zhanghaohao666/markitdown-skill.git ~/.codex/skills/markitdown-skill
```

Claude Code:

```bash
git clone https://github.com/Zhanghaohao666/markitdown-skill.git ~/.claude/skills/markitdown-skill
```

Project-local Claude Code install:

```bash
mkdir -p .claude/skills
git clone https://github.com/Zhanghaohao666/markitdown-skill.git .claude/skills/markitdown-skill
```

Then install MarkItDown in the Python environment the agent will use:

```bash
python -m pip install -U "markitdown[all]"
```

For smaller installs, choose only the extras you need:

```bash
python -m pip install -U "markitdown[pdf,docx,pptx,xlsx]"
```

Optional OCR, LLM, and Azure support:

```bash
python -m pip install -U "markitdown-ocr" "openai"
python -m pip install -U "markitdown[az-doc-intel]"
python -m pip install -U "markitdown[az-content-understanding]"
```

### Use With an Agent

Ask Codex or Claude Code to use the skill:

```text
Use $markitdown-skill to convert report.pdf to Markdown.
```

```text
Use $markitdown-skill to batch convert all PDFs and Word files in ./docs into ./markdown.
```

```text
Use $markitdown-skill to convert this scanned PDF with OCR or Azure extraction if needed.
```

Claude Code may also expose the skill as:

```text
/markitdown-skill
```

### Use the Wrapper Script Directly

Single file:

```bash
python scripts/markitdown_convert.py "report.pdf" -o "report.md"
```

Batch directory conversion:

```bash
python scripts/markitdown_convert.py "docs" --recursive --include "*.pdf" --include "*.docx" --output-dir "markdown"
```

Local-only safer conversion:

```bash
python scripts/markitdown_convert.py "local-file.docx" -o "local-file.md" --local-only
```

Use plugins:

```bash
python scripts/markitdown_convert.py "document.pdf" -o "document.md" --use-plugins
```

Use LLM image descriptions:

```bash
python scripts/markitdown_convert.py "slides.pptx" -o "slides.md" --llm-model "gpt-4o"
```

Use Azure Document Intelligence:

```bash
python scripts/markitdown_convert.py "report.pdf" -o "report.md" --docintel-endpoint "<endpoint>"
```

Use Azure Content Understanding:

```bash
python scripts/markitdown_convert.py "invoice.pdf" -o "invoice.md" --cu-endpoint "<endpoint>" --cu-analyzer-id "<analyzer>"
```

### Files

- `SKILL.md`: main skill instructions and trigger metadata
- `scripts/markitdown_convert.py`: reusable conversion wrapper
- `references/markitdown-reference.md`: detailed usage reference, recipes, quality checks, and troubleshooting
- `agents/openai.yaml`: Codex UI metadata

### Notes

MarkItDown output is optimized for LLM and text-analysis pipelines, not pixel-perfect human-facing document conversion. Always spot-check important Markdown output, especially scanned PDFs, complex tables, spreadsheets, slide decks, and image-heavy documents.

---

## 中文

MarkItDown Skill 是一个适用于 Codex、Claude Code 以及其他兼容 `SKILL.md` 的编码智能体的 Agent Skill。它封装了 Microsoft [MarkItDown](https://github.com/microsoft/markitdown)，让智能体可以稳定地把文档、Office 文件、网页、媒体、压缩包和 URL 转换成 Markdown，方便后续交给 LLM 阅读、总结、检索或分析。

### 功能

- 使用上游 `markitdown` Python 包把文件和 URL 转换成 Markdown。
- 支持常见 MarkItDown 输入类型：PDF、Word、PowerPoint、Excel、图片、音频、HTML、CSV、JSON、XML、ZIP 压缩包、YouTube URL、EPub，以及当前安装版本和插件支持的其他格式。
- 提供可复用脚本，支持单文件转换、批量转换、递归目录转换、URL 转换、本地安全模式、自动输出命名和覆盖控制。
- 支持 MarkItDown 插件，包括安装对应插件后的 OCR 类流程。
- 支持通过 OpenAI 兼容客户端为图片或幻灯片中的图像生成 LLM 描述。
- 支持 Azure Document Intelligence 和 Azure Content Understanding，用于更高质量的版面解析、OCR、多模态转换和结构化字段提取。
- 包含不可信文件、远程 URL、插件和文档内提示注入的安全使用说明。

### 可以在哪里使用

- **Codex 个人 skill**：`~/.codex/skills/markitdown-skill/SKILL.md`
- **Claude Code 个人 skill**：`~/.claude/skills/markitdown-skill/SKILL.md`
- **Claude Code 项目级 skill**：`<project>/.claude/skills/markitdown-skill/SKILL.md`
- **兼容 Agent Skills 的工具**：任何能发现包含 `SKILL.md` 文件夹的工具
- **直接作为脚本使用**：在安装了 Python 和 MarkItDown 的环境里直接运行 `scripts/markitdown_convert.py`

### 安装

把这个仓库克隆到个人 skill 目录。

Codex：

```bash
git clone https://github.com/Zhanghaohao666/markitdown-skill.git ~/.codex/skills/markitdown-skill
```

Claude Code：

```bash
git clone https://github.com/Zhanghaohao666/markitdown-skill.git ~/.claude/skills/markitdown-skill
```

Claude Code 项目级安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/Zhanghaohao666/markitdown-skill.git .claude/skills/markitdown-skill
```

然后在智能体会使用的 Python 环境里安装 MarkItDown：

```bash
python -m pip install -U "markitdown[all]"
```

如果只需要部分格式，可以安装更小的依赖集合：

```bash
python -m pip install -U "markitdown[pdf,docx,pptx,xlsx]"
```

可选 OCR、LLM 和 Azure 支持：

```bash
python -m pip install -U "markitdown-ocr" "openai"
python -m pip install -U "markitdown[az-doc-intel]"
python -m pip install -U "markitdown[az-content-understanding]"
```

### 在智能体里使用

可以直接让 Codex 或 Claude Code 使用这个 skill：

```text
Use $markitdown-skill to convert report.pdf to Markdown.
```

```text
Use $markitdown-skill to batch convert all PDFs and Word files in ./docs into ./markdown.
```

```text
Use $markitdown-skill to convert this scanned PDF with OCR or Azure extraction if needed.
```

Claude Code 中也可能可以直接这样调用：

```text
/markitdown-skill
```

### 直接使用脚本

单文件转换：

```bash
python scripts/markitdown_convert.py "report.pdf" -o "report.md"
```

批量转换目录：

```bash
python scripts/markitdown_convert.py "docs" --recursive --include "*.pdf" --include "*.docx" --output-dir "markdown"
```

更安全的本地文件转换：

```bash
python scripts/markitdown_convert.py "local-file.docx" -o "local-file.md" --local-only
```

启用插件：

```bash
python scripts/markitdown_convert.py "document.pdf" -o "document.md" --use-plugins
```

使用 LLM 图片描述：

```bash
python scripts/markitdown_convert.py "slides.pptx" -o "slides.md" --llm-model "gpt-4o"
```

使用 Azure Document Intelligence：

```bash
python scripts/markitdown_convert.py "report.pdf" -o "report.md" --docintel-endpoint "<endpoint>"
```

使用 Azure Content Understanding：

```bash
python scripts/markitdown_convert.py "invoice.pdf" -o "invoice.md" --cu-endpoint "<endpoint>" --cu-analyzer-id "<analyzer>"
```

### 文件结构

- `SKILL.md`：skill 主说明和触发元数据
- `scripts/markitdown_convert.py`：可复用转换脚本
- `references/markitdown-reference.md`：详细用法、命令示例、质量检查和排错说明
- `agents/openai.yaml`：Codex UI 元数据

### 注意事项

MarkItDown 的输出主要面向 LLM 和文本分析流程，不是像素级还原的文档排版转换工具。对扫描 PDF、复杂表格、电子表格、幻灯片和图片较多的文档，建议检查关键段落和表格后再使用。
