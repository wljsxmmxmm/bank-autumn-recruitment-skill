import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "generate_email_reminders.py"


class GenerateEmailRemindersTest(unittest.TestCase):
    def run_script(self, rows, today="2026-06-15", recipient="user@example.com"):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "rows.json"
            output_path = Path(tmp) / "email-draft.md"
            input_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--today",
                    today,
                    "--recipient",
                    recipient,
                    "--output",
                    str(output_path),
                ],
                check=True,
            )

            return output_path.read_text(encoding="utf-8")

    def test_generates_deadline_digest_without_sending(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "上海银行",
                    "岗位名称": "管培生",
                    "投递状态": "未投",
                    "投递优先级": "P0主攻",
                    "截止时间": "2026-06-17",
                    "网申入口": "https://example.com/shbank",
                    "下一动作": "完成网申",
                },
            ]
        )

        self.assertIn("To: user@example.com", markdown)
        self.assertIn("[银行秋招提醒]", markdown)
        self.assertIn("上海银行", markdown)
        self.assertIn("dry-run: 未发送", markdown)
        self.assertIn("## 回写建议", markdown)

    def test_skips_already_sent_today_and_new_job_reason(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "交通银行",
                    "岗位名称": "金融市场方向",
                    "投递状态": "未投",
                    "截止时间": "2026-06-16",
                    "网申入口": "https://example.com/bocom",
                    "上次邮件时间": "2026-06-15",
                    "邮件提醒原因": "截止临近",
                },
                {
                    "银行名称": "杭州银行",
                    "岗位名称": "管培生",
                    "投递状态": "待用户确认",
                    "邮件提醒原因": "新增可投",
                    "公告链接": "https://example.com/hzbank",
                },
            ]
        )

        self.assertIn("暂无需要发送的邮件草稿", markdown)
        self.assertNotIn("交通银行 | 金融市场方向", markdown)
        self.assertNotIn("杭州银行 | 管培生", markdown)

    def test_deadline_reminder_can_use_notion_page_url(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "中国建设银行",
                    "岗位名称": "管培生",
                    "投递状态": "未投",
                    "截止时间": "2026-06-17",
                    "url": "https://app.notion.com/p/example",
                    "下一动作": "确认基层轮岗比例",
                }
            ]
        )

        self.assertIn("中国建设银行", markdown)
        self.assertIn("https://app.notion.com/p/example", markdown)
        self.assertIn("临近截止 1 个", markdown)


if __name__ == "__main__":
    unittest.main()
