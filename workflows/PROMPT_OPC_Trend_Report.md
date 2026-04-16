# 任务提示词 · OPC 趋势报告生成

> **发给新 Claude Code 窗口的完整指令**。把 `---` 之间的全部内容复制粘贴即可。
> 生成时间：2026-04-15
> 发起人：Daneel（PM Agent）代 Franklin 拟定

---

# 任务：为 Solarian 官网撰写《OPC 趋势报告》

你是一位负责**市场趋势研究**的工程师，要为一家叫 **Solarian** 的 AI 创业公司撰写一份数据驱动的研究报告，并集成到官网公告栏中。

---

## 一、项目背景

### 公司 Solarian

- **产品**：为 OPC（One-Person Company，一人公司）时代设计的 AI 团队操作系统——让一个人能指挥一支硅基劳动力
- **品牌来源**：Isaac Asimov《裸阳》中 Solaria 星球的居民。详见官网 news.html 已发布的 "Brand Story" 文章
- **目标用户**：一人公司创始人、独立创业者、OPC 时代的早期实践者
- **品牌调性**：warm-minimal professional（Anthropic 风格）—— 不做花哨营销，靠数据和叙事建立信任

### 设计系统

- **主 BG**：`#F5F0E6` 米白
- **主 accent**：`#0d9488` teal
- **次 accent**：`#D97757` 暖陶土（Terracotta）
- **深色段**：`#1a1f2e` 炭蓝
- **正文字体**：Noto Serif SC（衬线，用于长篇阅读）
- **标题字体**：Space Grotesk + Noto Sans SC
- 完整色彩系统定义在 `DESIGN_TOKENS.md`

---

## 二、项目物理位置与文件结构

**项目根目录**：
```
C:\Users\jinha\OneDrive\桌面\AgentFlow webpage\
```

**关键文件**：

| 文件 | 用途 |
|------|------|
| `index.html` | 官网主页（浅色主题，基准） |
| `news.html` | 公告栏（你要修改的文件——本任务最终输出在这里） |
| `trends.html` | OPC 博客（旧深色主题，**不要动**） |
| `about.html` | 关于页 |
| `DESIGN_TOKENS.md` | 色彩系统文档（**必读**，你写报告里的颜色标签要遵循这个） |
| `assets/` | 图片、logo、视频 |

**你要创建的新文件夹**（第一步就建）：
```
C:\Users\jinha\OneDrive\桌面\AgentFlow webpage\research\
```

---

## 三、核心任务

为 Solarian 官网的**公告栏**新增一篇**深度研究报告**：

**报告标题**：《OPC 趋势报告：一人公司时代已经到来》
**报告类型**：Research Report（与现有 Brand Story 并列）
**长度**：**2500-3500 字**（中文）
**发布日期**：2026-04-15
**署名**：Solarian Research

**三个必须覆盖的核心章节**（对应 index.html 主页 "Market × Product" 段落里引用的三个数字）：

1. **中国灵活就业人口 · 3 亿**
   - 权威来源（国家统计局、人社部、社科院、第三方智库）
   - 历史趋势（2015-2026 增长曲线）
   - 构成结构（年龄、行业、收入分布）
   - 相关政策环境
   
2. **OPC 扶持政策 · 20+ 城市**
   - **至少 15-20 个具体城市**（上海、深圳、杭州、北京、成都、广州、苏州、武汉、南京、重庆、宁波、合肥、西安、厦门、福州等）
   - 政策类型（税收减免、办公补贴、注册简化、社保优惠、人才认定等）
   - 政策时间线（最早起源到近期动态）
   - 每个城市政策必须附**官方文件或权威新闻**引用
   
3. **AI vs 手动效率差距 · 4.2×**
   - 具体研究出处（Nielsen Norman Group、McKinsey、BCG、GitHub/GitClear、Anthropic 官方研究、Stanford/MIT 学术论文等）
   - 研究方法（A/B 测试、任务基准、生产力追踪）
   - 行业分布（编码 / 写作 / 研究 / 客服 / 运营 等不同职能的效率提升数据）
   - 典型案例或用户故事

---

## 四、执行方式：Agent Team 并行

**必须使用 Agent 并行调用**（一条消息里发多个 Agent 工具调用）。

### Phase 1：并行研究（派 4 个 agent）

**Agent A — 中国就业数据研究员**
- 搜索关键词：
  - "中国灵活就业人口 2025 2026 国家统计局"
  - "新就业形态 规模 数据"
  - "gig economy China workforce"
  - "人社部 就业形势 报告 2026"
- 目标：拿到权威数据 + 历史趋势（至少 3 个数据点）+ 可验证 URL
- 保存到：`research/raw_A_employment.md`

**Agent B — OPC 政策扫描员**
- 搜索关键词：
  - "一人公司 扶持政策 [城市名]"
  - "个体工商户 税收优惠 2025"
  - "独立创业者 补贴"
  - 各省市"一人有限责任公司 工商登记"
- 目标：**至少 15-20 个城市**的具体政策，按城市/政策类型整理
- 每个政策条目附：城市、政策名、出台时间、官方文件 URL、政策核心内容（2 行以内）
- 保存到：`research/raw_B_policies.md`

**Agent C — AI 效率研究员**
- 搜索关键词：
  - "GenAI productivity study" / "AI workforce efficiency research"
  - "GitHub Copilot productivity study" / "code generation speed up"
  - "Nielsen Norman Group AI productivity"
  - "McKinsey generative AI economic potential"
- 目标：至少 3 个独立学术/机构研究，提供具体数字（效率提升百分比）+ URL
- 保存到：`research/raw_C_ai_efficiency.md`

**Agent D — BP 搜索员**（可选）
- 先检查以下位置是否存在 Solarian 的 BP（商业计划书）：
  - `C:\Users\jinha\OneDrive\桌面\AgentFlow webpage\` 根目录
  - `C:\Frank_vibe_coding\agentflow_v3\` 及子目录
  - `C:\My Space (Obsidian)\` 下含关键字：`BP`、`business plan`、`商业计划`、`Solarian`、`pitch`、`investor`
- 文件名匹配：`*BP*.md`、`*business-plan*.md`、`*商业计划书*.md`、`pitch*.md`、`investor*.md`
- 若找到：提炼报告中可复用的观点（产品愿景、市场定位、差异化）
- 若没找到：**跳过本 agent 的产出，不要编造**
- 保存到：`research/raw_D_bp_context.md`（如果找到）

### Phase 2：合并与撰写

所有 agent 返回后：
1. 阅读全部 raw 文件
2. 在 `research/opc-trend-report-draft.md` 中完成 markdown 全文草稿
3. 每个数据点必须有脚注引用（`<sup>[1]</sup>` 指向参考文献部分）
4. **没有来源的数据禁止出现**——宁缺毋滥

### Phase 3：集成到 news.html

把最终版本**直接嵌入** `news.html`：

---

## 五、集成细节（重要 · 精确操作）

### 5.1 先通读 news.html

在动手前**完整读一遍** `news.html`，理解：
- 现有 Brand Story article 的 HTML 结构（`<article class="story" id="article-brand-story">`）
- `.story-header`、`.lede`、`h2`、`blockquote`、`.section-break`、`.signature` 等 class 的用法
- 列表视图（`#newsList` 里的 `.news-row`）的结构
- JS 函数 `openArticle()` / `closeArticle()` 的逻辑（左侧 TOC 会自动从 h2 生成，不要手写 TOC）

### 5.2 列表视图：新增一行

在 `#newsList` 的 `.news-table` 内部，**紧跟现有 Brand Story `.news-row` 之后**，添加：

```html
<div class="news-row" onclick="openArticle('opc-trend-report')">
  <div class="news-date">2026-04-15</div>
  <div class="news-tag tag-research">Research</div>
  <div class="news-title-cell">
    <div class="news-title">OPC 趋势报告：一人公司时代已经到来</div>
    <div class="news-summary">3 亿灵活就业人口、20+ 城市扶持政策、4.2× AI 效率差距——Solarian 研究团队整理的一份事实清单。</div>
  </div>
  <div class="news-arrow">→</div>
</div>
```

### 5.3 文章视图：新增文章

在 `#newsArticle` 的 `.article-main` 内部，**紧跟现有 Brand Story article 之后**，添加新 article（骨架如下）：

```html
<article class="story" id="article-opc-trend-report" style="display:none"
         data-tag="Research Report" data-date="2026-04-15" data-author="Solarian Research">
  <div class="story-header">
    <span class="story-header-eyebrow">Research Report</span>
    <h1>OPC 趋势报告：<em>一人公司时代已经到来</em></h1>
    <div class="story-header-meta">
      2026-04-15<span>·</span>Solarian Research
    </div>
  </div>

  <p class="lede">
    [ 80-120 字引子段。问题陈述，为什么这份报告重要 ]
  </p>

  <p>[ 总体介绍段 ]</p>

  <div class="section-break"></div>

  <h2>一、3 亿 与正在发生的革命</h2>
  <p>[ 正文，带脚注 <sup>[1]</sup> ]</p>
  <p>[ 数据 + 分析 ]</p>
  <blockquote>[ 可选：关键引文或核心数据 ]</blockquote>
  <p>[ 小结 + 暗示 Solarian 解决什么 ]</p>

  <div class="section-break"></div>

  <h2>二、20 座城市的政策转向</h2>
  <p>[ 正文，按城市群或政策类型组织 ]</p>
  [ 可以用 <ul> 或 <ol> 列举代表性城市政策 ]
  <p>[ 小结 ]</p>

  <div class="section-break"></div>

  <h2>三、4.2× 和效率的新基准</h2>
  <p>[ 正文，覆盖多个研究 ]</p>
  <blockquote>[ 可选：最有分量的单一引文 ]</blockquote>
  <p>[ 小结 ]</p>

  <div class="section-break"></div>

  <h2>结论：OPC 时代需要怎样的工具</h2>
  <p>[ 收束三个事实，引向 Solarian 的价值主张 ]</p>
  <p>[ 一句定调的收尾 ]</p>

  <div class="section-break"></div>

  <h2>参考来源</h2>
  <ol class="references">
    <li>[ 来源 1 的标题及发布方] · <a href="URL" target="_blank" rel="noopener">[URL]</a></li>
    <li>[ 来源 2 ...] · <a href="URL" target="_blank" rel="noopener">[URL]</a></li>
    [ 至少 8-12 条可验证的真实 URL ]
  </ol>

  <div class="signature">
    <strong>Solarian Research</strong>
    OPC 趋势研究系列 · 第 1 期<br>
    2026-04-15
  </div>
</article>
```

### 5.4 CSS 补齐：给 news.html 的 `<style>` 末尾追加

```css
/* Research tag (绿色，用 DESIGN_TOKENS 里的 success 色) */
.tag-research{background:rgba(95,141,78,0.14);color:#5F8D4E}

/* References 列表样式 */
article.story ol.references{
  list-style:decimal;
  margin:0 0 32px 0;padding-left:28px;
  font-family:var(--font-body);
  font-size:.85rem;
  color:var(--text-sub);
  line-height:1.7;
}
article.story ol.references li{margin-bottom:10px}
article.story ol.references a{
  color:var(--accent);
  word-break:break-all;
  text-decoration:underline;
  text-decoration-color:var(--accent-sub);
  text-underline-offset:2px;
}
article.story ol.references a:hover{
  text-decoration-color:var(--accent);
}

/* 脚注角标 */
article.story sup{
  font-size:.65em;
  color:var(--accent);
  font-family:var(--font-body);
  font-weight:600;
  padding:0 1px;
}
article.story sup a{color:inherit;text-decoration:none}
article.story sup a:hover{text-decoration:underline}
```

### 5.5 验证清单

完成后手动确认：
- [ ] 打开 news.html 看到两行（Brand Story + OPC 趋势报告）
- [ ] 点击 OPC 趋势报告行，文章正常打开
- [ ] 左侧 sidebar 自动从 h2 标题生成 TOC
- [ ] 滚动文章时 TOC 当前项正确高亮
- [ ] 参考文献链接全部可点击
- [ ] 点击"返回公告列表"能回到列表视图
- [ ] 深色 CTA 区（加入 Waitlist）在文章底部正常显示
- [ ] 没有破坏现有 Brand Story 文章的显示

---

## 六、写作规范

### 语气与风格

- **严肃权威**，不是营销口吻
- **但保持可读性**——不要学究化。每段 3-5 句话为主
- **每个数据点指向产品**：章节结尾可以暗示"这是 Solarian 要解决的问题"，但不要硬广告
- **em 标签（terracotta 高亮色）**克制使用，只给最关键的词，例如"*已经到来*"、"*正在发生的革命*"、"*新基准*"。一段里最多 1-2 个

### 数据引用规范

- 每个具体数字必须有出处
- 引用格式：`三亿多<sup>[1]</sup>`，其中 `[1]` 指向"参考来源"部分对应序号
- 如果搜不到某个具体数据的权威源，**宁可不用那个具体数字**，换成区间估计（如"数以亿计"）并说明来源类型

### 不能做的事

- 不要编造任何数据或 URL
- 不要删除或修改现有的 Brand Story 文章
- 不要改动 Solarian 配色系统（只用 DESIGN_TOKENS.md 中定义的颜色）
- 不要在 news.html 之外修改其他 HTML 文件
- 不要给 news.html 引入新的第三方库

---

## 七、交付物

1. **`research/raw_A_employment.md`** · Agent A 的原始研究笔记
2. **`research/raw_B_policies.md`** · Agent B 的原始研究笔记
3. **`research/raw_C_ai_efficiency.md`** · Agent C 的原始研究笔记
4. **`research/raw_D_bp_context.md`**（若 BP 存在）
5. **`research/opc-trend-report-draft.md`** · 合并后的中文 Markdown 草稿
6. **修改后的 `news.html`** · 含新 article + 新 row + 新 CSS
7. **完成后的简短总结**（向发起人报告）：
   - 找到的关键数据点数量
   - 引用源数量
   - 新文章 URL：`news.html#opc-trend-report`
   - 遇到的问题或需要人工决策的地方

---

## 八、质量标准（发起人验收重点）

- [ ] 至少 **8-12 个**外部可验证引用源（真实可点击的 URL）
- [ ] 中国就业数据至少 **3 个权威源**（国家级统计或学术）
- [ ] OPC 政策覆盖**至少 15 个城市**，每个带政策描述
- [ ] AI 效率至少 **3 个独立研究**的具体数字
- [ ] 全文中文 **2500-3500 字**
- [ ] 整合后点击公告列表能正常打开，TOC 自动生成，滚动高亮正常
- [ ] 没有未标注来源的具体数据

---

开始吧。从派出 4 个并行 Agent 开始。

记住：**这不是写一篇博客文章，是写一份能被 VC 看、被媒体引用的研究报告**。
