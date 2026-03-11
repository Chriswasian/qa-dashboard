import csv
import os
import datetime

INPUT_FILE = "test-results.csv"
OUTPUT_FILE = "dashboard.html"

def load_results():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file '{INPUT_FILE}' not found.")
        return []
    with open(INPUT_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def calculate_stats(results):
    total = len(results)
    passed = sum(1 for r in results if r['result'] == 'PASSED')
    failed = total - passed
    rate = (passed / total * 100) if total > 0 else 0
    return total, passed, failed, rate

def generate_html(results, total, passed, failed, rate):
    rows = ""
    for r in results:
        color = "#6ee7b7" if r['result'] == "PASSED" else "#f87171"
        rows += f"""
<tr>
<td>{r['test']}</td>
<td style="color:{color};font-weight:bold">{r['result']}</td>
<td>{r['duration']}</td>
<td>{r['timestamp']}</td>
</tr>"""
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>QA Dashboard</title>
<style>
body {{ font-family: sans-serif; background: #0f1932; color: white; padding: 30px; }}
h1 {{ color: #c084fc; }}
.stats {{ display: flex; gap: 20px; margin: 20px 0; }}
.card {{ background: #1e2d50; padding: 20px; border-radius: 12px; min-width: 120px; text-align: center; }}
.num {{ font-size: 2em; font-weight: bold; color: #6ee7b7; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
th {{ background: #2d1b69; padding: 10px; text-align: left; }}
td {{ padding: 10px; border-bottom: 1px solid #2d1b69; }}
</style>
</head>
<body>
<h1>Wilsons QA Results Dashboard</h1>
<div class="stats">
<div class="card"><div class="num">{total}</div>Total</div>
<div class="card"><div class="num" style="color:#6ee7b7">{passed}</div>Passed</div>
<div class="card"><div class="num" style="color:#f87171">{failed}</div>Failed</div>
<div class="card"><div class="num" style="color:#fde68a">{rate:.1f}%</div>Pass Rate</div>
</div>
<table>
<tr><th>Test</th><th>Result</th><th>Duration</th><th>Timestamp</th></tr>
{rows}
</table>
</body>
</html>"""

def save_html(html):
    with open(OUTPUT_FILE, mode='w') as file:
        file.write(html)
    print(f"Dashboard saved to '{OUTPUT_FILE}'")

def main():
    results = load_results()
    total, passed, failed, rate = calculate_stats(results)
    html = generate_html(results, total, passed, failed, rate)
    save_html(html)

main()