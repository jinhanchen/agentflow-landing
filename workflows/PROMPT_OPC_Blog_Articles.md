# 任务提示词 · 扩充 OPC 博客内容（trends.html）

> **发给新 Claude Code 窗口的完整指令**。把 `---` 之间的全部内容复制粘贴即可。
> 生成时间：2026-04-15
> 发起人：Daneel（PM Agent）代 Franklin 拟定

---

# 任务：从 Franklin 的 Obsidian 知识库挖素材，扩充 Solarian 官网的 OPC 博客

你要读 Franklin 本地 Obsidian vault 里已有的深度笔记，**挑 3-5 篇最契合 OPC 话题的**，改写成官网博客文章，并按**已搭好的构建架构**落地。

---

## 一、项目背景

### Solarian（公司）

- **产品**：为一人公司（OPC, One-Person Company）设计的 AI 团队操作系统
- **目标用户**：一人公司创始人、独立创业者、OPC 时代早期实践者
- **品牌**：warm-minimal professional（Anthropic 风格）
- **配色**：米白 `#F5F0E6` + teal `#0d9488` + terracotta `#D97757`

### 官网架构（**非常重要，先读懂再动手**）

**项目根目录**：
```
C:\Users\jinha\OneDrive\桌面\AgentFlow webpage\
```

**OPC 博客（trends.html）已经改成"源码分离 + 构建"架构**：

```
AgentFlow webpage/
├── trends.html              ← 不要直接编辑！这是构建产物
├── build.py                 ← 构建脚本
├── src/
│   └── trends/
│       ├── template.html    ← HTML 壳（{{ARTICLES_JS}} 占位）
│       ├── index.json       ← 博客元数据列表
│       └── articles/
│           ├── 001.html     ← 每篇文章的 HTML 内容片段（无 JS 外壳）
│           ├── 002.html
│           ├── ...
│           └── 008.html
└── assets/                  ← 图片
```

**工作流（铁律）**：
1. 改源码：编辑 `src/trends/articles/*.html` 和/或 `src/trends/index.json`
2. 运行：`python build.py`
3. 构建成功会打印 `[OK] Built trends.html | N articles | XXX chars`
4. 失败会打印 `[FAIL]`，根据错误修源码，直到成功

**不要直接手改 `trends.html`** —— 它会在下次 build 时被覆盖。

---

## 二、核心任务

### 2.1 读源文件

从以下 Obsidian 笔记中选出**最适合作为公开博客发表**的素材。优先级已排序：

**Tier 1（最直接对口 OPC 主题，强烈推荐入选）**：
1. `C:\My Space (Obsidian)\My space\03 Resources\一人公司（OPC）时代的工具箱.md`
2. `C:\My Space (Obsidian)\My space\03 Resources\OpenClaw 省钱实战：每月 AI 开支从 $1000 降到 $200.md`
3. `C:\My Space (Obsidian)\My space\03 Resources\SaaS业数千亿市值蒸发：AI如何变革组织架构？.md`

**Tier 2（AI 生态 / 思想性，酌情选 1-2 篇）**：
4. `C:\My Space (Obsidian)\My space\03 Resources\【文字稿】AI's Killer-App Isn't Chatbots, It's Social Linkedin Founder Reid Hoffman.md`
5. `C:\My Space (Obsidian)\My space\03 Resources\Multica — AI-native 项目管理平台.md`
6. `C:\My Space (Obsidian)\My space\03 Resources\吴恩达skills 教程.md`

**目标**：最终新增 **3-5 篇博客文章**。先读全部，判断哪些适合公开博客（剔除过于私人、未完成、或纯技术操作手册性质的），然后精选。

### 2.2 改写要点

原笔记是**内部思考笔记**，直接发布不合适。你要做的是**改写**，不是复制：

- **删除**：个人笔记标签（#todo、@someone）、Markdown 里的私人 callout、未完成的句子、不公开的项目细节
- **保留**：核心观点、数据、案例、结构
- **增强**：
  - 开头加一段"Hook"吸引读者
  - 结尾加一段"So What"回到 Solarian 的价值主张（不硬广，自然过渡）
  - 把口语化的表达改成可发布的书面语
- **长度**：每篇 **800-1500 字**（中文）。原笔记如果太长，浓缩到这个区间；太短就不选。
- **语气**：博客 voice—— 知识分子、务实、不煽情、不装 X

### 2.3 每篇文章要生成的元数据

参照 `src/trends/index.json` 中现有 8 篇的格式，每篇新文章需要：

```json
{
  "id": "009",                       // 从 009 开始递增（字符串、3 位数字）
  "num": 9,                          // 对应数字（整数）
  "title": "标题",
  "tag": "标签文字",                  // 见下方 tag 表
  "tagClass": "tag-opinion",         // 对应 CSS class
  "desc": "卡片上的一句话摘要，50-80 字",
  "source": "作者/来源（通常是 Solarian 或 原作者名）",
  "date": "2026.04",                 // 格式 YYYY.MM
  "readTime": "6 分钟",               // 预估（800 字≈4 分钟，1500 字≈7 分钟）
  "cover": "assets/blog-xxx.jpg"     // 封面图路径（见 2.4）
}
```

**Tag 对照表**（使用现有 CSS class，不要新增）：

| tagClass | 颜色 | 适用内容 |
|----------|------|---------|
| `tag-policy` | 蓝 | 政策、法规、制度 |
| `tag-case` | 绿 | 真实案例、数据复盘 |
| `tag-trend` | 紫 | 行业趋势、宏观观察 |
| `tag-opinion` | 橙 | 观点、评论、人物访谈 |
| `tag-insight` | 青 | 方法论、工具箱、洞察 |
| `tag-story` | 粉 | 故事、随笔 |

### 2.4 封面图（**记住要配图**）

每篇文章必须有 `cover` 字段指向一张图。三种来源，**按顺序优先**：

**Option 1 — 复用 `assets/` 已有图**（首选）：
现有可用图片（用 `ls "assets/"` 查看完整列表）：
- `cockpit_screenshot.png` / `scenario_illustration.png` — 产品/场景类
- `daneel.jpg` / `dors.jpg` / `hober.jpg` / `robin.jpg` / `marcus.jpg` / `luna.png` — agent 头像
- `sam_altman.jpg` / `garry_tan.jpg` — 人物
- `news_shenzhen_opc.png` / `news_xinhua_opc.png` — 新闻头图
- `medvi_nyt.jpg` — 案例
- `workflow_flywheel.svg` / `n8n_series_c.png` — 抽象概念

**Option 2 — 从 Unsplash 下载 CC0 免费图**（如果现有的都不贴切）：
用 `curl` 下载 Unsplash Source 图（免 API key）：
```bash
# 下到 assets/ 目录，文件名用 blog- 前缀
curl -L "https://source.unsplash.com/1600x900/?KEYWORD1,KEYWORD2" -o "assets/blog-<topic>.jpg"
```
关键词示例：
- 工具箱文章 → `toolbox,workspace,minimalist`
- AI 组织变革 → `office,empty,transformation`
- 独立创业 → `solo,founder,laptop`

**Option 3 — 用 CSS 渐变当 fallback**（不推荐，除非实在没图）：
在 index.json 里加 `"gradNull": true`，构建脚本会保留现有行为。

### 2.5 写好的博客内容规范

**文件路径**：`src/trends/articles/<id>.html`

**内容格式**：就是 `<p>`、`<strong>`、`<ul>`、`<h3>` 等 HTML 片段，**不要加 `<article>` 外壳**（构建脚本处理）。

**参考格式**（来自现有文章）：
```html
<p>这里是第一段开篇。</p>
<p>这里是第二段，可以用 <strong>加粗</strong> 强调重点。</p>
<h3>一个小节标题</h3>
<p>小节内容。</p>
<ul>
  <li>列表项 1</li>
  <li>列表项 2</li>
</ul>
<p>收尾段，自然过渡到 Solarian 能如何帮助解决这个问题。</p>
```

**不要使用**：
- `<h1>`（已经被文章头占用）
- `<article>` / `<section>` 外壳
- 内联样式（`style="..."`）
- 自定义 class（现有 CSS 已覆盖所有 blog 排版）

---

## 三、执行步骤

### Phase 1：读取 + 分析

1. 先 `ls src/trends/articles/` 确认当前有哪些文件（应该是 001.html 到 008.html）
2. 读 `src/trends/index.json` 理解元数据结构
3. 读 1-2 篇现有文章（比如 003.html、005.html）参考写作风格
4. 读所有 Tier 1 + Tier 2 候选 Obsidian 笔记
5. 挑出 3-5 篇最合适的（不够就减，够就不凑数）

### Phase 2：改写

对每篇入选的笔记：

1. 在脑子里（或草稿中）构思博客版本的结构
2. 写成 800-1500 字的 HTML 片段
3. 决定 tag / tagClass（用上面的对照表）
4. 选或下载封面图
5. 保存到 `src/trends/articles/<id>.html`（从 009 开始编号）
6. 把元数据添加到 `src/trends/index.json` 的 `articles` 数组**末尾**

### Phase 3：构建 + 验证

```bash
cd "C:\Users\jinha\OneDrive\桌面\AgentFlow webpage"
python build.py
```

期望输出：
```
[OK] Built news.html | 2 articles | 35,079 chars
[OK] Built trends.html | N articles | XXX chars   ← N 应该是 8 + 新增的数量
```

构建失败时，**检查 index.json 语法**（逗号、引号）和 **article HTML 是否有未闭合标签**。

### Phase 4：对外交付

双击 `trends.html` 打开：
- 博客 gallery 里应该看到新加的卡片（带你选的封面图）
- 点击每张卡片能打开文章，内容正常显示
- 返回按钮能回 gallery

---

## 四、不要做什么

- ❌ 不要直接修改 `trends.html`（会被 build 覆盖）
- ❌ 不要删除或修改现有 8 篇文章
- ❌ 不要在文章里加 `<h1>` 或 `<article>` 外壳
- ❌ 不要编造不存在的内容（如果 Obsidian 笔记里没说某个数据，就不要写）
- ❌ 不要写超过 1500 字（读者在官网博客上不会读 3000 字）
- ❌ 不要加 Obsidian 特有语法（`[[wikilinks]]`、`%%comments%%`、`#tags`）—— 改写时全部清理
- ❌ 不要引用 Franklin 的私人信息（个人健康、家庭、未公开的具体数字）

---

## 五、质量自检清单

交付前自己确认：

- [ ] 3-5 篇新文章，每篇 800-1500 字
- [ ] 每篇都有真实（或合理下载）的封面图
- [ ] 6 种 tagClass 至少用了 3 种（不要全挤在一个分类）
- [ ] 每篇标题精准、诱人，不起"震惊体"
- [ ] 每篇结尾自然过渡到 Solarian 的价值（不生硬、不硬广）
- [ ] `python build.py` 成功执行，输出字符数增加了
- [ ] 双击打开 trends.html，所有新文章正常显示、点击可读
- [ ] 构建后的 `trends.html` 已 git diff 过，变更合理（只有你新增的卡片 + 文章块）

---

## 六、交付汇报

完成后告诉发起人：

1. **新加了哪几篇文章**（标题 + tag + 源头 Obsidian 文件）
2. **每篇封面图来源**（复用 assets/ 哪张 / 从 Unsplash 下的什么关键词）
3. **构建输出字符数**（验证 build 成功）
4. **截了 1 张 trends.html gallery 视图的截图**（可选，但有帮助）

---

开工。先从 `ls src/trends/articles/` 和读 `src/trends/index.json` 开始认清当前状态，再去 Obsidian 读源文件。
