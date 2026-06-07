### The Rule

> **AI is your co-planner, not your project owner.**

>

> If AI touches your project, it goes in your tracker.

  

### What AI Can Help With

- Brainstorming project ideas

- Narrowing your project scope

- Turning a broad idea into an MVP

- Suggesting Python skills that match your idea

- Explaining confusing concepts

  

### What AI Cannot Do

- Generate your whole project for you to submit

- Skip the planning process

- Hide AI use (you must log everything)

- Complete an entire milestone in one step

  

### How to Talk to AI

  

**If you do not have an idea yet, copy and paste this prompt:**

  

```

I am a high school computer science student planning a Python final project.

  

I know functions, lists, dictionaries, APIs, basic OOP, and error handling.

  

Give me 8 realistic project ideas.

  

For each idea, include:

1. Target user

2. Smallest working version

3. Python skills used

4. One possible stretch feature

  

Keep the ideas realistic for a student project.

```

  

**If you already have an idea, copy and paste this prompt:**

  

```

I am a high school computer science student planning a Python final project.

  

I know functions, lists, dictionaries, APIs, basic OOP, and error handling.

  

My project idea is: [INSERT YOUR IDEA HERE]

  

Help me turn this into a realistic MVP. Give me:

1. A simple version

2. Three must-have features

3. Two features that are probably too big

4. Python skills I could show

5. The first tiny thing I should build



  

## Part 5: Log Your AI Usage

  

**Immediately after** you use AI, open `02 AI Usage Tracker` and fill out this template:

  

```markdown

# AI Usage Tracker

  

## Entry 1 — [4/28]

  

### What I Asked AI

(Have some launch idea)

  

### Why I Asked

(What were you stuck on? What did you need help with?)
Nop

  

### What AI Gave Me

(Summarize what AI suggested or explained)
Some launch idea 

  

### What I Used

(What parts of AI's response did you actually use?)

  

### What I Changed or Rejected

(What did you modify or decide not to use?)

  

### What I Still Do Not Fully Understand

(Be honest. What is still confusing?)

  

### My Next Step

(What will you do next based on this conversation?)

```

  # AI Usage Tracker - Life Simulator

## Entry 1

### Date
2026-05-20

### AI Tool Used
Claude (via chat)

### What I Asked AI
"请你帮我做一个 life simulator，根据我的产品介绍，在 obsidian_vault 文件夹里面制作一个 main.py 文件来记录。游戏需要包含：5个属性（Health, Happiness, Intelligence, Wealth, Social），从5岁到25岁的分支故事，每个事件有2-3个选择，选择会改变属性，最终根据最高属性给出结局。"

### Why I Asked
我从来没有做过这么大的项目，不知道从哪里开始。需要 AI 帮我搭建基础框架，包括 Player 类、事件系统、属性系统。

### What AI Gave Me
完整的 main.py 代码，包含：
- Player 类（属性、apply_effects、to_dict/from_dict）
- 几个示例事件（年龄 5, 10, 15, 20, 25）
- get_ending() 结局函数
- 命令行界面的 Game 类
- JSON 存档功能

### What I Used
全部使用了。AI 给的代码直接能跑，帮我快速验证了游戏设计是否可行。

### What I Changed or Rejected
没有改，先用了基础版本测试。

### What I Still Do Not Fully Understand
JSON 的 save/load 机制，但运行几次后就明白了。

### My Next Step
测试游戏是否好玩，然后添加更多事件。

---

## Entry 2

### Date
2026-05-25

### AI Tool Used
Claude

### What I Asked AI
"请给游戏加更多事件，让事件更好笑一点。现有的故事太平淡了，想要更搞笑的剧情，比如吃蜡笔、芹菜帮这种。年龄扩展到 100 岁。"

### Why I Asked
基础版本只有 5 个事件，玩一遍太快了。而且故事太正经，我想要更幽默的风格来吸引玩家。

### What AI Gave Me
- 扩展了 build_events() 函数，从 age 3 到 age 100，共 15+ 个事件
- 加入了搞笑剧情：幼儿园吃蜡笔、芹菜帮、青草如运动会等
- 加入了条件事件（if player.has_history）
- 加入了 stat requirement 系统（需要 70+ Social 才能追到 crush）

### What I Used
全部事件数据都用了。事件系统（year, scene, text, choices, effects, tag, requires）的结构完全采纳。

### What I Changed or Rejected
微调了一些 stat 变化数值，让游戏更平衡。比如吃蜡笔的 Health 从 -10 改成了 -5。

### What I Still Do Not Fully Understand
`build_events()` 里条件事件如何根据 player.history 动态添加，但看代码逻辑后理解了。

### My Next Step
测试新事件，确保连锁反应（celery_gang → veggie crime）正常工作。

---

## Entry 3

### Date
2026-05-30

### AI Tool Used
Claude

### What I Asked AI
"帮我用 Git 把代码上传到 GitHub。我不知道怎么操作。"

### Why I Asked
之前从来没做过 Git 操作，需要 AI 教我步骤。

### What AI Gave Me
- 终端命令：`git init`, `git add .`, `git commit -m "..."`, `git push`
- 解释每个命令的作用
- 教我怎么在 GitHub 网站上创建仓库

### What I Used
命令步骤全部照做了。成功把代码 push 到了 GitHub。

### What I Changed or Rejected
没有改，直接用了命令。

### What I Still Do Not Fully Understand
Git 的分支和 merge，但我目前只需要基本的 push/pull。

### My Next Step
继续开发前端 UI。

---

## Entry 4

### Date
2026-06-02

### AI Tool Used
Claude

### What I Asked AI
"帮我制作 2D CSS 动画，让每个游戏事件都有一个卡通插图。用纯 CSS，不要图片。需要动画效果，比如心形漂浮、蜡笔摇摆、迪斯科球旋转。"

### Why I Asked
我想让网页版更好看，但我完全不会 CSS 动画。不知道 `@keyframes` 怎么用。

### What AI Gave Me
- 完整的 scenes.css 文件，包含 15+ 个场景动画
- 每个场景的 CSS 类（.scene-kindergarten, .scene-prom, .scene-graveyard 等）
- 动画关键帧：`@keyframes heart-float`, `@keyframes crayon-wobble`, `@keyframes disco-spin`
- 用 `::before` 和 `::after` 伪元素绘制角色

### What I Used
全部用了。CSS 代码直接复制到 scenes.css 文件。

### What I Changed or Rejected
微调了颜色和一些动画时长，让效果更 smooth。

### What I Still Do Not Fully Understand
`transform: translateY()` 和 `top` 的区别。AI 解释后知道 translateY 更流畅。

### My Next Step
确保动画和事件场景匹配（kindergarten → 幼儿园动画）。

---

## Entry 5

### Date
2026-06-04

### AI Tool Used
Claude

### What I Asked AI
"让 2D 动画和每个事件对应好。我的事件有 scene 字段（kindergarten, prom, hospital 等），帮我确保每个 scene 都有对应的 CSS 动画。"

### Why I Asked
之前有些事件（比如 celery_gang）没有对应的场景动画，页面会空白。

### What AI Gave Me
- 补充了缺失的场景：gym, street, party, office, home, promotion, midlife, hospital, retirement, grandkids, reflection, journalist, graveyard
- 每个场景的独特动画（猫咪说话、心跳线、升职信漂浮、跑车等）
- 确保 event["scene"] 和 CSS 类名完全匹配

### What I Used
全部用了。现在每个事件都有对应的 CSS 插图。

### What I Changed or Rejected
把 celery 场景的动画从静态改成了摇摆动画。

### What I Still Do Not Fully Understand
CSS 的 `position: absolute` 在动画中的定位逻辑，但慢慢调也调好了。

### My Next Step
做老师的 regrade 要求：拆分 engine 和界面，写测试，部署。

---

## Summary

**Total AI sessions:** 5

**Most helpful:** CSS 动画部分，我完全不会，AI 帮我从零做出了 15+ 个场景动画。

**What I would do differently:** 早点开始拆分 engine 和界面，不要等老师 feedback。

**How AI changed my learning:** 不是用 AI 替代思考，而是用 AI 加速学习。每个 AI 给的代码我都读懂了才用。

**You must fill this out every time you use AI for this project.**

# Part 6: Write Your Ownership Paragraph

  

After using AI, answer these three questions honestly. Paste this at the bottom of your `02 AI Usage Tracker`:

  

1. **After using AI, my project idea changed because ai give me more valuable idea

2. **The part I understand best is  about game 

3. **The part I still need help with is creating
