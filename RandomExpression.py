#coding:utf8
import os
import random

def GetRandomExp():
    directory=os.listdir("Expressions")
    index=int(random.uniform(0,len(directory)-1))    
    return "Expressions/"+directory[index]


if __name__=='__main__':
    print GetRandomExp()