# Programming for Data Science — MyAnimeList

Đồ án môn CSC17104 tìm hiểu hành vi xem anime trên MyAnimeList. Hướng khảo sát ban đầu là so sánh tỷ lệ được người dùng đánh dấu **đã xem xong** giữa các nhóm anime theo số tập, thể loại và định dạng phát hành.

Hiện tại, notebook `01_data_collection.ipynb` mô tả chủ đề và nguồn dữ liệu. Các notebook trong `notebooks/` là khung làm việc cho bước khám phá, phân tích và học máy; dự án chưa có kết quả phân tích được xác nhận.

## Dữ liệu

Nguồn: [MyAnimeList Dataset trên Kaggle](https://www.kaggle.com/datasets/azathoth42/myanimelist). Thông tin mô tả được lưu trong [data_description.txt](data_description.txt).

| File | Nội dung |
|---|---|
| `AnimeList.csv` | Thông tin anime: tiêu đề, số tập, thể loại, định dạng, điểm số và thời gian phát hành. |
| `UserList.csv` | Hồ sơ người dùng và các thông tin tổng hợp từ danh sách xem. |
| `UserAnimeList.csv` | Quan hệ người dùng–anime: điểm cá nhân, trạng thái xem và thời điểm cập nhật. |

Tải và giải nén ba file trên từ Kaggle vào `data/raw/` để dùng cho quy trình phân tích. Các bản CSV đã có ở `data/` trên máy có thể được sao chép vào `data/raw/` khi cần. Dữ liệu tải xuống không được đưa vào Git; riêng `UserAnimeList.csv` hiện có dung lượng gần 5 GB. Khi đọc file này, nên chọn các cột cần thiết và xử lý theo từng phần (`chunksize`) để giảm bộ nhớ sử dụng.

Trạng thái xem là thông tin do người dùng cập nhật, nên cần cân nhắc các danh sách chưa được cập nhật khi diễn giải tỷ lệ hoàn thành. Điều kiện sử dụng và ghi nguồn cần được đối chiếu trên trang dataset trước khi phân phối lại dữ liệu.

## Cấu trúc thư mục

```text
.
├── 01_data_collection.ipynb         # Mô tả chủ đề và nguồn dữ liệu
├── data_description.txt            # Thông tin mô tả dataset
├── data/
│   ├── raw/                        # Dữ liệu gốc tải từ Kaggle
│   └── processed/                  # Dữ liệu sau xử lý
├── docs/question_plan.md           # Kế hoạch câu hỏi và tiêu chí đánh giá
├── notebooks/
│   ├── 01_collection_exploration.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_ml_question.ipynb
├── src/audit.py                    # Hàm hỗ trợ kiểm tra chất lượng dữ liệu
├── environment.yml                # Môi trường Conda
└── LLM_USAGE.md                    # Nhật ký hỗ trợ từ LLM
```

## Thiết lập môi trường

Cài Conda hoặc Miniconda, sau đó chạy:

```bash
git clone --branch caoban https://github.com/PhamPhuong72/Programming-For-DS.git
cd Programming-For-DS
conda env create -f environment.yml
conda activate csc17104-final
jupyter lab
```

Môi trường sử dụng Python 3.11 cùng JupyterLab, NumPy, pandas, Matplotlib, SciPy và scikit-learn. Mở `01_data_collection.ipynb` để đọc phần giới thiệu. Sau khi tải dữ liệu, tiếp tục hoàn thiện các notebook trong `notebooks/` theo thứ tự `01` → `02` → `03`; đây hiện là các notebook khung.

## Quy ước làm việc

- Giữ nguyên dữ liệu gốc; ghi rõ các bước làm sạch và lưu kết quả vào `data/processed/`.
- Với mỗi bước lọc, gộp hoặc loại bỏ dữ liệu, báo cáo số dòng trước/sau và lý do.
- Các file có tên kết thúc bằng `_example` trước phần mở rộng, chẳng hạn `01_data_collection_example.ipynb`, được bỏ qua trong Git và vẫn giữ tại máy.
- Hoàn thiện câu hỏi, phân công thành viên và tiêu chí kiểm chứng trong [docs/question_plan.md](docs/question_plan.md).
- Ghi nhận các hỗ trợ đáng kể từ LLM trong [LLM_USAGE.md](LLM_USAGE.md).
