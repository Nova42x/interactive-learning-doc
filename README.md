# interactive-learning-doc

一个把**任何技术内容**（论文、项目源码、教程、工具说明）转成**单文件互动式 HTML 学习文档**的 agent skill。

面向零基础读者：由浅入深的章节 + 手绘 SVG 图解 + 可交互代码块（悬停某行 → 框选高亮 + 右侧面板显示该行解释）+ 提示框 + 小测验 + 词汇表。产出是**单个 HTML 文件，离线可用**（图片 base64 内嵌，无 CDN 依赖）。

## 产出效果

- 左侧 264px 目录侧栏 + 右侧 330px 悬停解释面板，内容单栏居中
- 代码块：语法高亮、行悬停框选高亮、点击锁定、右侧逐行解释
- 五色提示框（蓝=发现、黄=坑、绿=类比、灰=细节、紫=行动）
- 小测验、词汇表、阅读进度条
- 固定设计令牌：纸感米白背景 `#f6f7f4` + 绿色主色 `#0e7c5b`，风格统一不做自由发挥

## 文件结构

```
interactive-learning-doc/
├── SKILL.md                        # skill 主文件：触发条件、工作流、已知坑、验证清单
└── references/
    ├── ui-theme.css                # 完整 UI 主题（全部组件样式，直接内嵌到 <style>）
    ├── skeleton.html               # 可直接复制的完整骨架（head + CSS + sidebar + 全部组件示例 + JS）
    └── check-explain-lines.py      # 校验脚本：逐行解释键数 vs 代码块实际行数
```

## 安装

把整个目录复制到 agent 的 skills 目录即可：

```bash
# ZCode
cp -r interactive-learning-doc ~/.zcode/skills/

# Claude Code
cp -r interactive-learning-doc ~/.claude/skills/
```

## 使用

对 agent 说：

- "把这个做成网页带我读"
- "给我做个学习页面"
- "图文并茂的阅读文档"
- "做个教程 HTML"

适用素材不限于代码：

| 素材类型 | 教学侧重 |
|---|---|
| 论文 | 概念 → 方法 → 结果 → 差异点 |
| 项目源码 | 文件地图 → 数据流 → 核心代码 → 训练/部署 |
| 教程/技术文档 | 概念 → 快速上手 → 进阶 → 常见坑 |
| 工具使用 | 安装 → 核心命令 → 参数 → 实战案例 |
| 面试速览 | 概念卡 → 类比 → 小测验 |

## 交付前校验（skill 内置流程）

```bash
# ① JS 语法检查（先于浏览器验证）
node --check extracted-script.js

# ② 行号对齐核对（有代码块时必跑）
python references/check-explain-lines.py guide.html
```

再加浏览器实测（悬停核心代码块首末行、console 零错误）与截图视觉确认。完整清单见 SKILL.md。

## 已知坑（已内置规避方案）

语法高亮正则互相污染（全占位符方案）、逐行解释行号错位、JS 拼接 `},,` 崩溃、CSS 伪元素与文本 emoji 双图标、长行溢出、CRLF 匹配失败、file:// 下 console 报错定位难、IIFE 链中断——细节见 SKILL.md"已知坑"一节。

## License

[MIT](LICENSE)
