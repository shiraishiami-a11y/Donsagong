import ephem
from datetime import datetime, timezone, timedelta

# KST
KST = timezone(timedelta(hours=9))

# 立春の計算テスト
sun = ephem.Sun()
observer = ephem.Observer()
observer.long = '127.0'
observer.lat = '37.5'

# 2024年の立春を探す（2月4日頃のはず）
test_date = ephem.Date('2024/2/4')
observer.date = test_date
sun.compute(observer)

print(f"2024/2/4の太陽黄経: {float(sun.hlon) * 180 / ephem.pi:.1f}度")
print(f"立春は太陽黄経315度")

# 2024年の立秋を探す（8月7日頃のはず）  
test_date2 = ephem.Date('2024/8/7')
observer.date = test_date2
sun.compute(observer)

print(f"2024/8/7の太陽黄経: {float(sun.hlon) * 180 / ephem.pi:.1f}度")
print(f"立秋は太陽黄経135度")
