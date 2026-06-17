#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


COLUMNS = [
    "银行名称",
    "总行/分行",
    "推荐岗位方向",
    "银行类型",
    "同类梯队",
    "投递优先级",
    "投递批次",
    "开始时间",
    "截止时间",
    "投递日期",
    "官方招聘网站",
    "网申入口",
    "公告链接",
    "简历版本",
    "投递状态",
    "笔试",
    "一面",
    "二面",
    "三面/终面",
    "推荐理由",
    "主要风险",
    "下一动作",
    "提醒日期",
    "提醒状态",
    "备注1",
    "备注2",
]

TIER_RANK = {
    "政策性-T0": 0,
    "政策性-T1": 1,
    "国有大行-T0": 0,
    "国有大行-T1": 1,
    "股份行-T0": 0,
    "股份行-T1": 1,
    "股份行-T2": 2,
    "城商行-T0": 0,
    "城商行-T1": 1,
    "城商行-T2": 2,
    "农商行-T0": 0,
    "农商行-T1": 1,
    "农商行-T2": 2,
    "第一梯队": 1,
    "第二梯队": 1,
    "第三梯队": 1,
    "第四梯队": 1,
}

PRIORITY_RANK = {
    "P0": 0,
    "P1": 1,
    "P2": 2,
    "P3": 3,
    "放弃": 9,
}

BANK_UNIVERSE = [
    ("国家开发银行", "政策性银行", "政策性-T1"),
    ("中国进出口银行", "政策性银行", "政策性-T1"),
    ("中国农业发展银行", "政策性银行", "政策性-T1"),
    ("中国工商银行", "国有六大行", "国有大行-T1"),
    ("中国农业银行", "国有六大行", "国有大行-T1"),
    ("中国银行", "国有六大行", "国有大行-T1"),
    ("中国建设银行", "国有六大行", "国有大行-T1"),
    ("交通银行", "国有六大行", "国有大行-T1"),
    ("中国邮政储蓄银行", "国有六大行", "国有大行-T1"),
    ("招商银行", "股份制银行", "股份行-T0"),
    ("浦发银行", "股份制银行", "股份行-T1"),
    ("中信银行", "股份制银行", "股份行-T1"),
    ("兴业银行", "股份制银行", "股份行-T1"),
    ("中国光大银行", "股份制银行", "股份行-T1"),
    ("中国民生银行", "股份制银行", "股份行-T1"),
    ("平安银行", "股份制银行", "股份行-T1"),
    ("广发银行", "股份制银行", "股份行-T2"),
    ("华夏银行", "股份制银行", "股份行-T2"),
    ("浙商银行", "股份制银行", "股份行-T2"),
    ("恒丰银行", "股份制银行", "股份行-T2"),
    ("渤海银行", "股份制银行", "股份行-T2"),
    ("北京银行", "城商行", "城商行-T0"),
    ("上海银行", "城商行", "城商行-T0"),
    ("江苏银行", "城商行", "城商行-T0"),
    ("南京银行", "城商行", "城商行-T0"),
    ("宁波银行", "城商行", "城商行-T0"),
    ("杭州银行", "城商行", "城商行-T0"),
    ("徽商银行", "城商行", "城商行-T1"),
    ("成都银行", "城商行", "城商行-T1"),
    ("重庆银行", "城商行", "城商行-T1"),
    ("长沙银行", "城商行", "城商行-T1"),
    ("广州银行", "城商行", "城商行-T1"),
    ("深圳农村商业银行", "农商行", "农商行-T0"),
    ("上海农商银行", "农商行", "农商行-T0"),
    ("北京农商银行", "农商行", "农商行-T0"),
    ("广州农商银行", "农商行", "农商行-T1"),
    ("重庆农村商业银行", "农商行", "农商行-T1"),
    ("东莞银行", "城商行", "城商行-T1"),
    ("苏州银行", "城商行", "城商行-T1"),
    ("厦门银行", "城商行", "城商行-T1"),
    ("齐鲁银行", "城商行", "城商行-T1"),
    ("青岛银行", "城商行", "城商行-T1"),
    ("郑州银行", "城商行", "城商行-T2"),
    ("西安银行", "城商行", "城商行-T2"),
    ("贵阳银行", "城商行", "城商行-T2"),
    ("贵州银行", "城商行", "城商行-T2"),
    ("兰州银行", "城商行", "城商行-T2"),
    ("甘肃银行", "城商行", "城商行-T2"),
    ("晋商银行", "城商行", "城商行-T2"),
    ("河北银行", "城商行", "城商行-T2"),
    ("天津银行", "城商行", "城商行-T2"),
    ("大连银行", "城商行", "城商行-T2"),
    ("盛京银行", "城商行", "城商行-T2"),
    ("哈尔滨银行", "城商行", "城商行-T2"),
    ("吉林银行", "城商行", "城商行-T2"),
    ("中原银行", "城商行", "城商行-T2"),
    ("汉口银行", "城商行", "城商行-T2"),
    ("湖北银行", "城商行", "城商行-T2"),
    ("江西银行", "城商行", "城商行-T2"),
    ("九江银行", "城商行", "城商行-T2"),
    ("福建海峡银行", "城商行", "城商行-T2"),
    ("桂林银行", "城商行", "城商行-T2"),
    ("广西北部湾银行", "城商行", "城商行-T2"),
    ("云南红塔银行", "城商行", "城商行-T2"),
    ("昆仑银行", "城商行", "城商行-T2"),
    ("青海银行", "城商行", "城商行-T2"),
    ("宁夏银行", "城商行", "城商行-T2"),
    ("内蒙古银行", "城商行", "城商行-T2"),
    ("厦门国际银行", "城商行", "城商行-T1"),
]

BANK_TIER_BY_NAME = {bank_name: tier for bank_name, _, tier in BANK_UNIVERSE}


def tier_rank(row):
    text = f"{canonical_tier(row)} {row.get('银行类型', '')}"
    for key, rank in TIER_RANK.items():
        if key in text:
            return rank
    return 99


def canonical_tier(row):
    bank_name = str(row.get("银行名称", ""))
    bank_type = str(row.get("银行类型", ""))
    tier = str(row.get("同类梯队", ""))
    if "-" in tier:
        return tier
    if bank_name in BANK_TIER_BY_NAME:
        return BANK_TIER_BY_NAME[bank_name]
    if bank_type == "政策性银行":
        return "政策性-T1"
    if bank_type == "国有六大行":
        return "国有大行-T1"
    if bank_type == "股份制银行":
        return "股份行-T1"
    if bank_type == "城商行":
        return "城商行-T1"
    if bank_type == "农商行":
        return "农商行-T1"
    return tier


def priority_rank(row):
    value = str(row.get("投递优先级", ""))
    for key, rank in PRIORITY_RANK.items():
        if key in value:
            return rank
    return 8


def markdown_cell(value):
    text = "" if value in (None, "") else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def normalize_row(row):
    normalized = {column: markdown_cell(row.get(column)) for column in COLUMNS}
    normalized["同类梯队"] = markdown_cell(canonical_tier(row))
    return normalized


def default_priority(bank_type):
    if bank_type == "国有六大行":
        return "P0主攻"
    if bank_type in ("股份制银行", "城商行", "农商行"):
        return "P1重点"
    return "P2冲刺"


def build_comprehensive_template():
    rows = []
    for bank_name, bank_type, tier in BANK_UNIVERSE:
        rows.append(
            {
                "银行名称": bank_name,
                "总行/分行": "待用户确认",
                "推荐岗位方向": "综合",
                "银行类型": bank_type,
                "同类梯队": tier,
                "投递优先级": default_priority(bank_type),
                "投递批次": "校园招聘",
                "开始时间": "",
                "截止时间": "",
                "投递日期": "",
                "官方招聘网站": "",
                "网申入口": "",
                "公告链接": "",
                "简历版本": "银行通用版",
                "投递状态": "待用户确认",
                "笔试": "待通知",
                "一面": "待通知",
                "二面": "待通知",
                "三面/终面": "待通知",
                "推荐理由": "待结合用户背景判断",
                "主要风险": "开放批次、岗位、城市和截止日待用户确认",
                "下一动作": "回到官方来源确认开放状态、岗位和截止时间",
                "提醒日期": "",
                "提醒状态": "待提醒",
                "备注1": "全面机会池骨架，需回到官方来源确认",
                "备注2": "未确认开放状态，不代表当年岗位已开放",
            }
        )
    return rows


def render_table(rows):
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            priority_rank(row),
            tier_rank(row),
            row.get("银行名称", ""),
        ),
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
