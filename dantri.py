import requests
from bs4 import BeautifulSoup
import schedule
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_article_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('article a[href]')
    full_links = []
    for link in links:
        href = link.get('href')
        if href and href.startswith('/'):
            full_links.append('https://dantri.com.vn' + href)
        elif href and href.startswith('https://'):
            full_links.append(href)
    return list(set(full_links))

def parse_article(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one('h1.dt-news__title').get_text(strip=True)
        sapo_tag = soup.select_one('h2.dt-news__sapo')
        sapo = sapo_tag.get_text(strip=True) if sapo_tag else ''
        content_blocks = soup.select('div.dt-news__content p')
        content = '\n'.join([p.get_text(strip=True) for p in content_blocks if p.get_text(strip=True)])

        image_tag = soup.select_one('div.dt-news__content img')
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''

        return {
            'url': url,
            'title': title,
            'sapo': sapo,
            'content': content,
            'image': image_url
        }
    except Exception as e:
        print(f"Lỗi xử lý {url}: {e}")
        return None

def save_to_google_sheets(data, sheet_id, json_file):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1

    sheet.clear()
    headers = ["URL", "Tiêu đề", "Sapo", "Nội dung", "Hình ảnh"]
    sheet.append_row(headers)

    for item in data:
        sheet.append_row([item['url'], item['title'], item['sapo'], item['content'], item['image']])

    print("✅ Dữ liệu đã được ghi vào Google Sheets.")

def main():
    print("Bắt đầu thu thập từ dantri.com.vn...")
    url = "https://dantri.com.vn/suc-manh-so.htm"
    links = get_article_links(url)
    print(f"Tìm thấy {len(links)} bài viết.")

    articles = []
    for link in links:
        print(f"Đang xử lý: {link}")
        article = parse_article(link)
        if article:
            articles.append(article)

    if articles:
        sheet_id = "1h-qI9bmvuUyIxe2IkB9zmWcxR1H_pPke6g1ZZNr3A2E"
        json_file = "baomoi-7112004-1174839ef644.json"
        save_to_google_sheets(articles, sheet_id, json_file)
    else:
        print("Không có bài viết nào được lưu.")

schedule.every().day.at("06:00").do(main)

if __name__ == '__main__':
    print(" Chờ đến lịch chạy...")
    while True:
        schedule.run_pending()
        time.sleep(60)
