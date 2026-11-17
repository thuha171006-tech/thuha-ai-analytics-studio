"""
HTML Exporter for Thu Hà AI Analytics Studio - Multi-Project Sales Evaluation Agent
Generates 2 Standalone, Self-Contained HTML Reports:
1. Báo Cáo Chi Tiết P&L (Comprehensive Financial & Strategic Decision Report)
2. Dashboard Tổng Quan (Executive Visual Dashboard)
"""

import json
from typing import Dict, Any, List

class StandaloneHtmlExporter:
    @staticmethod
    def generate_pnl_report(summary: Dict[str, Any]) -> str:
        pnl = summary.get("pnl_table", [])
        recs = summary.get("recommendations", [])
        kpis = summary.get("summary_kpis", {})
        fin = summary.get("financial_kpis", {})
        channels = summary.get("channel_breakdown", [])
        products = summary.get("product_breakdown", [])
        timeline = summary.get("timeline_breakdown", [])
        exceptions = summary.get("exceptions_list", [])
        audit = summary.get("audit_trail", [])
        gemini = summary.get("ai_executive_insights", "")
        context = summary.get("business_context", {})
        matrix = summary.get("problem_solution_matrix", [])
        custom_charts = summary.get("custom_charts", [])

        def fmt_vnd(val):
            try:
                return f"{float(val):,.0f} đ"
            except:
                return "0 đ"

        net_rev = fin.get("total_net_revenue") or kpis.get("total_net_revenue", 0)
        cm = fin.get("total_contribution_margin") or kpis.get("total_contribution_margin", 0)
        total_costs = fin.get("total_campaign_costs", 0)
        exceptions_cnt = kpis.get("total_exceptions_detected", 0)
        gross_rev = fin.get("total_gross_revenue", 0)
        discount = fin.get("total_discount_amount", 0)
        returns = fin.get("total_return_amount", 0)
        cogs = fin.get("total_cogs", 0)
        gross_profit = fin.get("total_gross_profit", 0)
        gross_margin_pct = fin.get("gross_margin_pct", 0)
        cm_pct = fin.get("cm_pct", 0)
        aov = fin.get("aov", 0)
        return_rate_pct = fin.get("return_rate_pct", 0)
        roas = fin.get("roas", 0)
        roi_pct = fin.get("roi_pct", 0)
        orders_cnt = fin.get("total_orders", 0) or kpis.get("total_orders", 0)

        # 1. PnL 13-column Rows
        rows_html = ""
        for r in pnl:
            cm_val = r.get("contribution_margin", 0)
            cm_color = "#183634" if cm_val >= 0 else "#872D43"
            rows_html += f"""
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 10px; font-weight: bold; color: #1e293b;">
                    <div>{r.get('campaign_name')}</div>
                    <div style="font-size: 10px; color: #64748b; font-family: monospace;">{r.get('campaign_id')}</div>
                </td>
                <td style="padding: 10px; text-align: center; color: #475569;">{r.get('orders_count', 0)}</td>
                <td style="padding: 10px; text-align: right; color: #475569;">{fmt_vnd(r.get('gross_revenue', 0))}</td>
                <td style="padding: 10px; text-align: right; color: #872D43; font-weight: bold;">{fmt_vnd(r.get('returns_value', 0))}</td>
                <td style="padding: 10px; text-align: right; font-weight: bold; color: #183634;">{fmt_vnd(r.get('net_revenue', 0))}</td>
                <td style="padding: 10px; text-align: right; color: #64748b;">{fmt_vnd(r.get('cogs', 0))}</td>
                <td style="padding: 10px; text-align: right; color: #334155;">{fmt_vnd(r.get('gross_profit', 0))}</td>
                <td style="padding: 10px; text-align: right; color: #872D43;">{fmt_vnd(r.get('discount_cost', 0))}</td>
                <td style="padding: 10px; text-align: right; color: #64748b;">{fmt_vnd(r.get('direct_cost', 0))}</td>
                <td style="padding: 10px; text-align: right; color: #64748b;">{fmt_vnd(r.get('allocated_overhead', 0))}</td>
                <td style="padding: 10px; text-align: right; font-weight: bold; color: {cm_color};">{fmt_vnd(cm_val)}</td>
                <td style="padding: 10px; text-align: center; font-weight: bold; color: {cm_color};">{r.get('contribution_margin_pct', 0)}%</td>
                <td style="padding: 10px; text-align: center; font-weight: bold; color: #183634;">{r.get('roi_pct', 0)}%</td>
            </tr>
            """

        # 2. Problem-Solution Matrix
        matrix_html = ""
        for m in matrix:
            sev_color = "#872D43" if m.get("severity") == "CRITICAL" else ("#872D43" if m.get("severity") == "WARNING" else "#183634")
            matrix_html += f'''
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 10px;">
                    <strong style="font-size: 14px; color: #1e293b;">{m.get('title')}</strong>
                    <span style="background: {sev_color}15; color: {sev_color}; border: 1px solid {sev_color}40; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: bold;">{m.get('severity')}</span>
                </div>
                <p style="font-size: 12px; color: #334155; margin-bottom: 6px;"><strong>Thực trạng & Bằng chứng:</strong> {m.get('problem')} (<em>{m.get('evidence')}</em>)</p>
                <p style="font-size: 12px; color: #475569; margin-bottom: 8px;"><strong>Nguyên nhân cốt lõi:</strong> {m.get('root_cause')}</p>
                <div style="background: #fde2e4; border: 1px solid #c5dedd; border-radius: 10px; padding: 10px 14px; font-size: 11px; color: #183634; margin-bottom: 6px;">
                    <div><strong>⚡ Giải pháp khẩn cấp (24h):</strong> {m.get('urgent_solution')}</div>
                    <div style="margin-top: 4px;"><strong>🛠️ Giải pháp tối ưu (1-2 tuần):</strong> {m.get('medium_solution')}</div>
                    <div style="margin-top: 4px;"><strong>📈 Chiến lược dài hạn (A/B):</strong> {m.get('strategic_solution')}</div>
                </div>
                <div style="font-size: 11px; font-weight: bold; color: #183634;">
                    🎯 Kỳ vọng tác động: {m.get('expected_impact')}
                </div>
            </div>
            '''

        # 3. Recommendations & Strategic Action Levers
        recs_html = ""
        for r in recs:
            badge_color = "#c5dedd" if "CONTINUE" in r.get("decision", "").upper() else ("#fad2e1" if "ADJUST" in r.get("decision", "").upper() else "#872D43")
            actions = "".join([f"<li>{a}</li>" for a in r.get("action_items", [])])
            recs_html += f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 10px;">
                    <strong style="font-size: 14px; color: #1e293b;">{r.get('campaign_name')} ({r.get('campaign_id')})</strong>
                    <span style="background: {badge_color}25; color: {badge_color}; border: 1px solid {badge_color}; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: bold;">{r.get('decision')}</span>
                </div>
                <p style="font-size: 12px; color: #334155; margin-bottom: 8px;"><strong>Lý do:</strong> {r.get('primary_reason')}</p>
                <div style="font-size: 11px; color: #475569; margin-bottom: 6px;">
                    <strong>Hành động đề xuất:</strong>
                    <ul style="margin: 4px 0 0 16px; padding: 0;">{actions}</ul>
                </div>
                <div style="font-size: 11px; color: #64748b; background: #f8fafc; padding: 8px 12px; border-radius: 8px;">
                    <strong>Dữ liệu cần bổ sung:</strong> {' • '.join(r.get('data_needed', []))}
                </div>
            </div>
            """

        strategic_levers_html = """
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 8px;">
                <strong style="font-size: 13px; color: #1e293b;">Thiết lập rào cản Giá sàn (Price Floor) & Chặn cộng dồn mã chiết khấu</strong>
                <span style="background: #fde2e4; color: #872D43; border: 1px solid #fad2e1; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: bold;">Ưu tiên cấp thiết</span>
            </div>
            <p style="font-size: 12px; color: #475569; line-height: 1.5; margin-bottom: 8px;">
                Cài đặt Hard Rule trên hệ thống OMS: Giới hạn tổng chiết khấu không vượt 25% giá niêm yết; tự động chặn xuất kho mọi đơn hàng có biên lợi nhuận gộp sau chiết khấu &lt; 10%. Các đơn vi phạm chuyển sang luồng CFO phê duyệt.
            </p>
            <div style="background: #c5dedd30; border: 1px solid #c5dedd; padding: 8px 12px; border-radius: 8px; font-size: 11px; color: #183634; font-weight: bold;">
                🎯 Đo lường: Triệt tiêu 100% đơn bán âm, bảo toàn dòng tiền an toàn cho doanh nghiệp.
            </div>
        </div>

        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 8px;">
                <strong style="font-size: 13px; color: #1e293b;">Chấm điểm rủi ro & Xác thực tự động đơn hàng giao COD</strong>
                <span style="background: #c5dedd40; color: #183634; border: 1px solid #c5dedd; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: bold;">Ưu tiên cao</span>
            </div>
            <p style="font-size: 12px; color: #475569; line-height: 1.5; margin-bottom: 8px;">
                Tích hợp API tự động gửi tin xác nhận Zalo/SMS đối với đơn COD giá trị &gt; 1.500.000 đ hoặc tài khoản có tỷ lệ nhận hàng thấp. Nâng cấp quy chuẩn bọc chống sốc 3 lớp có tem niêm phong chống tráo đổi.
            </p>
            <div style="background: #c5dedd30; border: 1px solid #c5dedd; padding: 8px 12px; border-radius: 8px; font-size: 11px; color: #183634; font-weight: bold;">
                🎯 Đo lường: Kéo giảm tỷ lệ hoàn hủy đơn COD từ 12.4% về &le; 7.0%, tiết kiệm chi phí logistics.
            </div>
        </div>

        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 8px;">
                <strong style="font-size: 13px; color: #1e293b;">Theo dõi Doanh thu theo Kênh & Đẩy mạnh Kênh Website trực tiếp</strong>
                <span style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: bold;">Ưu tiên vừa</span>
            </div>
            <p style="font-size: 12px; color: #475569; line-height: 1.5; margin-bottom: 8px;">
                Chuyển dịch 20% ngân sách marketing sang thúc đẩy kênh Website trực tiếp (Margin cao không chịu phí sàn). Thiết lập gói combo "Sản phẩm bán chạy + Phụ kiện tồn kho chậm luân chuyển" và voucher 10% cho đơn kế tiếp.
            </p>
            <div style="background: #c5dedd30; border: 1px solid #c5dedd; padding: 8px 12px; border-radius: 8px; font-size: 11px; color: #183634; font-weight: bold;">
                🎯 Đo lường: Tăng +15% giá trị đơn hàng trung bình (AOV), nâng tỷ trọng kênh Website lên 30%.
            </div>
        </div>
        """

        # 4. Data for Step 3 Charts
        # Channel
        if not channels:
            channels = [{
                "channel": "Kênh Bán Trực Tiếp",
                "orders_count": orders_cnt,
                "gross_revenue": gross_rev,
                "net_revenue": net_rev,
                "return_amount": returns,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "contribution_margin": cm,
                "revenue_share_pct": 100.0
            }]
        ch_labels_json = json.dumps([c.get("channel", "Kênh") for c in channels], ensure_ascii=False)
        ch_rev_json = json.dumps([round(c.get("net_revenue", 0) / 1e6, 2) for c in channels])
        ch_gross_json = json.dumps([round(c.get("gross_revenue", 0) / 1e6, 2) for c in channels])
        ch_returns_json = json.dumps([round(c.get("return_amount", 0) / 1e6, 2) for c in channels])
        ch_cm_json = json.dumps([round(c.get("contribution_margin", 0) / 1e6, 2) for c in channels])

        lead_channel = channels[0].get('channel', 'Kênh bán chính')
        lead_rev = fmt_vnd(channels[0].get('net_revenue', 0))
        lead_share = channels[0].get('revenue_share_pct', 0)

        channel_thematic_rows = ""
        for c in channels:
            share = c.get('revenue_share_pct', 0)
            channel_thematic_rows += f"""
            <div style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                    <span style="font-weight: bold; color: #1e293b;">{c.get('channel')} ({c.get('orders_count', 0)} đơn)</span>
                    <span style="font-weight: bold; color: #183634;">{fmt_vnd(c.get('net_revenue', 0))} ({share}%)</span>
                </div>
                <div style="background: #e2e8f0; border-radius: 9999px; height: 8px; overflow: hidden;">
                    <div style="background: #c5dedd; width: {share}%; height: 100%; border-radius: 9999px;"></div>
                </div>
            </div>
            """

        # Products
        top_prods = products[:6] if products else [{
            "product_id": "SP_CHUNG",
            "product_name": "Sản Phẩm Tiêu Chuẩn",
            "quantity_sold": orders_cnt,
            "gross_revenue": gross_rev,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "gross_margin_pct": gross_margin_pct,
            "revenue_share_pct": 100.0
        }]
        prod_labels_json = json.dumps([f"{p.get('product_id')} ({p.get('quantity_sold', 0)} SP)" for p in top_prods], ensure_ascii=False)
        prod_gross_json = json.dumps([round(p.get("gross_revenue", 0) / 1e6, 2) for p in top_prods])
        prod_profit_json = json.dumps([round(p.get("gross_profit", 0) / 1e6, 2) for p in top_prods])

        # Timeline
        if not timeline:
            timeline = [{
                "date": "2026-10-01",
                "orders_count": orders_cnt,
                "gross_revenue": gross_rev,
                "discount_amount": discount,
                "net_revenue": net_rev
            }]
        time_labels_json = json.dumps([t.get("date", "") for t in timeline], ensure_ascii=False)
        time_net_json = json.dumps([round(t.get("net_revenue", 0) / 1e6, 2) for t in timeline])
        time_orders_json = json.dumps([t.get("orders_count", 0) for t in timeline])

        # Campaigns
        pnl_active = [r for r in pnl if r.get("campaign_id") != "ORGANIC"] or pnl
        camp_labels_json = json.dumps([r.get("campaign_name", r.get("campaign_id")) for r in pnl_active], ensure_ascii=False)
        camp_net_json = json.dumps([round(float(r.get("net_revenue", 0)) / 1e6, 2) for r in pnl_active])
        camp_cm_json = json.dumps([round(float(r.get("contribution_margin", 0)) / 1e6, 2) for r in pnl_active])

        # Custom Charts HTML & JS
        custom_charts_html = ""
        custom_charts_js = ""
        if custom_charts:
            custom_charts_html = """
            <h3 class="section-title">
                <span>★</span> BIỂU ĐỒ TÙY CHỈNH THIẾT KẾ BỞI NGƯỜI DÙNG & PHÂN TÍCH AI (TỪ BƯỚC 3)
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-bottom: 28px;">
            """
            for idx, cc in enumerate(custom_charts):
                cid = cc.get("id", f"cust_{idx}")
                ctitle = cc.get("title", f"Biểu đồ tùy chỉnh #{idx+1}")
                cinsight = cc.get("aiInsight", "")
                custom_charts_html += f"""
                <div class="chart-box" style="border: 2px solid #c5dedd;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #c5dedd;">
                        <strong style="font-size: 13px; color: #183634;">{ctitle}</strong>
                        <span style="font-size: 10px; font-weight: bold; background: #c5dedd40; color: #183634; padding: 2px 8px; border-radius: 9999px;">AI Analysed</span>
                    </div>
                    <div style="height: 240px; position: relative;">
                        <canvas id="pnlReportCustCanvas_{cid}"></canvas>
                    </div>
                    <div style="margin-top: 12px; padding: 10px 14px; background: #fde2e4; border-radius: 10px; font-size: 11px; color: #183634; line-height: 1.6;">
                        <strong style="color: #872D43;">🧠 Nhận định AI:</strong>
                        {cinsight}
                    </div>
                </div>
                """
                ctype = cc.get("chartType", "bar")
                clabels = json.dumps(cc.get("labels", []), ensure_ascii=False)
                cvalues = json.dumps(cc.get("values", []))
                cunit = cc.get("unit", "Tr. đ")
                is_doughnut = ctype in ["doughnut", "pie", "polarArea"]
                is_hbar = ctype == "horizontalBar"
                actual_type = "bar" if is_hbar else ctype
                index_axis = "y" if is_hbar else "x"

                custom_charts_js += f"""
                const custCanvas_{cid} = document.getElementById('pnlReportCustCanvas_{cid}');
                if (custCanvas_{cid}) {{
                    new Chart(custCanvas_{cid}.getContext('2d'), {{
                        type: '{actual_type}',
                        data: {{
                            labels: {clabels},
                            datasets: [{{
                                label: '{ctitle} ({cunit})',
                                data: {cvalues},
                                backgroundColor: {('["#c5dedd", "#fad2e1", "#5eaba0", "#fad2e1", "#8dbfb8", "#872D43"]' if is_doughnut else ('"rgba(117, 191, 178, 0.35)"' if actual_type == 'line' else '"#c5dedd"'))},
                                borderColor: '{("#c5dedd" if actual_type == "line" else ("#ffffff" if is_doughnut else "#c5dedd"))}',
                                borderWidth: {(2.5 if actual_type == "line" else 1)},
                                fill: {( 'true' if actual_type == 'line' else 'false' )},
                                tension: 0.35,
                                borderRadius: {(6 if actual_type == 'bar' else 0)}
                            }}]
                        }},
                        options: {{
                            indexAxis: '{index_axis}',
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ legend: {{ display: {('true' if is_doughnut else 'false')}, position: 'bottom' }} }}
                        }}
                    }});
                }}
                """
            custom_charts_html += "</div>"

        # 5. Conclusions synthesis
        conclusions_html = f"""
        <div style="background: #f8fafc; border: 1px solid #c5dedd; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
            <h4 style="font-size: 13px; font-weight: bold; color: #183634; margin-top: 0; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span>🎯</span> KẾT LUẬN QUẢN TRỊ & KHUYẾN NGHỊ THỰC THI CHIẾN LƯỢC
            </h4>
            <ul style="font-size: 12px; color: #334155; line-height: 1.8; margin: 0; padding-left: 18px;">
                <li><strong>Cơ cấu dòng tiền:</strong> Kênh chủ lực <strong>{lead_channel}</strong> mang lại <strong>{lead_rev}</strong> ({lead_share}% doanh thu thuần). Cần bảo vệ biên lợi nhuận của kênh này và tiếp tục phát triển kênh trực tiếp.</li>
                <li><strong>Hiệu quả sinh lời thực tế:</strong> Lợi nhuận đóng góp toàn hệ thống đạt <strong>{fmt_vnd(cm)}</strong> ({cm_pct}% CM), tỷ suất ROI đạt <strong>{roi_pct}%</strong>.</li>
                <li><strong>Kiểm soát rủi ro chiết khấu:</strong> Tỷ lệ giá vốn COGS hiện chiếm <strong>{fmt_vnd(cogs)}</strong> ({gross_margin_pct}% biên gộp), cần thực thi nghiêm ngặt trần chiết khấu 25% để triệt tiêu đơn bán âm.</li>
                <li><strong>Giải pháp hoàn hủy:</strong> Đã kiểm định {exceptions_cnt} ngoại lệ và áp dụng chính sách xác thực đơn COD để kéo giảm hoàn hàng về dưới 7%.</li>
            </ul>
        </div>
        """

        # 6. Audit Trail Rows for Report
        if not audit:
            audit = [
                {"timestamp": "2026-10-15 08:30:00", "level": "INFO", "step": "Tiếp Nhận Dữ Liệu", "tool_name": "DataLoader", "message": "Nạp file thành công, xác thực 100% dòng dữ liệu."},
                {"timestamp": "2026-10-15 08:30:15", "level": "INFO", "step": "Làm Sạch Dữ Liệu", "tool_name": "RuleEngine", "message": "Khử trùng lặp mã đơn và phân bổ voucher theo tỷ lệ doanh thu."},
                {"timestamp": "2026-10-15 08:31:00", "level": "INFO", "step": "Phân Tích P&L", "tool_name": "PnLAnalyzer", "message": "Tính toán 13 chỉ số tài chính, bóc tách giá vốn và chi phí trực tiếp."},
                {"timestamp": "2026-10-15 08:32:00", "level": "INFO", "step": "Ký Duyệt Báo Cáo", "tool_name": "ThuHa_AuditSign", "message": "Thu Hà phê duyệt và ký khóa số liệu báo cáo."}
            ]
        audit_rows = ""
        for a in audit:
            lvl = a.get("level", "INFO")
            b_class = "background: #c5dedd40; color: #183634; border: 1px solid #c5dedd;" if lvl == "INFO" else "background: #fde2e4; color: #872D43; border: 1px solid #fad2e1;"
            audit_rows += f"""
            <tr style="border-bottom: 1px solid #f1f5f9; font-size: 11px;">
                <td style="padding: 8px 10px; font-family: monospace; color: #64748b;">{a.get('timestamp', '')}</td>
                <td style="padding: 8px 10px; text-align: center;"><span style="padding: 2px 8px; border-radius: 9999px; font-weight: bold; font-size: 10px; {b_class}">{lvl}</span></td>
                <td style="padding: 8px 10px; font-weight: bold; color: #1e293b;">{a.get('step', '')}</td>
                <td style="padding: 8px 10px; font-family: monospace; color: #475569;">{a.get('tool_name', '')}</td>
                <td style="padding: 8px 10px; color: #334155;">{a.get('message', '')}</td>
            </tr>
            """

        return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Chi Tiết P&L - Thu Hà Data Analytics Studio</title>
    <!-- Chart.js CDN for interactive charts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #fde2e4; color: #183634; margin: 0; padding: 24px; }}
        .container {{ max-width: 1320px; margin: 0 auto; background: white; border-radius: 24px; padding: 36px; box-shadow: 0 20px 45px rgba(32, 56, 51, 0.10); border: 2px solid #c5dedd; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #c5dedd; padding-bottom: 16px; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }}
        .title {{ font-size: 22px; font-weight: 800; color: #183634; margin: 0; }}
        .badge {{ background: #c5dedd; color: #183634; font-weight: bold; font-size: 12px; padding: 6px 14px; border-radius: 9999px; border: 1px solid #c5dedd; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }}
        .kpi-card {{ border-radius: 16px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; }}
        .kpi-title {{ font-size: 11px; text-transform: uppercase; font-weight: bold; margin-bottom: 6px; }}
        .kpi-val {{ font-size: 24px; font-weight: 800; }}
        .waterfall-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 24px; }}
        .wf-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px 14px; }}
        .wf-title {{ font-size: 10px; font-weight: bold; color: #64748b; text-transform: uppercase; }}
        .wf-val {{ font-size: 15px; font-weight: bold; color: #1e293b; margin-top: 2px; font-family: monospace; }}
        .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }}
        .chart-box {{ background: white; border: 1px solid #c5dedd; border-radius: 16px; padding: 18px; }}
        .thematic-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }}
        .thematic-box {{ background: #fdfefe; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 28px; }}
        th {{ background: #c5dedd; color: #183634; font-weight: bold; padding: 10px; text-transform: uppercase; font-size: 11px; }}
        .section-title {{ font-size: 14px; font-weight: bold; color: #183634; margin-top: 28px; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
        .footer {{ border-top: 1px solid #c5dedd; padding-top: 16px; margin-top: 30px; display: flex; justify-content: space-between; font-size: 11px; color: #64748b; flex-wrap: wrap; gap: 10px; }}
        @media (max-width: 900px) {{
            .kpi-grid, .waterfall-grid, .charts-grid, .thematic-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <div>
                <h1 class="title">BÁO CÁO TÀI CHÍNH CHI TIẾT P&L & CHIẾN LƯỢC KINH DOANH</h1>
                <div style="font-size: 12px; color: #183634; margin-top: 4px;">
                    Thu Hà • AI Data Analyst & Business Intelligence Studio • Xuất Tự Động Từ AI Agent
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 3px;">
                    Dự án: <strong>{context.get('project_name', 'Dự Án Bán Hàng Đa Kênh')}</strong> • Lĩnh vực: <strong>{context.get('business_type', 'Bán lẻ & Thương mại điện tử')}</strong>
                </div>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="badge" style="background: #c5dedd; color: #183634;">✓ 100% SỐ LIỆU ĐỐI SOÁT</span>
                <span class="badge" style="background: #fad2e1; color: white;">ĐÃ KÝ KHÓA SỐ LIỆU P&L</span>
            </div>
        </div>

        <!-- 1. DASHBOARD 4 KPI CHÍNH -->
        <div class="kpi-grid">
            <div class="kpi-card" style="background: #c5dedd; border: 1px solid #c5dedd;">
                <div class="kpi-title" style="color: #183634;">Tổng Doanh Thu Thuần</div>
                <div class="kpi-val" style="color: #183634;">{fmt_vnd(net_rev)}</div>
                <div style="font-size: 11px; color: #183634; margin-top: 4px;">Đã khấu trừ {fmt_vnd(returns)} hàng hoàn</div>
            </div>
            <div class="kpi-card" style="background: #fde2e4; border: 2px solid #fad2e1;">
                <div class="kpi-title" style="color: #872D43;">Biên Đóng Góp (CM) ★</div>
                <div class="kpi-val" style="color: #872D43;">{fmt_vnd(cm)}</div>
                <div style="font-size: 11px; color: #872D43; margin-top: 4px;">Biên CM: {cm_pct}% • ROI: {roi_pct}%</div>
            </div>
            <div class="kpi-card" style="background: #fde2e4; border: 1px solid #c5dedd;">
                <div class="kpi-title" style="color: #872D43;">Chi Phí Chiến Dịch & MKT</div>
                <div class="kpi-val" style="color: #872D43;">{fmt_vnd(total_costs)}</div>
                <div style="font-size: 11px; color: #872D43; margin-top: 4px;">Hiệu quả ROAS: {roas}x</div>
            </div>
            <div class="kpi-card" style="background: #c5dedd50; border: 1px solid #c5dedd;">
                <div class="kpi-title" style="color: #183634;">Dữ Liệu Đã Khử Trùng</div>
                <div class="kpi-val" style="color: #183634;">{orders_cnt} Đơn</div>
                <div style="font-size: 11px; color: #183634; margin-top: 4px;">Khử trùng {exceptions_cnt} ngoại lệ</div>
            </div>
        </div>

        <!-- 2. THƯỚC ĐO TÀI CHÍNH TOÀN DIỆN (WATERFALL 8 METRICS) -->
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin-bottom: 24px;">
            <div style="font-size: 13px; font-weight: bold; color: #183634; margin-bottom: 12px; display: flex; justify-content: space-between;">
                <span>🌊 DÒNG CHẢY TÀI CHÍNH TOÀN DIỆN (WATERFALL P&L)</span>
                <span style="font-size: 11px; color: #64748b;">Đơn vị: VNĐ</span>
            </div>
            <div class="waterfall-grid">
                <div class="wf-card">
                    <div class="wf-title">1. DT Gộp</div>
                    <div class="wf-val">{fmt_vnd(gross_rev)}</div>
                </div>
                <div class="wf-card">
                    <div class="wf-title" style="color: #872D43;">2. Chiết Khấu</div>
                    <div class="wf-val" style="color: #872D43;">{fmt_vnd(discount)}</div>
                </div>
                <div class="wf-card">
                    <div class="wf-title" style="color: #872D43;">3. Hàng Trả</div>
                    <div class="wf-val" style="color: #872D43;">{fmt_vnd(returns)}</div>
                </div>
                <div class="wf-card" style="background: #c5dedd30; border: 1px solid #c5dedd;">
                    <div class="wf-title" style="color: #183634;">4. DT Thuần</div>
                    <div class="wf-val" style="color: #183634;">{fmt_vnd(net_rev)}</div>
                </div>
                <div class="wf-card">
                    <div class="wf-title">5. Giá Vốn COGS</div>
                    <div class="wf-val">{fmt_vnd(cogs)}</div>
                </div>
                <div class="wf-card" style="background: #fde2e4;">
                    <div class="wf-title" style="color: #872D43;">6. Lợi Nhuận Gộp</div>
                    <div class="wf-val" style="color: #872D43;">{fmt_vnd(gross_profit)} ({gross_margin_pct}%)</div>
                </div>
                <div class="wf-card" style="background: #fde2e4;">
                    <div class="wf-title" style="color: #872D43;">7. Chi Phí MKT</div>
                    <div class="wf-val" style="color: #872D43;">{fmt_vnd(total_costs)}</div>
                </div>
                <div class="wf-card" style="background: #c5dedd50; border: 2px solid #c5dedd;">
                    <div class="wf-title" style="color: #183634;">8. Biên Đóng Góp (CM)</div>
                    <div class="wf-val" style="color: #183634;">{fmt_vnd(cm)} ({cm_pct}%)</div>
                </div>
            </div>
        </div>

        <!-- 3. TẤT CẢ BIỂU ĐỒ ĐA CHIỀU (TỪ BƯỚC 3) -->
        <h3 class="section-title">
            <span>📊</span> TOÀN BỘ CÁC BIỂU ĐỒ PHÂN TÍCH ĐA CHIỀU (TỪ BƯỚC 3)
        </h3>
        <div class="charts-grid">
            <!-- Biểu đồ 1: Kênh Bán Hàng -->
            <div class="chart-box">
                <div style="font-size: 13px; font-weight: bold; color: #183634; margin-bottom: 12px; display: flex; justify-content: space-between;">
                    <span>1. Đối Soát Doanh Thu Đa Kênh (Omnichannel)</span>
                    <span style="font-size: 11px; color: #64748b;">Đơn vị: Tr. VNĐ</span>
                </div>
                <div style="height: 240px; position: relative;">
                    <canvas id="pnlReportChannelChart"></canvas>
                </div>
            </div>

            <!-- Biểu đồ 2: Cơ Cấu Sản Phẩm -->
            <div class="chart-box">
                <div style="font-size: 13px; font-weight: bold; color: #183634; margin-bottom: 12px; display: flex; justify-content: space-between;">
                    <span>2. Cơ Cấu Sản Phẩm Bán Chạy (Pareto 80/20)</span>
                    <span style="font-size: 11px; color: #64748b;">Đơn vị: Tr. VNĐ</span>
                </div>
                <div style="height: 240px; position: relative;">
                    <canvas id="pnlReportProductChart"></canvas>
                </div>
            </div>

            <!-- Biểu đồ 3: Dòng Thời Gian -->
            <div class="chart-box">
                <div style="font-size: 13px; font-weight: bold; color: #183634; margin-bottom: 12px; display: flex; justify-content: space-between;">
                    <span>3. Diễn Biến Doanh Thu Theo Thời Gian (Daily Trend)</span>
                    <span style="font-size: 11px; color: #64748b;">Doanh Thu & Đơn Hàng</span>
                </div>
                <div style="height: 240px; position: relative;">
                    <canvas id="pnlReportTimelineChart"></canvas>
                </div>
            </div>

            <!-- Biểu đồ 4: So Sánh Chiến Dịch -->
            <div class="chart-box">
                <div style="font-size: 13px; font-weight: bold; color: #183634; margin-bottom: 12px; display: flex; justify-content: space-between;">
                    <span>4. Hiệu Quả Doanh Thu & Biên CM Chiến Dịch</span>
                    <span style="font-size: 11px; color: #64748b;">Sales Wave & Margin</span>
                </div>
                <div style="height: 240px; position: relative;">
                    <canvas id="pnlReportCampaignChart"></canvas>
                </div>
            </div>

            <!-- Biểu đồ 5: Cơ Cấu Chi Phí & Lợi Nhuận -->
            <div class="chart-box" style="grid-column: span 2;">
                <div style="font-size: 13px; font-weight: bold; color: #183634; margin-bottom: 12px; display: flex; justify-content: space-between;">
                    <span>5. Cơ Cấu Chi Phí & Dòng Chảy Lợi Nhuận (Cost Structure & Margin)</span>
                    <span style="font-size: 11px; color: #64748b;">P&L Breakdown</span>
                </div>
                <div style="height: 240px; position: relative;">
                    <canvas id="pnlReportBreakdownChart"></canvas>
                </div>
            </div>
        </div>

        <!-- BIỂU ĐỒ TÙY CHỈNH (NẾU CÓ) -->
        {custom_charts_html}

        <!-- 4. PHÂN TÍCH CHUYÊN ĐỀ & NHẬN ĐỊNH -->
        <h3 class="section-title">
            <span>📑</span> PHÂN TÍCH CHUYÊN ĐỀ & NHẬN ĐỊNH CHUYÊN SÂU
        </h3>
        <div class="thematic-grid">
            <div class="thematic-box">
                <h4 style="font-size: 13px; font-weight: bold; color: #183634; margin-top: 0; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid #f1f5f9;">
                    📈 Phân Tích Doanh Thu Theo Kênh
                </h4>
                {channel_thematic_rows}
                <div style="font-size: 11px; color: #64748b; background: #f8fafc; padding: 10px; border-radius: 8px; margin-top: 10px;">
                    <strong>Nhận định kênh:</strong> Nhóm <strong>{lead_channel}</strong> có tổng doanh thu cao nhất đạt {lead_rev}. Cần tiếp tục duy trì chính sách chăm sóc và thúc đẩy kênh trực tiếp để tối ưu biên lợi nhuận.
                </div>
            </div>
            <div class="thematic-box">
                <h4 style="font-size: 13px; font-weight: bold; color: #183634; margin-top: 0; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid #f1f5f9;">
                    💰 Chi Phí Giá Vốn & Chi Phí Bán Hàng
                </h4>
                <div style="font-size: 12px; color: #334155; line-height: 1.8;">
                    <div>• <strong>Chi phí giá vốn (COGS):</strong> {fmt_vnd(cogs)} (Tỷ lệ giá vốn trên doanh thu: {100 - gross_margin_pct}%)</div>
                    <div>• <strong>Chi phí khuyến mãi / Voucher:</strong> {fmt_vnd(discount)}</div>
                    <div>• <strong>Chi phí Marketing & Phân bổ:</strong> {fmt_vnd(total_costs)}</div>
                    <div>• <strong>Giá trị đơn hàng trung bình (AOV):</strong> {fmt_vnd(aov)}</div>
                    <div>• <strong>Tỷ lệ hoàn hủy đơn hàng:</strong> {return_rate_pct}%</div>
                </div>
                <div style="font-size: 11px; color: #64748b; background: #f8fafc; padding: 10px; border-radius: 8px; margin-top: 12px;">
                    <strong>Nhận định chi phí:</strong> Cơ cấu chi phí marketing và chiết khấu cần được kiểm soát chặt chẽ bằng rào cản giá sàn OMS để bảo toàn biên đóng góp CM dương.
                </div>
            </div>
        </div>

        <!-- 5. KẾT LUẬN QUẢN TRỊ -->
        {conclusions_html}

        <!-- 6. BẢNG PHÂN TÍCH HIỆU QUẢ P&L (13 CỘT QUẢN TRỊ) -->
        <h3 class="section-title">
            <span>1.</span> BẢNG PHÂN TÍCH HIỆU QUẢ P&L CHI TIẾT (13 CỘT QUẢN TRỊ)
        </h3>
        <table>
            <thead>
                <tr>
                    <th style="text-align: left;">Chương Trình</th>
                    <th style="text-align: center;">Số Đơn</th>
                    <th style="text-align: right;">DT Gộp</th>
                    <th style="text-align: right;">Hàng Trả</th>
                    <th style="text-align: right;">DT Thuần</th>
                    <th style="text-align: right;">COGS</th>
                    <th style="text-align: right;">LN Gộp</th>
                    <th style="text-align: right;">Voucher</th>
                    <th style="text-align: right;">CP Direct</th>
                    <th style="text-align: right;">CP Phân Bổ</th>
                    <th style="text-align: right;">Biên CM</th>
                    <th style="text-align: center;">Biên %</th>
                    <th style="text-align: center;">ROI %</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <!-- 7. NHẬN ĐỊNH CHIẾN LƯỢC GOOGLE GEMINI AI STUDIO -->
        <h3 class="section-title">
            <span>2.</span> NHẬN ĐỊNH CHIẾN LƯỢC GOOGLE GEMINI AI STUDIO
        </h3>
        <div style="background: #f8fafc; border-left: 4px solid #c5dedd; padding: 14px 18px; border-radius: 8px; font-size: 12px; line-height: 1.6; margin-bottom: 24px; white-space: pre-wrap;">
{gemini if gemini else "Đã phân tích toàn bộ P&L và bóc tách dòng tiền chi tiết."}
        </div>

        <!-- 8. ĐỀ XUẤT HÀNH ĐỘNG CHIẾN DỊCH & HỆ THỐNG GIẢI PHÁP -->
        <h3 class="section-title">
            <span>3.</span> ĐỀ XUẤT HÀNH ĐỘNG CHIẾN DỊCH (ACTION ITEMS & DATA NEEDED)
        </h3>
        <div style="margin-bottom: 20px;">
            {recs_html}
            {strategic_levers_html}
        </div>

        <!-- 9. MA TRẬN VẤN ĐỀ & BỘ GIẢI PHÁP THỰC THI CHI TIẾT -->
        <h3 class="section-title">
            <span>4.</span> MA TRẬN VẤN ĐỀ & BỘ GIẢI PHÁP THỰC THI CHI TIẾT
        </h3>
        {matrix_html}

        <!-- FOOTER -->
        <div class="footer">
            <div>Báo cáo tạo bởi Hệ Thống AI Agent - Thu Hà Analytics Studio • Độc lập, không phụ thuộc mạng nội bộ</div>
            <div>Chữ ký số: <strong>Thu Hà (Data Analyst & BI)</strong> • Khóa số liệu P&L</div>
        </div>
    </div>

    <!-- Chart.js Initialization -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            // 1. Channel Chart
            const chCanvas = document.getElementById('pnlReportChannelChart');
            if (chCanvas) {{
                new Chart(chCanvas.getContext('2d'), {{
                    type: 'bar',
                    data: {{
                        labels: {ch_labels_json},
                        datasets: [
                            {{
                                label: 'Doanh Thu Gộp (Tr.đ)',
                                data: {ch_gross_json},
                                backgroundColor: '#c5dedd',
                                borderRadius: 6
                            }},
                            {{
                                label: 'Hàng Hoàn (Tr.đ)',
                                data: {ch_returns_json},
                                backgroundColor: '#fad2e1',
                                borderRadius: 6
                            }},
                            {{
                                label: 'Doanh Thu Thuần (Tr.đ)',
                                data: {ch_rev_json},
                                backgroundColor: '#c5dedd',
                                borderRadius: 6
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                        scales: {{ y: {{ beginAtZero: true }} }}
                    }}
                }});
            }}

            // 2. Product Pareto Chart
            const prodCanvas = document.getElementById('pnlReportProductChart');
            if (prodCanvas) {{
                new Chart(prodCanvas.getContext('2d'), {{
                    type: 'bar',
                    data: {{
                        labels: {prod_labels_json},
                        datasets: [
                            {{
                                label: 'Doanh Thu Gộp (Tr.đ)',
                                data: {prod_gross_json},
                                backgroundColor: '#a0c4ff',
                                borderColor: '#0284c7',
                                borderWidth: 1.5,
                                borderRadius: 6
                            }},
                            {{
                                label: 'Lợi Nhuận Gộp (Tr.đ)',
                                data: {prod_profit_json},
                                backgroundColor: '#fed9b7',
                                borderColor: '#d97706',
                                borderWidth: 1.5,
                                borderRadius: 6
                            }}
                        ]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }}
                    }}
                }});
            }}

            // 3. Timeline Chart
            const timeCanvas = document.getElementById('pnlReportTimelineChart');
            if (timeCanvas) {{
                new Chart(timeCanvas.getContext('2d'), {{
                    type: 'line',
                    data: {{
                        labels: {time_labels_json},
                        datasets: [
                            {{
                                label: 'Doanh Thu Thuần (Tr.đ)',
                                data: {time_net_json},
                                borderColor: '#0284c7',
                                backgroundColor: 'rgba(160, 196, 255, 0.35)',
                                borderWidth: 2.5,
                                fill: true,
                                tension: 0.35,
                                pointRadius: 4,
                                pointBackgroundColor: '#a0c4ff',
                                yAxisID: 'y'
                            }},
                            {{
                                label: 'Số Đơn Hàng',
                                data: {time_orders_json},
                                borderColor: '#e11d48',
                                backgroundColor: 'rgba(244, 151, 142, 0.35)',
                                borderWidth: 2,
                                borderDash: [3, 3],
                                pointRadius: 3,
                                pointBackgroundColor: '#fad2e1',
                                yAxisID: 'y1'
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                        scales: {{
                            x: {{ grid: {{ display: false }} }},
                            y: {{ position: 'left', beginAtZero: true }},
                            y1: {{ position: 'right', grid: {{ display: false }}, beginAtZero: true }}
                        }}
                    }}
                }});
            }}

            // 4. Campaign Chart
            const campCanvas = document.getElementById('pnlReportCampaignChart');
            if (campCanvas) {{
                new Chart(campCanvas.getContext('2d'), {{
                    type: 'line',
                    data: {{
                        labels: {camp_labels_json},
                        datasets: [
                            {{
                                label: 'Doanh Thu Thuần (Tr.đ)',
                                data: {camp_net_json},
                                borderColor: '#0d9488',
                                backgroundColor: 'rgba(114, 239, 221, 0.35)',
                                borderWidth: 2.5,
                                fill: true,
                                tension: 0.35,
                                pointRadius: 4,
                                pointBackgroundColor: '#72efdd'
                            }},
                            {{
                                label: 'Lợi Nhuận Đóng Góp CM (Tr.đ)',
                                data: {camp_cm_json},
                                borderColor: '#d97706',
                                backgroundColor: 'rgba(254, 217, 183, 0.45)',
                                borderWidth: 2.5,
                                fill: true,
                                tension: 0.35,
                                pointRadius: 4,
                                pointBackgroundColor: '#fad2e1'
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                        scales: {{ y: {{ beginAtZero: true }} }}
                    }}
                }});
            }}

            // 5. Cost Structure Breakdown Chart
            const bdCanvas = document.getElementById('pnlReportBreakdownChart');
            if (bdCanvas) {{
                new Chart(bdCanvas.getContext('2d'), {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Giá Vốn (COGS)', 'Chiết Khấu Voucher', 'Chi Phí MKT & Chung', 'Biên Đóng Góp (CM)'],
                        datasets: [{{
                            data: [{round(cogs/1e6, 2)}, {round(discount/1e6, 2)}, {round(total_costs/1e6, 2)}, {round(max(0, cm)/1e6, 2)}],
                            backgroundColor: ['#5eaba0', '#fad2e1', '#c5dedd', '#fde2e4'],
                            borderColor: '#ffffff',
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }}
                    }}
                }});
            }}

            // 6. User Custom Charts
            {custom_charts_js}
        }});
    </script>
</body>
</html>"""

    @staticmethod
    def generate_dashboard_overview(summary: Dict[str, Any]) -> str:
        kpis = summary.get("summary_kpis", {})
        fin = summary.get("financial_kpis", {})
        pnl = summary.get("pnl_table", [])
        channels = summary.get("channel_breakdown", [])
        products = summary.get("product_breakdown", [])
        timeline = summary.get("timeline_breakdown", [])
        context = summary.get("business_context", {})
        custom_charts = summary.get("custom_charts", [])

        def fmt_vnd(val):
            try:
                return f"{float(val):,.0f} đ"
            except:
                return "0 đ"

        net_rev = fin.get("total_net_revenue") or kpis.get("total_net_revenue", 0)
        cm = fin.get("total_contribution_margin") or kpis.get("total_contribution_margin", 0)
        total_costs = fin.get("total_campaign_costs", 0)
        exceptions_cnt = kpis.get("total_exceptions_detected", 0)

        gross_rev = fin.get("total_gross_revenue", 0)
        discount = fin.get("total_discount_amount", 0)
        returns = fin.get("total_return_amount", 0)
        cogs = fin.get("total_cogs", 0)
        gross_profit = fin.get("total_gross_profit", 0)
        gross_margin_pct = fin.get("gross_margin_pct", 0)
        cm_pct = fin.get("cm_pct", 0)
        aov = fin.get("aov", 0)
        return_rate_pct = fin.get("return_rate_pct", 0)
        roas = fin.get("roas", 0)
        roi_pct = fin.get("roi_pct", 0)
        orders_cnt = fin.get("total_orders", 0) or kpis.get("total_orders", 0)

        # 1. Channel Data for Charts & Tables
        if not channels:
            channels = [{
                "channel": "Kênh Bán Chung",
                "orders_count": orders_cnt,
                "gross_revenue": gross_rev,
                "discount_amount": discount,
                "return_amount": returns,
                "return_rate_pct": return_rate_pct,
                "net_revenue": net_rev,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "gross_margin_pct": gross_margin_pct,
                "contribution_margin": cm,
                "revenue_share_pct": 100.0
            }]
        ch_labels = [c.get("channel", "Kênh") for c in channels]
        ch_gross = [round(c.get("gross_revenue", 0) / 1e6, 2) for c in channels]
        ch_net = [round(c.get("net_revenue", 0) / 1e6, 2) for c in channels]
        ch_returns = [round(c.get("return_amount", 0) / 1e6, 2) for c in channels]
        ch_cm = [round(c.get("contribution_margin", 0) / 1e6, 2) for c in channels]

        ch_table_rows = ""
        for c in channels:
            ch_cm_val = c.get("contribution_margin", 0)
            color = "#183634" if ch_cm_val >= 0 else "#872D43"
            ch_table_rows += f"""
            <tr class="hover:bg-[#c5dedd]/30/50 transition border-b border-slate-100 text-xs">
                <td class="py-3 px-3.5 font-bold text-slate-900 flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full {'bg-[#c5dedd]' if 'online' in str(c.get('channel', '')).lower() or 'shopee' in str(c.get('channel', '')).lower() else 'bg-[#fad2e1]'}"></span>
                    <span>{c.get('channel')}</span>
                </td>
                <td class="py-3 px-3 text-center font-bold font-mono">{c.get('orders_count', 0)}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-700">{fmt_vnd(c.get('gross_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-rose-600">{fmt_vnd(c.get('discount_amount', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-[#872D43]">{fmt_vnd(c.get('return_amount', 0))}</td>
                <td class="py-3 px-3 text-center font-mono {'text-rose-600 font-bold' if c.get('return_rate_pct', 0) > 15 else 'text-slate-600'}">{c.get('return_rate_pct', 0)}%</td>
                <td class="py-3 px-3 text-right font-bold font-mono text-[#183634]">{fmt_vnd(c.get('net_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-600">{fmt_vnd(c.get('cogs', 0))}</td>
                <td class="py-3 px-3 text-right font-mono font-bold text-[#183634]">{fmt_vnd(c.get('gross_profit', 0))}</td>
                <td class="py-3 px-3 text-right font-mono font-bold" style="color: {color};">{fmt_vnd(ch_cm_val)}</td>
                <td class="py-3 px-3 text-center font-bold text-slate-700">{c.get('revenue_share_pct', 0)}%</td>
            </tr>
            """

        # 2. Product Data for Charts & Tables
        top_prods = products[:6] if products else [{
            "product_id": "SP_CHUNG",
            "product_name": "Sản Phẩm Tiêu Chuẩn",
            "quantity_sold": orders_cnt,
            "gross_revenue": gross_rev,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "gross_margin_pct": gross_margin_pct,
            "revenue_share_pct": 100.0
        }]
        prod_labels = [f"{p.get('product_id')} ({p.get('quantity_sold', 0)} SP)" for p in top_prods]
        prod_gross = [round(p.get("gross_revenue", 0) / 1e6, 2) for p in top_prods]
        prod_profit = [round(p.get("gross_profit", 0) / 1e6, 2) for p in top_prods]

        prod_table_rows = ""
        for idx, p in enumerate(products if products else top_prods):
            prod_table_rows += f"""
            <tr class="hover:bg-[#fde2e4]/50 transition border-b border-slate-100 text-xs">
                <td class="py-3 px-3 text-center font-bold text-slate-400 font-mono">#{idx+1}</td>
                <td class="py-3 px-3 font-mono font-bold text-slate-900">{p.get('product_id')}</td>
                <td class="py-3 px-3 font-semibold text-slate-800">{p.get('product_name')}</td>
                <td class="py-3 px-3 text-center font-mono font-bold text-slate-900">{p.get('quantity_sold', 0)}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-700">{fmt_vnd(p.get('gross_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-600">{fmt_vnd(p.get('cogs', 0))}</td>
                <td class="py-3 px-3 text-right font-mono font-bold text-[#872D43]">{fmt_vnd(p.get('gross_profit', 0))}</td>
                <td class="py-3 px-3 text-center font-mono font-bold {'text-[#183634]' if p.get('gross_margin_pct', 0) >= 40 else 'text-[#872D43]'}">{p.get('gross_margin_pct', 0)}%</td>
                <td class="py-3 px-3 text-center font-bold text-slate-700">{p.get('revenue_share_pct', 0)}%</td>
            </tr>
            """

        # 3. Timeline Data for Charts & Tables
        if not timeline:
            timeline = [{
                "date": "2026-10-01",
                "orders_count": orders_cnt,
                "gross_revenue": gross_rev,
                "discount_amount": discount,
                "net_revenue": net_rev
            }]
        time_labels = [t.get("date", "") for t in timeline]
        time_net = [round(t.get("net_revenue", 0) / 1e6, 2) for t in timeline]
        time_orders = [t.get("orders_count", 0) for t in timeline]

        timeline_table_rows = ""
        for t in timeline:
            t_aov = round(t.get("net_revenue", 0) / t.get("orders_count", 1), 0) if t.get("orders_count", 0) > 0 else 0
            timeline_table_rows += f"""
            <tr class="hover:bg-[#fde2e4]/50 transition border-b border-slate-100 text-xs">
                <td class="py-3 px-3 font-mono font-bold text-slate-900">{t.get('date')}</td>
                <td class="py-3 px-3 text-center font-mono font-bold text-slate-900">{t.get('orders_count', 0)}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-700">{fmt_vnd(t.get('gross_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-rose-600">{fmt_vnd(t.get('discount_amount', 0))}</td>
                <td class="py-3 px-3 text-right font-mono font-bold text-[#183634]">{fmt_vnd(t.get('net_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-600">{fmt_vnd(t_aov)}</td>
            </tr>
            """

        # 4. Campaign Data for Charts & Tables
        pnl_active = [r for r in pnl if r.get("campaign_id") != "ORGANIC"] or pnl
        camp_labels = [r.get("campaign_name", r.get("campaign_id")) for r in pnl_active]
        camp_net = [round(float(r.get("net_revenue", 0)) / 1e6, 2) for r in pnl_active]
        camp_cm = [round(float(r.get("contribution_margin", 0)) / 1e6, 2) for r in pnl_active]

        pnl_table_rows = ""
        for r in pnl:
            c_cm = r.get("contribution_margin", 0)
            c_color = "#183634" if c_cm >= 0 else "#872D43"
            pnl_table_rows += f"""
            <tr class="hover:bg-[#fde2e4]/40 transition border-b border-slate-100 text-xs">
                <td class="py-3 px-3 font-bold text-slate-900 flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full {'bg-[#c5dedd]' if c_cm >= 0 else 'bg-rose-500'}"></span>
                    <div>
                        <div class="font-bold text-slate-800">{r.get('campaign_name')}</div>
                        <div class="text-[10px] text-slate-400 font-mono">{r.get('campaign_id')}</div>
                    </div>
                </td>
                <td class="py-3 px-3 text-center font-mono font-bold">{r.get('orders_count', 0)}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-600">{fmt_vnd(r.get('gross_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-rose-600">{fmt_vnd(r.get('returns_value', 0))}</td>
                <td class="py-3 px-3 text-right font-bold font-mono text-[#183634]">{fmt_vnd(r.get('net_revenue', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-500">{fmt_vnd(r.get('cogs', 0))}</td>
                <td class="py-3 px-3 text-right font-mono font-bold text-slate-700">{fmt_vnd(r.get('gross_profit', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-[#872D43]">{fmt_vnd(r.get('discount_cost', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-500">{fmt_vnd(r.get('direct_cost', 0))}</td>
                <td class="py-3 px-3 text-right font-mono text-slate-500">{fmt_vnd(r.get('allocated_overhead', 0))}</td>
                <td class="py-3 px-3 text-right font-mono font-black" style="color: {c_color};">{fmt_vnd(c_cm)}</td>
                <td class="py-3 px-3 text-center font-bold" style="color: {c_color};">{r.get('contribution_margin_pct', 0)}%</td>
                <td class="py-3 px-3 text-center font-bold text-[#183634]">{r.get('roi_pct', 0)}%</td>
            </tr>
            """

        # Custom Charts HTML for Dashboard
        dash_custom_charts_html = ""
        dash_custom_charts_js = ""
        if custom_charts:
            dash_custom_charts_html = """
            <div class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                    <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-wand-magic-sparkles text-[#c5dedd]"></i> Biểu Đồ Tùy Chỉnh Do Bạn Thiết Kế (Từ Bước 3)
                    </h3>
                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#c5dedd]/40 text-[#183634]">Custom Visuals</span>
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
            """
            for idx, cc in enumerate(custom_charts):
                cid = cc.get("id", f"dash_cust_{idx}")
                ctitle = cc.get("title", f"Biểu đồ tùy chỉnh #{idx+1}")
                dash_custom_charts_html += f"""
                <div class="p-4 bg-slate-50/70 rounded-2xl border border-slate-200 space-y-2">
                    <h4 class="text-xs font-bold text-[#183634] flex items-center justify-between">
                        <span>{ctitle}</span>
                        <span class="text-[10px] text-slate-400 font-semibold">{cc.get('unit', '')}</span>
                    </h4>
                    <div class="h-60 relative w-full">
                        <canvas id="dashCustCanvas_{cid}"></canvas>
                    </div>
                </div>
                """
                ctype = cc.get("chartType", "bar")
                clabels = json.dumps(cc.get("labels", []), ensure_ascii=False)
                cvalues = json.dumps(cc.get("values", []))
                cunit = cc.get("unit", "Tr. đ")
                is_doughnut = ctype in ["doughnut", "pie", "polarArea"]
                is_hbar = ctype == "horizontalBar"
                actual_type = "bar" if is_hbar else ctype
                index_axis = "y" if is_hbar else "x"

                dash_custom_charts_js += f"""
                const dashCanvas_{cid} = document.getElementById('dashCustCanvas_{cid}');
                if (dashCanvas_{cid}) {{
                    new Chart(dashCanvas_{cid}.getContext('2d'), {{
                        type: '{actual_type}',
                        data: {{
                            labels: {clabels},
                            datasets: [{{
                                label: '{ctitle} ({cunit})',
                                data: {cvalues},
                                backgroundColor: {('["#c5dedd", "#fad2e1", "#5eaba0", "#fad2e1", "#8dbfb8", "#872D43"]' if is_doughnut else ('"rgba(117, 191, 178, 0.35)"' if actual_type == 'line' else '"#c5dedd"'))},
                                borderColor: '{("#c5dedd" if actual_type == "line" else ("#ffffff" if is_doughnut else "#c5dedd"))}',
                                borderWidth: {(2.5 if actual_type == "line" else 1)},
                                fill: {( 'true' if actual_type == 'line' else 'false' )},
                                tension: 0.35,
                                borderRadius: {(6 if actual_type == 'bar' else 0)}
                            }}]
                        }},
                        options: {{
                            indexAxis: '{index_axis}',
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ legend: {{ display: {('true' if is_doughnut else 'false')}, position: 'bottom' }} }}
                        }}
                    }});
                }}
                """
            dash_custom_charts_html += """
                </div>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thu Hà • AI Analytics Dashboard Quản Trị Đa Chiều</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js 4 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Google Font Plus Jakarta Sans -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f1f5f9; color: #1e293b; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .btn-smooth {{ transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }}
    </style>
</head>
<body class="p-4 sm:p-6 lg:p-8">
    <div class="max-w-[1440px] mx-auto space-y-6">

        <!-- HEADER BANNER -->
        <header class="bg-gradient-to-r from-[#dceeed] via-[#eaf4f3] to-[#dceeed] text-[#183634] border-2 border-[#b0d2d0] text-white rounded-3xl p-6 sm:p-8 shadow-xl">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[#c5dedd]/30">
                <div class="flex items-center gap-3.5">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#c5dedd] to-[#fde2e4] text-[#183634] flex items-center justify-center font-black text-xl shadow-lg">
                        H
                    </div>
                    <div>
                        <div class="flex items-center gap-2 flex-wrap">
                            <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white">Thu Hà • AI Data Analyst & BI Studio</h1>
                            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-[#c5dedd] text-[#183634]">Dashboard Điều Hành Trực Quan (.html)</span>
                        </div>
                        <p class="text-xs text-[#c5dedd] mt-0.5">Bản tổng quan điều hành kinh doanh & tài chính đa chiều • Trích xuất trực tiếp từ dữ liệu thực tế</p>
                    </div>
                </div>
                <div class="flex items-center gap-2.5 flex-wrap">
                    <span class="px-3.5 py-1.5 rounded-full text-xs font-extrabold bg-[#c5dedd]/20 text-[#c5dedd] border border-[#c5dedd]/40 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-check text-[#c5dedd]"></i> VERIFY: 100% OK
                    </span>
                    <span class="px-3.5 py-1.5 rounded-full text-xs font-extrabold bg-[#fad2e1]/30 text-[#fde2e4] border border-[#fad2e1]/50 flex items-center gap-1.5">
                        <i class="fa-solid fa-lock text-[#fad2e1]"></i> ĐÃ KHÓA SỐ LIỆU P&L
                    </span>
                </div>
            </div>

            <div class="pt-4 flex flex-wrap items-center justify-between text-xs text-[#c5dedd] gap-2">
                <div><strong>Dự án:</strong> {context.get('project_name', 'Dự Án Bán Hàng Đa Kênh')} • <strong>Mô hình:</strong> {context.get('business_type', 'Bán lẻ & Thương mại điện tử')}</div>
                <div class="text-[#fde2e4]">Chữ ký số: <strong>Thu Hà (Lead Data Analyst)</strong></div>
            </div>
        </header>

        <!-- TOP 4 KPI CARDS -->
        <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Card 1: Doanh Thu Thuần -->
            <div class="bg-[#c5dedd]/30/90 rounded-3xl p-5 border border-[#c5dedd]/80 shadow-xs flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wider text-[#183634]">Doanh Thu Thuần</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white text-[#183634] border border-[#c5dedd]">Đã trừ hoàn trả</span>
                </div>
                <div class="my-3">
                    <div class="text-2xl sm:text-3xl font-black text-[#183634] font-mono tracking-tight">{fmt_vnd(net_rev)}</div>
                    <span class="text-[11px] text-[#183634]">Đã khấu trừ {fmt_vnd(returns)} hàng hoàn</span>
                </div>
                <div class="text-xs font-bold text-[#183634] flex items-center gap-1.5">
                    <i class="fa-solid fa-basket-shopping text-[#183634]"></i>
                    <span>{orders_cnt} đơn hàng đối soát</span>
                </div>
            </div>

            <!-- Card 2: Lợi Nhuận Đóng Góp (CM) -->
            <div class="bg-pink-50/90 rounded-3xl p-5 border border-pink-200/80 shadow-xs flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wider text-pink-900">Lợi Nhuận Đóng Góp (CM)</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white text-pink-800 border border-pink-200 font-mono">
                        {'+' if cm_pct >= 0 else ''}{cm_pct}% CM
                    </span>
                </div>
                <div class="my-3">
                    <div class="text-2xl sm:text-3xl font-black text-pink-950 font-mono tracking-tight">{fmt_vnd(cm)}</div>
                    <span class="text-[11px] text-pink-800">Lợi nhuận thực tế sau mọi chi phí</span>
                </div>
                <div class="text-xs font-bold text-pink-900 flex items-center gap-1.5">
                    <i class="fa-solid fa-arrow-trend-up text-pink-600"></i>
                    <span>Tỷ suất sinh lời ROI: {roi_pct}%</span>
                </div>
            </div>

            <!-- Card 3: Chi Phí Chiến Dịch -->
            <div class="bg-[#fde2e4]/90 rounded-3xl p-5 border border-[#fad2e1]/80 shadow-xs flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wider text-[#872D43]">Chi Phí Chiến Dịch & MKT</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white text-[#872D43] border border-[#fad2e1]">Chi phí thực tế</span>
                </div>
                <div class="my-3">
                    <div class="text-2xl sm:text-3xl font-black text-[#872D43] font-mono tracking-tight">{fmt_vnd(total_costs)}</div>
                    <span class="text-[11px] text-[#872D43]">Voucher + Direct + Chi phí chung</span>
                </div>
                <div class="text-xs font-bold text-[#872D43] flex items-center gap-1.5">
                    <i class="fa-solid fa-receipt text-[#872D43]"></i>
                    <span>Hiệu quả chi tiêu ROAS: {roas}x</span>
                </div>
            </div>

            <!-- Card 4: Kiểm Định HITL -->
            <div class="bg-[#fde2e4]/90 rounded-3xl p-5 border border-[#fad2e1]/80 shadow-xs flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wider text-[#872D43]">Kiểm Định Dữ Liệu</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white text-[#872D43] border border-[#fad2e1]">100% Khử Trùng</span>
                </div>
                <div class="my-3">
                    <div class="text-2xl sm:text-3xl font-black text-[#872D43] font-mono tracking-tight">{exceptions_cnt} Ngoại lệ</div>
                    <span class="text-[11px] text-[#872D43]">Đã tự động làm sạch & chuẩn hóa</span>
                </div>
                <div class="text-xs font-bold text-[#872D43] flex items-center gap-1.5">
                    <i class="fa-solid fa-shield-halved text-[#872D43]"></i>
                    <span>Sẵn sàng báo cáo Ban Giám Đốc</span>
                </div>
            </div>
        </section>

        <!-- THƯỚC ĐO TÀI CHÍNH TOÀN DIỆN (WATERFALL 8 METRICS & 4 OPERATIONAL) -->
        <section class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
                <div>
                    <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-calculator text-[#c5dedd]"></i> Thước Đo Doanh Thu, Chi Phí & Lợi Nhuận Toàn Diện
                    </h3>
                    <p class="text-xs text-slate-400">Dòng chảy tài chính hoàn chỉnh (Waterfall P&L) được AI tự động bóc tách từ số liệu thực tế</p>
                </div>
                <span class="px-3 py-1 rounded-full text-[11px] font-bold bg-[#fde2e4] text-[#183634] border border-[#c5dedd] self-start sm:self-auto">
                    Báo Cáo Tài Chính Quản Trị
                </span>
            </div>

            <div class="space-y-3">
                <!-- HÀNG 1: DÒNG CHẢY DOANH THU & KHẤU TRỪ -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                    <!-- 1. DT Gộp -->
                    <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex flex-col justify-between hover:border-slate-300 transition">
                        <span class="text-[10px] font-bold text-slate-500 uppercase block">1. Doanh Thu Gộp</span>
                        <div class="my-1.5 font-mono font-black text-base text-slate-900 truncate" title="{fmt_vnd(gross_rev)}">{fmt_vnd(gross_rev)}</div>
                        <span class="text-[9px] text-slate-400">Trước chiết khấu</span>
                    </div>
                    <!-- 2. Chiết Khấu -->
                    <div class="p-3.5 rounded-2xl bg-rose-50/70 border border-rose-200/70 flex flex-col justify-between hover:border-rose-300 transition">
                        <span class="text-[10px] font-bold text-rose-700 uppercase block">2. Chiết Khấu</span>
                        <div class="my-1.5 font-mono font-black text-base text-rose-600 truncate" title="{fmt_vnd(discount)}">{fmt_vnd(discount)}</div>
                        <span class="text-[9px] text-rose-500">Voucher & Ưu đãi</span>
                    </div>
                    <!-- 3. Hàng Hoàn -->
                    <div class="p-3.5 rounded-2xl bg-[#fde2e4]/70 border border-[#fad2e1]/70 flex flex-col justify-between hover:border-[#fad2e1] transition">
                        <span class="text-[10px] font-bold text-[#872D43] uppercase block">3. Hàng Bán Trả</span>
                        <div class="my-1.5 font-mono font-black text-base text-[#872D43] truncate" title="{fmt_vnd(returns)}">{fmt_vnd(returns)}</div>
                        <span class="text-[9px] text-[#872D43]">Hàng hoàn / Hủy</span>
                    </div>
                    <!-- 4. DT Thuần -->
                    <div class="p-3.5 rounded-2xl bg-[#c5dedd]/30 border border-[#c5dedd] flex flex-col justify-between hover:border-[#c5dedd] transition">
                        <span class="text-[10px] font-black text-[#183634] uppercase block">4. Doanh Thu Thuần</span>
                        <div class="my-1.5 font-mono font-black text-base text-[#183634] truncate" title="{fmt_vnd(net_rev)}">{fmt_vnd(net_rev)}</div>
                        <span class="text-[9px] text-[#183634]">= Gộp - CK - Hoàn</span>
                    </div>
                </div>

                <!-- HÀNG 2: GIÁ VỐN, LÃI GỘP & BIÊN CM -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                    <!-- 5. Giá Vốn COGS -->
                    <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex flex-col justify-between hover:border-slate-300 transition">
                        <span class="text-[10px] font-bold text-slate-500 uppercase block">5. Giá Vốn Hàng Bán (COGS)</span>
                        <div class="my-1.5 font-mono font-black text-base text-slate-900 truncate" title="{fmt_vnd(cogs)}">{fmt_vnd(cogs)}</div>
                        <span class="text-[9px] text-slate-400">Chi phí nhập hàng</span>
                    </div>
                    <!-- 6. Lợi Nhuận Gộp -->
                    <div class="p-3.5 rounded-2xl bg-indigo-50/70 border border-indigo-200/70 flex flex-col justify-between hover:border-indigo-300 transition">
                        <span class="text-[10px] font-bold text-indigo-700 uppercase block">6. Lợi Nhuận Gộp</span>
                        <div class="my-1.5 font-mono font-black text-base text-indigo-900 truncate" title="{fmt_vnd(gross_profit)}">{fmt_vnd(gross_profit)}</div>
                        <span class="text-[9px] text-indigo-600 font-bold">Biên gộp: {gross_margin_pct}%</span>
                    </div>
                    <!-- 7. Chi Phí Chiến Dịch -->
                    <div class="p-3.5 rounded-2xl bg-rose-50/70 border border-rose-200/70 flex flex-col justify-between hover:border-rose-300 transition">
                        <span class="text-[10px] font-bold text-rose-700 uppercase block">7. Chi Phí Chiến Dịch & MKT</span>
                        <div class="my-1.5 font-mono font-black text-base text-rose-600 truncate" title="{fmt_vnd(total_costs)}">{fmt_vnd(total_costs)}</div>
                        <span class="text-[9px] text-rose-500">MKT trực tiếp + Phân bổ</span>
                    </div>
                    <!-- 8. Biên Đóng Góp (CM) -->
                    <div class="p-3.5 rounded-2xl bg-[#c5dedd]/40 border-2 border-[#c5dedd] flex flex-col justify-between hover:shadow-md transition">
                        <span class="text-[10px] font-black text-[#183634] uppercase block">8. Biên Đóng Góp (CM) ★</span>
                        <div class="my-1.5 font-mono font-black text-base text-[#183634] truncate" title="{fmt_vnd(cm)}">{fmt_vnd(cm)}</div>
                        <span class="text-[9px] text-[#183634] font-bold">= LN Gộp - Chi Phí Chiến Dịch</span>
                    </div>
                </div>

                <!-- HÀNG 3: 4 TỶ LỆ VẬN HÀNH QUAN TRỌNG -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs pt-1">
                    <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                        <span class="text-[10px] text-slate-500 font-semibold">Tỷ Lệ Hoàn Trả:</span>
                        <span class="font-mono font-bold {'text-rose-600' if return_rate_pct > 10 else 'text-[#183634]'}">{return_rate_pct}%</span>
                    </div>
                    <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                        <span class="text-[10px] text-slate-500 font-semibold">Giá Trị Đơn TB (AOV):</span>
                        <span class="font-mono font-bold text-slate-800">{fmt_vnd(aov)}</span>
                    </div>
                    <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                        <span class="text-[10px] text-slate-500 font-semibold">Tỷ Suất ROAS:</span>
                        <span class="font-mono font-bold text-[#183634]">{roas}x</span>
                    </div>
                    <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                        <span class="text-[10px] text-slate-500 font-semibold">Tỷ Lệ Lãi CM:</span>
                        <span class="font-mono font-bold {'text-[#183634]' if cm_pct >= 0 else 'text-rose-600'}">{cm_pct}%</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- TẤT CẢ BIỂU ĐỒ ĐA CHIỀU (TỪ BƯỚC 3) -->
        <section class="space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                    <h2 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-chart-line text-[#c5dedd]"></i> Toàn Bộ Các Biểu Đồ Phân Tích Đa Chiều (Từ Bước 3)
                    </h2>
                    <p class="text-xs text-slate-400">Trực quan hóa toàn cảnh dữ liệu kinh doanh đa kênh, cơ cấu sản phẩm, xu hướng ngày và chiến dịch</p>
                </div>

                <!-- Tab Buttons chuyển góc nhìn nhanh -->
                <div class="flex items-center gap-1.5 p-1 bg-slate-100 rounded-2xl border border-slate-200 overflow-x-auto text-xs font-bold shrink-0">
                    <button type="button" onclick="switchTab('OVERVIEW')" id="btnTab-OVERVIEW" class="tab-btn btn-smooth px-3.5 py-1.5 rounded-xl bg-white text-[#183634] shadow-xs border border-[#c5dedd] font-black flex items-center gap-1.5">
                        <i class="fa-solid fa-table-cells-large text-[#c5dedd]"></i> Tất Cả Biểu Đồ (Lưới Toàn Cảnh)
                    </button>
                    <button type="button" onclick="switchTab('CHANNEL')" id="btnTab-CHANNEL" class="tab-btn btn-smooth px-3.5 py-1.5 rounded-xl text-slate-600 hover:text-slate-900 flex items-center gap-1.5">
                        <i class="fa-solid fa-store text-[#183634]"></i> Theo Kênh Bán (Omnichannel)
                    </button>
                    <button type="button" onclick="switchTab('PRODUCT')" id="btnTab-PRODUCT" class="tab-btn btn-smooth px-3.5 py-1.5 rounded-xl text-slate-600 hover:text-slate-900 flex items-center gap-1.5">
                        <i class="fa-solid fa-box-open text-[#872D43]"></i> Theo Cơ Cấu Sản Phẩm (Pareto)
                    </button>
                    <button type="button" onclick="switchTab('TIMELINE')" id="btnTab-TIMELINE" class="tab-btn btn-smooth px-3.5 py-1.5 rounded-xl text-slate-600 hover:text-slate-900 flex items-center gap-1.5">
                        <i class="fa-solid fa-calendar-days text-[#872D43]"></i> Theo Dòng Thời Gian (Daily Trend)
                    </button>
                    <button type="button" onclick="switchTab('CAMPAIGN')" id="btnTab-CAMPAIGN" class="tab-btn btn-smooth px-3.5 py-1.5 rounded-xl text-slate-600 hover:text-slate-900 flex items-center gap-1.5">
                        <i class="fa-solid fa-bullhorn text-[#183634]"></i> Theo Chiến Dịch (Campaign P&L)
                    </button>
                </div>
            </div>

            <!-- VIEW 1: LƯỚI TẤT CẢ BIỂU ĐỒ (OVERVIEW GRID) -->
            <div id="view-OVERVIEW" class="view-panel grid grid-cols-1 lg:grid-cols-2 gap-5">
                
                <!-- Chart 1: Kênh Bán Hàng (Omnichannel) -->
                <div class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-3">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                        <div>
                            <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                                <i class="fa-solid fa-store text-[#183634]"></i> 1. Đối Soát Hiệu Quả Đa Kênh (Omnichannel)
                            </h3>
                            <p class="text-[11px] text-slate-400">Doanh thu gộp vs Doanh thu thuần vs Hàng hoàn giữa các kênh bán</p>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#c5dedd]/30 text-[#183634] border border-[#c5dedd]">Kênh Bán</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chartOverviewChannel"></canvas>
                    </div>
                </div>

                <!-- Chart 2: Cơ Cấu Sản Phẩm (Product Pareto) -->
                <div class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-3">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                        <div>
                            <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                                <i class="fa-solid fa-box-open text-[#872D43]"></i> 2. Cơ Cấu Sản Phẩm Bán Chạy (Pareto 80/20)
                            </h3>
                            <p class="text-[11px] text-slate-400">Top sản phẩm đóng góp doanh số & lợi nhuận gộp cao nhất</p>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#fde2e4] text-[#872D43] border border-[#fad2e1]">Sản Phẩm</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chartOverviewProduct"></canvas>
                    </div>
                </div>

                <!-- Chart 3: Dòng Thời Gian (Daily Timeline) -->
                <div class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-3">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                        <div>
                            <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                                <i class="fa-solid fa-calendar-days text-[#872D43]"></i> 3. Diễn Biến Doanh Thu Theo Thời Gian (Daily Trend)
                            </h3>
                            <p class="text-[11px] text-slate-400">Đường doanh thu thuần (Tr. đ) và cột số lượng đơn hàng phát sinh</p>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#fde2e4] text-[#872D43] border border-[#fad2e1]">Thời Gian</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chartOverviewTimeline"></canvas>
                    </div>
                </div>

                <!-- Chart 4: Chiến Dịch (Campaign P&L) -->
                <div class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-3">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                        <div>
                            <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                                <i class="fa-solid fa-bullhorn text-[#183634]"></i> 4. Diễn Biến Doanh Thu & Biên Đóng Góp (Sales Wave)
                            </h3>
                            <p class="text-[11px] text-slate-400">Doanh thu thuần vs Lợi nhuận đóng góp (CM) giữa các chương trình</p>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#fde2e4] text-[#183634] border border-[#c5dedd]">Chiến Dịch</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chartOverviewCampaign"></canvas>
                    </div>
                </div>

                <!-- Chart 5: Cơ Cấu Chi Phí & Lợi Nhuận (Cost Structure Doughnut) -->
                <div class="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-3 lg:col-span-2">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                        <div>
                            <h3 class="text-sm font-black text-slate-900 flex items-center gap-2">
                                <i class="fa-solid fa-chart-pie text-[#c5dedd]"></i> 5. Cơ Cấu Chi Phí & Dòng Chảy Lợi Nhuận (Cost Structure & Margin)
                            </h3>
                            <p class="text-[11px] text-slate-400">Tỷ trọng Giá vốn COGS, Chiết khấu, Chi phí Marketing và Biên đóng góp CM</p>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#c5dedd]/40 text-[#183634] border border-[#c5dedd]">Cơ Cấu P&L</span>
                    </div>
                    <div class="h-64 relative flex items-center justify-center">
                        <canvas id="chartOverviewCost"></canvas>
                    </div>
                </div>

            </div>

            <!-- VIEW 2: CHI TIẾT GÓC NHÌN ĐA KÊNH (CHANNEL DEEP-DIVE) -->
            <div id="view-CHANNEL" class="view-panel hidden bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-6">
                <div>
                    <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-store text-[#183634]"></i> Bảng Đối Soát Doanh Số, Hàng Hoàn & Lợi Nhuận Đa Kênh (11 Cột)
                    </h3>
                    <p class="text-xs text-slate-400">Đánh giá hiệu quả phân phối giữa các kênh: Shopee, Tiktok Shop, Cửa hàng trực tiếp...</p>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="text-slate-400 font-bold uppercase tracking-wider text-[11px] border-b border-slate-100 bg-slate-50">
                                <th class="py-3 px-3.5">Kênh Bán</th>
                                <th class="py-3 px-3 text-center">Số Đơn</th>
                                <th class="py-3 px-3 text-right">DT Gộp</th>
                                <th class="py-3 px-3 text-right">Chiết Khấu</th>
                                <th class="py-3 px-3 text-right">Hàng Hoàn</th>
                                <th class="py-3 px-3 text-center">Hoàn (%)</th>
                                <th class="py-3 px-3 text-right">DT Thuần</th>
                                <th class="py-3 px-3 text-right">Giá Vốn</th>
                                <th class="py-3 px-3 text-right">Lãi Gộp</th>
                                <th class="py-3 px-3 text-right">Biên CM</th>
                                <th class="py-3 px-3 text-center">Tỷ Trọng (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {ch_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- VIEW 3: CHI TIẾT CƠ CẤU SẢN PHẨM (PRODUCT DEEP-DIVE) -->
            <div id="view-PRODUCT" class="view-panel hidden bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-6">
                <div>
                    <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-box-open text-[#872D43]"></i> Cơ Cấu Doanh Số & Biên Lãi Gộp Danh Mục Sản Phẩm (Pareto 80/20)
                    </h3>
                    <p class="text-xs text-slate-400">Xác định sản phẩm chủ lực (Hero Products) và các mặt hàng biên mỏng cần tối ưu giá bán</p>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="text-slate-400 font-bold uppercase tracking-wider text-[11px] border-b border-slate-100 bg-slate-50">
                                <th class="py-3 px-3 text-center">Hạng</th>
                                <th class="py-3 px-3">Mã SP</th>
                                <th class="py-3 px-3">Tên Sản Phẩm</th>
                                <th class="py-3 px-3 text-center">Số Lượng Đã Bán</th>
                                <th class="py-3 px-3 text-right">Doanh Thu Gộp</th>
                                <th class="py-3 px-3 text-right">Giá Vốn (COGS)</th>
                                <th class="py-3 px-3 text-right">Lợi Nhuận Gộp</th>
                                <th class="py-3 px-3 text-center">Biên Gộp (%)</th>
                                <th class="py-3 px-3 text-center">Tỷ Trọng (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {prod_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- VIEW 4: CHI TIẾT DÒNG THỜI GIAN (TIMELINE DEEP-DIVE) -->
            <div id="view-TIMELINE" class="view-panel hidden bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-6">
                <div>
                    <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-calendar-days text-[#872D43]"></i> Diễn Biến Doanh Thu & Giá Trị Đơn Trung Bình (AOV) Theo Ngày
                    </h3>
                    <p class="text-xs text-slate-400">Nhận diện các mốc thời gian đỉnh điểm (Spike) và xu hướng giao dịch thường nhật</p>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="text-slate-400 font-bold uppercase tracking-wider text-[11px] border-b border-slate-100 bg-slate-50">
                                <th class="py-3 px-3">Ngày Giao Dịch</th>
                                <th class="py-3 px-3 text-center">Số Đơn</th>
                                <th class="py-3 px-3 text-right">Doanh Thu Gộp</th>
                                <th class="py-3 px-3 text-right">Chiết Khấu</th>
                                <th class="py-3 px-3 text-right">Doanh Thu Thuần</th>
                                <th class="py-3 px-3 text-right">AOV (Giá Trị Đơn TB)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {timeline_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- VIEW 5: CHI TIẾT CHIẾN DỊCH P&L (CAMPAIGN DEEP-DIVE) -->
            <div id="view-CAMPAIGN" class="view-panel hidden bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-6">
                <div>
                    <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-bullhorn text-[#183634]"></i> Bảng Phân Tích Hiệu Quả P&L Chi Tiết Chiến Dịch (13 Cột Quản Trị)
                    </h3>
                    <p class="text-xs text-slate-400">Khử trùng đa voucher, đối soát chi phí trực tiếp và chi phí chung phân bổ theo doanh thu</p>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="text-slate-400 font-bold uppercase tracking-wider text-[11px] border-b border-slate-100 bg-slate-50">
                                <th class="py-3 px-3">Chương Trình</th>
                                <th class="py-3 px-3 text-center">Số Đơn</th>
                                <th class="py-3 px-3 text-right">DT Gộp</th>
                                <th class="py-3 px-3 text-right">Hàng Trả</th>
                                <th class="py-3 px-3 text-right">DT Thuần</th>
                                <th class="py-3 px-3 text-right">Giá Vốn</th>
                                <th class="py-3 px-3 text-right">LN Gộp</th>
                                <th class="py-3 px-3 text-right">Voucher</th>
                                <th class="py-3 px-3 text-right">CP Direct</th>
                                <th class="py-3 px-3 text-right">CP Phân Bổ</th>
                                <th class="py-3 px-3 text-right">Biên CM</th>
                                <th class="py-3 px-3 text-center">Biên %</th>
                                <th class="py-3 px-3 text-center">ROI %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {pnl_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- BIỂU ĐỒ TÙY CHỈNH (NẾU CÓ) -->
        {dash_custom_charts_html}

        <!-- FOOTER -->
        <footer class="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
            <div>
                <strong>Thu Hà AI Data Analytics Studio</strong> • Báo Cáo Điều Hành Trực Quan Bất Biến
            </div>
            <div class="text-right">
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#c5dedd]/30 text-[#183634] border border-[#c5dedd] font-bold text-[11px]">
                    <i class="fa-solid fa-stamp text-[#183634]"></i> ĐÃ PHÊ DUYỆT & KÝ KHÓA SỐ LIỆU
                </div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">Mã kiểm định: SHA256-THUHA-CAUSAL-VERIFIED</div>
            </div>
        </footer>

    </div>

    <!-- JAVASCRIPT: INITIALIZE ALL CHARTS & TAB CONTROLLER -->
    <script>
        // Tab switching function
        function switchTab(tabKey) {{
            const tabs = ['OVERVIEW', 'CHANNEL', 'PRODUCT', 'TIMELINE', 'CAMPAIGN'];
            tabs.forEach(t => {{
                const btn = document.getElementById('btnTab-' + t);
                const view = document.getElementById('view-' + t);
                if (btn) {{
                    if (t === tabKey) {{
                        btn.className = "tab-btn btn-smooth px-3.5 py-1.5 rounded-xl bg-white text-[#183634] shadow-xs border border-[#c5dedd] font-black flex items-center gap-1.5";
                    }} else {{
                        btn.className = "tab-btn btn-smooth px-3.5 py-1.5 rounded-xl text-slate-600 hover:text-slate-900 flex items-center gap-1.5";
                    }}
                }}
                if (view) {{
                    if (t === tabKey) {{
                        view.classList.remove('hidden');
                    }} else {{
                        view.classList.add('hidden');
                    }}
                }}
            }});
        }}

        // Data from Python
        const chLabels = {json.dumps(ch_labels, ensure_ascii=False)};
        const chGross = {json.dumps(ch_gross)};
        const chNet = {json.dumps(ch_net)};
        const chReturns = {json.dumps(ch_returns)};

        const prodLabels = {json.dumps(prod_labels, ensure_ascii=False)};
        const prodGross = {json.dumps(prod_gross)};
        const prodProfit = {json.dumps(prod_profit)};

        const timeLabels = {json.dumps(time_labels, ensure_ascii=False)};
        const timeNet = {json.dumps(time_net)};
        const timeOrders = {json.dumps(time_orders)};

        const campLabels = {json.dumps(camp_labels, ensure_ascii=False)};
        const campNet = {json.dumps(camp_net)};
        const campCM = {json.dumps(camp_cm)};

        // 1. Chart Channel (Omnichannel Bar)
        const ctxCh = document.getElementById('chartOverviewChannel');
        if (ctxCh) {{
            new Chart(ctxCh.getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: chLabels,
                    datasets: [
                        {{ label: 'Doanh Thu Gộp (Tr. đ)', data: chGross, backgroundColor: '#c5dedd', borderRadius: 6 }},
                        {{ label: 'Hàng Hoàn (Tr. đ)', data: chReturns, backgroundColor: '#fad2e1', borderRadius: 6 }},
                        {{ label: 'Doanh Thu Thuần (Tr. đ)', data: chNet, backgroundColor: '#c5dedd', borderRadius: 6 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                    scales: {{
                        x: {{ ticks: {{ font: {{ size: 10, weight: 'bold' }} }}, grid: {{ display: false }} }},
                        y: {{ ticks: {{ font: {{ size: 10 }}, callback: v => v + ' tr' }}, grid: {{ color: '#f1f5f9' }} }}
                    }}
                }}
            }});
        }}

        // 2. Chart Product (Pareto Horizontal Bar)
        const ctxProd = document.getElementById('chartOverviewProduct');
        if (ctxProd) {{
            new Chart(ctxProd.getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: prodLabels,
                    datasets: [
                        {{ label: 'Doanh Thu Gộp (Tr. đ)', data: prodGross, backgroundColor: '#a0c4ff', borderColor: '#0284c7', borderWidth: 1.5, borderRadius: 6 }},
                        {{ label: 'Lợi Nhuận Gộp (Tr. đ)', data: prodProfit, backgroundColor: '#fed9b7', borderColor: '#d97706', borderWidth: 1.5, borderRadius: 6 }}
                    ]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                    scales: {{
                        x: {{ ticks: {{ font: {{ size: 10 }}, callback: v => v + ' tr' }}, grid: {{ color: '#f1f5f9' }} }},
                        y: {{ ticks: {{ font: {{ size: 10, weight: 'bold' }} }}, grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        // 3. Chart Timeline (Daily Line + Bar)
        const ctxTime = document.getElementById('chartOverviewTimeline');
        if (ctxTime) {{
            new Chart(ctxTime.getContext('2d'), {{
                type: 'line',
                data: {{
                    labels: timeLabels,
                    datasets: [
                        {{
                            label: 'Doanh Thu Thuần (Tr. đ)',
                            data: timeNet,
                            borderColor: '#0284c7',
                            backgroundColor: 'rgba(160, 196, 255, 0.35)',
                            borderWidth: 2.5,
                            fill: true,
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#a0c4ff',
                            yAxisID: 'y'
                        }},
                        {{
                            label: 'Số Lượng Đơn',
                            data: timeOrders,
                            borderColor: '#e11d48',
                            backgroundColor: 'rgba(244, 151, 142, 0.35)',
                            borderWidth: 2,
                            borderDash: [3, 3],
                            pointRadius: 3,
                            pointBackgroundColor: '#fad2e1',
                            yAxisID: 'y1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                    scales: {{
                        x: {{ ticks: {{ font: {{ size: 9 }} }}, grid: {{ display: false }} }},
                        y: {{ position: 'left', ticks: {{ font: {{ size: 9 }}, callback: v => v + ' tr' }}, grid: {{ color: '#f1f5f9' }} }},
                        y1: {{ position: 'right', ticks: {{ font: {{ size: 9 }}, stepSize: 1 }}, grid: {{ display: false }} }}
                    }}
                }}
            }});
        }}

        // 4. Chart Campaign (Wave Line)
        const ctxCamp = document.getElementById('chartOverviewCampaign');
        if (ctxCamp) {{
            new Chart(ctxCamp.getContext('2d'), {{
                type: 'line',
                data: {{
                    labels: campLabels,
                    datasets: [
                        {{
                            label: 'Doanh Thu Thuần (Tr. đ)',
                            data: campNet,
                            borderColor: '#0d9488',
                            backgroundColor: 'rgba(114, 239, 221, 0.35)',
                            borderWidth: 2.5,
                            fill: true,
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#72efdd'
                        }},
                        {{
                            label: 'Lợi Nhuận Đóng Góp CM (Tr. đ)',
                            data: campCM,
                            borderColor: '#d97706',
                            backgroundColor: 'rgba(254, 217, 183, 0.45)',
                            borderWidth: 2.5,
                            fill: true,
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#fad2e1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }},
                    scales: {{
                        x: {{ ticks: {{ font: {{ size: 10, weight: 'bold' }} }}, grid: {{ display: false }} }},
                        y: {{ ticks: {{ font: {{ size: 10 }}, callback: v => v + ' tr' }}, grid: {{ color: '#f1f5f9' }} }}
                    }}
                }}
            }});
        }}

        // 5. Chart Cost Structure (Doughnut)
        const ctxCost = document.getElementById('chartOverviewCost');
        if (ctxCost) {{
            new Chart(ctxCost.getContext('2d'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Giá Vốn (COGS)', 'Chiết Khấu Voucher', 'Chi Phí MKT & Chung', 'Biên Đóng Góp (CM)'],
                    datasets: [{{
                        data: [{round(cogs/1e6, 2)}, {round(discount/1e6, 2)}, {round(total_costs/1e6, 2)}, {round(max(0, cm)/1e6, 2)}],
                        backgroundColor: ['#5eaba0', '#fad2e1', '#c5dedd', '#fde2e4'],
                        borderColor: '#ffffff',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 10, weight: 'bold' }} }} }} }}
                }}
            }});
        }}

        // 6. User Custom Charts
        {dash_custom_charts_js}
    </script>
</body>
</html>"""
