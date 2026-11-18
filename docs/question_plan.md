# Question Plan & Acceptance Checklist

- **Số lượng thành viên ($n$):** 3 thành viên (`Trần Trọng Tú - 24122024`, `Phạm Phương`, `Cao Bản`)
- **Tổng số câu hỏi ($2 \times n$):** 6 câu hỏi (4 câu hỏi Non-ML chuyên sâu + 2 câu hỏi Machine Learning có giám sát)
- **Phân công:** Mỗi thành viên phụ trách đúng 2 câu hỏi.

| ID | Owner | Specific question | Stakeholder / decision | Non-ML criteria D1–D6 or ML | Status |
|---|---|---|---|---|---|
| **Q1** | Trần Trọng Tú (`24122024`) | Trong nhóm người dùng đã thực sự bắt đầu xem (`my_status_clean` ∈ {1,2,3,4}), tổng thời lượng cam kết (`total_runtime_hours`, số tập) ảnh hưởng thế nào đến tỷ lệ bỏ dở thực tế (`active_drop_rate`) và tiến độ bỏ cuộc sớm sau khi kiểm soát định dạng & thể loại? | Ủy ban sản xuất & nền tảng streaming quyết định cấu trúc *split-cour* (12 tập) thay vì 24+ tập liền mạch | **D1, D3, D4, D5, D6** | Completed |
| **Q2** | Phạm Phương | Mặt bằng điểm cá nhân (`my_score_clean`) và tỷ lệ bỏ dở dịch chuyển ra sao giai đoạn 2006–2018, và hiện tượng anime mới điểm cao phản ánh lạm phát điểm hay độ trễ khám phá (`watch_lag_years`)? | Đội ngũ xếp hạng nền tảng & mua bản quyền hiệu chỉnh thuật toán xếp hạng theo độ trễ thời gian | **D1, D2, D3, D4, D5** | Completed |
| **Q3** | Cao Bản | Các phần tiếp theo (`Direct Sequel`) cao điểm hơn phần gốc bao nhiêu, quy mô người xem giữ lại được bao nhiêu %, và bao nhiêu phần chênh lệch điểm đến từ hiệu ứng *tự chọn lọc khán giả* trên cùng tài khoản? | Nhà đầu tư & Studio phân bổ vốn giữa sản xuất *Sequel* và phát triển IP mới (*Standalone*) | **D1, D3, D4, D5, D6** | Completed |
| **Q4** | Cao Bản | Độ hào phóng chấm điểm (`user_score_leniency`) và tỷ lệ hoàn thành thay đổi thế nào theo bậc thâm niên xem anime (`exp_tier`) và nhân khẩu học (`gender_clean`, nhóm tuổi)? | Đội ngũ Cá nhân hóa chuẩn hóa điểm người dùng và thiết kế luồng gợi ý cho người mới vs. người xem kỳ cựu | **D1, D2, D3, D4, D5, D6** | Completed |
| **Q5** | Trần Trọng Tú (`24122024`) | Dự báo xác suất một người dùng sẽ bỏ dở (`Dropped = 1`) thay vì hoàn thành (`Completed = 0`) một bộ anime TV dựa trên thông tin sẵn có trước khi xem | Hệ thống Recommendation điều chỉnh thứ hạng gợi ý theo rủi ro bỏ dở cá nhân hóa | **ML – Classification** (`GroupShuffleSplit` + `GroupKFold`, Leave-one-out, Pipeline, PR-AUC) | Completed |
| **Q6** | Phạm Phương | Dự báo điểm cộng đồng (`score_clean`) của anime sắp ra mắt chỉ từ siêu dữ liệu tiền sản xuất (*pre-release metadata*) | Bộ phận Licensing thẩm định giá trị bản quyền trước mùa chiếu | **ML – Regression** (`Temporal Split` ≤2015 → 2016–2018 + `TimeSeriesSplit`, Pipeline, RMSE) | Completed |

## Verify coverage
- [x] At least 1 ML question (2 câu hỏi ML đầy đủ: Q5 Classification & Q6 Regression).
- [x] Each non-ML question meets >=2 relevant D criteria (mỗi câu Q1–Q4 đạt từ 4 đến 5 tiêu chí).
- [x] Non-ML questions together cover >=4 of D1–D6 (bao phủ trọn vẹn **6/6 tiêu chí D1–D6**).
- [x] Each question explains motivation, stakeholder and informed decision (`notebooks/03_question_formulation.ipynb`).
- [x] Each question includes preprocessing description, row-count checks (`report_row_change` / `verify_merge`), method rationale, >=2 labelled plots, quantified answer and limitations (`notebooks/04_data_analysis.ipynb`).

## ML checklist (áp dụng cho cả Q5 và Q6)
- [x] Explain prediction task, user and prediction-time features; list excluded leakage features.
- [x] Split correctly (`GroupShuffleSplit`/`GroupKFold` theo `username` cho Q5; `Temporal Split` ≤2015 vs 2016–2018 + `TimeSeriesSplit` cho Q6).
- [x] Compare trivial baseline (`DummyClassifier` / `DummyRegressor`) with >=2 ML models (3 mô hình ML mỗi câu); preprocess within `sklearn.pipeline.Pipeline` & `ColumnTransformer`.
- [x] Tune using cross-validation (`GridSearchCV`) on train only; hold out test until final single evaluation.
- [x] Justify metrics (PR-AUC cho dữ liệu lệch lớp ở Q5; RMSE & MAE cho định giá điểm ở Q6); analyze failure cases by subgroups & concrete rows; interpret model with `permutation_importance`; answer original question.
