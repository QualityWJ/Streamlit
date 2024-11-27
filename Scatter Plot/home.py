import streamlit as st
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title = "Scatter Plot",
    page_icon="📈")

st.title('산점도')
st.sidebar.title('Upload Data')

NORMAL_DATA = None
CLAIM_DATA = None

if temp1 := st.sidebar.file_uploader("전체 데이터를 업로드 하세요. (CSV 파일)", type = ['csv']) :
     with st.spinner("전체 데이터 업로드 중...") :
        st.sidebar.success("업로드 완료")

if temp2 := st.sidebar.file_uploader("하자 데이터를 업로드 하세요. (CSV 파일)", type = ['csv']) :
     with st.spinner("하자 데이터 업로드 중...") :
        st.sidebar.success("업로드 완료")

st.sidebar.caption("Create By WJ")

st.markdown("""
<style>
.h1 {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html = True)

st.markdown("""
<style>
.h2 {
    font-size:18px !important;
}
</style>
""", unsafe_allow_html = True)

st.markdown("""
<style>
.h3 {
    font-size:16px !important;
}
</style>
""", unsafe_allow_html = True)

def Improvement(num, color) :
    col10, col11, col12 = st.columns(3)
    with st.form(f"{num}차 개선 진행") :
        Fix_Text = col10.text_input(f"{num}. 개선 사항을 입력해주세요. (10자 이내)", value = f'{num}차 개선', max_chars = 10)
        Fix_Date = "2018-01-01"

        Fix_Date = str(col11.date_input(f"{num}. 개선 적용 일자를 입력해주세요.", value = datetime.date(2022, 1, 1)))

        loc = col12.radio(label = f"{num}. Text 위치", options = ['top right', 'top left'])

        fig.add_vline(x = datetime.datetime.strptime(Fix_Date, "%Y-%m-%d").timestamp() * 1000, line_width = 3, line_dash = "dash", line_color = color, 
                    annotation_text = f"&nbsp; <b>{Fix_Text} <br> &nbsp;{Fix_Date}</b>", annotation_position = loc, annotation_font_color = color, annotation_font_size = 12)

if (temp1 is not None) & (temp2 is not None) :

    NORMAL_DATA = pd.read_csv(temp1)
    CLAIM_DATA = pd.read_csv(temp2)

    col1, col2 = st.columns(2)
    col6, col7, col8, col9 = st.columns(4)
    col3, col4, col5 = st.columns(3)

    with st.form("Filtering") :

        NORMAL_OPH = col6.text_input("전체 데이터 가동시간 Column", value = 'Total Operation Hours (TMS)')
        NORMAL_Date = col7.text_input("전체 데이터 Date Column Default : 생산일자", value = 'Created Date')
        CLAIM_OPH = col8.text_input("하자 데이터 가동시간 Column", value = 'Operating Hours')
        CLAIM_Date = col9.text_input("하자 데이터 Date Column Default : 생산일자", value = 'Equipment Created Date')

        NORMAL_DATA.rename(inplace = True, columns = {'﻿"Equipment Number"' : "Equipment Number", NORMAL_OPH : "OPH", NORMAL_Date : "일자"})
        NORMAL_DATA['정상/하자'] = "정상"

        CLAIM_DATA.rename(inplace = True, columns = {CLAIM_OPH : "OPH", CLAIM_Date : "일자"})
        CLAIM_DATA['정상/하자'] = "하자"

        Date_Start = col3.date_input("일자 Start", value = datetime.date(2022, 1, 1))
        Date_End = col4.date_input("일자 End", value = datetime.date.today())
        Time_End = col5.number_input("시간 End", 0, 10000, value = 2500)
        
        col1.metric(label = '전체 장비 수', value = f'{str(NORMAL_DATA.loc[(NORMAL_DATA['일자'] >= datetime.datetime.strftime(Date_Start, format = "%Y-%m-%d")) & 
                                                                          (NORMAL_DATA['일자'] <= datetime.datetime.strftime(Date_End, format = "%Y-%m-%d")) &
                                                                          (NORMAL_DATA['OPH'] > 0) & 
                                                                          (NORMAL_DATA['OPH'] <= Time_End), :].shape[0] + 1)} 대')
        col2.metric(label = '하자 장비 수', value = f'{str(CLAIM_DATA.loc[(NORMAL_DATA['일자'] >= datetime.datetime.strftime(Date_Start, format = "%Y-%m-%d")) & 
                                                                               (NORMAL_DATA['일자'] <= datetime.datetime.strftime(Date_End, format = "%Y-%m-%d")) &
                                                                               (NORMAL_DATA['OPH'] > 0) & 
                                                                               (NORMAL_DATA['OPH'] <= Time_End), :].shape[0] + 1)} 대')

    # 그래프 생성
    fig = go.Figure()

    Improve = st.radio(label = "개선 진행이 몇 번 이뤄졌나요?", options = ['0번', '1번(1차 개선 완료)', '2번(2차 개선 완료)', '3번(3차 개선 완료)'], horizontal = True)
    if Improve == '0번' :
        pass
    elif Improve == '1번(1차 개선 완료)' :
        Improvement(1, "rgb(200, 0, 0)")
    elif Improve == '2번(2차 개선 완료)' :
        Improvement(1, "rgb(0, 50, 200)")
        Improvement(2, "rgb(200, 0, 0)")
    else :
        Improvement(1, "rgb(0, 50, 200)")
        Improvement(2, "rgb(0, 50, 200)")
        Improvement(3, "rgb(200, 0, 0)")

    fig.add_trace(go.Scatter(x = NORMAL_DATA['일자'], y = NORMAL_DATA['OPH'], name = "정상", mode = "markers", marker_color = "rgb(180, 180, 180)"))
    fig.add_trace(go.Scatter(x = CLAIM_DATA['일자'], y = CLAIM_DATA['OPH'], name = "하자", mode = "markers", marker_color = "red"))
    
    fig.update_xaxes(title_text = '일자', title_font_color = "rgb(0, 0, 0)", title_font_size = 20, tickfont_size = 15, range = [Date_Start, Date_End], tickfont_color = "rgb(0, 0, 0)")
    fig.update_yaxes(title_text = '가동시간', title_font_color = "rgb(0, 0, 0)", title_font_size = 20, tickfont_size = 15, range = [0, Time_End], tickfont_color = "rgb(0, 0, 0)")

    fig.update_layout(template = "plotly", title = "Scatter plot", title_font_size = 30, title_font_family = "Times New Roman", title_x = 0.5)
    fig.update_layout(margin = dict(l = 100, r = 100, t = 100, b = 50), width = 2000, height = 600)
    fig.update_layout(legend_font_size = 15)

    fig.update_traces(hovertemplate = '일자 : %{x:YYYY-mm-dd} <br>'+
                                    '가동시간: %{y:.0f}시간')
    fig.update_layout(
            hoverlabel_bgcolor="white",
            hoverlabel_font_size=15,
            hoverlabel_font_color='red')

    fig.update_xaxes(showspikes = True, spikecolor = "black", spikesnap = "cursor", spikemode = "across", spikethickness = 1)
    fig.update_yaxes(showspikes = True, spikecolor = "black", spikethickness = 1)

    if st.button('산점도 생성') :
        with st.spinner("산점도 생성 중...") :
            st.plotly_chart(fig, use_container_width = True)

elif (temp1 is not None) & (temp2 is None) :

    NORMAL_DATA = pd.read_csv(temp1)

    col1, col2 = st.columns(2)
    col6, col7, col8, col9 = st.columns(4)
    col3, col4, col5 = st.columns(3)

    with st.form("Filtering") :

        NORMAL_OPH = col6.text_input("전체 데이터 가동시간 Column", value = 'Total Operation Hours (TMS)')
        NORMAL_Date = col7.text_input("전체 데이터 Date Column Default : 생산일자", value = 'Created Date')

        NORMAL_DATA.rename(inplace = True, columns = {'﻿"Equipment Number"' : "Equipment Number", NORMAL_OPH : "OPH", NORMAL_Date : "일자"})

        Date_Start = col3.date_input("일자 Start", value = datetime.date(2022, 1, 1))
        Date_End = col4.date_input("일자 End", value = datetime.date.today())
        Time_End = col5.number_input("시간 End", 0, 10000, value = 2500)
        
        col1.metric(label = '전체 장비 수', value = f'{str(NORMAL_DATA.loc[(NORMAL_DATA['일자'] >= datetime.datetime.strftime(Date_Start, format = "%Y-%m-%d")) & 
                                                                          (NORMAL_DATA['일자'] <= datetime.datetime.strftime(Date_End, format = "%Y-%m-%d")) &
                                                                          (NORMAL_DATA['OPH'] > 0) & 
                                                                          (NORMAL_DATA['OPH'] <= Time_End), :].shape[0] + 1)} 대')

    # 그래프 생성
    fig = go.Figure()

    fig.add_trace(go.Scatter(x = NORMAL_DATA['일자'], y = NORMAL_DATA['OPH'], mode = "markers", marker_color = "rgb(180, 180, 180)"))
    
    fig.update_xaxes(title_text = '일자', title_font_color = "rgb(0, 0, 0)", title_font_size = 20, tickfont_size = 15, range = [Date_Start, Date_End], tickfont_color = "rgb(0, 0, 0)")
    fig.update_yaxes(title_text = '가동시간', title_font_color = "rgb(0, 0, 0)", title_font_size = 20, tickfont_size = 15, range = [0, Time_End], tickfont_color = "rgb(0, 0, 0)")

    fig.update_layout(template = "plotly", title = "Scatter plot", title_font_size = 30, title_font_family = "Times New Roman", title_x = 0.5)
    fig.update_layout(margin = dict(l = 100, r = 100, t = 100, b = 50), width = 2000, height = 600)
    fig.update_layout(legend_font_size = 15)

    fig.update_traces(hovertemplate = '일자 : %{x:YYYY-mm-dd} <br>'+
                                    '가동시간: %{y:.0f}시간')
    fig.update_layout(
            hoverlabel_bgcolor="white",
            hoverlabel_font_size=15,
            hoverlabel_font_color='red')

    fig.update_xaxes(showspikes = True, spikecolor = "black", spikesnap = "cursor", spikemode = "across", spikethickness = 1)
    fig.update_yaxes(showspikes = True, spikecolor = "black", spikethickness = 1)

    if st.button('산점도 생성') :
        with st.spinner("산점도 생성 중...") :
            st.plotly_chart(fig, use_container_width = True)


else :
    st.markdown(f'<p class="h2">왼쪽 사이드바에 전체/하자 데이터를 모두 업로드 해주세요.</p>', unsafe_allow_html = True)


    

# Streamlit
# 코딩 부담없이 빠르고 간편하게 데이터를 효과적으로 시각화할 수 있도록 도와주는 Python 기반 Web Application Tool






