#coding=utf-8
import wx
class MyFrame(wx.Frame):
    def _init_(self):
        super(MyFrame, self).__init__(None, title="列表",size=(400, 200))
        panel = wx.Panel(parent=self)

        st1 = wx. StaticText(panel, label='选择你喜欢的编程语言:', pos = (200, 20))
        list1 = ['Python', 'C++', 'Java']
        #创建列表控件,参数choices用于设置列表选项;参数style用于设置列表风格样式,wx.LB_SINGLE指单选列表控件:
        lb1 = wx.ListBox(panel, choices=list1, style=wx.LB_SINGLE)
        #绑定列表选择事件wx.EVT_LISTBOX到self.on_listbox1()方法:
        self.Bind(wx.EVT_LISTBOX, self.on_listbox1,lb1)

        st2 = wx.StaticText(panel,label='选择你喜欢吃的水果:', pos = (200, 60))
        list2 =['菜果', '橘子', '香蕉']
        #style=wx.LB_EXTENDED表示创建多选列表控件:
        lb2 = wx.ListBox(panel, choices=list2, style=wx.LB_EXTENDED)
        self.Bind(wx.EVT_LISTBOX, self.on_listbox1,lb2)

        hbox1 = wx.BoxSizer()
        hbox1.Add(st1, proportion=1, flag=wx.LEFT|wx.RIGHT, border=5)
        hbox1.Add(lb1, proportion=1)

        hbox2 = wx.BoxSizer()
        hbox2.Add(st2, proportion=1, flag=wx.LEFT|wx.RIGHT, border=5)
        hbox2.Add(lb2, proportion=1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, f1ag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALL|wx.EXPAND, border=5)

        panel.SetSizer(vbox)

    def on_listbox1(self, event):
        listbox = event.GetEventObject()
        print('选择{0}'.format(listbox.GetSelection()))  #返回单个选中项目的索引序号


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
# app = wx.App()  #创建应用程序对象
# frm = MyFrame()  #创建窗口对象
# frm.Show()  #显示窗口
# app.MainLoop()  #进入主事件循环