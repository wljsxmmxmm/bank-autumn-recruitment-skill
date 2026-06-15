import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("generate_tracking_table.py")


class GenerateTrackingTableTest(unittest.TestCase):
    def run_script(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "rows.json"
            output_path = Path(tmp) / "preview.md"
            input_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

            subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path), "--output", str(output_path)],
                check=True,
            )

            return output_path.read_text(encoding="utf-8")

    def test_sorts_by_tier_then_probability(self):
        markdown = self.run_script(
            [
                {"银行名称": "招商银行", "银行类型": "股份制银行", "梯队": "第三梯队", "岗位名称": "管培生", "上岸概率": "55%-65%"},
                {"银行名称": "国家开发银行", "银行类型": "政策性银行", "梯队": "第一梯队", "岗位名称": "总行管培", "上岸概率": "20%-30%"},
                {"银行名称": "中国银行", "银行类型": "国有六大行", "梯队": "第二梯队", "岗位名称": "金融科技", "上岸概率": "65%-75%"},
            ]
        )

        lines = [line for line in markdown.splitlines() if line.startswith("| ")][2:]
        self.assertIn("| 国家开发银行 |", lines[0])
        self.assertIn("| 中国银行 |", lines[1])
        self.assertIn("| 招商银行 |", lines[2])

    def test_keeps_different_branches_as_separate_rows(self):
        markdown = self.run_script(
            [
                {"银行名称": "建设银行", "银行类型": "国有六大行", "梯队": "第二梯队", "岗位名称": "综合营销岗", "分行/总行": "上海分行", "上岸概率": "50%-60%"},
                {"银行名称": "建设银行", "银行类型": "国有六大行", "梯队": "第二梯队", "岗位名称": "综合营销岗", "分行/总行": "浙江分行", "上岸概率": "60%-70%"},
            ]
        )

        self.assertEqual(markdown.count("| 建设银行 |"), 2)
        self.assertIn("| 浙江分行 |", markdown)
        self.assertIn("| 上海分行 |", markdown)

    def test_includes_full_process_tracking_columns(self):
        markdown = self.run_script(
            [
                {"银行名称": "招商银行", "银行类型": "股份制银行", "梯队": "第三梯队", "岗位名称": "管培生", "上岸概率": "55%-65%"},
            ]
        )

        header = markdown.splitlines()[0]
        required_columns = [
            "信息来源",
            "投递链接",
            "简历版本",
            "网申账号",
            "测评状态",
            "笔试时间",
            "面试轮次",
            "下次跟进日",
            "复盘记录",
            "Offer状态",
            "签约风险",
        ]
        for column in required_columns:
            self.assertIn(column, header)

    def test_comprehensive_template_covers_major_bank_tiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "preview.md"

            subprocess.run(
                [sys.executable, str(SCRIPT), "--template", "comprehensive", "--output", str(output_path)],
                check=True,
            )

            markdown = output_path.read_text(encoding="utf-8")
            data_lines = [line for line in markdown.splitlines() if line.startswith("| ")][2:]
            self.assertGreaterEqual(len(data_lines), 60)
            for bank in ["国家开发银行", "中国工商银行", "招商银行", "北京银行", "上海农商银行"]:
                self.assertIn(bank, markdown)
            for tier in ["第一梯队", "第二梯队", "第三梯队", "第四梯队"]:
                self.assertIn(tier, markdown)


if __name__ == "__main__":
    unittest.main()
