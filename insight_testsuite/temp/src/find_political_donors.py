#! /usr/bin/python
#--------------------------------------------------------------
#
#
#--------------------------------------------------------------

from heapdefinition import MaxHeap, MinHeap
import datetime
import sys

class Solution:

  def __init__(self):
    self.mediansAndTotalByZip = {}
    self.mediansAndTotalByDate = {}


  def readInput(self, fileInput):
    ''' Read the N-th row from the inputfile and trim the extra information and return only the neccessary information in the form of tuple '''
    columnNames = {"CMTE_ID" : 1, "AMNDT_IND" : 2, "RPT_TP" : 3, "TRANSACTION_PGI" : 4, "IMAGE_NUM" : 5, "TRANSACTION_TP" : 6, "ENTITY_TP" : 7,
		   "NAME" : 8, "CITY" : 9, "STATE" : 10, "ZIP_CODE" : 11, "EMPLOYER" : 12, "OCCUPATION" : 13, "TRANSACTION_DT" : 14,
                   "TRANSACTION_AMT": 15, "OTHER_ID" : 16, "TRAN_ID" : 17, "FILE_NUM" : 18, "MEMO_CD" : 19, "MEMO_TEXT" : 20, "SUB_ID" : 21}
    rowString = fileInput.readline()
    if rowString == "" or rowString == '\n':  # end-of-file reached return a null
      return None
    columnValueString = rowString.split("|")
    cmte_id = columnValueString[columnNames["CMTE_ID"] - 1]
    #print columnValueString, columnNames["ZIP_CODE"]
    zip_code = columnValueString[columnNames["ZIP_CODE"] - 1]
    zip_code = zip_code[:5]
    transaction_dt = columnValueString[columnNames["TRANSACTION_DT"] - 1]
#    transaction_dt = datetime.datetime.strptime(transaction_dt, "%m%d%Y").date()
    transaction_amt = columnValueString[columnNames["TRANSACTION_AMT"] - 1]
#    transaction_amt = int(transaction_amt)
    other_id = columnValueString[columnNames["OTHER_ID"] - 1]
    return (cmte_id, zip_code, transaction_dt, transaction_amt, other_id)


  def worker(self):
    ''' working subroutine to read the row sequentially, calculate the running median, and save the running median to the appropriate output files '''
    #fileInput = open("../input/itcont.txt", "r")
    #fileOutputZip = open("../output/medianvals_by_zip.txt", "w+")
    #fileOutputDate = open("../output/medianvals_by_date.txt", "w+")
    fileInput = open(sys.argv[1], "r")
    fileOutputZip = open(sys.argv[2], "w+")
    fileOutputDate = open(sys.argv[3], "w+")
    rowItem = self.readInput(fileInput)
    while rowItem != None:
      if rowItem[4] != "": # test whether or not the other id field is empty, if it is not empty skip this entry, otherwise calcualte the running median
        pass
      elif rowItem[0] == "" or rowItem[3] == "": # either the recipient or the transaction amount fields are empty, skip this entry
        pass
      elif len(rowItem[1]) != 5 and len(rowItem[2]) != 8: # both the zip and transaction dates are empty or malformed, skip this entry
        pass
      elif len(rowItem[1]) == 5 and len(rowItem[2]) != 8: # the zip code is valid, but the transaction date is invalid skip this entry for medianValsByDate
        rowItem = (rowItem[0], rowItem[1], rowItem[2], int(rowItem[3]), rowItem[4]) # convert transaction amount to integer
        medianAndTotalRowItem = self.calculateMedianAndTotal(rowItem, 0)
        self.saveOutput((rowItem[0], rowItem[1]), medianAndTotalRowItem, fileOutputZip)
      elif len(rowItem[1]) != 5 and len(rowItem[2]) == 8: # the zip code is invalid, the transaction date is valid, skip this entry for medianValsByZip
        rowItem = (rowItem[0], rowItem[1], rowItem[2], int(rowItem[3]), rowItem[4]) # convert transaction amount to integer
        self.calculateMedianAndTotal(rowItem, 1)
      elif len(rowItem[1]) == 5 and len(rowItem[2]) == 8: # use this entry for both medianValsByDate and medianValsByZip
        rowItem = (rowItem[0], rowItem[1], rowItem[2], int(rowItem[3]), rowItem[4]) # convert transaction amount to integer
        medianAndTotalRowItem = self.calculateMedianAndTotal(rowItem, 0)
        self.saveOutput((rowItem[0], rowItem[1]), medianAndTotalRowItem, fileOutputZip)
        self.calculateMedianAndTotal(rowItem, 1)
      rowItem = self.readInput(fileInput)
        

    self.saveOutputByDate(fileOutputDate)   
    fileInput.close()
    fileOutputZip.close()
    fileOutputDate.close()

  def calculateMedianAndTotal(self, rowItem, byKey):
    ''' function to calculate the running median of contributions,
        byKey is the case indicator for by (cmte_id, zip_code) or by (cmte_id, date)
        byKey = 0 is by zip_code
        byKey = 1 is by date
    
        rowItem is the N-th row trimmed input
        
        return as (median, count, total amount)
    '''
    if byKey == 0:
      key = (rowItem[0], rowItem[1])
      mediansAndTotalDict = self.mediansAndTotalByZip
    else:
      key = (rowItem[0], rowItem[2])
      mediansAndTotalDict = self.mediansAndTotalByDate
    if key not in mediansAndTotalDict: # the combination of key is not found previously
      minHp = MinHeap() # minimum heap to store half of the data entry whose key is in consideration
      maxHp = MaxHeap() # maximum heap to store half of the data entry whose key is in consideration
      count = 0 # number of entries corresponding to the data whose key is in consideration
      totalAmount = 0 #total amount of contributions whose key is in consideration
      count += 1
      totalAmount += rowItem[3]
      minHp.heappush(rowItem[3])
      median = minHp[0]
      mediansAndTotalDict[key] = (minHp, maxHp, count, totalAmount, median)  # medianAndTotal Dictionary minimun heap, maximum heap, count, total amount, and median
    else: # the combination of key was found previously
      minHp = mediansAndTotalDict[key][0]
      maxHp = mediansAndTotalDict[key][1]
      count = mediansAndTotalDict[key][2]
      totalAmount = mediansAndTotalDict[key][3]
      if len(minHp) == len(maxHp) + 1:
        if rowItem[3] > minHp[0]:
          minHp.heappush(rowItem[3])
          maxHp.heappush(minHp.heappop())
        else:
          maxHp.heappush(rowItem[3])
      else:
        if rowItem[3] > minHp[0]:
          minHp.heappush(rowItem[3])
        else:
          maxHp.heappush(rowItem[3])
          minHp.heappush(maxHp.heappop())
      count += 1
      totalAmount += rowItem[3]
      #mediansAndTotalDict[key] = (minHp, maxHp, count, totalAmount)
      
      if len(minHp) == len(maxHp) + 1: # min heap has one more element than the max heap
        median = minHp[0] # return the head of the min heap
      else: # the min heap and max heap has the same amount of data, the median should be the average of the head of these two heaps
        minHpHead = minHp[0]
        maxHpHead = maxHp[0]
        medianFloat = (minHpHead + maxHpHead) / 2.0
        if medianFloat - int(medianFloat) >= 0.5:
          median = int(medianFloat) + 1
        else:
          median = int(medianFloat)
      mediansAndTotalDict[key] = (minHp, maxHp, count, totalAmount, median)
    return (median, mediansAndTotalDict[key][2], mediansAndTotalDict[key][3]) 



  def saveOutput(self, key, medianAndTotal, fileOutput):
    row = (key[0] + '|' + key[1] + '|' +
          str(medianAndTotal[0]) + '|' + str(medianAndTotal[1]) + '|' + str(medianAndTotal[2]) +
          '\n')
    fileOutput.write(row)


  def saveOutputByDate(self, fileOutput):
    for key in sorted(self.mediansAndTotalByDate.iterkeys(), key = self.orderByRecipientAndDate):
      #print key, self.mediansAndTotalByDate[key]
      item = self.mediansAndTotalByDate[key]
      median = item[4]
      count = item[2]
      totalAmount = item[3]
      row = (median, count, totalAmount)
      self.saveOutput(key, row, fileOutput) 

  def orderByRecipientAndDate(self, recipientAndDate):
    return (recipientAndDate[0], datetime.datetime.strptime(recipientAndDate[1], "%m%d%Y").date())

#----------------------------------------------------------------
# class definition for min and max heap
#----------------------------------------------------------------
if __name__ == "__main__":
  sol = Solution()
  sol.worker()
