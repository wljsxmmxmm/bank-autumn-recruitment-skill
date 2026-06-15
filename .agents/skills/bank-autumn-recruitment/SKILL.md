---
name: bank-autumn-recruitment
description: Use when users need bank autumn campus recruitment support, including resume competitiveness assessment, bank targeting, personalized application tracking, Notion or online-table conversion, written tests, interviews, follow-ups, or bank offer decisions. Do not use for generic career chats, bank product questions, legal advice, or automatic job applications.
---

# 银行秋招 Skill

默认服务 2027 届银行秋招/校招。把用户从简历评估带到银行选择、投递跟进、在线表格、笔试面试准备和 Offer 决策；不替用户投递，不编造实时招聘信息。

## 服务流程

1. 简历竞争力评估: 用户上传或粘贴简历时，读取 `references/resume-competitiveness.md`，按六维模型给证据链、加权总分、短板和提升建议。
2. 银行梯队策略: 读取 `references/bank-tier-strategy.md`，按政策行、六大行、股份行、目标地域城商农商行输出投递优先级。
3. 定制投递表: 读取 `references/personalized-bank-tracking-template.md` 和 `references/application-tracker.md`；最终表必须用 `scripts/generate_tracking_table.py` 生成 Markdown 预览。
4. 外部表和提醒: 用户确认 Markdown 表后，读取 `references/external-doc-conversion-rules.md` 转 Notion/腾讯文档等；创建外部链接后读取 `references/automation-playbook.md` 建议截止、进度、公告和周复盘提醒。
5. 公告后简历定制: 新公告或 JD 出现时，读取 `references/announcement-resume-tailoring.md`，先选岗位，再定制简历和网申细节。
6. 笔试面试准备: 用户进入测评、笔试、无领导、半结构化或结构化面试时，读取 `references/exam-interview-guidance.md`。
7. Offer 决策: 用户拿到意向、体检、签约通知或多个 Offer 时，读取 `references/offer-decision-framework.md`；涉及合同、三方、违约金、户口等只做风险清单，建议核验官方材料或咨询专业人士。

## 参考资料加载

- `references/resume-competitiveness.md`: 简历上传、竞争力评估、六维评分、短板诊断。
- `references/bank-tier-strategy.md`: 四级梯队、推荐银行池、隐性门槛、概率区间。
- `references/bank-recruitment-library-template.md`: 银行主档案、年度公告、岗位信息库模板。
- `references/bank-recruitment-library-sample-cdb.md`: 国家开发银行投递库样例。
- `references/bank-recruitment-library-samples-major-banks.md`: 主流银行投递库骨架。
- `references/personalized-bank-tracking-template.md`: 从银行库筛选并生成用户定制投递表。
- `references/application-tracker.md`: Markdown 追踪表预览、脚本输入输出、在线文档创建规范。
- `references/external-doc-conversion-rules.md`: 将 Markdown 投递表转换为 Notion、腾讯文档、飞书表格、Google Sheets 或 Excel。
- `references/automation-playbook.md`: 外部投递表创建后的截止提醒、流程巡检、公告巡检和周复盘自动化。
- `references/announcement-resume-tailoring.md`: 招聘公告或 JD 出现后的岗位选择、简历定制和网申细节。
- `references/exam-interview-guidance.md`: EPI/行测、英语、金融经济、银行特色知识、无领导、半结构化、结构化。
- `references/offer-decision-framework.md`: 银行 Offer 不可能三角、专业追问、风险核验和决策输出。
- `assets/personalized-bank-tracking-sample.md`: 个性化投递表示例。
- `assets/bank-autumn-workflow-sample.md`: 全流程示例输出。

## 强约束

- 追踪表必须先生成 Markdown 预览；用户确认前不要创建 Notion 或其他在线文档。
- 银行追踪表必须使用 `scripts/generate_tracking_table.py`；不要手写最终排序表。
- 用户要求追踪表尽可能全面覆盖银行时，使用 `scripts/generate_tracking_table.py --template comprehensive` 生成机会池骨架。
- 银行信息、咨询判断和投递跟进要分开处理；不要把所有内容混成一张不可维护的大表。
- 不同分行、总行、子公司和城市必须分成独立行。
- 涉及当前开放岗位、截止日、笔试时间、薪资、批次、宣讲会或招聘政策时，必须联网核验或让用户提供链接；无法确认写 `待验证`。
- `上岸概率` 只能是区间和相对判断，不能写成录用保证。
- 输出必须区分 `用户提供`、`已核验`、`经验判断`、`待验证`。

## Gotchas

- 不要把该 Skill 用成普通简历润色器；公告和目标岗位明确后才进入岗位版简历定制。
- 不要把“银行名称”当作一个机会；总行、分行、子公司、城市和岗位会改变竞争强度。
- 不要把政策行、六大行、股份行、城商农商行的门槛写成同一套。
- 不要用二手整理表替代官方招聘页；二手信息只能作为线索。
- 不要把小红书、社群截图或匿名流程帖当作官方通知；只能作为弱线索提醒用户核验。
- 不要在 Offer 信息缺失时直接排序；必须先追问合同主体、机构层级、岗位真相、薪酬拆解、KPI 和签约约束。
- 不要声称邮件、Notion 或在线文档已经创建，除非对应工具调用成功。

## 常用启动语

- `我上传了简历，帮我评估银行秋招竞争力，并生成投递梯队和追踪表预览。`
- `我是 2027 届，想投银行校招，从简历到 Offer 做一个陪跑计划。`
- `把这些银行岗位生成 Markdown 追踪表，确认后再放到我的 Notion 里。`
- `这个银行公告出来了，帮我选岗位、改简历和准备网申。`
- `我拿到两个银行 Offer，帮我用不可能三角做决策。`
