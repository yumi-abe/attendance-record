import tkinter as tk
import tkinter.messagebox as messagebox
import ttkbootstrap as tb
from InputSpreadSheet import InputSpreadSheet
from datetime import datetime

class AttendanceApp:
    def __init__(self, root: tk.Tk):
        """初期化"""
        # ボタンのオンオフ管理フラグ
        self.attendance_flag = False
        self.leaving_flag = False
        
        self.inputSpreadSheet = InputSpreadSheet()
        
        self.root = root
        self.root.title ("打刻アプリ")
        self.root.geometry("700x700+1000+100")
        
        # 出勤ボタン
        self.attendance_button = tb.Button(root, text="出勤",bootstyle="success", command=lambda: self.stamping(self.attendance_button))
        self.attendance_button.pack(pady=10)
        
        # 退勤ボタン
        self.leaving_button = tb.Button(root, text="退勤",bootstyle="success", command=lambda: self.stamping(self.leaving_button))
        self.leaving_button.pack(pady=10)
        
        # 打刻完了メッセージ
        self.stamping_message = tb.Label(root, text="", bootstyle="success")
        self.stamping_message.pack(pady=10)
    
        # 日付選択
        self.date_input = tb.DateEntry(root,)
        self.date_input.pack(pady=10)
        # 出勤時間入力
        tb.Label(root, text="出勤時刻", bootstyle="success").pack(pady=(5))
        self.attendance_input = tb.Entry(root,)
        self.attendance_input.pack(pady=5)
        
        # 退勤時間入力
        tb.Label(root, text="退勤時刻", bootstyle="success").pack(pady=(5))
        self.leaving_input = tb.Entry(root,)
        self.leaving_input.pack(pady=5)
        
        # 対応内容
        tb.Label(root, text="対応内容", bootstyle="success").pack(pady=(5))
        self.task_input = tb.Text(root,height=5, width=40)
        self.task_input.pack(pady=5)
        
        # 記録ボタン
        self.record_button = tb.Button(root, text="記録", bootstyle="success", command=self.record)
        self.record_button.pack(pady=10)
        
        # 記録完了メッセージ
        self.record_message = tb.Label(root, text="", bootstyle="success")
        self.record_message.pack(pady=10)
        
        # 打刻リセットボタン
        self.resetStamping_button = tb.Button(root, text="打刻リセット",bootstyle="light", command=self.resetStamping)
        self.resetStamping_button.pack(pady=10)
        
        # 対応内容リセットボタン
        self.resetTask_button = tb.Button(root, text="対応内容リセット",bootstyle="light", command=self.resetTask)
        self.resetTask_button.pack(pady=10)
        
        # リセット完了メッセージ
        self.reset_message = tb.Label(root, text="", bootstyle="success")
        self.reset_message.pack(pady=10)
        
    def getTimeNow(self):
        """現在日時を取得"""
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H:%M:%S")
        get_time = [now, date, time]
        return get_time
    
    def getInputDate(self):
        """選択した日付を取得"""
        date = self.date_input.entry.get()
        format_date = datetime.strptime(date.replace('/', '-'),"%Y-%m-%d").date()
        input_date = [date, format_date]
        return input_date
    
    def disableButton(self, button: tk.Button, flag: bool):
        """ボタンのオンオフを切り替える"""
        if flag:
            button.config(state=tk.DISABLED)
        else:
            button.config(state=tk.NORMAL)
    
    def resetMessage(self):
        self.stamping_message.config(text="")
        self.record_message.config(text="")
        self.reset_message.config(text="")
        
    def stamping(self, button: tk.Button):
        """出退勤ボタンを押した日時を取得し記録する"""
        self.resetMessage()
        label = button.cget("text")
        now = self.getTimeNow()
        if label == "出勤":
            self.attendance_flag = True
            self.leaving_flag = False
            self.disableButton(self.attendance_button, self.attendance_flag)
            self.disableButton(self.leaving_button, self.leaving_flag)
            self.inputSpreadSheet.InputTime(now[1], now[2], True)
            self.stamping_message.config(text=f"{now[1]} {now[2]}{label}完了")
            
        elif label == "退勤":
            self.attendance_flag = False
            self.leaving_flag = True
            self.disableButton(self.attendance_button, self.attendance_flag)
            self.disableButton(self.leaving_button, self.leaving_flag)
            self.inputSpreadSheet.InputTime(now[1], now[2], False)
            self.stamping_message.config(text=f"{now[1]} {now[2]}{label}完了")
    
    def record(self):
        """入力したデータを記録する"""
        self.resetMessage()
        input_date = self.getInputDate()
        attendance_time = self.attendance_input.get()
        leaving_time = self.leaving_input.get()
        task = self.task_input.get("1.0", "end-1c")
        inputs = [attendance_time, leaving_time, task]
        self.inputSpreadSheet.InputValues(input_date[1], inputs)
        self.record_message.config(text=f"{input_date[0]}に記録しました")
        

    def resetStamping(self):
        """打刻のリセット"""
        self.resetMessage()
        input_date = self.getInputDate()
        confirm = messagebox.askyesno("確認", f"{input_date[0]}の打刻をリセットします")
        if confirm:
            self.attendance_button.config(state=tk.NORMAL)
            self.leaving_button.config(state=tk.NORMAL)
            self.inputSpreadSheet.resetStampData(input_date[1])
            self.reset_message.config(text=f"{input_date[0]}の打刻をリセットしました")
        
        
    def resetTask(self):
        """対応内容のリセット"""
        self.resetMessage()
        input_date = self.getInputDate()
        confirm = messagebox.askyesno("確認", f"{input_date[0]}の対応内容をリセットします")
        if confirm:
            self.inputSpreadSheet.resetTaskData(input_date[1])
            self.reset_message.config(text=f"{input_date[0]}の対応内容をリセットしました")

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = AttendanceApp(root)
    root.mainloop()