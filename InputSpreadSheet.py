import gspread
from datetime import datetime
from typing import List, Union

class InputSpreadSheet:
    def __init__(self):
        self.gc = gspread.service_account(
            filename="spreadsheet.json"
        )

        self.sh = self.gc.open(
            "出勤簿",
            folder_id="14pZt8UcJ-jrj0eMD-1DHx7vBCz0xrF8g"
        )
        self.ws = self.sh.worksheet("2025.2")

        self.values = self.ws.col_values(10)[5:]
        
    def get_cells(self, input_date: datetime):
        for num,value in enumerate(self.values, start=6):
            date = datetime.strptime(value,"%Y-%m-%d").date()
            if date == input_date:
                index = num
                cells = [f"B{index}", f"C{index}", f"I{index}"]
                break
        return cells
        
    def InputValues(self, input_date: datetime, inputs: List[Union[datetime,str]]):
        cells = self.get_cells(input_date)
        for i,input in enumerate(inputs):
            if input:
                self.ws.update_acell(cells[i], input)

    
    def InputTime(self, input_date: datetime, time: str, attendance: bool):
        cells = self.get_cells(input_date)
        if attendance:
            self.ws.update_acell(cells[0], time)
        else:
            self.ws.update_acell(cells[1], time)
    
    def resetStampData(self, input_date: datetime):
        cells = self.get_cells(input_date)
        self.ws.update_acell(cells[0], "")
        self.ws.update_acell(cells[1], "")

    def resetTaskData(self, input_date: datetime):
        cells = self.get_cells(input_date)
        self.ws.update_acell(cells[2], "")
        
