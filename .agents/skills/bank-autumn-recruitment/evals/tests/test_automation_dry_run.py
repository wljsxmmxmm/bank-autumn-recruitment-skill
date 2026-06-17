import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "automation_dry_run.py"


class AutomationDryRunTest(unittest.TestCase):
    def run_script(self, rows, today="2026-06-15"):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "rows.json"
            output_path = Path(tmp) / "dry-run.md"
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

    def test_reports_deadline_and_email_candidates_without_sending(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "上海银行",
                    "岗位名称": "管培生",
                    "投递优先级": "P0主攻",
                    "投递状态": "未投",
                    "截止时间": "2026-06-17",
                    "网申入口": "https://example.com/apply",
                    "下一动作": "完成网申",
                }
            ]
        )

        self.assertIn("## 截止提醒", markdown)
        self.assertIn("上海银行", markdown)
        self.assertIn("2 天", markdown)
        self.assertIn("## 邮件待发送", markdown)
        self.assertIn("dry-run: 未发送", markdown)

    def test_lists_missing_dates_as_waiting_for_user_confirmation(self):
        markdown = self.run_script(
            [
                {
                    "银行名称": "南京银行",
                    "岗位名称": "公司金融方向待用户确认",
                    "投递优先级": "P0主攻",
                    "投递状态": "待用户确认",
                    "截止时间": "待用户确认",
                    "网申入口": "",
                    "下一动作": "核验公告",
                }
            ]
        )

        self.assertIn("## 待用户确认", markdown)
        self.assertIn("南京银行", markdown)
        self.assertNotIn("待核验", markdown)
        self.assertNotIn("待验证", markdown)


if __name__ == "__main__":
    unittest.main()
