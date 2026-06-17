import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "generate_tracking_table.py"


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

    def test_sorts_by_priority_then_tier(self):
        markdown = self.run_script(
            [
                {"银行名称": "招商银行", "银行类型": "股份制银行", "同类梯队": "股份行-T0", "推荐岗位方向": "管培生", "投递优先级": "P1重点"},
                {"银行名称": "国家开发银行", "银行类型": "政策性银行", "同类梯队": "政策性-T1", "推荐岗位方向": "总行管培", "投递优先级": "P2冲刺"},
                {"银行名称": "中国银行", "银行类型": "国有六大行", "同类梯队": "国有大行-T1", "推荐岗位方向": "金融科技", "投递优先级": "P0主攻"},
            ]
        )

        lines = [line for line in markdown.splitlines() if line.startswith("| ")][2:]
        self.assertIn("| 中国银行 |", lines[0])
        self.assertIn("| 招商银行 |", lines[1])
        self.assertIn("| 国家开发银行 |", lines[2])

    def test_keeps_different_branches_as_separate_rows(self):
        markdown = self.run_script(
            [
                {"银行名称": "建设银行上海分行", "总行/分行": "上海分行", "银行类型": "国有六大行", "同类梯队": "国有大行-T1", "推荐岗位方向": "公司金融", "备注1": "城市：上海"},
                {"银行名称": "建设银行浙江分行", "总行/分行": "浙江分行", "银行类型": "国有六大行", "同类梯队": "国有大行-T1", "推荐岗位方向": "公司金融", "备注1": "城市：杭州"},
            ]
        )

        self.assertIn("| 建设银行上海分行 |", markdown)
        self.assertIn("| 建设银行浙江分行 |", markdown)
        self.assertIn("上海分行", markdown)
        self.assertIn("浙江分行", markdown)

    def test_uses_notion_workspace_columns_as_markdown_header(self):
        markdown = self.run_script(
            [
                {"银行名称": "招商银行", "银行类型": "股份制银行", "同类梯队": "股份行-T0", "推荐岗位方向": "管培生"},
            ]
        )

        header = markdown.splitlines()[0]
        header_columns = [cell.strip() for cell in header.strip("|").split("|")]
        required_columns = [
            "银行名称",
            "总行/分行",
            "推荐岗位方向",
            "银行类型",
            "同类梯队",
            "投递优先级",
            "截止时间",
            "提醒日期",
            "提醒状态",
            "下一动作",
            "简历版本",
        ]
        for column in required_columns:
            self.assertIn(column, header_columns)
        self.assertEqual(header_columns[:3], ["银行名称", "总行/分行", "推荐岗位方向"])
        for old_column in ["信息来源", "投递链接", "梯队", "岗位名称", "网申截止日", "上岸概率", "优先级"]:
            self.assertNotIn(old_column, header_columns)

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
            for tier in ["政策性-T1", "国有大行-T1", "股份行-T0", "城商行-T0", "农商行-T0"]:
                self.assertIn(tier, markdown)

    def test_tier_options_include_policy_and_major_bank_t0(self):
        markdown = self.run_script(
            [
                {"银行名称": "政策行总行专项", "银行类型": "政策性银行", "同类梯队": "政策性-T0"},
                {"银行名称": "国有大行总行专项", "银行类型": "国有六大行", "同类梯队": "国有大行-T0"},
            ]
        )

        self.assertIn("政策性-T0", markdown)
        self.assertIn("国有大行-T0", markdown)


if __name__ == "__main__":
    unittest.main()
