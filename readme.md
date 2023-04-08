# Demo Ứng Dụng Bờ Lốc Chen 🪙🪙

Code các thuật toán rất phức tạp, nên mong mọi người đọc kỹ hướng dẫn dưới đây trước khi làm để quá trình code dễ dàng hơn.
## Quy ước lập trình 😎
- Tên biến, tên hàm, tên phương thức dùng camelCase.
- Tên class, tên struct dùng PascalCase.
- Tên file của class dùng PascalCase.

## Quản lý mã nguồn 🗃️
- Cú pháp tiêu đề của commit:
	- Chức năng nhỏ: `feat (scope): <tên chức năng nhỏ>`, với scope là tên class hoặc tên file.
	- Sửa lỗi: `fix (scope): <tên lỗi>`.
	- Linh tinh : `misc (scope): <tên thay đổi>`.
- Bên dưới tiêu đề có thể có mô tả chi tiết về commit, mỗi ý là một gạch đầu dòng.
- Push lên branch riêng, sau đó tạo pull request.
- Cú pháp đặt tên branch `<tên developer>/<tên chức năng chính>`.

## Tuần 1
- Cài đặt thuật toán SHA256: có thể tùy ý thiết kế lớp, phương thức, ... Mục đích của chúng ta là xây dựng phương thức `string SHA256::hash (string)` để hash một chuỗi bất kỳ.
- Tài liệu tham khảo:
	- https://blog.boot.dev/cryptography/how-sha-2-works-step-by-step-sha-256/
	- Mọi người có thể tìm thêm nếu thích 😉.
- Các phần cần code:
	1. Padding thông điệp thành các khối 512 bit.
	2. Các vòng lặp biến đổi.
- Code trong file `SHA256.h`, `SHA256.cpp` và `main.cpp`. Các file khác không cần quan tâm.
