# Hệ thống Quản lý Nhà hàng Gọi món

## Giới thiệu
Ứng dụng hỗ trợ quản lý gọi món tại nhà hàng, giúp phục vụ, bếp và thu ngân làm việc hiệu quả hơn.

## Chức năng chính

### 1. Nhận đơn tại bàn
- Nhân viên phục vụ ghi nhận món khách gọi  
- Mỗi bàn chỉ có 1 phiếu tại một thời điểm  
- Không ghi trùng món, tự động cộng dồn số lượng  

### 2. Bếp nhận và chế biến
- Đơn hàng được chuyển xuống bếp theo thời gian thực  
- Bếp chỉ thấy các món chưa hoàn tất  
- Cập nhật trạng thái món (đang nấu, hoàn thành)  
- Thông báo lại cho phục vụ khi hoàn tất  

### 3. Thanh toán hóa đơn
- Tổng hợp món ăn và tính tiền  
- Tính VAT 10%  
- Giảm giá 5% nếu hóa đơn > 500.000 VND  

## Công nghệ sử dụng
- Backend: Python Flask  
- Cơ sở dữ liệu: MySQL  

## Mục tiêu
Xây dựng hệ thống đơn giản giúp quản lý quy trình gọi món, chế biến và thanh toán trong nhà hàng.
