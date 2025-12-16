import pandas as pd

# Dữ liệu kế hoạch Hardcore Agile (15 Sprints)
data = [
    ["Sprint 1", "Week 1-2", "1. Foundation", "Architecture", "DevOps", "Setup Monorepo & Infra", "Cấu trúc thư mục backend/frontend riêng. Setup Docker Compose (Mongo, Redis). Setup ESLint, Prettier, Husky.", "Repo chuẩn, chạy được docker-compose up."],
    ["Sprint 1", "Week 1-2", "1. Foundation", "Auth", "Backend", "Auth API Core", "Login/Register/Refresh Token. Dùng JWT + HttpOnly Cookie. Mailer Service (BullMQ) gửi email xác thực.", "API bảo mật, không lưu token ở LocalStorage."],
    ["Sprint 1", "Week 1-2", "1. Foundation", "Auth", "Frontend", "Auth UI & Guard", "UI Login/Register/Forgot Pass (Reactive Forms). AuthGuard chặn route. Interceptor xử lý lỗi 401 tự refresh token.", "Login mượt, F5 không mất phiên."],
    ["Sprint 1", "Week 1-2", "1. Foundation", "Layout", "Frontend", "Dashboard Layout", "Sidebar (Collapsible), Header, Breadcrumbs. Responsive mobile/desktop.", "Giao diện khung sườn hoàn chỉnh."],
    ["Sprint 2", "Week 3-4", "1. Foundation", "Asset Manager", "Backend", "S3 Integration & Queue", "AWS S3 SDK (Upload/Delete/Presigned URL). Queue BullMQ: Resize ảnh, Lấy duration video (FFmpeg).", "Upload file 500MB ok. Tự sinh thumbnail."],
    ["Sprint 2", "Week 3-4", "1. Foundation", "Asset Manager", "Frontend", "Asset Library UI", "Grid View (Virtual Scroll). Upload Component (Drag & Drop, Progress Bar). Context Menu (Phải chuột).", "UX giống Google Drive. Upload nhiều file."],
    ["Sprint 3", "Week 5-6", "1. Foundation", "Playlist", "Backend", "Playlist Logic Core", "CRUD Playlist. Validate: File tồn tại? Tổng thời lượng? Check quyền Owner. Logic Duplicate Playlist.", "API chặt chẽ, không lỗi data rác."],
    ["Sprint 3", "Week 5-6", "1. Foundation", "Playlist", "Frontend", "Playlist Editor (Advanced)", "Tích hợp Angular CDK Drag-Drop. UI 2 cột (Source -> Target). Tính năng: Sắp xếp, Chỉnh duration, Preview Modal.", "Kéo thả mượt mà, Auto-save."],
    ["Sprint 4", "Week 7-8", "1. Foundation", "Connectivity", "Backend", "Socket Gateway", "Socket.io + Redis Adapter. Quản lý Room theo DeviceID. API Pairing (Mã 6 số, TTL 5 phút).", "Kết nối Realtime ổn định."],
    ["Sprint 4", "Week 7-8", "1. Foundation", "Connectivity", "Frontend", "Screens Management", "List thiết bị (Status Online/Offline realtime). Màn hình nhập Pairing Code.", "Hiển thị đúng trạng thái thiết bị."],
    ["Sprint 4", "Week 7-8", "1. Foundation", "Player", "Player App", "Offline Player Engine", "Web App. Logic tải Playlist & Media về IndexedDB. Loop Logic: Tự chuyển bài, Preload item tiếp theo.", "Rút dây mạng vẫn phát bình thường."],
    ["Sprint 5", "Week 9-10", "2. Stability", "Scheduling", "Backend", "Smart Schedule Engine", "DB Schema (Priority, Recurring). Thuật toán Conflict Detection (Check trùng giờ). Timezone handling.", "Không cho phép tạo lịch trùng nhau."],
    ["Sprint 5", "Week 9-10", "2. Stability", "Scheduling", "Frontend", "Calendar UI", "Tích hợp FullCalendar. Drag Playlist vào lịch. Form Recurring (Lặp T2-T6). Visual Conflict Warning.", "Giao diện lịch trực quan, dễ dùng."],
    ["Sprint 6", "Week 11-12", "2. Stability", "Automation", "Backend", "Ops & Alerts", "API Power Schedule. Alert Service: Cronjob check heartbeat -> Gửi mail nếu Offline > 15p. Command API (Reboot).", "Cảnh báo đúng lúc, không spam."],
    ["Sprint 6", "Week 11-12", "2. Stability", "Automation", "Player", "Player Ops Logic", "Logic check giờ hệ thống -> Show Black Screen (Sleep). Lắng nghe lệnh Reboot/Screenshot từ Socket.", "Player tự động tắt/bật theo lịch."],
    ["Sprint 7", "Week 13-14", "2. Stability", "Support", "Backend", "Ticket & Logging", "API Ticket (CRUD, Upload ảnh). API nhận Log lỗi từ Player. API Dashboard Stats (Storage/Bandwidth).", "Admin nắm được sức khỏe hệ thống."],
    ["Sprint 7", "Week 13-14", "2. Stability", "Support", "Frontend", "Help Center & Dash", "Trang Static Docs. Form gửi Ticket. Dashboard Chart.js (Uptime).", "Giao diện Admin chuyên nghiệp."],
    ["Sprint 8", "Week 15-16", "3. Monetization", "Billing", "Backend", "Stripe Integration", "API Customer, Subscription. Webhook Handler (Payment Success/Fail). Middleware Quota Guard (Check giới hạn gói).", "Tự động khóa/mở tính năng theo gói."],
    ["Sprint 8", "Week 15-16", "3. Monetization", "Billing", "Frontend", "Billing UI", "Pricing Table. Stripe Elements (Form thẻ). Billing Portal (History, Cancel).", "Thanh toán mượt, xử lý lỗi thẻ."],
    ["Sprint 9", "Week 17-18", "3. Monetization", "Store", "Backend", "Hardware Store API", "DB Product, Inventory, Order. API Create Order. Email xác nhận đơn hàng.", "Luồng mua hàng cơ bản hoàn tất."],
    ["Sprint 9", "Week 17-18", "3. Monetization", "Store", "Frontend", "Shop & Invoice", "UI Shop List, Detail, Cart (LocalStorage). Checkout Form. Invoice History (Download PDF).", "Trải nghiệm E-commerce tốt."],
    ["Sprint 10", "Week 19-20", "4. Engage", "Design Studio", "Frontend", "Canvas Editor Core", "Tích hợp Fabric.js. Toolbar: Text, Image, Shape. Layer Panel. Undo/Redo. Group/Ungroup.", "Vẽ được banner cơ bản trên web."],
    ["Sprint 10", "Week 19-20", "4. Engage", "Design Studio", "Backend", "Template System", "API Save/Load JSON Canvas. Server-side Thumbnail Gen (Puppeteer).", "Lưu và xem lại thiết kế."],
    ["Sprint 11", "Week 21-22", "4. Engage", "Interactive", "Frontend", "Kiosk & QR Tools", "UI Config Kiosk URL. Tool tạo QR Code. Overlay Editor (Đặt QR lên video).", "Tạo nội dung tương tác."],
    ["Sprint 11", "Week 21-22", "4. Engage", "Interactive", "Player", "Kiosk Runtime", "Iframe Sandbox. Auto-home timer. Mobile Control: Scan QR -> Socket -> Điều khiển Player.", "Player thành Kiosk cảm ứng."],
    ["Sprint 12", "Week 23-24", "5. Enterprise", "Security", "Backend", "RBAC & Audit", "Refactor Auth (Roles: Owner/Admin/Viewer). Audit Log Middleware (Ghi lại mọi thao tác). SSO (Google/SAML).", "Bảo mật cấp doanh nghiệp."],
    ["Sprint 12", "Week 23-24", "5. Enterprise", "Security", "Frontend", "Team & Audit UI", "UI Mời thành viên, Phân quyền. UI Xem nhật ký hoạt động (Filter/Search). SSO Button.", "Quản lý đội nhóm hiệu quả."],
    ["Sprint 13", "Week 25-26", "5. Enterprise", "Reports", "Backend", "Proof-of-Play & WhiteLabel", "Aggregation Pipeline log phát (TimeSeries). Export CSV Service. API Config Tenant (Logo/Color).", "Báo cáo dữ liệu lớn."],
    ["Sprint 13", "Week 25-26", "5. Enterprise", "Reports", "Frontend", "Report UI & Theme", "Chart thống kê lượt phát. Dynamic Theme Loader (Load màu/logo theo config).", "App thay đổi giao diện theo Brand."],
    ["Sprint 14", "Week 27-28", "6. Launch", "Native Build", "Mobile", "Android/TV Build", "Dùng Capacitor build APK. Config Android Manifest (Boot on start). Tối ưu Memory.", "App chạy trên TV Box thật."],
    ["Sprint 15", "Week 29-30", "6. Launch", "Final Prep", "DevOps", "Production Setup", "Setup AWS EC2, Load Balancer, SSL, Domain. Pentest (SQLi/XSS). Code trang Legal (Terms/Privacy).", "Sẵn sàng Go Live bán hàng."]
]

# Tạo DataFrame
columns = ["Sprint", "Tuần", "Giai đoạn", "Phân hệ", "Loại việc", "Công việc chính", "Yêu cầu kỹ thuật (Hardcore)", "Kết quả mong đợi"]
df = pd.DataFrame(data, columns=columns)

# Xuất ra Excel
file_name = "SCIO_Master_Plan.xlsx"
df.to_excel(file_name, index=False)

print(f"✅ Đã xuất file thành công: {file_name}")
print("Hãy mở file này lên để bắt đầu chạy Sprint 1!")