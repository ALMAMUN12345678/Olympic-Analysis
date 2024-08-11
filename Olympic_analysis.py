import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pylab as plt
import seaborn as sns
import scipy
import plotly.figure_factory as ff
import data_analysis
df = pd.read_csv('E:/Python_file/Olympic_analysis/athlete_events.csv')
region = pd.read_csv('E:/Python_file/Olympic_analysis/noc_regions.csv')
st.sidebar.title('Olympic Analysis')
st.sidebar.image('https://www.bioanalysis-zone.com/wp-content/uploads/2024/07/Olympics-anti-doping.png')
#st.markdown('<h1 style="text-align: center;">😎 <span style="color:red;">My first Project</span> 😎</h1>', unsafe_allow_html=True)
# st.markdown('<h2 style="text-align: center; color: blue;"><em>Olympic Dataset</em></h2>', unsafe_allow_html=True)
user_menu = st.sidebar.radio(   
    'Select an Option',
    ("Overall Analysis","Medal Tally","Country-wise Analysis","Athlete wise Analysis",'Graphs')
    )
data = data_analysis.process()

if user_menu =='Medal Tally':
    flag = [0,1,2]
    st.header('Medal Tally')
    #df = data_analysis.show_tally()
    select_flag=st.sidebar.selectbox('Select Flag',flag)
    year, country = data_analysis.country_year_list()
    select_country =st.sidebar.selectbox('Select Country',country)
    select_year=st.sidebar.selectbox('Select Year',year)
    df1 = data_analysis.fetch__medal_tally(select_year,select_country,select_flag)
    if select_year == 'Overall' and select_country == 'Overall':
        st.title('Overall Tally')
    if select_year != 'Overall' and select_country == 'Overall':
        st.title(f'Medal Tally in {str(select_year)} Olympics')
    if select_year == 'Overall' and select_country != 'Overall':
        st.title(f'{select_country} Overall Performance')
    if select_year != 'Overall' and select_country != 'Overall':
        st.title(f'{select_country} performance in {str(select_year)} Olympics')
    st.table(df1)


if user_menu =='Overall Analysis':
    medal_tally = data_analysis.process()
    year = medal_tally['Year'].unique().shape[0]
    city = medal_tally['City'].unique().shape[0]
    sport = medal_tally['Sport'].unique().shape[0]
    event = medal_tally['Event'].unique().shape[0]
    name = medal_tally['Name'].unique().shape[0]
    region = medal_tally['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Host')
        st.title(city)

    with col2:
        st.header('Sport')
        st.title(sport)
    with col3:
        st.header('Event')
        st.title(event)
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Athletes')
        st.title(name)

    with col2:
        st.header('Region')
        st.title(region)
    with col3:
        st.header('Year')
        st.title(year)
    st.title(':red[Analysis Based on Sport]')
    region_list = data_analysis.region_list()
    list_1 =st.selectbox('Select Sport', region_list)
    region = data_analysis.top_medal(list_1)
    st.table(region)

if user_menu == 'Graphs':
    list = ['Event','City','Sport','Name','region']
    select_value = st.sidebar.selectbox('Select Columns For Change graphs',list)
    name_of_year=data_analysis.graph_1(select_value)
    fig = px.line(name_of_year, x='Edition', y=f'No.of {select_value if select_value != "Name" else "Player"}')
    st.title(f':red[{select_value if select_value !="Name" else "Player"} Over the Years]')
    st.plotly_chart(fig)

    st.title(':red[Name of events changes over year]')
    x = data_analysis.graph_2()
    fig,ax = plt.subplots(figsize=(30,30))
    ax =sns.heatmap(x.pivot_table(index='Sport',columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot=True,cmap='coolwarm',cbar_kws={'shrink': 1})
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=25)
    ax.set_yticklabels(ax.get_yticklabels(),ha='right', fontsize=25)
    ax.set_xlabel(ax.get_xlabel(), ha='right', fontsize=35)
    ax.set_ylabel(ax.get_ylabel(), ha='right', fontsize=35)
    st.pyplot(fig)

if user_menu =='Country-wise Analysis':
    region_list = data_analysis.just_region()
    list_1 =st.sidebar.selectbox(':red[Select Region]', region_list)
    year_1 = data_analysis.year_wise_tally(list_1)
    fig = px.line(year_1,x='Year',y='total')
    st.title(f'Total medal of {list_1} based on different year')
    st.plotly_chart(fig)

    st.title(f'Yearwise heatmap of {list_1}')
    x = data_analysis.graph_3(list_1)
    fig, ax = plt.subplots(figsize=(30, 30))  # Increase width for larger x-axis
    ax = sns.heatmap(x, annot=True, cmap='coolwarm',cbar_kws={'shrink': 1})
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=25)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right', fontsize=25)
    ax.set_xlabel(ax.get_xlabel(), ha='right', fontsize=35)
    ax.set_ylabel(ax.get_ylabel(), ha='right', fontsize=35)
    st.pyplot(fig)

    st.title(':red[Top Ten Player and Their Medals]')
    top = data_analysis.top_ten_player(df,region,list_1)
    st.table(top)

if user_menu=="Athlete wise Analysis":
    # x,x1,x2,x3 = data_analysis.athlete_age_graph(df,region)
    # fig = ff.create_distplot([x,x1,x2,x3],['Overall Age','Golden Medalist','Bronze Medalist','Silver Medalist'],show_hist=False,show_rug = False)
    # st.plotly_chart(fig)
    col = ['Overall','Gold','Bronze','Silver']
    age_side = st.sidebar.selectbox(':red[Select Medal For 1 & 2 No. Graph]',col)
    st.title(f":red[1. {age_side} Distribution of Age]")
    a1,a2 = data_analysis.age_graph(df,region,age_side)
    fig =ff.create_distplot([a2 if age_side=='Overall' else a1],[f'{age_side+" "+"Age" if age_side =="Overall" else age_side + " " + "Medalist"}'],show_hist=False,show_rug = False)
    fig.update_layout(autosize=False,width=1000,height=600)
    fig.update_xaxes(title_text=f"Age of {age_side}")
    st.plotly_chart(fig)

    st.title(':red[2. Distribution of Age based on Sport]')
    sport,age =data_analysis.age_based_on_sport(df,region,age_side)
    fig =ff.create_distplot(age,sport,show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    fig.update_xaxes(title_text="Age")
    st.plotly_chart(fig)

    st.title(':red[3. Relation Between Weight And Height]')
    Sport = data_analysis.no_of_sport(df,region)
    height_vs_weight = st.sidebar.selectbox(':red[Select Sport For 3 No. Graph]',Sport)
    temp_weight,weight = data_analysis.weight_vs_height(df,region,height_vs_weight)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(weight if height_vs_weight=='Overall' else temp_weight , x='Weight',y='Height',hue = 'Medal',style='Sex',s=60)
    st.pyplot(fig)
    
    st.title(':red[4. Realtions Between Male and Female Participants Over Year]')
    part = data_analysis.participants(df,region)
    fig = px.line(part, x='Year',y= ['Male', 'Female'])
    fig.update_layout(
    legend_title_text='Sex')
    fig.update_yaxes(title_text="Number of Players")
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)







#st.write(option)

# st.dataframe(df)

# if user_menu =='Overall Data':
#     st.markdown('<h2 style="text-align: center; color:black;">Data Table</span></h2>', unsafe_allow_html=True)
#     st.dataframe(data)
# elif ('Overall Data' and "Country-wise Analysis" and "Athlete wise Analysis"):
#     st.header('Medal Tally')
#     year, country = data_analysis.country_year_list()
#     st.sidebar.selectbox('Select Year',year)
#     st.sidebar.selectbox('Select Country',country)
#st.dataframe(df)