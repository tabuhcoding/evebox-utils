# utils/revenue_analysis.py

import pandas as pd
from langchain_community.chat_models import ChatOpenAI
from datetime import datetime

def format_percentage(val: float) -> str:
    return f"{val * 100:.2f}%"

def analyze_revenue_event(data: dict, query: str = "") -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    event_title = data.get("eventTitle", "Sự kiện không tên")
    start_time = data.get("startTime")
    end_time = data.get("endTime")
    tickets_sold = data.get("ticketsSold", 0)
    total_tickets = data.get("totalTickets", 0)
    percentage_sold = data.get("percentageSold", 0.0)
    total_revenue = data.get("totalRevenue", 0)

    time_range = f"{start_time} đến {end_time}" if start_time and end_time else "Không rõ"

    # Format revenueChart
    revenue_df = pd.DataFrame(data.get("revenueChart", []))
    revenue_markdown = revenue_df.to_markdown(index=False) if not revenue_df.empty else "Không có dữ liệu doanh thu theo ngày."

    # Format ticket type
    ticket_type_df = pd.DataFrame(data.get("byTicketType", []))
    ticket_type_markdown = ticket_type_df.to_markdown(index=False) if not ticket_type_df.empty else "Không có dữ liệu theo loại vé."

    # Prompt
    if query.strip() == "":
        prompt = f"""
Bạn là chuyên gia phân tích dữ liệu sự kiện.

Thông tin sự kiện:
- Tên sự kiện: {event_title}
- Thời gian diễn ra: {time_range}
- Tổng vé đã bán: {tickets_sold} / {total_tickets} vé
- Tỉ lệ bán ra: {format_percentage(percentage_sold)}
- Tổng doanh thu: {total_revenue:,} VND

### Doanh thu theo tuần:
{revenue_markdown}

### Thống kê loại vé:
{ticket_type_markdown}

Hãy:
1. Đánh giá hiệu quả bán vé hiện tại
2. Nhận xét xu hướng doanh thu
3. Gợi ý 2-3 hành động cụ thể giúp cải thiện việc bán vé
"""
    else:
        prompt = f"""
Dưới đây là dữ liệu sự kiện:

- Tên sự kiện: {event_title}
- Thời gian: {time_range}
- Tổng vé: {total_tickets}, vé đã bán: {tickets_sold}
- Tỉ lệ bán ra: {format_percentage(percentage_sold)}
- Doanh thu: {total_revenue:,} VND

### Doanh thu theo tuần:
{revenue_markdown}

### Thống kê loại vé:
{ticket_type_markdown}

Câu hỏi: {query}
Hãy phân tích và trả lời ngắn gọn, rõ ràng.
"""

    response = llm.invoke(prompt)
    return response.content
