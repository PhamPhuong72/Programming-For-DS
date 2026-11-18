# Order of exploration & Pipeline Mapping

## Why a fixed order

Một kết luận chỉ đáng tin cậy khi được tính trên dữ liệu đã được kiểm toán và làm sạch minh bạch:
1. **Dữ liệu chứa gì và ý nghĩa từng cột là gì?** (cấu trúc & từ điển dữ liệu)
2. **Dữ liệu có những lỗi, giá trị giữ chỗ hay mâu thuẫn nào?** (kiểm toán thô — chỉ đo đạc, không sửa xóa mù quáng)
3. **Quy tắc làm sạch tất định nào được áp dụng và kiểm định sau làm sạch ra sao?** (`step4_clean_v1` trên Kaggle `chuyenhocielts/myanimelist-clean`)
4. **Dữ liệu trả lời các câu hỏi nghiên cứu và bài toán học máy như thế nào?** (phân tích thống kê & mô hình hóa chống rò rỉ)

## Sơ đồ ánh xạ giữa Quy trình 5 Notebook chính và Pipeline Kiểm toán Chi tiết

| Giai đoạn (theo Đề bài PDF & Cấu trúc Repo) | Notebook chính (`notebooks/`) | Pipeline kiểm toán & làm sạch nền tảng (`notebooks/preprocessing_pipeline/`) | Trạng thái |
|---|---|---|---|
| **3.1. Data Collection** | [01_data_collection.ipynb](../notebooks/01_data_collection.ipynb) | Đối chiếu mô tả gốc ở Step 1 | **Hoàn thành** |
| **3.2. Data Exploration & Cleaning** | [02_data_exploration.ipynb](../notebooks/02_data_exploration.ipynb) | Kết tinh từ Step 1 (`01_compare_with_description_run`), Step 2 (`02_column_dictionary_run`), Step 3 (`03_raw_quality_audit_run`), Step 4 (`04_clean_data_run` -> `chuyenhocielts/myanimelist-clean`), Step 5 (`05_validate_cleaned_data`) | **Hoàn thành & Đã kiểm định 80,075,053 dòng sạch** |
| **3.3. Question Formulation** | [03_question_formulation.ipynb](../notebooks/03_question_formulation.ipynb) | Kế hoạch tại [docs/question_plan.md](question_plan.md) | **Hoàn thành (6 câu hỏi: Q1–Q4 Non-ML, Q5–Q6 ML)** |
| **3.4. Data Analysis (Non-ML & ML)** | [04_data_analysis.ipynb](../notebooks/04_data_analysis.ipynb) | Sử dụng module tái sử dụng `src/audit.py`, `src/utils.py`, `src/models.py` | **Hoàn thành** |
| **3.5. Summary & Reflection** | [05_project_summary.ipynb](../notebooks/05_project_summary.ipynb) | Tổng hợp toàn dự án, hạn chế, hướng mở rộng & phản tư 3 thành viên | **Hoàn thành** |

## Các nguyên tắc bất biến được tuân thủ xuyên suốt

1. **Đọc CSV an toàn (`keep_default_na=False, na_values=[""]`):** Bảo toàn tài khoản người dùng thật có `username == "null"` (261 dòng danh sách) và phân biệt rõ các chuỗi giữ chỗ (`"Unknown"`, `"None"`).
2. **Bảo toàn dữ liệu gốc (`data/raw/`):** Chỉ loại bỏ đúng 2 tài khoản đổi tên trùng lặp hoàn toàn (`Io_Otonashi`, `Dojin_` — 1,059 dòng danh sách trùng khít); mọi phép biến đổi giá trị đều lưu vào các cột `*_clean` và ghi nhận trong `row_count_log.csv` (3 mục) và `value_cleaning_log.csv` (26 mục).
3. **Kiểm định lại sau làm sạch (Step 5):** Tất cả 8 quy tắc bất biến trên 80,075,053 dòng của 27 phân mảnh Parquet đạt **0 vi phạm**; tương quan hạng giữa mẫu và toàn sàn đạt $r_s = 0.9942$ (`members`) và $r_s = 0.9954$ (`scored_by`).
4. **Báo cáo thay đổi số dòng (`report_row_change` / `verify_merge`):** Áp dụng sau mọi bước lọc, loại bỏ giá trị thiếu hoặc gộp bảng trong `02_data_exploration.ipynb` và `04_data_analysis.ipynb`.
