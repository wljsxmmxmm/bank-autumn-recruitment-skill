# Quality Evals

## Resume assessment

Prompt: 用户粘贴一份只有教育、两段实习、一段社团的简历，问适合政策行还是股份行。

Must include:
- 六维评分、权重、证据来源、理由、加权总分。
- 政策行和股份行的权重差异。
- 短板诊断和优先提升建议。

Must not:
- 给录用保证。
- 用没有证据的党员、排名、证书、实习成果做判断。

## Tracking table

Prompt: 用户给出 5 个银行岗位，其中建设银行上海分行和浙江分行岗位相同，要求生成追踪表。

Must include:
- 先用 `scripts/generate_tracking_table.py` 生成 Markdown 预览。
- 建设银行两个分行保留为两行。
- 字段覆盖岗位来源、投递链接、银行/岗位信息、招聘批次、网申账号、简历版本、材料清单、网申提交日、测评/笔试/面试、下次跟进日、提醒级别、关键证据、主要风险、复盘记录、Offer状态、签约风险、备注、优先级。
- 用户确认后再创建在线文档。

Must not:
- Agent 手写排序后的表格。
- 未确认就创建 Notion/在线表。

## Comprehensive bank pool

Prompt: 用户说“秋招投递追踪表应该尽可能全面，涵盖大部分银行。”

Must include:
- 使用 `scripts/generate_tracking_table.py --template comprehensive` 生成 Markdown 预览。
- 覆盖政策性银行、国有六大行、主要股份制银行、代表性城商行/农商行。
- 所有当前开放状态、截止日、笔试时间和投递链接标为 `待验证`。
- 提醒用户按城市、岗位类别、简历竞争力筛选 P0/P1。

Must not:
- 手写银行名单表。
- 声称全面模板等于当年岗位已开放。

## Exam and interview

Prompt: 用户已经收到股份行笔试和半结构化面试通知。

Must include:
- EPI/行测、英语、金融经济专业知识、银行特色知识。
- 股份行侧重差异。
- 高频真题和 STAR/PREP/金字塔等框架。

Must not:
- 承诺押题或泄露题库。
