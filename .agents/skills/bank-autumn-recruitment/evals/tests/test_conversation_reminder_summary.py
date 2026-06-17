import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "conversation_reminder_summary.py"


class ConversationReminderSummaryTest(unittest.TestCase):
    def run_script(self, rows, today="2026-06-16"):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "rows.json"
            output_path = Path(tmp) / "summary.md"
            input_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--today",
                    today,
                    "--output",
                    str(output_path),
                ],
                check=True,
            )

            return output_path.read_text(encoding="utf-8")

    def test_renders_four_conversation_summary_sections(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "招商银行",
                    "推荐岗位方向": "公司金融",
                    "投递优先级": "P1重点",
                    "投递状态": "待用户确认",
                    "截止时间": "2026-06-17",
                    "网申入口": "https://example.com/cmb",
                    "公告链接": "https://example.com/cmb-notice",
                    "简历版本": "银行业务版",
                    "主要风险": "岗位可能偏营销",
                    "下一动作": "确认岗位条线并完成网申",
                },
                {
                    "银行名称": "交通银行",
                    "推荐岗位方向": "金融市场",
                    "投递优先级": "P0主攻",
                    "投递状态": "笔试",
                    "截止时间": "2026-06-20",
                    "公告链接": "https://example.com/bocom-notice",
                    "笔试": "待通知",
                    "下一动作": "查邮箱、短信和站内信",
                },
                {
                    "银行名称": "上海银行",
                    "投递优先级": "P0主攻",
                    "投递状态": "offer",
                    "截止时间": "2026-06-17",
                    "下一动作": "进入 offer 决策",
                },
            ]
        )

        self.assertIn("# 银行秋招对话内提醒摘要", markdown)
        self.assertIn("运行日期: 2026-06-16", markdown)
        self.assertIn("## 1. 截止日提醒", markdown)
        self.assertIn("招商银行 公司金融", markdown)
        self.assertIn("1 天", markdown)
        self.assertNotIn("上海银行 | P0主攻 | offer | 2026-06-17", markdown)

        self.assertIn("## 2. 网申陪跑", markdown)
        self.assertIn("银行业务版", markdown)
        self.assertIn("岗位可能偏营销", markdown)

        self.assertIn("## 3. 流程线索巡检", markdown)
        self.assertIn("交通银行 金融市场", markdown)
        self.assertIn("弱线索只提示查邮箱/短信/站内信，不判断个人结果", markdown)

        self.assertIn("## 4. 周复盘", markdown)
        self.assertIn("| 流程中 | 1 |", markdown)
        self.assertIn("下周优先处理 P0/P1 临近截止和流程中岗位。", markdown)

    def test_lists_missing_dates_without_guessing(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "南京银行",
                    "推荐岗位方向": "总分行管培",
                    "投递优先级": "P0主攻",
                    "投递状态": "未投",
                    "截止时间": "",
                    "公告链接": "",
                    "网申入口": "",
                    "下一动作": "核验官方公告和截止时间",
                }
            ]
        )

        self.assertIn("## 待用户确认", markdown)
        self.assertIn("南京银行 总分行管培", markdown)
        self.assertIn("截止时间或官方链接待确认", markdown)
        self.assertNotIn("2026-06-23", markdown)


if __name__ == "__main__":
    unittest.main()
