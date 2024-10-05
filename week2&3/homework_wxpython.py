import sqlite3

import wx

# 連結資料庫
conn = sqlite3.connect('./test.db')
cursor = conn.cursor()

# 插入學生資料
def insert_student(SID, fname, lname, grade, sex):
    cursor.execute("INSERT INTO student (SID, fname, lname, grade, sex) VALUES (?, ?, ?, ?, ?)", (SID, fname, lname, grade, sex))
    conn.commit()

# 插入課程資料
def insert_course(CID, fname):
    cursor.execute("INSERT INTO course (CID, fname) VALUES (?, ?)", (CID, fname))
    conn.commit()

# 插入選課資料
def insert_enrollment(SID, CID, midscore=None, finalscore=None):
    SIDCID = SID + CID
    cursor.execute("SELECT * FROM enrollment WHERE SIDCID = ?", (SIDCID,))
    if cursor.fetchone():
        if midscore is None:
            cursor.execute("SELECT midscore FROM enrollment WHERE SIDCID = ?", (SIDCID,))
            midscore = cursor.fetchone()[0]
        if finalscore is None:
            cursor.execute("SELECT finalscore FROM enrollment WHERE SIDCID = ?", (SIDCID,))
            finalscore = cursor.fetchone()[0]
        cursor.execute("UPDATE enrollment SET midscore = ?, finalscore = ? WHERE SIDCID = ?", (midscore, finalscore, SIDCID))
        conn.commit()
    else:
        cursor.execute("INSERT INTO enrollment (SID, CID, midscore, finalscore, SIDCID) VALUES (?, ?, ?, ?, ?)", (SID, CID, midscore, finalscore, SIDCID))
        conn.commit()

# 取得課程分數
def get_course_score(CID):
    cursor.execute("SELECT SID, midscore, finalscore FROM enrollment WHERE CID = ?", (CID,))
    scores = cursor.fetchall()
    result = "SID\t\tMidterm\tFinal\tTotalScore\n"
    for row in scores:
        result += f"{row[0]}\t{row[1]}\t{row[2]}\t{0.4 * row[1] + 0.6 * row[2]:.2f}\n"
    return result

# 取得學生SID
def get_student_sid():
    cursor.execute("SELECT SID FROM student")
    return cursor.fetchall()

# 取得課程CID
def get_course_cid():
    cursor.execute("SELECT CID FROM course")
    return cursor.fetchall()

# 創建 wxPython GUI
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Student Management System")
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        
        notebook = wx.Notebook(self)
        
        # 四個 Tab 對應四個功能
        tab1 = InsertStudentTab(notebook)
        tab2 = InsertCourseTab(notebook)
        tab3 = InsertEnrollmentTab(notebook)
        tab4 = GetCourseScoreTab(notebook)
        
        # 加入 notebook 中
        notebook.AddPage(tab1, "Insert Student")
        notebook.AddPage(tab2, "Insert Course")
        notebook.AddPage(tab3, "Insert Enrollment")
        notebook.AddPage(tab4, "Get Course Score")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetSize((500, 400))

# 學生資料插入的 Tab
class InsertStudentTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)
        # labeling input
        
        self.sid_input = wx.TextCtrl(self, -1, "SID", style=wx.TE_LEFT)
        self.fname_input = wx.TextCtrl(self, -1, "fname", style=wx.TE_LEFT)
        self.lname_input = wx.TextCtrl(self, -1, "lname", style=wx.TE_LEFT)
        # use radio box
        self.grade_input = wx.RadioBox(self, -1, "Grade", choices=["1", "2", "3", "4"], style=wx.RA_SPECIFY_ROWS)
        # use radio box
        self.sex_input = wx.RadioBox(self, -1, choices=["M", "F"], style=wx.RA_SPECIFY_ROWS)

        insert_btn = wx.Button(self, label="Insert Student")
        insert_btn.Bind(wx.EVT_BUTTON, self.on_insert_student)

        self.result = wx.StaticText(self, label="")

        vbox.Add(self.sid_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.fname_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.lname_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.grade_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.sex_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(insert_btn, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(self.result, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(vbox)

    def on_insert_student(self, event):
        SID = self.sid_input.GetValue()
        fname = self.fname_input.GetValue()
        lname = self.lname_input.GetValue()
        grade = self.grade_input.GetStringSelection()
        sex = self.sex_input.GetStringSelection()
        insert_student(SID, fname, lname, grade, sex)
        self.result.SetLabel(f"Inserted student: {SID}")
        # clear input
        self.sid_input.SetValue("")
        self.fname_input.SetValue("")
        self.lname_input.SetValue("")
        self.grade_input.SetSelection(0)
        

# 課程資料插入的 Tab
class InsertCourseTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.cid_input = wx.TextCtrl(self, -1, "", style=wx.TE_LEFT)
        self.fname_input = wx.TextCtrl(self, -1, "", style=wx.TE_LEFT)

        insert_btn = wx.Button(self, label="Insert Course")
        insert_btn.Bind(wx.EVT_BUTTON, self.on_insert_course)

        self.result = wx.StaticText(self, label="")

        vbox.Add(self.cid_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.fname_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(insert_btn, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(self.result, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(vbox)

    def on_insert_course(self, event):
        CID = self.cid_input.GetValue()
        fname = self.fname_input.GetValue()
        insert_course(CID, fname)
        self.result.SetLabel(f"Inserted course: {CID}")

# 選課資料插入的 Tab
class InsertEnrollmentTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # choose sid from combo box
        self.sid_input = wx.ComboBox(self, -1, "", choices=[sid[0] for sid in get_student_sid()], style=wx.CB_READONLY)
        # choose cid from combo box
        self.cid_input = wx.ComboBox(self, -1, "", choices=[cid[0] for cid in get_course_cid()], style=wx.CB_READONLY)
        
        self.midscore_input = wx.TextCtrl(self, -1, "", style=wx.TE_LEFT)
        self.finalscore_input = wx.TextCtrl(self, -1, "", style=wx.TE_LEFT)

        insert_btn = wx.Button(self, label="Insert Enrollment")
        insert_btn.Bind(wx.EVT_BUTTON, self.on_insert_enrollment)
        # add a button to refresh the combo box, position on button
        refresh_btn = wx.Button(self, label="Refresh")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh)

        self.result = wx.StaticText(self, label="")

        vbox.Add(self.sid_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.cid_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.midscore_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.finalscore_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(insert_btn, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(refresh_btn, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(self.result, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(vbox)
    
    def on_refresh(self, event):
        self.sid_input.SetItems([sid[0] for sid in get_student_sid()])
        self.cid_input.SetItems([cid[0] for cid in get_course_cid()])

    def on_insert_enrollment(self, event):
        SID = self.sid_input.GetValue()
        CID = self.cid_input.GetValue()
        midscore = self.midscore_input.GetValue() or None
        finalscore = self.finalscore_input.GetValue() or None
        insert_enrollment(SID, CID, midscore, finalscore)
        self.result.SetLabel(f"Inserted enrollment: {SID} - {CID}")

# 查詢課程分數的 Tab
class GetCourseScoreTab(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)
        # input cid from combo box
        self.cid_input = wx.ComboBox(self, -1, "", choices=[cid[0] for cid in get_course_cid()], style=wx.CB_READONLY)
        
        get_score_btn = wx.Button(self, label="Get Course Score")
        get_score_btn.Bind(wx.EVT_BUTTON, self.on_get_course_score)
        
        # add a button to refresh the combo box, position on button
        refresh_btn = wx.Button(self, label="Refresh")
        refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh)

        self.result = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox.Add(self.cid_input, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(get_score_btn, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(self.result, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(refresh_btn, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(vbox)

    def on_refresh(self, event):
        self.cid_input.SetItems([cid[0] for cid in get_course_cid()])

    def on_get_course_score(self, event):
        CID = self.cid_input.GetValue()
        result = get_course_score(CID)
        self.result.SetValue(result)

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
    conn.close()
