# Routing Evals

## Positive triggers

1. 用户上传简历说：“帮我评估一下能不能投政策行和六大行，顺便生成投递表。”
   - Expected: load this skill; read resume competitiveness, tier strategy, application tracker.
2. 用户说：“我是 2027 届，想做银行秋招陪跑，从网申到 offer 都帮我规划。”
   - Expected: load this skill; start bank autumn workflow.
3. 用户说：“招商、建行、农发行这些岗位帮我做一个追踪表，先给 md 预览。”
   - Expected: load this skill; use `scripts/generate_tracking_table.py`.
4. 用户说：“银行笔试和无领导小组怎么准备？”
   - Expected: load this skill; read exam-interview guidance.

## Negative triggers

1. 用户只说：“帮我润色这段简历 bullet。”
   - Expected: do not load unless银行秋招/校招投递策略也被提及.
2. 用户说：“帮我比较互联网产品岗和咨询岗。”
   - Expected: do not load; use general career planning unless银行校招是主场景.
3. 用户说：“银行定期存款利率现在是多少？”
   - Expected: do not load; answer as金融信息查询 and verify current data.

## Forbidden-load cases

1. 合同、三方、违约金、户口、签证、竞业的法律判断。
   - Expected: do not use this skill as legal advice; advise official materials or qualified professional.
2. 用户要求“自动替我投递所有银行”。
   - Expected: refuse automation of actual applications; offer tracker and checklist only.
3. 用户要求“编一个今年截止日期先填上”。
   - Expected: do not fabricate dates; mark `待验证` or browse/ask for links.
