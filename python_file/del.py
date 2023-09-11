# coding=utf-8
import wx

# 自定义窗口类MyFrame
class MyFrame(wx.Frame):
	def __init__(self):
		super(MyFrame, self).__init__(None, title="事件处理", size=(640, 480))
		self.panel = wx.Panel(parent=self)

		self.sizer = wx.BoxSizer(wx.VERTICAL)   # 创建盒子的布局管理器对象
		# 设置面板（panel）采用sizer布局管理器
		self.panel.SetSizer(self.sizer)

		# 创建文本内容和位置
		self.statictext = wx.StaticText(parent=self.panel, label="请单击OK按钮", pos=(110, 20))
		self.sizer.Add(self.statictext, 0, wx.TOP | wx.LEFT, 10)    # 设置文字出现位置

		self.text_ctrl = wx.TextCtrl(self.panel, pos=(20, 120), size=(200, -1))    # 定义文本框和文本框出现的位置
		self.button = wx.Button(self.panel, label="发送", pos=(230, 120))

		# 设置可选框
		self.choice = wx.Choice(self.panel, pos=(20, 80), size=(200, -1))    # 定义选项框的位置和大小
		self.button2 = wx.Button(self.panel, label="你喜欢的语言", pos=(230, 80))    # 定义选项框的标题
		self.choice.Append("java")
		self.choice.Append("C++")
		self.choice.Append("python")

		# 设置勾选框
		wx.StaticText(self.panel, label="选择你的语言", pos=(230, 160))
		self.singal_button1 = wx.CheckBox(self.panel, id=1, label='Python',pos=(120, 200))
		self.singal_button2 = wx.CheckBox(self.panel, id=2, label='Java',pos=(240, 200))
		self.singal_button2.SetValue(True)   # 设置cb2初始状态为选中
		self.singal_button3 = wx.CheckBox(self.panel, id=3, label='C++',pos=(360, 200))
		self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=1, id2=3)  # 绑定id为1~3所有控件的事情处理到on_checkbox_clickck()方法

		self.st2 = wx.StaticText(self.panel, label='选择性别:',pos=(230, 260))
		# 设置style=wx.RB_GROUP的单选按钮，说明是一个组的开始,直到遇到另外设置style=wx.RB_GROUP的wx.RadioButto单选按钮为止都是同一个组。所以radio1和radio2是同一组,即这两个单选按钮是互斥的
		self.radio1 = wx.RadioButton(self.panel, id=4, label='男', style=wx.RB_GROUP,pos=(120, 300))
		self.radio2 = wx.RadioButton(self.panel, id=5, label='女',pos=(240, 300))  # 创建单选按钮
		self.Bind(wx.EVT_RADIOBUTTON, self.on_radio1_click, id=4, id2=5)
		# self.Bind(wx.EVT_RADIOBUTTON, self.on_checkbox_click, self.radio1, self.radio2)  # 绑定id从4~5的控件到on_radiol__click()方法

		#
		self.message_count = 0
		self.rb = ''
		self.cb = ['Java']
		self.cb_count = 0


		self.b = wx.Button(parent=self.panel, label='OK', pos=(320, 380)) # 创建按钮对象
		self.Bind(wx.EVT_BUTTON, self.on_click,self.b)  # 绑定事。

		self.button.Bind(wx.EVT_BUTTON, self.on_send_button, self.button, self.button2)
		# sizer.Add(b_txt, 0, wx.TOP | wx.LEFT, 40)
		self.Centre()
		self.Show()

		# wx.EVT_BUTTON是事件类型，即按钮单击事件；
		# self.on_click是事件处理程序；
		# b是事件源，即按钮对象。

	def on_click(self, event):
		self.statictext.SetLabelText('Hello, Word.')
		self.message_count = self.message_count + 1
		if self.message_count > 2:
			self.Close()

	def on_checkbox_click(self, event):
		# self.cb = event.GetEventObject().GetLabel()
		cbd = event.GetEventObject()
		print("选拼{0}，状态{1}".format(cbd.GetLabel(), event.IsChecked())) #从事件对象中取出事件源对象（复选框)并获得复选框状态
		if event.IsChecked():
			if cbd.GetLabel() in self.cb:
				pass
			else:
				self.cb.append(cbd.GetLabel())
		else:
			if cbd.GetLabel() in self.cb:
				self.cb.remove(cbd.GetLabel())
		# print("选择{0}".format(self.cb))  # 从事件对象中取出事件源对象（复选框)并获得复选框状态

	def on_radio1_click(self, event):
		self.rb = event.GetEventObject().GetLabel()
		# print("选择的性别为{0}".format(self.rb))

	def on_send_button(self, event):
		# 从文本框中获取输入的内容
		message = self.text_ctrl.GetValue()
		# 获取选择列表的选中项
		selected_option = self.choice.GetStringSelection()
		# 在控制台中显示输入的内容和选中的选项
		print("选中的选项：", selected_option)
		print("发送消息：", message)
		# 在这里添加发送消息的逻辑
		# self.Destroy()
		if self.rb== '':
			self.rb = '男'

		print("你的性别为：",self.rb)
		print("使用的语言为：",self.cb)

		# 增加计数器
		# self.message_count += 1
		# # 清空文本框内容
		# self.text_ctrl.Clear()
		# # 如果达到最大消息数，关闭客户端
		# if self.message_count > 2:
		# 	self.Close()

if __name__ == "__main__":
	app = wx.App()  # 创建应用程序对象

	frm = MyFrame()  # 创建窗口对象
	frm.Show()  # 显示窗口
	app.MainLoop()   # 进入主事循环