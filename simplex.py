def getBiggestValueIndex(df, biggestColumn):
    biggestValues = df[df.loc[:,biggestColumn].values == [df.loc[:,biggestColumn].values.max()]].index.values
    if biggestValues.size > 1:
        maxVal = 0
        for value in biggestValues:
            if df['b'].loc[value]/df[biggestColumn].loc[value] > maxVal:
                maxVal = df['b'].loc[value]/df[biggestColumn].loc[value]
        return maxVal
    else:
        return biggestValues[0]
def getOtherRows(df, biggestIndex):
    rows = []
    for row in df.index:
        if(row != biggestIndex):
            rows.append(row)
    return rows
    
def getMultiplier(df, biggestValue, biggestColumn, index):
    value = df[biggestColumn].loc[index]
    return -value/biggestValue
    
def simplexTable(df):
    # Find biggest value in z column and get corresponding column name
    biggestColumn = df.loc['z'].idxmin()

    # Find biggest value in that column and get correspondig index
    biggestIndex = getBiggestValueIndex(df, biggestColumn)  

    # Get biggest value                                
    biggestValue = df[biggestColumn].max()

    # Get rows in the table except biggest index and z row
    rows = getOtherRows(df, biggestIndex)                            
    # Divide other rows that biggestColumn values would be zero
    for row in rows:
        if (df[biggestColumn].loc[row] != 0.0):
            multiplier = getMultiplier(df, biggestValue, biggestColumn, row)
            newBiggestIndex = df.loc[biggestIndex].mul(multiplier).values
            df.loc[row] = df.loc[row].add(newBiggestIndex)
            
    # Divide that row by biggest value                                
    df.loc[biggestIndex] = df.loc[biggestIndex].div(biggestValue).values
    
    # Change index name 
    df.rename({biggestIndex: biggestColumn}, axis='index', inplace=True)
    
    return df