"""Streamlit UI for contract audit web app."""
import streamlit as st
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.services.extractor import extract_text_from_docx, extract_text_from_pdf
from app.services.combined_engine import CombinedRulesEngine
from app.services.redline_docx import RedlineGenerator
from datetime import datetime
import re


def extract_document_info(text):
    """Extract document information for 5 cards."""
    info = {}
    
    # 1. 문서유형
    if '용역' in text:
        info['doc_type'] = '용역계약'
    elif '개발' in text or '소프트웨어' in text:
        info['doc_type'] = '개발계약'
    elif '공급' in text or '납품' in text:
        info['doc_type'] = '공급계약'
    else:
        info['doc_type'] = '일반계약'
    
    # 2. 계약기간 (수정된 로직)
    # 명시적인 개월 수를 우선 처리
    explicit_period = re.search(r'([0-9]{1,2})\s*개월', text)
    if explicit_period:
        num = int(explicit_period.group(1))
        if num == 12:
            info['period'] = "1년"
        elif num > 12:
            years = num // 12
            months = num % 12
            if months > 0:
                info['period'] = f"{years}년 {months}개월"
            else:
                info['period'] = f"{years}년"
        else:
            info['period'] = f"{num}개월"
    else:
        # 년 단위 찾기
        year_match = re.search(r'([0-9]{1,2})\s*년', text)
        if year_match:
            num = int(year_match.group(1))
            info['period'] = f"{num}년"
        else:
            # 날짜 형식으로 찾기 (개월 수 계산)
            date_match = re.search(r'([0-9]{4})[.-]([0-9]{1,2})[.-]([0-9]{1,2})[^0-9]*([0-9]{4})[.-]([0-9]{1,2})[.-]([0-9]{1,2})', text)
            if date_match:
                start_year = int(date_match.group(1))
                start_month = int(date_match.group(2))
                end_year = int(date_match.group(4))
                end_month = int(date_match.group(5))
                
                # 개월 수 계산
                if start_year == end_year:
                    total_months = end_month - start_month + 1
                else:
                    total_months = (end_year - start_year) * 12 + (end_month - start_month) + 1
                
                if total_months == 12:
                    info['period'] = "1년"
                elif total_months > 12:
                    years = total_months // 12
                    months = total_months % 12
                    if months > 0:
                        info['period'] = f"{years}년 {months}개월"
                    else:
                        info['period'] = f"{years}년"
                else:
                    info['period'] = f"{total_months}개월"
            else:
                info['period'] = '—'
    
    # 3. 계약금액
    amount_match = re.search(r'([0-9,]+)\s*원', text)
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '')
        try:
            amount = int(amount_str)
            if amount >= 100000000:
                info['amount'] = f"{amount//100000000}억원"
            elif amount >= 10000:
                info['amount'] = f"{amount//10000}만원"
            else:
                info['amount'] = f"{amount:,}원"
        except:
            info['amount'] = '—'
    else:
        info['amount'] = '—'
    
    # 4. 발주자 (회사명 우선 추출)
    client_patterns = [
        # 회사명 + 역할 패턴
        r'(㊩[^\(\)\n]{1,20}|[A-Za-z0-9\s]{2,20}주식회사|[^\(\)\n]{2,20}주식회사|[^\(\)\n]{2,20}회사)\s*\([^\)]*(위탁인|갑|발주자|주문자)[^\)]*\)',
        # 역할 + 회사명 패턴
        r'(위탁인|갑|발주자|주문자)[^\n]*?(㊩[^\(\)\n,]{1,20}|[A-Za-z0-9\s]{2,20}주식회사|[^\(\)\n,]{2,20}주식회사|[^\(\)\n,]{2,20}회사)',
        # 기본 패턴
        r'발주자[:\s]*([^\n,을갑에서는]{2,30})',
        r'갑[:\s]*([^\n,을갑에서는]{2,30})'
    ]
    
    for i, pattern in enumerate(client_patterns):
        match = re.search(pattern, text)
        if match:
            if i == 0:  # 회사명 + 역할
                info['client'] = match.group(1).strip()
            elif i == 1:  # 역할 + 회사명
                info['client'] = match.group(2).strip()
            else:  # 기본
                info['client'] = match.group(1).strip()
            break
    else:
        info['client'] = '—'
    
    # 5. 공급자 (회사명 우선 추출)
    supplier_patterns = [
        # 회사명 + 역할 패턴
        r'(㊩[^\(\)\n]{1,20}|[A-Za-z0-9\s]{2,20}주식회사|[^\(\)\n]{2,20}주식회사|[^\(\)\n]{2,20}회사)\s*\([^\)]*(수탁인|을|공급자|수급자)[^\)]*\)',
        # 역할 + 회사명 패턴
        r'(수탁인|을|공급자|수급자)[^\n]*?(㊩[^\(\)\n,]{1,20}|[A-Za-z0-9\s]{2,20}주식회사|[^\(\)\n,]{2,20}주식회사|[^\(\)\n,]{2,20}회사)',
        # 기본 패턴
        r'공급자[:\s]*([^\n,을갑에서는]{2,30})',
        r'을[:\s]*([^\n,을갑에서는]{2,30})'
    ]
    
    for i, pattern in enumerate(supplier_patterns):
        match = re.search(pattern, text)
        if match:
            if i == 0:  # 회사명 + 역할
                info['supplier'] = match.group(1).strip()
            elif i == 1:  # 역할 + 회사명
                info['supplier'] = match.group(2).strip()
            else:  # 기본
                info['supplier'] = match.group(1).strip()
            break
    else:
        info['supplier'] = '—'
    
    return info


def main():
    st.set_page_config(
        page_title="계약서 자동 검수",
        page_icon="📄",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .doc-card {
        background: white;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .card-label {
        font-size: 12px;
        color: #666;
        margin-bottom: 4px;
        font-weight: normal;
    }
    .card-value {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .card-value-missing {
        font-size: 20px;
        font-weight: bold;
        color: #999;
    }
    .status-chip {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    .chip-required {
        background-color: #ffebee;
        color: #c62828;
    }
    .chip-recommended {
        background-color: #fff3e0;
        color: #ef6c00;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📄 계약서 자동 검수 시스템")
    
    st.subheader("📁 계약서 업로드")
    
    # File upload
    uploaded_file = st.file_uploader(
        "계약서 파일을 업로드하세요",
        type=['docx', 'pdf']
    )
    
    if uploaded_file is not None:
        # Extract text
        file_bytes = uploaded_file.getvalue()
        
        try:
            if uploaded_file.name.endswith('.docx'):
                text = extract_text_from_docx(file_bytes)
                is_scanned = False
                file_type = "DOCX"
            else:  # PDF
                text, is_scanned = extract_text_from_pdf(file_bytes)
                file_type = "PDF"
            
            # Show extraction success
            st.success(f"✅ 텍스트 추출 완료 ({file_type}, {len(text):,}자)")
            
            # Scanned PDF warning
            if is_scanned:
                st.warning("⚠️ 스캔된 PDF로 감지되었습니다. 텍스트 추출이 제한적일 수 있습니다.")
            
            if len(text.strip()) < 100:
                st.error("추출된 텍스트가 너무 짧습니다. 다른 파일을 시도해보세요.")
                return
            
            # Document info cards (2x2+1 grid)
            st.subheader("📊 문서 정보")
            doc_info = extract_document_info(text)
            
            # First row
            col1, col2, col3 = st.columns(3)
            
            with col1:
                value = doc_info['doc_type']
                st.markdown(f"""
                <div class="doc-card">
                    <div class="card-label">문서유형</div>
                    <div class="card-value" title="{value}">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                value = doc_info['period']
                is_missing = value == '—'
                css_class = 'card-value-missing' if is_missing else 'card-value'
                st.markdown(f"""
                <div class="doc-card">
                    <div class="card-label">계약기간</div>
                    <div class="{css_class}" title="{value}">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                value = doc_info['amount']
                is_missing = value == '—'
                css_class = 'card-value-missing' if is_missing else 'card-value'
                st.markdown(f"""
                <div class="doc-card">
                    <div class="card-label">계약금액</div>
                    <div class="{css_class}" title="{value}">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            

            
            st.markdown("---")
            
            # Evaluate rules (Internal + Legal)
            rules_engine = CombinedRulesEngine()
            audit_result = rules_engine.evaluate_contract(text)
            
            # Filter toggle
            show_compliant = st.checkbox("✅ 적합 항목 보기", value=False)
            
            # Enhanced counter chips
            total_violations = audit_result.required_violations + audit_result.recommended_violations
            
            if total_violations > 0:
                st.markdown(f"""
                <div style="margin: 16px 0;">
                    <span style="font-size: 16px; font-weight: bold; margin-right: 12px;">📊 총 {audit_result.total_rules}개 규칙</span>
                    <span class="status-chip chip-required">❌ 필수 위반 {audit_result.required_violations}건</span>
                    <span class="status-chip chip-recommended">⚠️ 권고 위반 {audit_result.recommended_violations}건</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success(f"🎉 총 {audit_result.total_rules}개 규칙 모두 적합!")
            
            # Top violations with clickable items
            violations = [r for r in audit_result.rule_results if r.status != "present"]
            if violations:
                st.subheader("🔍 주요 위반사항 (Top 3)")
                
                # Add JavaScript for scrolling
                st.markdown("""
                <script>
                function scrollToRule(ruleId) {
                    setTimeout(() => {
                        const elements = document.querySelectorAll('td');
                        for (let el of elements) {
                            if (el.textContent === ruleId) {
                                el.parentElement.style.backgroundColor = '#fff3cd';
                                el.parentElement.scrollIntoView({behavior: 'smooth', block: 'center'});
                                setTimeout(() => {
                                    el.parentElement.style.backgroundColor = '';
                                }, 3000);
                                break;
                            }
                        }
                    }, 100);
                }
                </script>
                """, unsafe_allow_html=True)
                
                for i, violation in enumerate(violations[:3], 1):
                    severity_emoji = "●" if violation.severity == "required" else "○"
                    status_text = "누락" if violation.status == "missing" else "보완"
                    
                    # Clickable violation item
                    st.markdown(f"""
                    <div onclick="scrollToRule('{violation.rule_id}')" style="
                        cursor: pointer; 
                        padding: 8px; 
                        border-radius: 4px; 
                        margin: 4px 0;
                        background: #f8f9fa;
                        border-left: 3px solid {'#dc3545' if violation.severity == 'required' else '#fd7e14'};
                    ">
                        <strong>{i}. {severity_emoji} {violation.title}</strong> ({status_text})<br>
                        <small>💡 {violation.suggestion[:80]}{'...' if len(violation.suggestion) > 80 else ''}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Detailed results table with legend
            st.subheader("📋 규칙별 검토 결과")
            
            # Legend
            st.markdown("<p style='color: black; font-size: 12px;'>📊 <strong>범례</strong>: ❌누락(빨강) ⚠️보완(주황) ✅적합(초록) | ●필수 ○권고</p>", unsafe_allow_html=True)
            

            
            # Filter results based on toggle
            filtered_results = audit_result.rule_results
            if not show_compliant:
                filtered_results = [r for r in filtered_results if r.status != "present"]
            
            # Sort: required > recommended, missing > insufficient > present
            def sort_key(result):
                severity_order = {"required": 0, "recommended": 1}
                status_order = {"missing": 0, "insufficient": 1, "present": 2}
                return (severity_order[result.severity], status_order[result.status], result.rule_id)
            
            sorted_results = sorted(filtered_results, key=sort_key)
            
            table_data = []
            for result in sorted_results:
                status_map = {"present": "✅ 적합", "insufficient": "⚠️ 보완", "missing": "❌ 누락"}
                severity_map = {"required": "● 필수", "recommended": "○ 권고"}
                
                # Color coding for violations (removed unused row_style)
                
                table_data.append({
                    "ID": result.rule_id,
                    "검토 항목": result.title,
                    "중요도": severity_map[result.severity],
                    "결과": status_map[result.status],
                    "권장 수정사항": result.suggestion
                })
            
            if table_data:
                st.dataframe(table_data, use_container_width=True)
            else:
                st.info("표시할 결과가 없습니다. '적합 항목 보기'를 활성화하세요.")
            
            # Generate modified DOCX
            if uploaded_file.name.endswith('.docx'):
                st.subheader("📥 수정 파일 다운로드")
                
                with st.spinner("수정 파일을 생성하는 중..."):
                    redline_gen = RedlineGenerator()
                    redline_bytes = redline_gen.generate_redline_docx(file_bytes, audit_result)
                
                # Generate filename based on original
                base_name = uploaded_file.name.rsplit('.', 1)[0]
                new_filename = f"{base_name}_수정.docx"
                
                # Enhanced download UI
                col_download, col_info = st.columns([1, 2])
                
                with col_download:
                    st.download_button(
                        label="📥 수정 파일 다운로드",
                        data=redline_bytes,
                        file_name=new_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary",
                        use_container_width=True
                    )
                
                with col_info:
                    st.caption(f"📄 파일명: {new_filename}")
                    st.caption(f"📊 수정 대상: {total_violations}건 위반사항")
            else:
                st.info("💡 수정 파일 생성은 DOCX 파일에서만 지원됩니다.")
        
        except Exception as e:
            st.error(f"❌ 파일 처리 중 오류가 발생했습니다: {str(e)}")
    



if __name__ == "__main__":
    main()