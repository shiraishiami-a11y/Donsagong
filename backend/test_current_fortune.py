#!/usr/bin/env python3
from datetime import datetime
from zoneinfo import ZoneInfo
from lunar_python import Solar
from app.schemas.saju import FortuneDetail

# 今日の日付を取得
now = datetime.now(ZoneInfo("Asia/Seoul"))
today_str = now.strftime("%Y-%m-%d")
print(f"Today: {today_str}")

# lunar-pythonで今日の八字を計算
solar = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, 0, 0)
lunar = solar.getLunar()
eight_char = lunar.getEightChar()

# 年・月・日の干支を取得
year_stem = eight_char.getYearGan()
year_branch = eight_char.getYearZhi()
print(f"Year: {year_stem}{year_branch}")

# FortuneDetailを構築
year_fortune = FortuneDetail(
    stem=year_stem,
    branch=year_branch,
    fortuneLevel="平",
    description="年運",
)
print(f"Success! {year_fortune}")
