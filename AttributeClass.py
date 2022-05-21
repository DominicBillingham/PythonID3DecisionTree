import math
from array import *
import numpy
from anytree import *
 
class Attribute:
 
    # Data that is pulled from the attribute list or inserted later on
    Name = None
    ResultRow = None
    AttributeRow = None
    ParentRow = None
    ParentSortValue = None
 
    # Arrays that store all potential values for Attribute and Result data
    AttributeUnqiueValues = None
    ResultUnqiueValues = None
 
    # Entire entropy of an Attribute given a value to sort data by
    TotalEntropy = None
 
    # Initialisation fetches data from input and stores it in class attributes
    def __init__(self, RRow, ARow, Name):
        self.ResultRow = RRow
        self.AttributeRow = ARow
        self.Name = Name
 
        # Calls function within class to figure out the unqiue values.
        self.AttributeUnqiueValues = self.GetUniqueValues(ARow)
        self.ResultUnqiueValues = self.GetUniqueValues(RRow)
 
    # Method for figuring out unique values in an array
    def GetUniqueValues(self, Array):
 
        TempArray = []
 
        for data in Array:
            if data not in TempArray:
                TempArray.append(data)
 
        return TempArray
 
 
    # Removes any data that A) Does not contain the selected branch value B) Does not contain select attribute value
    def DataSorter(self, AttributeSortValue):
 
        sortedData = []
       
        if len(self.ParentRow) > 0:
            for i in range(len(self.AttributeRow)):
                if self.AttributeRow[i] == AttributeSortValue and self.ParentRow[i] == self.ParentSortValue:
                    sortedData.append(self.ResultRow[i])
 
        else:
            for i in range(len(self.AttributeRow)):
                if self.AttributeRow[i] == AttributeSortValue:
                    sortedData.append(self.ResultRow[i])
 
        return sortedData
 
    # Tales Sorted Data and then turns it into a count of all unique result values. E.G [ 5 yes, 4 no]
    def ResultCounter(self, sortedData): 
        
        ValueCount = []
        tempCount = 0
 
        for value in self.ResultUnqiueValues:
            tempCount = sortedData.count(value)
            ValueCount.append(tempCount)
 
        return ValueCount
 
    # This function performs an Entropy Calculation on one single outcome
    def EntCalc(self, OutcomeCount):
   
        total = sum(OutcomeCount)
        totalValEnt = 0
        temp = 0
 
        for val in OutcomeCount:
            if val != 0:
                temp = val / total
                totalValEnt = totalValEnt + ((-temp) * math.log(temp, 2))
            else:
                 totalValEnt = totalValEnt + 0
 
        return totalValEnt * (total / len(self.ResultRow))
 
    # Goes through all possible outcomes and calculates their entropy before adding them up
    def AttributeEntCalc(self):
 
        AttributeEntropy = 0
 
        for value in self.AttributeUnqiueValues:
            x = self.DataSorter(value)
            x = self.ResultCounter(x)
            x = self.EntCalc(x)
            AttributeEntropy = AttributeEntropy + x
 
        #return AttributeEntropy
        self.TotalEntropy = AttributeEntropy
 
    # Goes through all unqiue values the attribute results in, and checks to see if they are a leaf
    def FindLeafs(self):
 
        LeafList = []
 
        for value in self.AttributeUnqiueValues:
            x = self.DataSorter(value)
            LeafTuple = []
 
            if len(x) > 0:
                if (x.count(x[0]) == len(x)):
                    LeafTuple.append(value)
                    LeafTuple.append(x[0])
                    LeafList.append(LeafTuple)
 
        return LeafList


    # Finds all inconclusive leafs and uses them to calculate a percentage chance instead
    def FindLastLeafs(self, branch):

        LeafList = []

        ResultCount = self.DataSorter(branch)
        ResultCount = self.ResultCounter(ResultCount)

        total = 0
        for value in ResultCount:
            total = total + value

        for index in range(len(ResultCount)):
          
            Percent = self.intToFraction(ResultCount[index], total)

            LeafList.append( Percent + "" + self.ResultUnqiueValues[index] )
  
        return LeafList

    def intToFraction(self, top, bottom):

        if (top == 0 or bottom == 0): 
            return "0%"

        decimal = round (float(top) / float(bottom), 2)
        percent =  str(decimal * 100) + "%"
        return percent



