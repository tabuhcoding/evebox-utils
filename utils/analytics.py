import pandas as pd
from langchain.chat_models import ChatOpenAI

def format_percentage(val: float) -> str:
  return f"{val * 100:.2f}%"

def get_event_analytics(data: dict, query: str = "") -> str:
  llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

  event_title = data.get("eventTitle", "Sự kiện không tên")
  start_time = data.get("startTime")
  end_time = data.get("endTime")
  total_clicks = data.get("totalClicks", 0)
  week_clicks = data.get("weekClicks", 0)
  total_users = data.get("totalUsers", 0)
  total_buyers = data.get("totalBuyers", 0)
  total_orders = data.get("totalOrders", 0)
  
  time_range = f"{start_time} đến {end_time}" if start_time and end_time else "Không rõ"

  conversion_rate = (total_buyers / total_users) if total_users > 0 else 0.0

  # Format statistic data
  visits_df = pd.DataFrame(data.get("statistic", []))
  if not visits_df.empty:
      # Đổi tên cột để bảng markdown thân thiện hơn
      visits_df = visits_df.rename(columns={'weekStart': 'Tuần bắt đầu', 'visits': 'Lượt truy cập'})
      visits_markdown = visits_df.to_markdown(index=False)
  else:
      visits_markdown = "Không có dữ liệu truy cập theo tuần."

  # Prompt
  if not query.strip():
      # Prompt mặc định, yêu cầu phân tích toàn diện
      prompt = f"""
Bạn là một chuyên gia phân tích hiệu quả marketing sự kiện. Dựa vào các dữ liệu được cung cấp, hãy đưa ra một bản báo cáo ngắn gọn, tập trung vào các điểm chính và đề xuất hành động.

### Dữ liệu tổng quan về hiệu quả sự kiện:
- **Tên sự kiện:** {event_title}
- **Thời gian:** {time_range}
- **Tổng lượt click vào trang sự kiện:** {total_clicks:,}
- **Lượt click trong 7 ngày qua:** {week_clicks:,}
- **Số người dùng (unique users) đã truy cập:** {total_users:,}
- **Tổng số người mua vé:** {total_buyers:,}
- **Tổng số đơn hàng:** {total_orders:,}
- **Tỷ lệ chuyển đổi (từ truy cập thành người mua):** {format_percentage(conversion_rate)}

### Thống kê truy cập theo tháng:
{visits_markdown}

---

### Yêu cầu phân tích:
Hãy dựa vào các số liệu trên để:
1.  **Đánh giá tổng quan** về mức độ thu hút và quan tâm của sự kiện (dựa trên lượt click và số người dùng).
2.  **Phân tích hiệu quả chuyển đổi:** Tỷ lệ chuyển đổi hiện tại có tốt không? Có điểm gì bất thường giữa lượt truy cập và số người mua không?
3.  **Nhận xét xu hướng truy cập** qua các tháng (dựa vào bảng thống kê). Xu hướng đang tăng, giảm hay ổn định?
4.  **Đề xuất 2-3 hành động cụ thể** và khả thi để cải thiện hiệu quả marketing và tăng tỷ lệ chuyển đổi cho sự kiện này.
"""
  else:
      # Prompt tùy chỉnh khi người dùng có câu hỏi cụ thể
      prompt = f"""
Dưới đây là dữ liệu về hiệu quả marketing của một sự kiện.

### Dữ liệu sự kiện:
- **Tên sự kiện:** {event_title}
- **Thời gian:** {time_range}
- **Tổng click:** {total_clicks:,} (có {week_clicks:,} trong tuần qua)
- **Tổng người dùng truy cập:** {total_users:,}
- **Tổng người mua:** {total_buyers:,}
- **Tổng đơn hàng:** {total_orders:,}
- **Tỷ lệ chuyển đổi:** {format_percentage(conversion_rate)}

### Thống kê truy cập theo tháng:
{visits_markdown}

---

**Câu hỏi từ người dùng:** {query}

Hãy dựa vào dữ liệu trên để trả lời câu hỏi một cách ngắn gọn, chính xác và đi thẳng vào vấn đề.
"""
        
  response = llm.invoke(prompt)
  return response.content