import pandas as pd

def rawData2listClean(db, condition=0):
    a = False
    list01 = [0]*len(db)
    list02 = [0]*len(db)
    list03 = [0]*len(db)

    value_len = db[0].str.len()
    # db = db.loc[len < len.mean(),0]
    list03 = value_len >= value_len.mean()
    db_hasHyphen = (db.iloc[:,0].str.contains(r"[a-z]|[0-9]",case=False,regex=True))
    
   
    for e in range(0,len(db),1):
        if e==0:
            list01[e] = (False and (db_hasHyphen[e]) and not(db_hasHyphen[e+1]) and list03[e])
            if list01[e] == True:
                a = True
            list02[e] = a
        elif e==len(db)-1:
            list01[e] = (not(db_hasHyphen[e-1]) and (db_hasHyphen[e]) and False and list03[e])
            if list01[e] == True:
                a = True
            list02[e] = a
        else:
            list01[e] = (not(db_hasHyphen[e-1]) and (db_hasHyphen[e]) and not(db_hasHyphen[e+1]) and list03[e])
            if list01[e] == True:
                a = True
            list02[e] = a

    if condition == 0:  # Get column name row
        return db.iloc[list01,0].values[0]
    elif condition == 1: # Get data rows
        return db.iloc[[x and y and z for x,y,z in zip(list02,db_hasHyphen.to_list(), [not elem for elem in (list01)])],0].to_list()
    elif condition == 2: # Get bool for rows are full of "-"
        return db_hasHyphen.to_list()
    elif condition == 3: # Get bool for columns names
        return list01
    elif condition == 4: # Get bool for columns names
        return list02
    else:
        print('Use a integer 0 to 1 plz')

# %%
def getMatrixVerticalBar(rawColum):
    havesep = [a for a in range(len(rawColum)) if rawColum[a]=='|']
    matrixsep = [[havesep[b],havesep[b+1]] for b in range(len(havesep)-1)]
    return matrixsep
    
def splitStringByMatrix(rawData,matrixhavesep):
    
    dataList = [[rowRawData[matrixhavesep[c][0]+1:matrixhavesep[c][1]].strip() for c in range(len(matrixhavesep))] for rowRawData in rawData]
    return dataList

def table2dataframe(db):
    rawColumn = rawData2listClean(db,0)
    rawData = rawData2listClean(db,1)
    matrixhavesep_column = getMatrixVerticalBar(rawColumn)
    matrixhavesep_data = getMatrixVerticalBar(rawData[0])

    dfColumName = [rawColumn[matrixhavesep_column[c][0]+1:matrixhavesep_column[c][1]].strip() for c in range(len(matrixhavesep_column))]
    
    # dfColumName = splitStringByMatrix(rawColumn,matrixhavesep_column)
    dfData = splitStringByMatrix(rawData,matrixhavesep_data)

    df = pd.DataFrame(columns=dfColumName,data=dfData)

    return df #bd_df