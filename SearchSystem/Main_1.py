
import wx
import wx.xrc
import sys
from UI.noname import MyFrame01
from UI.Page import Page_1
from UI.Page import Page_2
app = wx.App()
#frame = MyFrame1(None)
frame = Page_1(None)

##############################
#初始化后台接口 9/4更改
##########################
from Interface import Interface
interface = Interface()
interface.init()


####List传输##########################################

#packages_Keywords =[1, 2, 'Keyword03','Keyword04', 'Keyword05', 'Keyword06','Keyword07', 'Keyword08', 'Keyword09','jessica alba', 'pomona', '1981','jessica alba', 'pomona', '1981']

#获取query，即keyword
queryDict = interface.getQueryDict()
queries = queryDict.keys()

#填充packages_Keywords
packages_Keywords=[]
for query in queries:
    packages_Keywords.append(str(query))

#储存单次搜索结果
#结构[query,title,description,avg_relevance,svm_pred,rf_pred,xgb_pred] 最后三项为模型评分

'''
packages_Descriptions = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984' )]
packages_Descriptions_01 = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984' )]
packages_Descriptions_02 = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984' )]
packages_Descriptions_03= [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
('angelina jolie', 'los angeles', '1975')]
'''

frame.List_Description.InsertColumn(0,'No')
frame.List_Description.InsertColumn(1,'Query')
frame.List_Description.InsertColumn(2,'Product Title')
frame.List_Description.InsertColumn(3,'Product Description')
frame.List_Description.InsertColumn(4,'Relevance')

frame.List_Keywords.InsertColumn(0,'Query')
#frame.List_Keywords.InsertColumn(1,'Count')

frame.List_Description.SetColumnWidth(0, 30)
frame.List_Description.SetColumnWidth(1, 120)
frame.List_Description.SetColumnWidth(2, 240)
frame.List_Description.SetColumnWidth(3, 240)
frame.List_Description.SetColumnWidth(4, 240)
frame.Show()

for key in packages_Keywords:
    index = frame.List_Keywords.InsertItem(frame.List_Keywords.GetItemCount(), str(key))

'''
for data in packages_Descriptions:
    index = frame.List_Description.InsertItem(frame.List_Description.GetItemCount(),str(data))

    frame.List_Description.SetItem(index, 0,data[1])
    frame.List_Description.SetItem(index, 1,data[0])
    frame.List_Description.SetItem(index, 2,data[1])
    frame.List_Description.SetItem(index, 3, data[2])
'''

def changeValue_package(packages_Descriptions_T):
    print("2111111111133333331")
    for data in packages_Descriptions_T:
        index = frame.List_Description.InsertItem(frame.List_Description.GetItemCount(),str(data))

        frame.List_Description.SetItem(index, 0,str(index+1))

        #填充  [query,title,description,avg_relevance]
        for i in range(len(data)):
            frame.List_Description.SetItem(index, i+1,data[i])
        '''
        frame.List_Description.SetItem(index, 1,data[0])
        frame.List_Description.SetItem(index, 2,data[1])
        frame.List_Description.SetItem(index, 3, data[2])
        '''


# Virtual event handlers, overide them in your derived class

def TTry(event):
    print("1111111111111111")
   # frame.Key_Words_Details.
    frame.List_Description.DeleteAllItems()
##############传入搜索结果情况####################################
    #packages_Descriptions_T = [('a', 'b', 'c'), ('d', 'new york', '1949'),
    #                           ('angelina jolie', 'ji', '1975')]
    
    #changeValue_package(packages_Descriptions_T)

    index = frame.List_Keywords.GetFocusedItem()
    print("clicked %d-th item" %index)
    if index >= 0:
        query = frame.List_Keywords.GetItemText(index, 0)


    ###查询搜索结果,result结果请勿更改
    frame.searchResults = interface.getSearchResult(query)

    #构建packages_Descriptions_T
    packages_Descriptions_T = []
    
    for result in frame.searchResults:
        #取每一项的前4项 [query,title,description,avg_relevance]
        sub_description = result[:4]
        packages_Descriptions_T.append(sub_description)
    
    changeValue_package(packages_Descriptions_T)


def TTry2(event):
    frame2 = Page_2(None)

    #################################
    #三个模型的名字为 SVM , RandomForest , XGBboost Linear
    # 正确率先不显示
    #下面演示获取点击的item所对应的三个模型的评分

    index = frame.List_Description.GetFocusedItem()
    print("clicked %d-th List_Description item" %index)
    if index <0: return
    
    svm_relevace,randomforest_relevace,xgb_relevance = frame.searchResults[index][4],\
        frame.searchResults[index][5],frame.searchResults[index][6]

    # [query,title,description,avg_relevance,svm_pred,rf_pred,xgb_pred]
    print("22222222222222222")
    frame2.Show()

#########################下标栏的信息切换###########################################
def Log_Tips01(event):
    frame.SetStatusText("Click it and then find the all results")
def Log_Tips02(event):
    frame.SetStatusText("Ready")
def Log_Tips03(event):
    frame.SetStatusText("Click it and then find the details of the calculation")
frame.List_Keywords.Bind(wx.EVT_LIST_ITEM_SELECTED, TTry)
frame.List_Description.Bind( wx.EVT_LIST_ITEM_SELECTED,TTry2 )
frame.List_Description.Bind( wx.EVT_ENTER_WINDOW, Log_Tips03 )
frame.List_Description.Bind( wx.EVT_LEAVE_WINDOW, Log_Tips02 )
frame.List_Keywords.Bind( wx.EVT_ENTER_WINDOW, Log_Tips01 )
frame.List_Keywords.Bind( wx.EVT_LEAVE_WINDOW, Log_Tips02 )

##### Beatiful Frame############

app.MainLoop()

