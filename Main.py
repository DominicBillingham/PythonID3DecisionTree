import math
from array import *
import numpy
from anytree import *
from AttributeClass import Attribute
import pandas as pd

def ImportData(file):

        CSVImport = pd.read_csv(file, encoding="ISO-8859-1")

        #This function drops any rows with NULL values within, doing a major part of the data scrubbing
        CSVImport.dropna()

        return CSVImport.to_dict(orient='list')

# Finds the highest gain when filted according to a branch
def FindHighestGainPerBranch(AttributeList, SortValue):
 
    HighestEntGain = 0
    HighestGainIndex = 0
    for Index in range(len(AttributeList)):
 
        #Update parent values
        AttributeList[Index].ParentSortValue = SortValue
        AttributeList[Index].ParentRow = TempData
 
        AttributeList[Index].AttributeEntCalc()
 
        gain = ResultRowEntropy - AttributeList[Index].TotalEntropy
        if gain > HighestEntGain:
            HighestEntGain = gain
            HighestGainIndex = Index
    
    return AttributeList[HighestGainIndex]
 
# Function for printing the tree
def PrintTree(RootNode):
 
    for pre, _, node in RenderTree(RootNode):
 
        try:
            ParentName = node.parent.name
            print("%sWHEN:%s=%s GOTO:%s" % (pre, ParentName, node.LinkVal, node.name))
        except:
            print("%sWHEN:%s GOTO:%s" % (pre, node.LinkVal, node.name))


 
#SETUP: Input the name of which row contains the result data
InputData = ImportData("HeartDataScrubbed.csv")
KeyRowName = "HeartAttack"
KeyRow = InputData[KeyRowName]
InputData.pop(KeyRowName)
 
# Creates an instance of Attribute to calculate the Total Entropy
ResultRowObject = Attribute(KeyRow, KeyRow, "ResultRow")
ResultRowEntropy = ResultRowObject.EntCalc(ResultRowObject.ResultCounter(KeyRow))
 
# Creates a list of all Attributes, and feeds them their data
AttributeList = []
for DataRow in InputData.keys():
    x = Attribute(KeyRow, InputData[DataRow], DataRow) 
    AttributeList.append(x)
 
 
 
 
# MAIN PROGRAM: Find the root node
TempData = []
AttributeX = FindHighestGainPerBranch(AttributeList, "Root")
RootNode = Node(name=AttributeX.Name, parent=None, LinkVal="Root", Branches=AttributeX.AttributeUnqiueValues, Data=AttributeX)
 
Leafs = RootNode.Data.FindLeafs()
for Leaf in Leafs:
    LeafNode = Node(name=Leaf[1], LinkVal=Leaf[0], parent=RootNode, Branches=[] )
    RootNode.Branches.remove(Leaf[0])
 
AttributeList.remove(AttributeX)
 
 
for x in range(len(AttributeList)):


    #Goes through and finds the best possible node with the best possible attribute to assign.
    HighestGain = 0
    BestNode = None
    BestAttribute = None
    HighestBranch = None
    
    for TreeNode in PreOrderIter(RootNode):

        try:
            x = TreeNode.Branches
        except AttributeError:
            continue

        for Branch in TreeNode.Branches:

             AttributeX = FindHighestGainPerBranch(AttributeList, Branch)
             Gain = ResultRowEntropy - AttributeX.TotalEntropy
 
             if Gain > HighestGain:
                HighestGain = Gain
                BestAttribute = AttributeX
                HighestBranch = Branch
                BestNode = TreeNode

    CurrentNode = BestNode

    # Add a node with the data found
    NewNode = Node(name=BestAttribute.Name, parent=CurrentNode, LinkVal=HighestBranch, Branches=BestAttribute.AttributeUnqiueValues, Data=BestAttribute)
 
    # For the new node, set the sort values needed to find leafs function
    NewNode.Data.ParentSortValue = NewNode.LinkVal
    NewNode.Data.ParentRow = CurrentNode.Data.AttributeRow
    Leafs = NewNode.Data.FindLeafs()
 
    # For the new node just added, go through and find any leafs
    for Leaf in Leafs:
        LeafNode = Node(name=Leaf[1], LinkVal=Leaf[0], parent=NewNode, Branches=[])
        NewNode.Branches.remove(Leaf[0])
 
    # Remove any branches that have now been used, remove the attribute now it's been used
    AttributeList.remove(BestAttribute)
    CurrentNode.Branches.remove(HighestBranch)


#Finally, once the tree has run it's course, go over all nodes that haven't had conclusive estimates and output uncertainity
for TreeNode in PreOrderIter(RootNode):

    try:
        x = TreeNode.Branches
    except AttributeError:
        continue
    
    for branch in x:

        tempName = ""
        for value in TreeNode.Data.FindLastLeafs(branch):
            tempName = tempName + " " + value
                
        LeafNode = Node(name=tempName, LinkVal=branch, parent=TreeNode )

PrintTree(RootNode)