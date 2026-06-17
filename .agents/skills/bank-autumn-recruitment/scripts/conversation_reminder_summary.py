#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


TERMINAL_STATUSES = {"offer", "拒绝", "放弃"}
WAITING_STATUSES = {"待用户确认", "未投"}
PIPELINE_STATUSES = {"已投", "测评", "笔试", "面试", "一面", "二面", "三面/终面", "体检"}


def load_rows(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("rows", [])
    if not isinstance(data, list):
        raise ValueError("input must be a JSON list or an object with a rows list")
    return data


def first_value(row, *keys):
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def parse_date(value):
    text = str(value or "").strip()
    if not text or text in {"待用户确认", "待补充", "待公布", "未投"}:
        return None
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def markdown_cell(value):
    text = "待用户确认" if value in (None, "") else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def row_name(row):
    bank = first_value(row, "银行名称", "公司名称")
    role = first_value(row, "推荐岗位方向", "岗位名称", "投递类别")
    if role.startswith("["):
        try:
            role = "、".join(json.loads(role))
        except json.JSONDecodeError:
            pass
    return f"{bank} {role}".strip()


def source_link(row):
    return first_value(row, "网申入口", "公告链接", "官方招聘网站", "url")


def render_table(headers, rows):
    if not rows:
        return "暂无。"
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(cell) for cell in row) + " |")
    return "\n".join(lines)


def deadline_summary(rows, today):
    reminders = []
    for row in rows:
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        deadline = parse_date(first_value(row, "截止时间", "截止日期", "网申截止日"))
        if status in TERMINAL_STATUSES or not deadline:
            continue
        days_left = (deadline - today).days
        if 0 <= days_left <= 7:
            reminders.append(
                [
                    row_name(row),
                    first_value(row, "投递优先级", "优先级", "匹配等级"),
                    status,
                    deadline.isoformat(),
                    f"{days_left} 天",
                    first_value(row, "下一动作") or "确认是否投递或进入下一步准备",
                ]
            )
    return reminders


def application_coaching_summary(rows):
    items = []
    for row in rows:
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        if status in TERMINAL_STATUSES or status not in WAITING_STATUSES or not source_link(row):
            continue
        items.append(
            [
                row_name(row),
                first_value(row, "投递优先级", "优先级", "匹配等级"),
                first_value(row, "简历版本") or "待确认",
                first_value(row, "主要风险") or "岗位条线、城市、轮岗和营销属性待确认",
                first_value(row, "下一动作") or "打开公告或网申入口，确认岗位后再投递",
                source_link(row),
            ]
        )
    return items


def pipeline_scan_summary(rows):
    items = []
    for row in rows:
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        if status not in PIPELINE_STATUSES:
            continue
        items.append(
            [
                row_name(row),
                first_value(row, "投递优先级", "优先级", "匹配等级"),
                status,
                first_value(row, "笔试", "一面", "二面", "三面/终面") or "待补充流程节点",
                "查邮箱/短信/站内信；再看牛客、小红书等同批次线索",
            ]
        )
    return items


def waiting_confirmation_summary(rows):
    items = []
    for row in rows:
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        if status in TERMINAL_STATUSES:
            continue
        deadline = parse_date(first_value(row, "截止时间", "截止日期", "网申截止日"))
        link = source_link(row)
        if not deadline or not link:
            items.append(
                [
                    row_name(row),
                    first_value(row, "投递优先级", "优先级", "匹配等级"),
                    "截止时间或官方链接待确认",
                    first_value(row, "下一动作") or "核验官方公告、截止时间和网申入口",
                ]
            )
    return items


def weekly_summary(rows):
    counts = {
        "待确认": 0,
        "未投": 0,
        "已投": 0,
        "流程中": 0,
        "offer/拒绝/放弃": 0,
    }
    for row in rows:
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        if status == "待用户确认":
            counts["待确认"] += 1
        elif status == "未投":
            counts["未投"] += 1
        elif status == "已投":
            counts["已投"] += 1
        elif status in PIPELINE_STATUSES:
            counts["流程中"] += 1
        elif status in TERMINAL_STATUSES:
            counts["offer/拒绝/放弃"] += 1

    rows_for_table = [[name, count, "按当前表状态统计"] for name, count in counts.items()]
    return rows_for_table


def build_summary(rows, today):
    deadline_rows = deadline_summary(rows, today)
    application_rows = application_coaching_summary(rows)
    pipeline_rows = pipeline_scan_summary(rows)
    confirmation_rows = waiting_confirmation_summary(rows)
    review_rows = weekly_summary(rows)

    sections = [
        "# 银行秋招对话内提醒摘要",
        "",
        f"运行日期: {today.isoformat()}",
        "说明: 本摘要只读投递表并生成对话内提醒，不写入 Notion，不发送邮件，不替用户投递。",
        "",
        "## 1. 截止日提醒",
        render_table(["机会", "优先级", "状态", "截止时间", "剩余", "下一动作"], deadline_rows),
        "",
        "## 2. 网申陪跑",
        render_table(["机会", "优先级", "简历版本", "主要风险", "今日动作", "来源"], application_rows),
        "",
        "## 3. 流程线索巡检",
        "弱线索只提示查邮箱/短信/站内信，不判断个人结果。",
        render_table(["机会", "优先级", "状态", "当前节点", "建议动作"], pipeline_rows),
        "",
        "## 4. 周复盘",
        render_table(["指标", "数量", "判断"], review_rows),
        "",
        "下周优先处理 P0/P1 临近截止和流程中岗位。",
        "",
        "## 待用户确认",
        render_table(["机会", "优先级", "待确认项", "下一动作"], confirmation_rows),
    ]
    return "\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate a conversation-friendly bank recruitment reminder summary.")
    parser.add_argument("--input", required=True, help="Path to JSON rows exported from the tracker.")
    parser.add_argument("--today", required=True, help="Current date in YYYY-MM-DD.")
    parser.add_argument("--output", required=True, help="Path to write Markdown summary.")
    args = parser.parse_args()

    rows = load_rows(args.input)
    today = datetime.strptime(args.today, "%Y-%m-%d").date()
    Path(args.output).write_text(build_summary(rows, today), encoding="utf-8")


if __name__ == "__main__":
    main()
