# Phân tích Hành vi Khán giả và Dự báo trên Hệ sinh thái MyAnimeList (80.08 Triệu Bản ghi)

## 1. Tổng quan dự án và thông tin nhóm

### 1.1. Tổng quan dự án

Dự án thực hiện quy trình Khoa học Dữ liệu hoàn chỉnh đầu–cuối (*end-to-end reproducible Data Science workflow*) trên hệ dữ liệu thực tế quy mô lớn của cộng đồng **MyAnimeList (MAL)** gồm **14,478 tựa anime**, **302,673 tài khoản người dùng** và **80,075,053 tương tác danh sách cá nhân**.

Từ việc tự kiểm toán dữ liệu thô (~5 GB), phát hiện và xử lý tất định các bẫy dữ liệu phức tạp (tài khoản tên `"null"`, bản sao đổi tên, tràn bộ đếm 16-bit/24-bit, ngày phát sóng tự điền), nhóm xây dựng và trả lời **6 câu hỏi nghiên cứu có chiều sâu**, kết nối trực tiếp phân tích thống kê kiểm soát biến nhiễu (`D1–D6`) với các mô hình Học máy chống rò rỉ dữ liệu (`Group-based Split` & `Temporal Split`).

### 1.2. Thông tin nhóm và phân công nhiệm vụ

- **Môn học:** CSC17104 – Lập trình cho Khoa học Dữ liệu (*Programming for Data Science*)
- **Trường:** Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM (`fit@hcmus`)

| Thành viên | MSSV | Câu hỏi sở hữu | Nhiệm vụ chuyên môn trong dự án |
|---|---|---|---|
| **Trần Trọng Tú** | `24122024` | **Q1** (Non-ML), **Q5** (ML – Classification) | Kiểm toán chất lượng dữ liệu thô, xây dựng pipeline làm sạch tất định `step4_clean_v1` (27 phân mảnh Parquet trên Kaggle), phân tích tỷ lệ bỏ dở & mô hình phân loại rủi ro bỏ dở theo nhóm người dùng (`GroupKFold`). |
| **Phạm Phương** | *(Cập nhật MSSV)* | **Q2** (Non-ML), **Q6** (ML – Regression) | Quản trị kho mã nguồn GitHub, chuẩn hóa kiến trúc module `src/`, phân tích chuỗi thời gian & độ trễ khám phá (2006–2018), xây dựng mô hình hồi quy dự báo điểm tiền sản xuất (`TimeSeriesSplit`). |
| **Cao Bản** | *(Cập nhật MSSV)* | **Q3** (Non-ML), **Q4** (Non-ML) | Thu thập & đối chiếu mô tả nguồn dữ liệu, khai phá đồ thị nhượng quyền `related` giải mã Nghịch lý Simpson ở các phần tiếp theo (*Sequel*) và phân tích độ khắt khe chấm điểm theo thâm niên/nhân khẩu học. |

---

## 2. Nguồn dữ liệu, Giấy phép và Công trình liên quan

### 2.1. Nguồn dữ liệu và truy vết phiên bản

1. **Bộ dữ liệu gốc (*Raw Source Dataset*):**
   - **Tên & Đường dẫn:** [MyAnimeList Dataset trên Kaggle](https://www.kaggle.com/datasets/azathoth42/myanimelist)
   - **Tác giả gốc:** Matěj Račinský (Czech Technical University in Prague), công bố năm **2018** (`doi: 10.34740/KAGGLE/DSV/45582`).
   - **Phương pháp thu thập:** Thu thập trang công khai từ `MyAnimeList.net` (tập hợp `username` từ diễn đàn thử thách xem anime 2015–2018 và ~40,000 câu lạc bộ đầu tiên; kết thúc tháng 05/2018).
   - **Giấy phép:** Open Database License / Database Contents License (`DbCL-1.0`) — cho phép sử dụng tự do cho mục đích học tập và nghiên cứu kèm trích dẫn tác giả gốc.

2. **Bộ dữ liệu đã làm sạch tất định của nhóm (*Processed Dataset — `step4_clean_v1`*):**
   - **Đường dẫn Kaggle công khai:** [chuyenhocielts/myanimelist-clean](https://www.kaggle.com/datasets/chuyenhocielts/myanimelist-clean)
   - **Quy mô sau làm sạch:** `AnimeList_clean.csv` (**14,478** dòng), `UserList_clean.csv` (**302,673** dòng sau khi loại 2 bí danh trùng lặp hoàn toàn `Io_Otonashi` và `Dojin_`), và `user_anime_list_parts/` (**27 phần Parquet, 80,075,053 dòng sạch**, nén còn ~0.82 GB kèm nhật ký `manifest.csv`, `row_count_log.csv`, `value_cleaning_log.csv`).

### 2.2. Khai báo các phân tích công khai hiện có và Điểm khác biệt của nhóm

Trên [trang Code công khai của dataset gốc](https://www.kaggle.com/datasets/azathoth42/myanimelist/code), đa số các notebook hiện có đi theo 3 hướng: *(1)* xây dựng hệ gợi ý Collaborative Filtering, *(2)* thống kê mô tả đơn biến theo thể loại/studio, hoặc *(3)* hồi quy dự đoán `score` nhưng đưa cả các biến hậu nghiệm (`members`, `scored_by`, `favorites`, `rank`) vào làm đầu vào gây **rò rỉ dữ liệu (*data leakage*)**.

**Điểm khác biệt cốt lõi của đồ án nhóm:**
- **Tự kiểm toán & làm sạch từ 3 bảng thô gốc** thay vì dùng bản lọc sẵn của tác giả; phát hiện và bảo toàn tài khoản thật có `username == "null"` (261 dòng), sửa 313 thời lượng tính bằng giây, khử 373 ngày phát sóng tự điền năm 2018 và các giá trị tràn số học (`65,535`, `16,777,215`).
- **Kiểm soát chặt biến nhiễu và thiên lệch chọn mẫu ở cả 4 câu hỏi Non-ML** (loại `Plan to Watch` khỏi mẫu số tỷ lệ bỏ dở; tách độ trễ xem `watch_lag_years`; đối sánh điểm Phần 1 -> Phần 2 trên *cùng một tài khoản* để chứng minh Nghịch lý Simpson; chuẩn hóa độ hào phóng `user_score_leniency`).
- **Thiết kế 2 bài toán Học máy chống rò rỉ dữ liệu nghiêm ngặt:** Tính lịch sử người dùng theo cơ chế *Leave-One-Out* kèm `GroupShuffleSplit`/`GroupKFold` theo `username` (Q5), và chỉ dùng siêu dữ liệu tiền sản xuất kèm `Temporal Split` $\le 2015 \to 2016\text{–}2018$ (Q6).

---

## 3. Danh sách 6 Câu hỏi Nghiên cứu

### 3.1. Nhóm 1: Phân tích thống kê chuyên sâu (Câu hỏi 1 – 4, bao phủ đủ 6/6 tiêu chí `D1–D6`)

- **Câu hỏi 1 (`D1, D3, D4, D5, D6` — Trần Trọng Tú):** Trong nhóm người dùng đã thực sự bắt đầu xem (`my_status_clean` ∈ {1, 2, 3, 4}), tổng thời lượng cam kết (`total_runtime_hours` và số tập) ảnh hưởng thế nào đến tỷ lệ bỏ dở thực tế (`active_drop_rate`) và thời điểm bỏ cuộc sớm, sau khi kiểm soát định dạng `TV` và thể loại?
- **Câu hỏi 2 (`D1, D2, D3, D4, D5` — Phạm Phương):** Mặt bằng điểm đánh giá cá nhân và tỷ lệ bỏ dở thay đổi ra sao theo quý/năm giai đoạn 2006–2018, và sự chênh lệch điểm giữa các thời kỳ phản ánh lạm phát điểm hay độ trễ khám phá (`watch_lag_years`)?
- **Câu hỏi 3 (`D1, D3, D4, D5, D6` — Cao Bản):** Các phần tiếp theo trực tiếp (`Direct Sequel`) chênh lệch điểm số và quy mô khán giả thế nào so với phần gốc, và bao nhiêu phần trăm mức tăng điểm đến từ hiệu ứng *tự chọn lọc khán giả* trên cùng một tài khoản?
- **Câu hỏi 4 (`D1, D2, D3, D4, D5, D6` — Cao Bản):** Độ hào phóng chấm điểm (`user_score_leniency`) và tỷ lệ hoàn thành thay đổi thế nào theo bậc thâm niên xem anime (`exp_tier`) và đặc điểm nhân khẩu học (`gender_clean`, nhóm tuổi)?

### 3.2. Nhóm 2: Học máy có giám sát (Câu hỏi 5 – 6)

- **Câu hỏi 5 (`ML – Classification` — Trần Trọng Tú):** Dự báo xác suất người dùng sẽ **bỏ dở (`Dropped = 1`)** thay vì **hoàn thành (`Completed = 0`)** một bộ anime TV dựa trên thông tin sẵn có trước khi xem (`GroupShuffleSplit` + `GroupKFold`, tối ưu `PR-AUC` trong `scikit-learn Pipeline`).
- **Câu hỏi 6 (`ML – Regression` — Phạm Phương):** Dự báo điểm đánh giá cộng đồng (`score_clean`) của anime sắp ra mắt chỉ từ thông tin tiền sản xuất (`Temporal Split` $\le 2015 \to 2016\text{–}2018$ + `TimeSeriesSplit`, tối ưu `RMSE` trong `scikit-learn Pipeline`).

---

## 4. Tổng hợp các phát hiện chính (Key Findings)

1. **Nghịch lý điểm số của các phần phim tiếp theo (*Sequel Survivorship / Simpson's Paradox* — Bất ngờ nhất, Q3):** `Direct Sequel` có điểm công bố cao hơn `Standalone` tới **`+0.875` điểm** (`7.184` vs `6.309`), nhưng đánh mất trung vị **43.74%** lượng người xem (tỷ lệ giữ chân **56.26%**). Theo dõi **581,474 lượt chấm trên cùng tài khoản**, nhóm tiếp tục xem Phần 2 vốn đã chấm Phần 1 cao hơn nhóm dừng lại **`+0.643` điểm** (`8.037` vs `7.395`), nhưng **chính họ lại chấm Phần 2 thấp hơn Phần 1 là `-0.153` điểm** (`7.884` vs `8.037`).
2. **Cam kết thời gian dài đẩy cao tỷ lệ bỏ dở và 3/4 người bỏ cuộc rời đi ngay trong 25% số tập đầu (Q1):** Tỷ lệ bỏ dở thực tế tăng từ **2.21%** (1 tập) lên **14.63%** (53+ tập). Trên riêng dòng `TV`, cấu trúc *2-cour* có tỷ lệ bỏ dở cao hơn *1-cour* (**10.79% vs 9.87%**, $p = 5.54 \times 10^{-4}$; gộp cả `on_hold` là **19.91% vs 15.97%**), và **71.4%–80.7%** ca bỏ dở xảy ra trong 1/4 thời lượng đầu.
3. **Không có "lạm phát điểm theo thời gian" — Điểm cao đến từ độ trễ sàng lọc kho lưu trữ (Q2):** Điểm chấm trung bình theo quý giảm từ **`7.69` (`2006Q1`) xuống `7.37` (`2018Q1`)**. Người xem trực tiếp ngay năm chiếu chấm trung bình **`7.454`**, thấp hơn **`0.34–0.36` điểm** so với người tìm xem lại sau 1–5 năm (**`7.80–7.82`**).
4. **Thâm niên xem càng cao, người dùng càng chấm điểm khắt khe (Q4):** Chỉ số chuẩn hóa `user_score_leniency` giảm đơn điệu từ **`+0.441` điểm** ở nhóm *Casual (10–50 bộ)* xuống **`-0.136` điểm** ở nhóm *Power Watchers (401+ bộ)* ($r_s = -0.2102, p < 10^{-169}$), dù nhóm *Power* có tỷ lệ hoàn thành cao nhất (**84.71%**).
5. **Mô hình dự báo chống rò rỉ đạt hiệu quả thực tiễn rõ rệt (Q5 & Q6):**
   - **Q5 (Classification):** `HistGradientBoostingClassifier` đạt **`Test PR-AUC = 0.4197`** (gấp **4.97×** Baseline `0.0844`) và **`ROC-AUC = 0.8642`** (`Recall = 81.29%`) trên tập người dùng mới.
   - **Q6 (Regression):** Chỉ từ metadata tiền sản xuất, `HistGradientBoostingRegressor` giảm **Test RMSE trên giai đoạn 2016–2018 từ `0.8979` xuống `0.6706`** (`MAE = 0.5082`, **$R^2 = 0.4288$**), đồng thời chỉ ra kịch bản gốc (`Original`, `MAE = 0.556`) rủi ro biến động cao hơn `Light novel` (`0.446`).

---

## 5. Cấu trúc thư mục dự án

```text
Programming-For-DS/
├── notebooks/                                  # 5 Jupyter Notebooks chính theo đúng quy trình đồ án
│   ├── 01_data_collection.ipynb                # Pha 3.1: Chủ đề, nguồn, giấy phép & phương pháp thu thập
│   ├── 02_data_exploration.ipynb               # Pha 3.2: EDA, kiểm toán chất lượng, làm sạch & kiểm định 80M dòng
│   ├── 03_question_formulation.ipynb           # Pha 3.3: Đặt 6 câu hỏi nghiên cứu, tiêu chí D1–D6 & đặc tả ML
│   ├── 04_data_analysis.ipynb                  # Pha 3.4: Phân tích thống kê (Q1–Q4) & Pipeline Học máy (Q5–Q6)
│   ├── 05_project_summary.ipynb                # Pha 3.5: Tổng kết insights, hạn chế, hướng mở rộng & phản tư cá nhân
│   └── preprocessing_pipeline/                 # Chuỗi notebook kiểm toán thô & đóng gói Parquet trên Kaggle (Steps 1–5)
│
├── src/                                        # Các module Python tái sử dụng
│   ├── __init__.py                             # Khởi tạo package
│   ├── audit.py                                # Kiểm toán thay đổi số dòng (report_row_change), merge D1 & missingness
│   ├── utils.py                                # Tự động dò đường dẫn dữ liệu, streaming Parquet, Bootstrap CI, đồ thị related
│   └── models.py                               # Xây dựng ColumnTransformer/Pipeline & tính Permutation Importance
│
├── data/                                       # Thư mục dữ liệu (không commit file lớn lên Git theo quy định)
│   ├── raw/                                    # Đặt 3 file gốc từ azathoth42/myanimelist (nếu chạy lại từ đầu)
│   └── processed/                              # Giải nén bộ step4_clean_v1 từ chuyenhocielts/myanimelist-clean
│
├── docs/                                       # Tài liệu kế hoạch câu hỏi & thứ tự khám phá
│   ├── exploration_order.md
│   └── question_plan.md
│
├── slides.pdf                                  # Bộ slide thuyết trình tổng kết đồ án (15 phút trình bày)
├── environment.yml                             # Cấu hình môi trường Conda chuẩn
├── requirements.txt                            # Danh sách thư viện Python cho pip
├── LLM_USAGE.md                                # Nhật ký khai báo sử dụng công cụ AI/LLM minh bạch
└── README.md                                   # Tài liệu hướng dẫn dự án
```

---

## 6. Hướng dẫn cài đặt và chạy lại dự án (Reproducibility Guide)

### Bước 1: Clone repository và tạo môi trường Conda (hoặc pip)

```bash
git clone https://github.com/PhamPhuong72/Programming-For-DS.git
cd Programming-For-DS

# Cách 1 (Khuyến nghị theo chuẩn môn học — Conda):
conda env create -f environment.yml
conda activate csc17104-final

# Cách 2 (Sử dụng pip):
pip install -r requirements.txt
```

### Bước 2: Tải dữ liệu sạch vào `data/processed/`

Tải bộ dữ liệu đã làm sạch **`step4_clean_v1`** từ Kaggle ([chuyenhocielts/myanimelist-clean](https://www.kaggle.com/datasets/chuyenhocielts/myanimelist-clean), ~819 MB) và giải nén vào `data/processed/` bằng Kaggle CLI (hoặc tải thủ công qua trình duyệt):

```bash
kaggle datasets download -d chuyenhocielts/myanimelist-clean -p data/processed --unzip
```

*(Tùy chọn: Nếu muốn chạy lại từ con số 0 bước tạo Parquet trong `notebooks/preprocessing_pipeline/04_clean_data_run.ipynb`, tải thêm 3 file gốc từ [azathoth42/myanimelist](https://www.kaggle.com/datasets/azathoth42/myanimelist) vào `data/raw/`).*

### Bước 3: Chạy các Notebook theo đúng thứ tự

Khởi động JupyterLab (`jupyter lab`) và chạy tuần tự từ `01` đến `05`:
1. `notebooks/01_data_collection.ipynb` — Bối cảnh thu thập, giấy phép và sai lệch mẫu.
2. `notebooks/02_data_exploration.ipynb` — Khám phá dữ liệu, đối chiếu log làm sạch và kiểm định 27 phân mảnh Parquet (~1.5 phút).
3. `notebooks/03_question_formulation.ipynb` — Đặc tả 6 câu hỏi nghiên cứu và ma trận tiêu chí.
4. `notebooks/04_data_analysis.ipynb` — Phân tích chuyên sâu Q1–Q4 và huấn luyện/đánh giá các Pipeline ML Q5–Q6 (~5–7 phút).
5. `notebooks/05_project_summary.ipynb` — Tổng hợp phát hiện chính, hạn chế, hướng mở rộng và phản tư cá nhân.
