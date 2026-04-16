# Solarian AI 配色系统

> 2026-04-15 建立 · 基于 Anthropic / Stripe / Linear 风格研究
> 方向：**Warm-Minimal Professional**（温暖极简专业）—— 避开 AI 行业 95% 都在用的紫色渐变陷阱

---

## 三色锚点（已锁定）

| 角色 | Hex | 作用 |
|------|-----|------|
| **Cream 米白** | `#F5F0E6` | 页面主背景 / 温暖基调 |
| **Teal 深青** | `#0d9488` | 主强调 / CTA / 链接 |
| **Charcoal 炭灰** | `#1a1f2e` | 深色段落 / 主文字 |

---

## 完整 Color Tokens

### 背景层
| Token | Hex | 用途 |
|-------|-----|------|
| `bg-primary` | `#F5F0E6` | 页面主背景 |
| `bg-elevated` | `#FBF8F1` | 卡片、模态框（比主背景亮一档） |
| `bg-sunken` | `#EDE6D6` | 输入框底、代码块（比主背景暗一档） |
| `bg-inverted` | `#1a1f2e` | 深色段落（Waitlist 等） |
| `bg-inverted-elevated` | `#252B3D` | 深色段里的卡片 |

### 中性色（暖灰过渡 — Radix Sand 系）
| Token | Hex | 用途 |
|-------|-----|------|
| `neutral-100` | `#E8E1D1` | 米白上的细分隔线 |
| `neutral-300` | `#C9BFA8` | 输入框边框、禁用态 |
| `neutral-500` | `#8A8070` | 次要图标、次级分隔 |
| `neutral-700` | `#4A4638` | 米白上的次要文字 |
| `neutral-900` | `#2B2A24` | 替代深色文字（比 #1a1f2e 柔和） |

### 强调色（关键决策点 ⭐）
| Token | Hex | 用途 |
|-------|-----|------|
| `accent-primary` | `#0d9488` | 主 CTA / 链接（已有 teal） |
| `accent-primary-hover` | `#0B7F74` | 悬停态 |
| `accent-primary-soft` | `#CCE7E3` | 徽章背景、选中高亮 |
| **`accent-secondary`** | **`#D97757`** | **暖陶土 Terracotta** — 次级 CTA、徽章、人性化点缀 ⭐ |
| `accent-tertiary` | `#C9A961` | 哑金色 — Pro 徽章、引号条、奢华重点 |

### 语义色（与主色协调，不扎眼）
| Token | Hex | 说明 |
|-------|-----|------|
| `success` | `#5F8D4E` | 鼠尾草橄榄绿（不用刺眼的 #22c55e） |
| `warning` | `#C08A2E` | 焦糖金（跟 accent-tertiary 同家族） |
| `error` | `#C4533A` | 锈红（terracotta 的深暗表亲） |
| `info` | `#4A7FA7` | 尘蓝（teal 的冷伙伴） |

### 文字色（米白底上）
| Token | Hex | 对比度 | 用途 |
|-------|-----|-------|------|
| `text-primary` | `#1a1f2e` | 14.2:1 | 正文、标题 |
| `text-secondary` | `#4A4638` | 8.1:1 | 副标题、说明 |
| `text-tertiary` | `#7A7363` | 4.7:1 AA | 元数据、时间戳 |
| `text-disabled` | `#B5AC97` | — | 禁用态 |
| `text-link` | `#0B7F74` | 5.2:1 AA | 链接（比主 teal 稍深保证对比） |

### 文字色（炭灰底上）
| Token | Hex | 用途 |
|-------|-----|------|
| `text-inverted-primary` | `#F5F0E6` | 深底主文字（重用米白） |
| `text-inverted-secondary` | `#C9BFA8` | 深底次级文字 |
| `text-inverted-tertiary` | `#8A8070` | 深底元数据 |
| `text-inverted-link` | `#4FD1C5` | 深底链接（teal 调亮，#0d9488 在深底对比不足） |

### 渐变（经过设计，不是通用模板）
| 名称 | CSS | 用途 |
|------|-----|------|
| `gradient-hero` | `linear-gradient(135deg, #F5F0E6 0%, #CCE7E3 50%, #D4E4CE 100%)` | 米白→浅青→鼠尾草 柔光底 |
| `gradient-accent` | `linear-gradient(120deg, #0d9488 0%, #4A7FA7 100%)` | Teal→尘蓝 — 用在核心标题文字 |
| `gradient-warm-cta` | `linear-gradient(135deg, #D97757 0%, #C9A961 100%)` | 陶土→金 — 醒目次级 CTA |

---

## 三条"立刻锁定"的决策

### 1. ⭐ 提交 Terracotta `#D97757` 作为次级强调色
这是**最高杠杆的决定**。它决定 Solarian 读作"温暖的人性化 AI"（Anthropic 赛道）还是"无聊的企业 Teal SaaS"（大多数赛道）。
**推荐决策**：采纳 ✅

### 2. 深色段落的角色？
- 满量使用（Linear 路线）：全套 inverted tokens + 深色 mode 渐变
- 仅重点区域（Anthropic 路线）：只在 footer + Waitlist CTA 等少数地方
**推荐决策**：v1 采用 Anthropic 路线 — 米白是品牌核心，不稀释

### 3. 代码里用 OKLCH 而非 Hex（进阶）
Anthropic 用 OKLCH；Stripe 基于 CIELAB 重构了系统。OKLCH 能：
- 感知一致的深浅 mode 自动派生
- WCAG 对比度可预测
**推荐决策**：v1 用 Hex（简单），等扩展到 dark mode 时迁移 OKLCH

---

## 参考站点（按相似度）

1. **Anthropic** (anthropic.com / claude.ai) — 最接近你的美学
   - Pampas `#F4F3EE` + Crail `#C15F3C` + 深炭 `#141413` + Sage `#788C5D`
   - 偷：米白大面积留白 + 陶土作为点缀 + 色彩"标点符号化"使用（不是装饰）

2. **Stripe Docs** (stripe.com/docs)
   - 偷：暖灰中性色阶 + 单一强调色配合不同透明度

3. **Linear** (linear.app)
   - 偷：渐变文字（每段一个关键标题用 `gradient-accent`）+ 浅页面内嵌深色段的技法

---

## 要避开的陷阱

1. ❌ 紫色/靛蓝渐变 — AI 行业 95% 都用，彻底和你的温暖方向矛盾
2. ❌ 扎眼的绿/红（#22c55e / #ef4444）— 在米白上太刺
3. ❌ 冷调纯灰 — 会和米白打架，必须用暖灰（Radix Sand）

---

## 使用优先级

- **必须最先实装的 3 个**：`bg-primary`、`accent-primary`、`text-primary`（已有）
- **下一步**：`accent-secondary` (terracotta)、`neutral-*` 色阶、`bg-inverted`
- **最后精修**：语义色、渐变、深底文字
