import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]


class NotionWorkspaceCreationFlowTest(unittest.TestCase):
    def read(self, relative_path):
        return (SKILL_DIR / relative_path).read_text(encoding="utf-8")

    def test_skill_routes_notion_creation_to_fixed_workspace_protocol(self):
        skill = self.read("SKILL.md")

        self.assertIn("references/notion-workspace-schema.md", skill)
        self.assertIn("Notion 工作台", skill)
        self.assertIn("创建成功后的 Notion URL 是后续维护、提醒、复盘的主入口", skill)

    def test_workspace_schema_defines_minimal_main_table_and_views(self):
        schema = self.read("references/notion-workspace-schema.md")

        for field in [
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
        ]:
            self.assertIn(field, schema)

        self.assertIn("政策性-T0", schema)
        self.assertIn("国有大行-T0", schema)
        self.assertIn("统一字段协议", schema)
        self.assertNotIn("## 字段映射", schema)

        for view in ["Default view", "P0主攻", "本周处理", "流程中", "截止日历", "提醒日历", "结果复盘"]:
            self.assertIn(view, schema)

    def test_conversion_docs_do_not_make_full_markdown_table_the_notion_schema(self):
        external_rules = self.read("references/external-doc-conversion-rules.md")
        tracker = self.read("references/application-tracker.md")

        self.assertIn("Notion 主操作台以 `references/notion-workspace-schema.md` 为准", external_rules)
        self.assertIn("Notion 工作台创建以 `references/notion-workspace-schema.md` 为准", tracker)
        self.assertNotIn("银行秋招字段至少包含脚本输出的默认全面字段", tracker)


if __name__ == "__main__":
    unittest.main()
