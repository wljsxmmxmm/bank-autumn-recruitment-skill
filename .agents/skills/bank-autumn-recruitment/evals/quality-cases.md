# Quality Evals

## Resume assessment

Prompt: 用户粘贴一份只有教育、两段实习、一段社团的简历，问适合政策行还是股份行。

Must include:
- 六维评分、权重、相关经历、理由、加权总分。
- 政策行和股份行的权重差异。
- 短板诊断和优先提升建议。

Must not:
- 给录用保证。
- 用材料中没有出现的党员、排名、证书、实习成果做判断。

## Resume self-introduction template

Prompt: 用户说“我没有整理好的简历，先给我一个模板，我按模板介绍自己后你再评估。”

Must include:
- 给出自述模板，覆盖教育背景、目标、实习、项目、证书、校园经历和约束。
- 说明用户也可以上传或粘贴简历，由 Skill 先解析。
- 如果模板内容不完整，只追问 1-3 个最影响判断的问题。

Must not:
- 在信息明显缺失时硬给完整评分。
- 把缺失信息脑补成用户已经具备的经历。

## Lightweight interactive entry

Prompt: 用户只说“我是 2027 届，想投银行秋招，先带我做规划。”

Must include:
- 先给 4 个以内的菜单选项，而不是直接输出长篇规划。
- 选项覆盖竞争力评估、投递策略/银行池、公告/JD 定制、笔试面试/Offer 阶段。
- 提醒用户未确认的公告、日期、岗位名和链接会标为 `待用户确认`，不编信息。

Must not:
- 一次问超过 3 个问题。
- 在用户没有提供足够背景时直接生成完整投递表。
- 使用 `待验证`、`待核验` 作为用户可见状态。

## Tracking table

Prompt: 用户给出 5 个银行岗位，其中建设银行上海分行和浙江分行岗位相同，要求生成追踪表。

Must include:
- 先用 `scripts/generate_tracking_table.py` 生成 Markdown 预览。
- 建设银行两个分行保留为两行。
- 字段覆盖岗位来源、投递链接、银行/岗位信息、招聘批次、网申账号、简历版本、材料清单、网申提交日、测评/笔试/面试、下次跟进日、提醒级别、匹配经历、主要风险、复盘记录、Offer状态、签约风险、备注、优先级。
- 用户确认后再创建在线文档。

Must not:
- Agent 手写排序后的表格。
- 未确认就创建 Notion/在线表。

## Comprehensive bank pool

Prompt: 用户说“秋招投递追踪表应该尽可能全面，涵盖大部分银行。”

Must include:
- 使用 `scripts/generate_tracking_table.py --template comprehensive` 生成 Markdown 预览。
- 覆盖政策性银行、国有六大行、主要股份制银行、代表性城商行/农商行。
- 所有当前开放状态、截止日、笔试时间和投递链接标为 `待用户确认`。
- 提醒用户按城市、岗位类别、简历竞争力筛选 P0/P1。

Must not:
- 手写银行名单表。
- 声称全面模板等于当年岗位已开放。

## Notion workspace creation

Prompt: 用户确认 Markdown 预览后说“把这版投递表创建到 Notion 里，后续提醒和复盘都围绕这个表。”

Must include:
- 读取 `references/notion-workspace-schema.md`，按固定主表字段和固定视图创建 Notion 工作台。
- 把 Markdown 预览视为创建前确认稿，不把全量 32 字段原样搬进 Notion 主表。
- 创建 `Default view`、`P0主攻`、`本周处理`、`流程中`、`截止日历`、`提醒日历`、`结果复盘`。
- 创建成功后明确 Notion URL 是后续维护、提醒、复盘和公告更新的主入口。

Must not:
- 用户未确认 Markdown 预览就创建 Notion。
- 在日期字段里填 `待用户确认`。
- 工具调用失败时声称 Notion 表已创建。

## Exam and interview

Prompt: 用户已经收到股份行笔试和半结构化面试通知。

Must include:
- EPI/行测、英语、金融经济专业知识、银行特色知识。
- 股份行侧重差异。
- 高频真题和 STAR/PREP/金字塔等框架。

Must not:
- 承诺押题或泄露题库。
