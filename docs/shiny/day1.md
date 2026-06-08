# Day 1: Hello World - 让你的第一个 Shiny App 跑起来

## 1. 开始之前的准备

### 1.1 安装 Shiny 包

打开 RStudio，在控制台输入：

```r
install.packages("shiny")
```

安装完成后，测试一下：

```r
library(shiny)
```

如果没有报错，说明安装成功了！

### 1.2 理解两个核心概念

在开始写代码之前，我们要理解 Shiny 的两个核心部分：

**UI（用户界面）：**

- 就是网页上你能看到的东西
- 按钮、文字、图片这些

**Server（服务器）：**

- 就是后台处理数据的地方
- 用户看不见，但在默默工作

简单理解

UI 就像餐厅的前厅（客人能看到的）
Server 就像餐厅的后厨（做菜的地方）

## 2. 第一个例子：最简单的 App

### 2.1 创建新文件

在 RStudio 中：

1. File → New File → Shiny Web App
2. 给它起个名字，比如 "my_first_app"
3. 选择 "Single File"
4. 点击 Create

RStudio 会自动生成一个模板；本节从空文件开始，便于理解最小结构。

### 2.2 最小 Hello World 示例

删掉所有代码，输入下面这些：

```r
library(shiny)

# UI 部分
ui <- fluidPage(
  "Hello World!"
)

# Server 部分
server <- function(input, output) {
  # 这里什么都不做
}

# 运行 App
shinyApp(ui = ui, server = server)
```

点击右上角的 "Run App" 按钮，你就能看到一个显示 "Hello World!" 的网页了！

代码解释

- `library(shiny)` - 加载 Shiny 包
- `ui <- fluidPage()` - 创建一个网页
- `server <- function()` - 创建后台处理函数
- `shinyApp()` - 把 UI 和 Server 组合起来运行

## 3. 加点料：添加标题

### 3.1 加个大标题

```r
library(shiny)

ui <- fluidPage(
  h1("我的第一个 Shiny App"),  # h1 是一级标题
  p("这是一个段落文字")         # p 是段落
)

server <- function(input, output) {
}

shinyApp(ui = ui, server = server)
```

### 3.2 多级标题示例

```r
library(shiny)

ui <- fluidPage(
  h1("一级标题 - 最大"),
  h2("二级标题 - 第二大"),
  h3("三级标题 - 中等"),
  h4("四级标题 - 较小"),
  p("普通段落文字"),
  br(),  # 换行
  p("这是另一个段落")
)

server <- function(input, output) {
}

shinyApp(ui = ui, server = server)
```

HTML 标签

Shiny 里可以用这些 HTML 标签：

- `h1()` 到 `h6()` - 标题（1最大，6最小）
- `p()` - 段落
- `br()` - 换行
- `strong()` - 加粗
- `em()` - 斜体

## 4. 第一个交互：按钮和文字

### 4.1 加个按钮

下面添加一个按钮事件示例：点击按钮后显示文字。

```r
library(shiny)

ui <- fluidPage(
  h1("点击按钮测试"),

  # 添加一个按钮
  actionButton("button1", "运行示例"),

  # 显示文字的地方
  textOutput("text1")
)

server <- function(input, output) {
  # 当按钮被点击时
  observeEvent(input$button1, {
    output$text1 <- renderText({
      "你点击了按钮！"
    })
  })
}

shinyApp(ui = ui, server = server)
```

运行后，点击按钮即可显示文字。

### 4.2 理解这个例子

让我们一步步理解：

**UI 部分：**

- `actionButton("button1", "运行示例")` - 创建一个按钮

  - `"button1"` 是这个按钮的 ID（身份证）
  - `"运行示例"` 是按钮上显示的文字
- `textOutput("text1")` - 创建一个显示文字的地方

  - `"text1"` 是这个输出的 ID

**Server 部分：**

- `observeEvent(input$button1, {...})` - 监听按钮点击

  - `input$button1` 获取按钮的状态
- `output$text1 <- renderText({...})` - 输出文字

  - `output$text1` 对应 UI 中的 `textOutput("text1")`

记住这个模式

1. UI 中用 `XXXInput()` 创建输入（如按钮）
2. UI 中用 `XXXOutput()` 创建输出位置
3. Server 中用 `input$ID` 获取输入
4. Server 中用 `output$ID <- renderXXX()` 创建输出

## 5. 更有趣的例子：滑块控制数字

### 5.1 基础版本

```r
library(shiny)

ui <- fluidPage(
  h1("滑块控制器"),

  # 创建一个滑块
  sliderInput("slider1",
              "选择一个数字：",
              min = 1,
              max = 100,
              value = 50),

  # 显示选中的数字
  textOutput("number1")
)

server <- function(input, output) {
  # 显示滑块的值
  output$number1 <- renderText({
    paste("你选择了：", input$slider1)
  })
}

shinyApp(ui = ui, server = server)
```

### 5.2 升级版：滑块控制图形

```r
library(shiny)

ui <- fluidPage(
  h1("滑块控制直方图"),

  # 侧边栏布局
  sidebarLayout(
    # 侧边栏放控件
    sidebarPanel(
      sliderInput("bins",
                  "选择直方图的组数：",
                  min = 1,
                  max = 50,
                  value = 30)
    ),

    # 主面板放图
    mainPanel(
      plotOutput("distPlot")
    )
  )
)

server <- function(input, output) {
  output$distPlot <- renderPlot({
    # 生成数据
    x <- rnorm(1000)

    # 画直方图
    hist(x,
         breaks = input$bins,  # 使用滑块的值
         col = 'lightblue',
         border = 'white',
         main = paste("直方图（", input$bins, "组）"))
  })
}

shinyApp(ui = ui, server = server)
```

运行这个例子，拖动滑块，图形会实时变化！

## 6. 常见错误和解决方法

### 6.1 错误：could not find function

```r
# 错误示例
ui <- fluidPage(
  sliderInput("test", "测试", 1, 100, 50)
)

# 解决：记得先加载包
library(shiny)
```

### 6.2 错误：object 'input' not found

```r
# 错误示例
ui <- fluidPage(
  textOutput("text1")
)

server <- function(input, output) {
  output$text1 <- renderText({
    input$slider1  # 但是 UI 里没有创建 slider1！
  })
}

# 解决：确保 UI 中有对应的输入控件
```

### 6.3 错误：ID 重复

```r
# 错误示例
ui <- fluidPage(
  sliderInput("id1", "滑块1", 1, 100, 50),
  sliderInput("id1", "滑块2", 1, 100, 50)  # ID 重复了！
)

# 解决：每个控件的 ID 必须唯一
ui <- fluidPage(
  sliderInput("id1", "滑块1", 1, 100, 50),
  sliderInput("id2", "滑块2", 1, 100, 50)  # 改成不同的 ID
)
```

## 7. 练习时间

### 7.1 练习 1：文本输入

创建一个 App，用户输入名字，显示 "你好，XXX！"

```r
library(shiny)

ui <- fluidPage(
  h1("问候程序"),

  # 提示：使用 textInput()
  textInput("name", "请输入你的名字："),

  # 显示问候语
  textOutput("greeting")
)

server <- function(input, output) {
  output$greeting <- renderText({
    # 提示：使用 paste() 组合文字
    paste("你好，", input$name, "！")
  })
}

shinyApp(ui = ui, server = server)
```

### 7.2 练习 2：多个控件

创建一个 App，有两个滑块，显示它们的和：

```r
library(shiny)

ui <- fluidPage(
  h1("加法计算器"),

  sliderInput("num1", "第一个数：", 0, 100, 50),
  sliderInput("num2", "第二个数：", 0, 100, 50),

  h3("结果："),
  textOutput("sum")
)

server <- function(input, output) {
  output$sum <- renderText({
    # 计算两个数的和
    result <- input$num1 + input$num2
    paste(input$num1, "+", input$num2, "=", result)
  })
}

shinyApp(ui = ui, server = server)
```

### 7.3 练习 3：条件显示

根据滑块的值显示不同的消息：

```r
library(shiny)

ui <- fluidPage(
  h1("温度计"),

  sliderInput("temp", "当前温度：", -10, 40, 20),

  textOutput("message")
)

server <- function(input, output) {
  output$message <- renderText({
    if (input$temp < 0) {
      "太冷了！❄️"
    } else if (input$temp < 15) {
      "有点冷 🧥"
    } else if (input$temp < 25) {
      "很舒适 😊"
    } else if (input$temp < 35) {
      "有点热 🌞"
    } else {
      "太热了！🔥"
    }
  })
}

shinyApp(ui = ui, server = server)
```

## 8. 今日总结

### 8.1 你学会了什么

1. **基本结构：**
   UI + Server + `shinyApp()`
2. **常用 UI 控件：**

   - `actionButton()` – 按钮
   - `sliderInput()` – 滑块
   - `textInput()` – 文本输入
   - `textOutput()` – 文本输出
   - `plotOutput()` – 图形输出
3. **Server 端模式：**

   - `output$ID <- renderXXX({...})` – 创建输出
   - `input$ID` – 获取输入值
   - `observeEvent()` – 监听事件

### 8.2 明天预告

明天我们会学习：

- 如何让 App 结构更清晰（布局和主题）
- 更多的布局选项
- 添加 CSS 美化

恭喜！

你已经成功创建了第一个 Shiny App！
记住：多动手练习，遇到错误是正常的。
每个错误都是学习的机会！

作业

试着结合今天学的内容，做一个"身高体重 BMI 计算器"：

- 两个滑块：身高（cm）和体重（kg）
- 显示计算出的 BMI 值
- 根据 BMI 值显示健康建议

BMI = 体重(kg) / (身高(m) × 身高(m))
