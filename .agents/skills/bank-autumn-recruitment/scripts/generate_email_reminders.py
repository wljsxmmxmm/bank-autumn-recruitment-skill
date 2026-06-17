#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


SENDABLE_STATUSES = {"待用户确认", "未投"}
TERMINAL_STATUSES = {"已投", "测评", "笔试", "面试", "一面", "二面", "三面/终面", "体检", "offer", "拒绝", "放弃"}


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


def already_sent_today(row, today):
    last_sent = parse_date(first_value(row, "上次邮件时间", "last_email_at"))
    return last_sent == today


def reminder_link(row):
    return first_value(row, "网申入口", "公告链接", "投递链接", "来源链接", "官方招聘网站", "url")


def classify_row(row, today):
    status = first_value(row, "投递状态", "状态") or "待用户确认"
    if status in TERMINAL_STATUSES or already_sent_today(row, today):
        return None

    deadline = parse_date(first_value(row, "截止时间", "网申截止日", "截止日期"))

    if deadline and status in SENDABLE_STATUSES:
        days_left = (deadline - today).days
        if days_left <= 3 and reminder_link(row):
            return "截止临近"

    return None


def build_draft(rows, today, recipient):
    deadline_rows = []
    update_rows = []

    for row in rows:
        reason = classify_row(row, today)
        if not reason:
            continue

        bank = first_value(row, "银行名称", "公司名称")
        role = first_value(row, "岗位名称", "推荐岗位方向", "投递类别")
        deadline = first_value(row, "截止时间", "网申截止日", "截止日期")
        status = first_value(row, "投递状态", "状态") or "待用户确认"
        action = first_value(row, "下一动作") or "打开官方链接确认并处理"
        link = reminder_link(row)

        if reason == "截止临近":
            deadline_rows.append([bank, role, deadline, status, action, link])

        update_rows.append([bank, role, "待发送", reason, today.isoformat(), "dry-run: 未发送"])

    if not update_rows:
        return "# 银行秋招邮件提醒草稿\n\n暂无需要发送的邮件草稿。\n"

    subject = f"[银行秋招提醒] 临近截止 {len(deadline_rows)} 个"
    sections = [
        "# 银行秋招邮件提醒草稿",
        "",
        f"To: {recipient}",
        f"Subject: {subject}",
        "Send status: dry-run: 未发送",
        "",
        "## 邮件正文",
        "",
        "你好，以下银行秋招机会临近截止，请尽快处理。",
        "",
        "### 临近截止",
        render_table(["银行", "岗位", "截止日期", "状态", "今日动作", "来源"], deadline_rows),
        "",
        "### 建议",
        "- 优先处理 P0/P1 岗位。",
        "- 截止日期或岗位说明待用户确认的岗位，先打开官方链接确认。",
        "- 已投岗位不要重复投递，改为记录反馈和准备笔面试。",
        "",
        "## 回写建议",
        render_table(["银行", "岗位", "邮件提醒状态", "邮件提醒原因", "上次邮件时间", "发送状态"], update_rows),
    ]
    return "\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate bank recruitment email reminder drafts without sending.")
    parser.add_argument("--input", required=True, help="Path to JSON rows.")
    parser.add_argument("--today", required=True, help="Current date in YYYY-MM-DD.")
    parser.add_argument("--recipient", required=True, help="Recipient email address for the draft.")
    parser.add_argument("--output", required=True, help="Path to write Markdown draft.")
    args = parser.parse_args()

    rows = load_rows(args.input)
    today = datetime.strptime(args.today, "%Y-%m-%d").date()
    draft = build_draft(rows, today, args.recipient)
    Path(args.output).write_text(draft, encoding="utf-8")


if __name__ == "__main__":
    main()
