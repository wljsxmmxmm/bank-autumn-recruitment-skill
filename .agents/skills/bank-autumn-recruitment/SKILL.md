---
name: bank-autumn-recruitment
description: Use when users need China mainland bank autumn campus recruitment support, including resume competitiveness assessment, bank targeting, personalized application tracking, Notion or online-table conversion, deadline reminders, written tests, interviews, follow-ups, or bank offer decisions. Do not use for generic career chats, bank product questions, legal advice, or automatic job applications.
---

# 银行秋招 Skill

服务中国大陆 2027 届银行秋招/校招。核心产出是: 竞争力判断、银行投递策略、可维护投递表、Notion 工作台、对话内提醒摘要、笔面试准备和 Offer 决策。不替用户投递，不编造实时招聘信息。

## 阶段路由

1. **入口判断**: 用户只说想做银行秋招规划/陪跑且背景不足时，读 `references/interactive-flow.md`，先给 A-D 菜单；信息足够时直接进入对应阶段。
2. **评估与定位**: 有简历或自述背景时，读 `references/resume-competitiveness.md`，输出六维评分、短板、目标城市/岗位/银行类型建议。
3. **策略与建表**: 需要银行池、投递优先级或追踪表时，读 `references/bank-tier-strategy.md`、`references/personalized-bank-tracking-template.md`、`references/application-tracker.md`；最终预览必须用 `scripts/generate_tracking_table.py`。
4. **创建工作台**: 用户确认 Markdown 预览后，Notion 读 `references/notion-workspace-schema.md`；腾讯文档、飞书、Google Sheets 或 Excel 读 `references/external-doc-conversion-rules.md`。创建成功后的 Notion URL 是后续维护、提醒、复盘的主入口。
5. **维护闭环**: 已有 Notion 或在线表后，读 `references/automation-playbook.md`，默认先用 `scripts/conversation_reminder_summary.py` 生成对话内提醒摘要；用户确认前不要写回 Notion、发送邮件或创建外部提醒。
6. **事件分支**: 新公告/JD 读 `references/announcement-resume-tailoring.md`；测评、笔试、面试读 `references/exam-interview-guidance.md`；意向、体检、签约或多个 Offer 读 `references/offer-decision-framework.md`。

## 资源导航

- `references/interactive-flow.md`: 背景不足时的轻量入口菜单。
- `references/resume-competitiveness.md`: 简历竞争力和六维评分。
- `references/bank-tier-strategy.md`: 政策行、六大行、股份行、城商农商行梯队判断。
- `references/bank-recruitment-library-template.md`、`references/bank-recruitment-library-sample-cdb.md`、`references/bank-recruitment-library-samples-major-banks.md`: 银行事实库模板和样例。
- `references/personalized-bank-tracking-template.md`、`references/application-tracker.md`: 定制投递表字段、排序和预览规则。
- `references/notion-workspace-schema.md`: Notion 工作台字段、视图和创建后检查。
- `references/external-doc-conversion-rules.md`: 非 Notion 在线文档转换规则。
- `references/automation-playbook.md`、`references/email-reminders.md`: 对话摘要、截止提醒、流程线索、公告巡检、周复盘和邮件草稿规则。
- `references/daily-job-monitor.md`、`references/role-source-catalog.md`: 需要扩展每日官方来源巡检或社区线索时读取。
- `references/banking-campus-demo.md`: 需要岗位族示例或展示材料时读取。
- `assets/full-workflow-case.md`: 需要完整展示案例、宣传素材或端到端测试素材时读取。
- `assets/bank-autumn-workflow-sample.md`、`assets/personalized-bank-tracking-sample.md`: 需要示例输出或质量对照时读取。

## 脚本

- `scripts/generate_tracking_table.py`: 生成银行投递表 Markdown 预览；不要手写最终排序表。
- `scripts/conversation_reminder_summary.py`: 生成四类对话内提醒摘要。
- `scripts/automation_dry_run.py`: 本地验证截止提醒逻辑，不写外部系统。
- `scripts/generate_email_reminders.py`: 生成邮件草稿和回写建议，不发送真实邮件。

## 强约束

- 追踪表必须先生成 Markdown 预览；用户确认前不要创建 Notion 或其他在线文档。
- Notion 工作台必须按 `references/notion-workspace-schema.md` 创建；不要把 Markdown 全量字段原样搬进 Notion 主表。
- 四类自动化默认先生成对话内提醒摘要；用户确认前不要真实写回 Notion、发送邮件或创建外部提醒。
- 不同总行、分行、子公司、城市和岗位必须拆成独立行。
- 涉及当前开放岗位、截止日、笔试时间、薪资、批次、宣讲会或招聘政策时，必须联网核验或让用户提供链接；无法确认写 `待用户确认`。
- 输出必须区分 `用户背景`、`已确认信息`、`经验判断`、`待用户确认`。
- `上岸概率` 只能是区间和相对判断，不能写成录用保证，也不要作为 Notion 主表字段。
- 用户要求真实建议时，直接指出短板、竞争劣势、岗位错配和不建议投入的方向。

## Gotchas

- 不要把该 Skill 用成普通简历润色器；公告和目标岗位明确后才进入岗位版简历定制。
- 不要把“银行名称”当作一个机会；机构层级、城市和岗位会改变竞争强度。
- 不要用二手整理表替代官方招聘页；小红书、社群截图或匿名流程帖只能作为弱线索。
- 不要把政策行、六大行、股份行、城商农商行写成同一套门槛。
- 不要在 Offer 信息缺失时直接排序；先追问合同主体、机构层级、岗位真相、薪酬拆解、KPI 和签约约束。
- 不要声称邮件、Notion 或在线文档已经创建，除非对应工具调用成功。

## 常用启动语

- `我是 2027 届，想投银行秋招，先带我做规划。`
- `我上传了简历，帮我评估银行秋招竞争力，并生成投递梯队和追踪表预览。`
- `把这些银行岗位生成 Markdown 追踪表，确认后再放到我的 Notion 里。`
- `读取我的 Notion 投递表，生成今天的截止提醒、网申陪跑、流程线索和周复盘摘要。`
- `这个银行公告出来了，帮我选岗位、改简历和准备网申。`
- `我拿到两个银行 Offer，帮我用不可能三角做决策。`
