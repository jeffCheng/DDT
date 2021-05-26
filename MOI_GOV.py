
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


#下載【內政部不動產時價登錄網 】中,位於【臺北市/新北市/桃園市/臺中市/高雄市】的
#【不動產買賣】資料,請選擇【本期下載】。
#使用【pandas】套件,讀取檔名【 a_lvr_land_a 】【 b_lvr_land_a 】 【 e_lvr_land_a 】
#【 f_lvr_land_a 】 【 h_lvr_land_a 】五份資料集,建立 dataframe 物件【df_a】【df_b】
#【df_e】【df_f】 【df_h】


# In[4]:


df_a = pd.read_csv("download/a_lvr_land_a.csv", skiprows=[1], encoding="utf-8")
df_a.insert(0, '縣市', '臺北市')
df_b = pd.read_csv("download/b_lvr_land_a.csv", skiprows=[1], encoding="utf-8")
df_b.insert(0, '縣市', '臺中市')
df_e = pd.read_csv("download/e_lvr_land_a.csv", skiprows=[1], encoding="utf-8")
df_e.insert(0, '縣市', '高雄市')
df_f = pd.read_csv("download/f_lvr_land_a.csv", skiprows=[1], encoding="utf-8")
df_f.insert(0, '縣市', '新北市')
df_h = pd.read_csv("download/h_lvr_land_a.csv", skiprows=[1], encoding="utf-8")
df_h.insert(0, '縣市', '桃園市')


# In[5]:


# 3. 操作 dataframe 物件,將五個物件合併成【df_all】。
# pd.set_option('display.max_columns', None)
df_all = pd.concat([df_a, df_b,df_e,df_f,df_h])


# In[6]:


df_all.head()


# In[21]:


# 4. 以下列條件從【df_all】篩選/計算出結果,並分別輸出【csv 檔案】 :
#filter_a.csv
#-【主要用途】為【住家用】
df_filter_a = df_all.loc[df_all['主要用途'] == '住家用']


# In[22]:


#-【建物型態】為【住宅大樓】
df_filter_a = df_filter_a.loc[df_filter_a['建物型態'].str.contains("住宅大樓")]


# In[23]:


#-【總樓層數】需【大於等於十三層】
def convertChineseDigit(chineseDigit):
    total= 0
    current_sum = 0
    
    for c in chineseDigit:
        digit = " ㄧ二三四五六七八九十百".find(c)
        if digit <= 9:
            current_sum = digit
        elif digit == 10:
            if current_sum > 0:
                total+= current_sum*10
            else:
                total+= 1*10
            current_sum = 0
        elif digit == 11:
            total+=current_sum*100
            current_sum = 0
    return total+current_sum


# In[24]:


df_filter_a['Int_Floor'] = df_filter_a.apply(lambda x: convertChineseDigit(x['總樓層數'][:-1]), axis=1)


# In[25]:


df_filter_a = df_filter_a.loc[df_filter_a['Int_Floor'] >= 13]
pd.set_option('display.max_columns', None)
df_filter_a.head()


# In[26]:


# df_filter_a
df_filter_a.to_csv(r'filter_a.csv', index = False)


# In[7]:


#* filter_b.csv
#- 計算【總件數】
len(df_all)


# In[8]:


#- 計算【總車位數】(透過交易筆棟數)
def cal_parking_lot(transaction_count:str):
    return transaction_count[transaction_count.index('車位')+2:]


# In[9]:


df_all['Parking_lot'] = df_all.apply(lambda x: cal_parking_lot(x['交易筆棟數']), axis=1)


# In[10]:


df_all.head()


# In[13]:


# df_all[['Parking_lot']].apply(pd.Series.value_counts)
df_all['Parking_lot'] = df_all['Parking_lot'].astype(int)
# 【總車位數】
df_all['Parking_lot'].sum()


# In[29]:


#- 計算【平均總價元】
df_all['總價元'] = df_all['總價元'].astype(int)
df_all['總價元'].mean()


# In[15]:


#- 計算【平均車位總價元】
df_all['Total_Parking_Val'] = df_all['車位總價元']*df_all['Parking_lot']
df_all['Total_Parking_Val'].mean()


# In[26]:


filter_b_dicts = {'總件數':len(df_all),'總車位數':df_all['Parking_lot'].sum(),'平均總價元':round(df_all['總價元'].mean(),0),'平均車位總價元':round(df_all['Total_Parking_Val'].mean(),0)}


# In[27]:


filter_b_dicts


# In[30]:


# df_filter_a.to_csv(r'filter_a.csv', index = False)
pd.DataFrame([filter_b_dicts]).to_csv('filter_b.csv', index=False)

