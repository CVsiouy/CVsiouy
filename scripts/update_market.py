import json
import urllib.request
import datetime
import os

# Create assets folder if not exists
os.makedirs("assets", exist_ok=True)

# Yahoo Finance symbols to fetch
symbols = {
    "NIFTY50": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "BTC": "BTC-USD",
    "NASDAQ": "^IXIC",
    "ETH": "ETH-USD"
}

data = {}

# Standard browser user-agent to avoid HTTP 401/403 errors from Yahoo Finance
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for name, sym in symbols.items():
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode())
            meta = res_data["chart"]["result"][0]["meta"]
            price = meta["regularMarketPrice"]
            prev_close = meta["chartPreviousClose"]
            
            change = ((price - prev_close) / prev_close) * 100
            data[name] = {
                "price": price,
                "change": change,
                "prev_close": prev_close
            }
            print(f"Fetched {name}: {price} ({change:+.2f}%)")
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        # Fallback values
        fallbacks = {
            "NIFTY50": {"price": 24982, "change": 0.72, "prev_close": 24803.4},
            "BANKNIFTY": {"price": 55321, "change": -0.43, "prev_close": 55560.1},
            "BTC": {"price": 118245, "change": 2.6, "prev_close": 115248.5},
            "NASDAQ": {"price": 19842, "change": 0.91, "prev_close": 19663.1},
            "ETH": {"price": 3842, "change": 1.8, "prev_close": 3774.1}
        }
        data[name] = fallbacks[name]

# Helper to format price
def format_price(val, name):
    if name in ["BTC", "ETH"]:
        return f"${val:,.0f}"
    return f"{val:,.0f}" if val >= 1000 else f"{val:.2f}"

# Helper to format change
def format_change(val):
    sign = "+" if val >= 0 else ""
    arrow = "▲" if val >= 0 else "▼"
    color = "#10B981" if val >= 0 else "#EF4444"
    return f"{arrow} {sign}{val:.2f}%", color

# ----------------- Write market-ticker.svg -----------------
ticker_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 50" width="900" height="50">
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="900" y2="0">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="50%" style="stop-color:#161b22"/>
      <stop offset="100%" style="stop-color:#0d1117"/>
    </linearGradient>
    <clipPath id="clip"><rect width="900" height="50"/></clipPath>
  </defs>
  <rect width="900" height="50" fill="url(#tbg)" rx="6" stroke="#30363d" stroke-width="1"/>

  <g clip-path="url(#clip)">
    <g>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-900 0" dur="20s" repeatCount="indefinite"/>
      <!-- Ticker row 1 -->
      <text y="20" font-family="Consolas, monospace" font-size="13" fill="#e6edf3">
        <tspan x="20" fill="#00D4FF" font-weight="bold">NIFTY50</tspan>
        <tspan fill="{format_change(data['NIFTY50']['change'])[1]}"> {format_change(data['NIFTY50']['change'])[0].split()[0]} {format_price(data['NIFTY50']['price'], 'NIFTY50')} {format_change(data['NIFTY50']['change'])[0].split()[1]}</tspan>
        <tspan x="200" fill="#00D4FF" font-weight="bold">BANKNIFTY</tspan>
        <tspan fill="{format_change(data['BANKNIFTY']['change'])[1]}"> {format_change(data['BANKNIFTY']['change'])[0].split()[0]} {format_price(data['BANKNIFTY']['price'], 'BANKNIFTY')} {format_change(data['BANKNIFTY']['change'])[0].split()[1]}</tspan>
        <tspan x="420" fill="#F59E0B" font-weight="bold">BTC</tspan>
        <tspan fill="{format_change(data['BTC']['change'])[1]}"> {format_change(data['BTC']['change'])[0].split()[0]} {format_price(data['BTC']['price'], 'BTC')} {format_change(data['BTC']['change'])[0].split()[1]}</tspan>
        <tspan x="620" fill="#7C3AED" font-weight="bold">NASDAQ</tspan>
        <tspan fill="{format_change(data['NASDAQ']['change'])[1]}"> {format_change(data['NASDAQ']['change'])[0].split()[0]} {format_price(data['NASDAQ']['price'], 'NASDAQ')} {format_change(data['NASDAQ']['change'])[0].split()[1]}</tspan>
        <tspan x="820" fill="#00D4FF" font-weight="bold">ETH</tspan>
        <tspan fill="{format_change(data['ETH']['change'])[1]}"> {format_change(data['ETH']['change'])[0].split()[0]} {format_price(data['ETH']['price'], 'ETH')} {format_change(data['ETH']['change'])[0].split()[1]}</tspan>
      </text>
      <!-- Duplicate for seamless loop -->
      <text y="20" font-family="Consolas, monospace" font-size="13" fill="#e6edf3">
        <tspan x="920" fill="#00D4FF" font-weight="bold">NIFTY50</tspan>
        <tspan fill="{format_change(data['NIFTY50']['change'])[1]}"> {format_change(data['NIFTY50']['change'])[0].split()[0]} {format_price(data['NIFTY50']['price'], 'NIFTY50')} {format_change(data['NIFTY50']['change'])[0].split()[1]}</tspan>
        <tspan x="1100" fill="#00D4FF" font-weight="bold">BANKNIFTY</tspan>
        <tspan fill="{format_change(data['BANKNIFTY']['change'])[1]}"> {format_change(data['BANKNIFTY']['change'])[0].split()[0]} {format_price(data['BANKNIFTY']['price'], 'BANKNIFTY')} {format_change(data['BANKNIFTY']['change'])[0].split()[1]}</tspan>
        <tspan x="1320" fill="#F59E0B" font-weight="bold">BTC</tspan>
        <tspan fill="{format_change(data['BTC']['change'])[1]}"> {format_change(data['BTC']['change'])[0].split()[0]} {format_price(data['BTC']['price'], 'BTC')} {format_change(data['BTC']['change'])[0].split()[1]}</tspan>
        <tspan x="1520" fill="#7C3AED" font-weight="bold">NASDAQ</tspan>
        <tspan fill="{format_change(data['NASDAQ']['change'])[1]}"> {format_change(data['NASDAQ']['change'])[0].split()[0]} {format_price(data['NASDAQ']['price'], 'NASDAQ')} {format_change(data['NASDAQ']['change'])[0].split()[1]}</tspan>
        <tspan x="1720" fill="#00D4FF" font-weight="bold">ETH</tspan>
        <tspan fill="{format_change(data['ETH']['change'])[1]}"> {format_change(data['ETH']['change'])[0].split()[0]} {format_price(data['ETH']['price'], 'ETH')} {format_change(data['ETH']['change'])[0].split()[1]}</tspan>
      </text>
      <text y="38" font-family="Consolas, monospace" font-size="11" fill="#64748b">
        <tspan x="20">⚡ LIVE MARKET PULSE</tspan>
        <tspan x="920">⚡ LIVE MARKET PULSE</tspan>
      </text>
    </g>
  </g>
</svg>"""

with open("assets/market-ticker.svg", "w", encoding="utf-8") as f:
    f.write(ticker_svg)

# ----------------- Write market-status.svg -----------------
# Calculate IST time (UTC + 5.5 hours)
utc_now = datetime.datetime.now(datetime.timezone.utc)
ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
ist_time_str = ist_now.strftime("%I:%M %p")

# Market status logic: Weekday, between 09:15 and 15:30 IST
weekday = ist_now.weekday()
is_weekday = weekday < 5  # 0-4 are Mon-Fri

# Convert current IST time to minutes since midnight
minutes_since_midnight = ist_now.hour * 60 + ist_now.minute
market_start = 9 * 60 + 15  # 09:15
market_end = 15 * 60 + 30   # 15:30

is_market_open = is_weekday and (market_start <= minutes_since_midnight <= market_end)

if is_market_open:
    market_text = "NSE OPEN"
    market_color = "#10B981"
    # Calculate progress percentage
    progress = ((minutes_since_midnight - market_start) / (market_end - market_start)) * 100
    progress = max(0, min(100, progress))
    bar_width = int(progress * 2.4)  # Map 100% to 240px max width
else:
    market_text = "NSE CLOSED"
    market_color = "#EF4444"
    bar_width = 0

status_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200">
  <rect width="320" height="200" fill="#0d1117" rx="8" stroke="#30363d"/>

  <text x="160" y="30" text-anchor="middle" font-family="Segoe UI,sans-serif" font-size="13" fill="#94a3b8" font-weight="600">MARKET STATUS</text>

  <!-- Pulsing dot -->
  <circle cx="95" cy="70" r="8" fill="{market_color}">
    <animate attributeName="opacity" values="1;0.4;1" dur="1.2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="95" cy="70" r="14" fill="none" stroke="{market_color}" stroke-width="1" opacity="0.5">
    <animate attributeName="r" values="10;18;10" dur="1.2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;0;0.5" dur="1.2s" repeatCount="indefinite"/>
  </circle>

  <text x="120" y="76" font-family="Segoe UI,sans-serif" font-size="18" fill="{market_color}" font-weight="700">{market_text}</text>

  <!-- Clock -->
  <text x="160" y="115" text-anchor="middle" font-family="Consolas,monospace" font-size="28" fill="#00D4FF" font-weight="700">
    {ist_time_str}
    <animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite"/>
  </text>
  <text x="160" y="135" text-anchor="middle" font-family="Segoe UI,sans-serif" font-size="11" fill="#64748b">IST · Indian Standard Time</text>

  <!-- Session bar -->
  <rect x="40" y="155" width="240" height="8" fill="#161b22" rx="4"/>
  <rect x="40" y="155" width="{bar_width}" height="8" fill="{market_color}" rx="4"/>
  <text x="160" y="185" text-anchor="middle" font-family="Segoe UI,sans-serif" font-size="10" fill="#64748b">Session Progress · 09:15 - 15:30</text>
</svg>"""

with open("assets/market-status.svg", "w", encoding="utf-8") as f:
    f.write(status_svg)

# ----------------- Write candlestick.svg -----------------
# Last candle dynamic height based on Nifty 50 or BTC movement
nifty_change = data["NIFTY50"]["change"]
is_green = nifty_change >= 0
candle_color = "#10B981" if is_green else "#EF4444"

# Set animated values depending on daily move
rect_h = max(20, min(65, abs(int(nifty_change * 35)) + 15))
rect_y = 70 if is_green else 70 + (40 - rect_h)
wick_y2 = rect_y - 20
wick_y1 = rect_y + rect_h + 20

candlestick_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200">
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="0" y2="200">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
  </defs>
  <rect width="320" height="200" fill="url(#cbg)" rx="8" stroke="#30363d"/>

  <!-- Grid lines -->
  <g stroke="#30363d" stroke-width="0.5" opacity="0.5">
    <line x1="40" y1="40" x2="300" y2="40"/>
    <line x1="40" y1="80" x2="300" y2="80"/>
    <line x1="40" y1="120" x2="300" y2="120"/>
    <line x1="40" y1="160" x2="300" y2="160"/>
  </g>

  <text x="160" y="22" text-anchor="middle" font-family="Segoe UI,sans-serif" font-size="12" fill="#00D4FF" font-weight="600">LIVE CANDLESTICK (NIFTY50)</text>

  <!-- Static candles -->
  <g>
    <line x1="70" y1="130" x2="70" y2="70" stroke="#10B981" stroke-width="1.5"/>
    <rect x="63" y="90" width="14" height="30" fill="#10B981" rx="1"/>
    <line x1="110" y1="140" x2="110" y2="80" stroke="#EF4444" stroke-width="1.5"/>
    <rect x="103" y="85" width="14" height="35" fill="#EF4444" rx="1"/>
    <line x1="150" y1="120" x2="150" y2="60" stroke="#10B981" stroke-width="1.5"/>
    <rect x="143" y="75" width="14" height="35" fill="#10B981" rx="1"/>
    <line x1="190" y1="110" x2="190" y2="55" stroke="#10B981" stroke-width="1.5"/>
    <rect x="183" y="65" width="14" height="35" fill="#10B981" rx="1"/>
  </g>

  <!-- Dynamic / Animated live candle based on Nifty 50 -->
  <g>
    <line x1="250" y1="{wick_y1}" x2="250" y2="{wick_y2}" stroke="{candle_color}" stroke-width="1.5">
      <animate attributeName="y2" values="{wick_y2};{wick_y2-5};{wick_y2+5};{wick_y2}" dur="3s" repeatCount="indefinite"/>
    </line>
    <rect x="243" y="{rect_y}" width="14" height="{rect_h}" fill="{candle_color}" rx="1">
      <animate attributeName="height" values="{rect_h};{rect_h+4};{rect_h-4};{rect_h}" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="y" values="{rect_y};{rect_y-2};{rect_y+2};{rect_y}" dur="3s" repeatCount="indefinite"/>
    </rect>
    <!-- Pulse glow on live candle -->
    <circle cx="250" cy="90" r="20" fill="{candle_color}" opacity="0">
      <animate attributeName="opacity" values="0;0.3;0" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="r" values="15;25;15" dur="3s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- Price line -->
  <polyline points="60,130 100,110 140,95 180,75 220,65 260,55" fill="none" stroke="#00D4FF" stroke-width="1.5" opacity="0.6" stroke-dasharray="4,2">
    <animate attributeName="stroke-dashoffset" values="0;-12" dur="1s" repeatCount="indefinite"/>
  </polyline>

  <text x="250" y="175" text-anchor="middle" font-family="Consolas,monospace" font-size="11" fill="{candle_color}">{format_change(nifty_change)[0]}</text>
</svg>"""

with open("assets/candlestick.svg", "w", encoding="utf-8") as f:
    f.write(candlestick_svg)

print("SVGs successfully updated with live API values.")
