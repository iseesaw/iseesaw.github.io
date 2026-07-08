---
name: add-publication
description: 添加或更新论文条目与缩略图。当用户要求添加论文、更新 papers.bib、添加/替换论文缩略图（preview 插图）、调整精选论文（selected/thread）或处理缩略图清晰度/尺寸问题时使用。包含 bib 字段规范、1600×900 letterbox 缩略图处理脚本与构建验证流程。
---

# 添加/更新论文与缩略图

## 收录规则（先判断）

只收录**一作、共一、通讯**的论文进 `_bibliography/papers.bib`。非主导作者的论文不上站（Google Scholar 兜底）。精选（`selected={true}`）保持在 8 篇左右，宁缺毋滥。

## 1. Bib 条目模板

```bibtex
@article{ShortKey,
  title={Full Paper Title},
  author={Zhang*†, Kaiyan and Last, First and authors, +N more and Zhou†, Bowen},
  abbr={NeurIPS 2025},
  year={2025},
  journal={The Thirty-Ninth Annual Conference on Neural Information Processing Systems},
  annotation={* Equal contribution<br>† Corresponding author},
  pdf={https://arxiv.org/pdf/XXXX.XXXXX},
  code={https://github.com/org/repo},
  preview={shortkey.jpg},
  thread={machinery},
  bibtex_show={true},
  selected={true}
}
```

字段规范：

- **key**：唯一且语义化（`TTRL`、`MARTIMARS2`）。构建不会检查重复 key，必须人工确认唯一。
- **abbr**：会议用 `NeurIPS 2025` 格式；预印本用 `arXiv`（注意大小写，不是 `Arxiv`）。
- **author**：`*`/`†` 标记直接贴在姓氏后（`Zhang*†, Kaiyan`），主题会渲染成上标并在 annotation 里解释。本人名字会自动加下划线高亮。
- **bibtex_show={true}**：所有条目必加（BIB 按钮）。
- **selected / thread / preview**：三者绑定出现。`thread` 取值 `machinery`（学习机制线）或 `application`（落地应用线），决定首页分组；新增第三条主线需同步改 `_includes/selected_papers.liquid` 的小节标题。
- 新精选挤掉旧精选时，把旧条目的 `selected`/`thread`/`preview` 三行删掉即可，缩略图文件可留存备用。

## 2. 缩略图处理（关键）

**规格：统一 1600×900（16:9）、白底 letterbox 居中、JPEG quality 88、单张 ≤ 300KB 左右。**

为什么是这个规格：列表显示仅 ~150px 宽，但主题带点击放大（medium-zoom），800px 源图放大后发虚，1600px 足够；不同论文插图比例不一（1.5–2.4 都有），统一画布保证首页行高一致；不裁剪不拉伸，留白用白色与论文图底色融合。

处理步骤：

```bash
# 原图放任意路径，运行规格化脚本（依赖 Pillow，python3 -c "import PIL" 验证）
python3 .claude/skills/add-publication/scripts/normalize_thumbnail.py 原图.png
# 输出到 assets/img/publication_preview/原图.jpg（自动转 jpg、letterbox、压缩）
```

脚本支持多文件与参数：`--width/--height/--quality/--out`。需要更高清晰度时用 `--width 2400 --height 1350`（体积约 1.5 倍）。

选图建议：优先论文 teaser 图或框架图；避免密集表格/文字截图（缩略图尺寸下糊成噪点）；如原图信息太密，裁出核心流程部分再处理。

**原图归档**：高清原图存 `_thumbnail_originals/`（下划线目录，Jekyll 不发布）。换规格重跑时以此目录为源，不要用已压缩的输出反复处理。

## 3. 构建与验证

```bash
LC_ALL=en_US.UTF-8 PATH="/opt/homebrew/opt/ruby/bin:$PATH" bundle exec jekyll build
```

必须带 UTF-8 locale（bib 里的 `†` 在 ASCII locale 下会让 bibtex-ruby 崩溃）和 Homebrew Ruby 路径。

验证清单：

1. 构建无报错；
2. 首页 selected publications：新论文出现在正确主线小节下，缩略图行高与其他条目一致；
3. publications 页：条目占整行、无徽章列（`publications-plain` 生效）；
4. 点击 BIB 按钮可展开 BibTeX；点击缩略图放大后清晰。

浏览器可能缓存旧 CSS/图片（bust 参数是静态的），验证时对图片和 main.css 强制刷新。

## 4. 顺手项

- 发表/中稿的同时在 `_news/` 加一条 inline news（带论文或 repo 链接；star 徽章只允许出现在 news，不进 bib）。
- 会议条目可在 `_data/venues.yml` 补链接（当前徽章列隐藏，此文件仅作元数据储备）。
