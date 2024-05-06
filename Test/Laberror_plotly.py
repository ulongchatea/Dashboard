import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os

# 파일이 존재하는 디렉토리 경로
dir_path = "/Users/BRADEN/Desktop"

# 파일 이름
file_name = 'lab error.csv'

# 절대 경로 생성
file_path = os.path.join(dir_path, file_name)

# CSV 데이터 로드
df = pd.read_csv(file_path)

# 제품명 분리
df['제품/원료/원자재'] = df['제품/원료/원자재'].str.split('+')

# HTML 파일에 추가할 문자열
html_content = ''

# 1. 발생유형(대분류) 별 랩에러 건수 시각화
error_types = df['대분류'].value_counts()
fig = px.bar(x=error_types.index, y=error_types.values, color=error_types.index, title='발생유형(대분류) 별 랩에러 건수', color_discrete_sequence=px.colors.qualitative.Safe)
html_content += fig.to_html(full_html=False)

# 2. 월별 랩에러 발생 추이 시각화
error_trend = df.groupby(pd.to_datetime(df['보고일자']).dt.month).size().reset_index()
error_trend.columns = ['월', '랩에러 건수']
fig = px.line(error_trend, x='월', y='랩에러 건수', title='월별 랩에러 발생 추이', markers=True)
html_content += fig.to_html(full_html=False)

# 3. 원인별 랩에러 건수 시각화
cause_counts = df['중분류'].value_counts()
fig = px.pie(names=cause_counts.index, values=cause_counts.values, title='원인별 랩에러 건수')
html_content += fig.to_html(full_html=False)

# 4. 제품/원자재별 랩에러 비율 시각화
product_errors = df.explode('제품/원료/원자재')['제품/원료/원자재'].value_counts(normalize=True).reset_index()
product_errors.columns = ['제품/원자재', '랩에러 비율']
product_errors['랩에러 비율'] *= 100
fig = px.bar(product_errors, x='제품/원자재', y='랩에러 비율', title='제품/원자재별 랩에러 비율', color='제품/원자재', color_discrete_sequence=px.colors.qualitative.Safe)
html_content += fig.to_html(full_html=False)

# 5. 기기별 랩에러 발생 건수 시각화
device_counts = df['기기번호'].value_counts().reset_index()
device_counts.columns = ['기기', '랩에러 건수']
fig = px.bar(device_counts, x='기기', y='랩에러 건수', title='기기별 랩에러 발생 건수', color='기기', color_discrete_sequence=px.colors.qualitative.Safe)
html_content += fig.to_html(full_html=False)

# 6. 위험도 분류별 랩에러 분포 시각화
severity_counts = df['Major/Minor'].value_counts()
fig = px.pie(names=severity_counts.index, values=severity_counts.values, title='위험도 분류별 랩에러 분포')
html_content += fig.to_html(full_html=False)

# 7. 상세 원인별 랩에러 건수 시각화
detailed_cause_counts = df['상세내용'].value_counts()
fig = px.bar(x=detailed_cause_counts.index, y=detailed_cause_counts.values, title='상세 원인별 랩에러 건수', color=detailed_cause_counts.index, color_discrete_sequence=px.colors.qualitative.Safe)
html_content += fig.to_html(full_html=False)

# 8. 월별 Major, Minor 위험도 분포 시각화
monthly_risk = df.groupby([pd.to_datetime(df['보고일자']).dt.month, df['Major/Minor']]).size().reset_index()
monthly_risk.columns = ['월', '위험도', '랩에러 건수']
fig = px.bar(monthly_risk, x='월', y='랩에러 건수', color='위험도', title='월별 Major, Minor 위험도 랩에러 분포', barmode='group', color_discrete_sequence=px.colors.qualitative.Safe)
fig.update_xaxes(tickvals=monthly_risk['월'].unique(), ticktext=[f'{month}월' for month in monthly_risk['월'].unique()])
html_content += fig.to_html(full_html=False)

# 파일에 HTML 내용 쓰기 (UTF-8 인코딩 사용)
with open('laberror_visualizations.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
