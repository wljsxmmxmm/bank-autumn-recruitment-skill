#!/usr/bin/env python3
import argparse
import json
from datetime import date, datetime
from pathlib import Path


ACTIVE_STATUSES = {"待用户确认", "未投", "已投", "测评", "笔试", "面试", "一面", "二面", "三面/终面", "体检"}
TERMINAL_STATUSES = {"offer", "拒绝", "放弃"}
EMAIL_STATUSES = {"待用户确认", "未投"}


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
    role = first_value(row, "岗位名称", "推荐岗位方向", "投递类别")
    return f"{bank} {role}".strip()


def render_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(cell) for cell in row) + " |")
    return "\n".join(lines)


def build_report(rows, today):
    deadline_rows = []
    today_rows = []
    email_rows = []
    confirmation_rows = []

    for row in rows:
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        priority = first_value(row, "投递优先级", "优先级", "匹配等级")
        action = first_value(row, "下一动作") or "核验公告和截止时间"
        deadline = parse_date(first_value(row, "截止时间", "网申截止日", "截止日期"))
        reminder = parse_date(first_value(row, "提醒日期", "下次跟进日"))
        link = first_value(row, "网申入口", "投递链接", "来源链接", "公告链接", "官方招聘网站")
        name = row_name(row)

        if status not in TERMINAL_STATUSES and deadline:
            days_left = (deadline - today).days
            if days_left <= 7:
                deadline_rows.append([name, priority, status, deadline.isoformat(), f"{days_left} 天", action])
            if days_left <= 1:
                today_rows.append([name, priority, status, "截止临近", action])
            if status in EMAIL_STATUSES and link and days_left <= 3:
                email_rows.append([name, priority, "截止临近", link, "dry-run: 未发送"])
        elif status in {"待用户确认", "未投"}:
            confirmation_rows.append([name, priority, "截止时间或链接待用户确认", action])

        if status not in TERMINAL_STATUSES and reminder and reminder <= today:
            today_rows.append([name, priority, status, "到达提醒日期", action])

    sections = ["# 银行秋招自动化 dry-run 摘要", ""]
    sections.append(f"运行日期: {today.isoformat()}")
    sections.append("说明: dry-run 只生成提醒清单，不发送邮件，不写入 Notion 或在线表格。")

    sections.extend(["", "## 今日处理"])
    sections.append(render_table(["机会", "优先级", "状态", "原因", "下一动作"], today_rows) if today_rows else "暂无。")

    sections.extend(["", "## 截止提醒"])
    sections.append(render_table(["机会", "优先级", "状态", "截止时间", "剩余", "下一动作"], deadline_rows) if deadline_rows else "暂无。")

    sections.extend(["", "## 邮件待发送"])
    sections.append(render_table(["机会", "优先级", "提醒原因", "来源", "发送状态"], email_rows) if email_rows else "暂无。")

    sections.extend(["", "## 待用户确认"])
    sections.append(render_table(["机会", "优先级", "待确认项", "下一动作"], confirmation_rows) if confirmation_rows else "暂无。")

    return "\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Dry-run bank recruitment reminders without external writes.")
    parser.add_argument("--input", required=True, help="Path to JSON rows.")
    parser.add_argument("--today", required=True, help="Current date in YYYY-MM-DD.")
    parser.add_argument("--output", required=True, help="Path to write Markdown report.")
    args = parser.parse_args()

    rows = load_rows(args.input)
    today = datetime.strptime(args.today, "%Y-%m-%d").date()
    report = build_report(rows, today)
    Path(args.output).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
