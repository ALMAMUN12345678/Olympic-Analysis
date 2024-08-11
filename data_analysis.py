import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import scipy
import plotly.express as px
import plotly.figure_factory as ff
df = pd.read_csv('E:/Python_file/Olympic_analysis/athlete_events.csv')
region = pd.read_csv('E:/Python_file/Olympic_analysis/noc_regions.csv')

def process():
    global df, region
    summer = df[df['Season']=='Summer']
    main = summer.merge(region, on='NOC',how='left')
    drop_duplicate = main.drop_duplicates()
    main_all = pd.concat([drop_duplicate,pd.get_dummies(drop_duplicate['Medal'],dtype=int)],axis=1)
    return main_all

# if __name__ == '__main__':
#     process()

def show_tally():
    global df, region
    summer = df[df['Season']=='Summer']
    main = summer.merge(region, on='NOC',how='left')
    drop_duplicate = main.drop_duplicates()
    main_all = pd.concat([drop_duplicate,pd.get_dummies(drop_duplicate['Medal'],dtype=int)],axis=1)
    final_drop = main_all.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    tally = final_drop.groupby('region').sum()[['Gold','Bronze','Silver']].sort_values(by='Gold',ascending=False).reset_index()
    tally['total'] = tally['Gold']+tally['Bronze']+tally['Silver']
    return tally

# if __name__ =='__main__':
#     show_tally()

def country_year_list():
    medal_tally= process()
    year =sorted(medal_tally['Year'].unique().tolist())
    year.insert(0,'Overall')
    country = sorted(medal_tally['region'].dropna().unique().tolist(),key = str)
    country.insert(0,'Overall')
    return year,country


def fetch__medal_tally(year,country,flag):
    medal_tally = process()
    #year,country = country_year_list()
    if year == 'Overall' and country =='Overall':
        fetch_df = medal_tally
    if year == 'Overall' and country !='Overall':
        fetch_df = medal_tally.loc[medal_tally['region']==country]
    if year != 'Overall' and country =='Overall':
        fetch_df = medal_tally.loc[medal_tally['Year']==int(year)]
    if year != 'Overall' and country !='Overall':
        fetch_df= medal_tally.loc[(medal_tally['region']==country) & (medal_tally['Year']==year)]
    if flag ==0:
        x = fetch_df.groupby('Year').sum()[['Gold','Bronze','Silver']].sort_values(by='Year',ascending=True).reset_index()
    elif flag==1:
        x = fetch_df.groupby('region').sum()[['Gold','Bronze','Silver']].sort_values(by='Gold',ascending=False).reset_index()
        x['total'] = x['Gold']+x['Bronze']+x['Silver']
    elif flag==2:
        x = fetch_df.groupby(['region','Year']).sum()[['Gold','Bronze','Silver']].sort_values(by='Gold',ascending=False).reset_index()
        x['total'] = x['Gold']+x['Bronze']+x['Silver']
    return x

# if __name__ == '__main__':
#     fetch__medal_tally() 

def graph_1(col):
    medal_tally = process()
    name_of_year =medal_tally.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_index()
    name_of_year.rename(columns={'Year': 'Edition', 'count': f'No.of {col if col != "Name" else "Player"}'}, inplace=True)
    return name_of_year

if __name__ == '__main__':
    graph_1() 

def graph_2():
    medal_tally = process()
    x = medal_tally.drop_duplicates(subset=['Year','Sport','Event'])
    return x

if __name__ == '__main__':
    graph_2()

def region_list():
    medal_tally = process()
    medal_tally['total'] = medal_tally['Bronze']+medal_tally['Gold']+medal_tally['Silver']
    data=medal_tally[medal_tally['total']==1].groupby(['region','Name','Sport'])['total'].sum().\
    reset_index().drop_duplicates(subset=['Name']).sort_values(by='total',ascending=False).reset_index()
    data=data.drop(columns=['index'])
    data.rename(columns={'Name':'Player Name', 'region':'Region', 'Sport':'Sport', 'total':'Total Medal'},inplace=True)
    region = sorted(data['Sport'].unique().tolist())
    region.insert(0,'Overall')
    return region
    

def top_medal(region_1):
    medal_tally = process()
    medal_tally['total'] = medal_tally['Bronze']+medal_tally['Gold']+medal_tally['Silver']
    data=medal_tally[medal_tally['total']==1].groupby(['region','Name','Sport'])['total'].sum().\
    reset_index().drop_duplicates(subset=['Name']).sort_values(by='total',ascending=False).reset_index().head(2500)
    data=data.drop(columns=['index'])
    data.rename(columns={'Name':'Player Name', 'region':'Region', 'Sport':'Sport', 'total':'Total Medal'},inplace=True)
    if region_1 =='Overall':
      data = data
    if region_1 != 'Overall':
        data = data[data['Sport']==region_1]
    return data


def top_ten_player(df, region,col):
    main_df =df.merge(region, on='NOC',how='left')
    medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
    medal_tally=medal.dropna(subset=['Medal'])
    medal_tally['total'] = medal_tally['Bronze']+medal_tally['Gold']+medal_tally['Silver']
    top_10 = medal_tally[medal_tally['total'].isin([1])].groupby(['Name','region','Sport'])['total'].sum().reset_index().sort_values(by='total',ascending=False)
    x = top_10[top_10['region']==col].head(10)
    return x

# if __name__ == '__main__':
#     top_medal()

def just_region():
    medal_tally= process()
    country = sorted(medal_tally['region'].dropna().unique().tolist(),key = str)
    return country


def year_wise_tally(col):
    medal_tally = process()
    medal_tally=medal_tally.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally['total'] = medal_tally['Bronze']+medal_tally['Gold']+medal_tally['Silver']
    x =medal_tally[medal_tally['region']==col].groupby('Year')['total'].sum().reset_index().sort_values(by='Year')
    return x

def graph_3(col):
    medal_tally = process()
    medal_tally=medal_tally.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally['total'] = medal_tally['Bronze']+medal_tally['Gold']+medal_tally['Silver']
    p =medal_tally[medal_tally['region']==col]
    df = p.pivot_table(index='Sport', columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return df

# def athlete_age_graph(df,region):
#     main_df =df.merge(region, on='NOC',how='left')
#     medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
#     athele = medal.drop_duplicates(subset=['Name','region'])
#     x = athele['Age'].dropna()
#     x1 = athele[athele['Medal']=='Gold']['Age'].dropna()
#     x2= athele[athele['Medal']=='Bronze']['Age'].dropna()
#     x3= athele[athele['Medal']=='Silver']['Age'].dropna()
#     return x , x1, x2, x3

def age_graph(df,region,col):
    main_df =df.merge(region, on='NOC',how='left')
    medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
    athele = medal.drop_duplicates(subset=['Name','region'])
    age_1 = athele['Age'].dropna()
    age =athele[athele['Medal']==col]['Age'].dropna()
    return age,age_1


famous_olympic_sports = [
    "Athletics",
    "Swimming",
    "Gymnastics",
    "Basketball",
    "Football",
    "Tennis",
    "Boxing",
    "Badminton",
    "Wrestling",
    "Cycling",
    "Weightlifting",
    "Volleyball",
    "Hockey",
    "Rowing",
    "Fencing",
    "Table Tennis",
    "Judo",
    "Archery",
    "Diving",
'Ice Hockey']

def no_of_sport(df, region):
    main_df =df.merge(region, on='NOC',how='left')
    medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
    medal['Medal'].fillna('No Medal',inplace=True)
    sport = sorted(medal['Sport'].unique().tolist())
    sport.insert(0,'Overall')
    return sport


def age_based_on_sport(df,region,col):
    play = []
    age = []
    main_df =df.merge(region, on='NOC',how='left')
    medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
    athele = medal.drop_duplicates(subset=['Name','region'])
    for sport in famous_olympic_sports:
        temp_sport = athele[athele['Sport']==sport]
        age.append( temp_sport['Age'].dropna() if col =='Overall' else temp_sport[temp_sport['Medal']==col]['Age'].dropna())
        play.append(sport)
    return play, age

def weight_vs_height(df, region,col):
    main_df =df.merge(region, on='NOC',how='left')
    medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
    medal['Medal'].fillna('No Medal',inplace=True)
    temp_medal =medal[medal['Sport']==col]
    return temp_medal,medal

def participants(df,region):
    main_df =df.merge(region, on='NOC',how='left')
    medal =pd.concat([main_df,pd.get_dummies(main_df['Medal'],dtype=int)],axis=1)
    men = medal[medal['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    Female = medal[medal['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    merge = men.merge(Female, on = 'Year',how='left')
    final = merge.rename(columns={'Name_x':'Male', 'Name_y':'Female'}).dropna()
    return final