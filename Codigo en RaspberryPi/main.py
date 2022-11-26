import connectionSheet
import time
import sensor
import queue

def readSheet(SpreadSheet,rangeNameSettings,service):
    valuesBooleans=None
    ban=True
    while ban:
        try:
            valuesBooleans = service.spreadsheets().values().get(spreadsheetId=SpreadSheet, range=rangeNameSettings,valueRenderOption='FORMATTED_VALUE').execute()
            ban=False
        except Exception as e:
            time.sleep(20)
            print(e)
    return valuesBooleans
def writeShhet(value,nameSheet,SpreadSheet,service):
    while True:
      TabName=nameSheet.split('!')[0]
      valuesR = []
      value_input_option = 'USER_ENTERED'
      valuesR.append(value)
      rangeNameSettings=nameSheet
      body = {
                  'values': value
      }
      request = service.spreadsheets().values().update(spreadsheetId=SpreadSheet, range=rangeNameSettings, valueInputOption=value_input_option, body=body)
      try:
          response = request.execute()
          break
      except Exception as e:
          print(e,'esperamos 20 s',TabName,SpreadSheet)
          time.sleep(20)
          writeShhet(value,nameSheet,SpreadSheet)
def copyTab(IdSheet,idSheetT,idSheetTCopy,service):
  # The ID of the sheet to copy.
  while True:

    sheet_id = idSheetT  # TODO: Update placeholder value.
    copy_sheet_to_another_spreadsheet_request_body = {
    'destination_spreadsheet_id': idSheetTCopy
    }
    request = service.spreadsheets().sheets().copyTo(spreadsheetId=IdSheet, sheetId=sheet_id, body=copy_sheet_to_another_spreadsheet_request_body)
    try:
        idsheetNew= request.execute()
        break
    except Exception as e:
        print(e,'esperamos 20 s')
        time.sleep(20)
        return copyTab(IdSheet,idSheetT,idSheetTCopy)

  idd=idsheetNew['sheetId']
  return idd
def deleteTab(sheetId,IdSheetData,service):
    while True:
      batch_update_spreadsheet_request_body = {
      "requests": [
      {
        "deleteSheet": {
          "sheetId": sheetId
        }
      }
    ]
      }
      request = service.spreadsheets().batchUpdate(spreadsheetId=IdSheetData, body=batch_update_spreadsheet_request_body)
      try:
          response = request.execute()
          break
      except Exception as e:
          print(e,'esperamos 20 s')
          pass
service=connectionSheet.get_service()
SpreadSheet='16fah92m0G2jjedTm7LPEi9xMwk2Fdl_VbAL7iWN8Zqk'
Tab='DatosTemperatura'
rangeNameSettings=Tab+'!A1:D'
vals=readSheet(SpreadSheet,rangeNameSettings,service)
print(vals)
tip=copyTab(SpreadSheet,'0',SpreadSheet,service)
deleteTab(tip,SpreadSheet,service)
rangeNameSettings=Tab+'!A1'



q1 = queue.Queue(250)
q2 = queue.Queue(250)

while (True != q1.full()):
    q1.put(sensor.sensor())

sensor.led() 

while (True != sensor.flama()):
    q1.get()
    q1.put(sensor.sensor())
    
  
while (True != q2.full()):
    q2.put(sensor.sensor())

sensor.ledFin()  


for i in range(250):
    print(i)
    rangeNameSettings=Tab+'!A'+ str(i+1)
    writeShhet([q1.get()],rangeNameSettings,SpreadSheet,service)
    time.sleep(1)
    rangeNameSettings=Tab+'!A'+ str(i+251)
    writeShhet([q2.get()],rangeNameSettings,SpreadSheet,service)
    time.sleep(1)
    
    
