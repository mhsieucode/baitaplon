Bước 1: Tạo repo
    
    Vào github
    Bấm "new repository"

Bước 2: Khởi tạo git

    Mở terminal tại thư mục chứa file dantri.py:
    git init
    git add .   
    git commit -m "Initial commit"

Bước 3: Kết nối repo
    git remote add origin https://github.com/mhsieucode/baitaplon1.git
    git branch -M main
    git push -u origin main

Bước 4: Cài đặt thư viện cần thiết:
    pip install -r requirements.txt

Bước 5: Chạy chương trình thủ công:
    python dantri.py

Bước 6: Lịch chạy tự động:

    Chương trình sẽ tự động chạy vào lúc 06:00 hàng ngày theo lịch đã thiết lập trong code (schedule.every().day.at("06:00")).



