import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash import html, dcc
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

# 데이터 준비
error_types = df['대분류'].value_counts()
error_trend = df.groupby(pd.to_datetime(df['보고일자']).dt.month).size().reset_index()
error_trend.columns = ['월', '랩에러 건수']
cause_counts = df['중분류'].value_counts()
product_errors = df.explode('제품/원료/원자재')['제품/원료/원자재'].value_counts(normalize=True).reset_index()
product_errors.columns = ['제품/원자재', '랩에러 비율']
product_errors['랩에러 비율'] *= 100
device_counts = df['기기번호'].value_counts().reset_index()
device_counts.columns = ['기기', '랩에러 건수']
severity_counts = df['Major/Minor'].value_counts()
detailed_cause_counts = df['상세내용'].value_counts()
monthly_risk = df.groupby([pd.to_datetime(df['보고일자']).dt.month, df['Major/Minor']]).size().reset_index()
monthly_risk.columns = ['월', '위험도', '랩에러 건수']

# Plotly 시각화 생성
fig1 = px.bar(x=error_types.index, y=error_types.values, color=error_types.index, title='발생유형(대분류) 별 랩에러 건수')
fig2 = px.line(error_trend, x='월', y='랩에러 건수', title='월별 랩에러 발생 추이', markers=True)
fig2.update_xaxes(tickvals=error_trend['월'], ticktext=[f'{month}월' for month in error_trend['월']])
fig3 = px.pie(names=cause_counts.index, values=cause_counts.values, title='원인별 랩에러 건수')
fig4 = px.bar(product_errors, x='제품/원자재', y='랩에러 비율', title='제품/원자재별 랩에러 비율', color='제품/원자재')
fig5 = px.bar(device_counts, x='기기', y='랩에러 건수', title='기기별 랩에러 발생 건수', color='기기')
fig6 = px.pie(names=severity_counts.index, values=severity_counts.values, title='위험도 분류별 랩에러 분포')
fig7 = px.bar(x=detailed_cause_counts.index, y=detailed_cause_counts.values, title='상세 원인별 랩에러 건수', color=detailed_cause_counts.index)
fig8 = px.bar(monthly_risk, x='월', y='랩에러 건수', color='위험도', title='월별 Major, Minor 위험도 랩에러 분포', barmode='group')
fig8.update_xaxes(tickvals=monthly_risk['월'].unique(), ticktext=[f'{month}월' for month in monthly_risk['월'].unique()])

# Dash 앱 생성
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('랩에러 데이터 시각화'),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7),
    dcc.Graph(figure=fig8)
])

if __name__ == '__main__':
    app.run_server(debug=True)
