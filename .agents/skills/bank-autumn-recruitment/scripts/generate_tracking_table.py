#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


COLUMNS = [
    "信息来源",
    "投递链接",
    "银行名称",
    "银行类型",
    "梯队",
    "岗位名称",
    "岗位类别",
    "分行/总行",
    "工作地点",
    "招聘批次",
    "网申截止日",
    "网申账号",
    "简历版本",
    "材料清单",
    "网申提交日",
    "笔试时间",
    "测评状态",
    "笔试状态",
    "面试轮次",
    "面试时间",
    "面试形式",
    "投递状态",
    "下次跟进日",
    "提醒级别",
    "上岸概率",
    "关键证据",
    "主要风险",
    "复盘记录",
    "Offer状态",
    "签约风险",
    "备注",
    "优先级",
]

TIER_RANK = {
    "第一梯队": 1,
    "政策性银行": 1,
    "第二梯队": 2,
    "国有六大行": 2,
    "第三梯队": 3,
    "股份制银行": 3,
    "第四梯队": 4,
    "城商行": 4,
    "农商行": 4,
}

BANK_UNIVERSE = [
    ("国家开发银行", "政策性银行", "第一梯队"),
    ("中国进出口银行", "政策性银行", "第一梯队"),
    ("中国农业发展银行", "政策性银行", "第一梯队"),
    ("中国工商银行", "国有六大行", "第二梯队"),
    ("中国农业银行", "国有六大行", "第二梯队"),
    ("中国银行", "国有六大行", "第二梯队"),
    ("中国建设银行", "国有六大行", "第二梯队"),
    ("交通银行", "国有六大行", "第二梯队"),
    ("中国邮政储蓄银行", "国有六大行", "第二梯队"),
    ("招商银行", "股份制银行", "第三梯队"),
    ("浦发银行", "股份制银行", "第三梯队"),
    ("中信银行", "股份制银行", "第三梯队"),
    ("兴业银行", "股份制银行", "第三梯队"),
    ("中国光大银行", "股份制银行", "第三梯队"),
    ("中国民生银行", "股份制银行", "第三梯队"),
    ("平安银行", "股份制银行", "第三梯队"),
    ("广发银行", "股份制银行", "第三梯队"),
    ("华夏银行", "股份制银行", "第三梯队"),
    ("浙商银行", "股份制银行", "第三梯队"),
    ("恒丰银行", "股份制银行", "第三梯队"),
    ("渤海银行", "股份制银行", "第三梯队"),
    ("北京银行", "城商行", "第四梯队"),
    ("上海银行", "城商行", "第四梯队"),
    ("江苏银行", "城商行", "第四梯队"),
    ("南京银行", "城商行", "第四梯队"),
    ("宁波银行", "城商行", "第四梯队"),
    ("杭州银行", "城商行", "第四梯队"),
    ("徽商银行", "城商行", "第四梯队"),
    ("成都银行", "城商行", "第四梯队"),
    ("重庆银行", "城商行", "第四梯队"),
    ("长沙银行", "城商行", "第四梯队"),
    ("广州银行", "城商行", "第四梯队"),
    ("深圳农村商业银行", "农商行", "第四梯队"),
    ("上海农商银行", "农商行", "第四梯队"),
    ("北京农商银行", "农商行", "第四梯队"),
    ("广州农商银行", "农商行", "第四梯队"),
    ("重庆农村商业银行", "农商行", "第四梯队"),
    ("东莞银行", "城商行", "第四梯队"),
    ("苏州银行", "城商行", "第四梯队"),
    ("厦门银行", "城商行", "第四梯队"),
    ("齐鲁银行", "城商行", "第四梯队"),
    ("青岛银行", "城商行", "第四梯队"),
    ("郑州银行", "城商行", "第四梯队"),
    ("西安银行", "城商行", "第四梯队"),
    ("贵阳银行", "城商行", "第四梯队"),
    ("贵州银行", "城商行", "第四梯队"),
    ("兰州银行", "城商行", "第四梯队"),
    ("甘肃银行", "城商行", "第四梯队"),
    ("晋商银行", "城商行", "第四梯队"),
    ("河北银行", "城商行", "第四梯队"),
    ("天津银行", "城商行", "第四梯队"),
    ("大连银行", "城商行", "第四梯队"),
    ("盛京银行", "城商行", "第四梯队"),
    ("哈尔滨银行", "城商行", "第四梯队"),
    ("吉林银行", "城商行", "第四梯队"),
    ("中原银行", "城商行", "第四梯队"),
    ("汉口银行", "城商行", "第四梯队"),
    ("湖北银行", "城商行", "第四梯队"),
    ("江西银行", "城商行", "第四梯队"),
    ("九江银行", "城商行", "第四梯队"),
    ("福建海峡银行", "城商行", "第四梯队"),
    ("桂林银行", "城商行", "第四梯队"),
    ("广西北部湾银行", "城商行", "第四梯队"),
    ("云南红塔银行", "城商行", "第四梯队"),
    ("昆仑银行", "城商行", "第四梯队"),
    ("青海银行", "城商行", "第四梯队"),
    ("宁夏银行", "城商行", "第四梯队"),
    ("内蒙古银行", "城商行", "第四梯队"),
    ("厦门国际银行", "城商行", "第四梯队"),
]


def tier_rank(row):
    text = f"{row.get('梯队', '')} {row.get('银行类型', '')}"
    for key, rank in TIER_RANK.items():
        if key in text:
            return rank
    return 99


def probability_midpoint(value):
    numbers = [float(match) for match in re.findall(r"\d+(?:\.\d+)?", str(value or ""))]
    if not numbers:
        return -1.0
    if len(numbers) >= 2:
        return (numbers[0] + numbers[1]) / 2
    return numbers[0]


def markdown_cell(value):
    text = "待补充" if value in (None, "") else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def normalize_row(row):
    return {column: markdown_cell(row.get(column)) for column in COLUMNS}


def default_priority(bank_type):
    if bank_type == "国有六大行":
        return "P0"
    if bank_type in ("股份制银行", "城商行", "农商行"):
        return "P1"
    return "P2"


def default_probability(bank_type):
    if bank_type == "国有六大行":
        return "35%-55%"
    if bank_type == "股份制银行":
        return "30%-50%"
    if bank_type in ("城商行", "农商行"):
        return "40%-65%"
    return "15%-35%"


def build_comprehensive_template():
    rows = []
    for bank_name, bank_type, tier in BANK_UNIVERSE:
        rows.append(
            {
                "信息来源": "待验证",
                "投递链接": "待验证",
                "银行名称": bank_name,
                "银行类型": bank_type,
                "梯队": tier,
                "岗位名称": "校招岗位待核验",
                "岗位类别": "待按用户目标归类",
                "分行/总行": "待核验",
                "工作地点": "待验证",
                "招聘批次": "秋招待验证",
                "网申截止日": "待验证",
                "网申账号": "待创建",
                "简历版本": "银行通用版",
                "材料清单": "简历、成绩单、证件照、证书待核验",
                "网申提交日": "未投",
                "笔试时间": "待公布",
                "测评状态": "待通知",
                "笔试状态": "待通知",
                "面试轮次": "待通知",
                "面试时间": "待通知",
                "面试形式": "待验证",
                "投递状态": "待核验",
                "下次跟进日": "待安排",
                "提醒级别": "观察",
                "上岸概率": default_probability(bank_type),
                "关键证据": "待结合简历匹配",
                "主要风险": "开放批次、岗位、城市和截止日待核验",
                "复盘记录": "待投递后更新",
                "Offer状态": "无",
                "签约风险": "待核验",
                "备注": "全面机会池骨架，需回到官方来源核验",
                "优先级": default_priority(bank_type),
            }
        )
    return rows


def render_table(rows):
    sorted_rows = sorted(
        rows,
        key=lambda row: (tier_rank(row), -probability_midpoint(row.get("上岸概率")), row.get("银行名称", "")),
    )
    lines = [
        "| " + " | ".join(COLUMNS) + " |",
        "| " + " | ".join(["---"] * len(COLUMNS)) + " |",
    ]
    for row in sorted_rows:
        normalized = normalize_row(row)
        lines.append("| " + " | ".join(normalized[column] for column in COLUMNS) + " |")
    return "\n".join(lines) + "\n"


def load_rows(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("rows", [])
    if not isinstance(data, list):
        raise ValueError("input must be a JSON list or an object with a rows list")
    return data


def main():
    parser = argparse.ArgumentParser(description="Generate a bank campus recruitment tracking table preview.")
    parser.add_argument("--input", help="Path to JSON rows.")
    parser.add_argument("--template", choices=["comprehensive"], help="Generate a built-in bank universe template.")
    parser.add_argument("--output", required=True, help="Path to write Markdown preview.")
    args = parser.parse_args()

    if args.template == "comprehensive":
        rows = build_comprehensive_template()
    elif args.input:
        rows = load_rows(args.input)
    else:
        parser.error("either --input or --template comprehensive is required")

    markdown = render_table(rows)
    Path(args.output).write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
