# Day 3: 各种输入控件 - 让用户与你的 App 交互

## 1. 开始之前：理解输入控件

### 1.1 什么是输入控件？

输入控件就是网页上让用户可以点击、输入、选择的东西。比如：

- 按钮 - 用户点击
- 文本框 - 用户输入文字
- 下拉框 - 用户选择选项
- 滑块 - 用户拖动选择数值

### 1.2 输入控件的通用规则

所有输入控件都有两个必需的参数：

1. **inputId** - 给控件起个名字（身份证）
2. **label** - 显示给用户看的说明文字

让我们从最简单的开始！

## 2. 文本输入框：textInput()

### 2.1 最基础的文本输入

我们先创建一个最简单的文本输入框：

```r
library(shiny)

ui <- fluidPage(
  # 创建一个文本输入框
  textInput("name", "请输入你的名字：")
)

server <- function(input, output) {
  # 暂时什么都不做
}

shinyApp(ui = ui, server = server)
```

运行后你会看到一个输入框，但输入内容后什么都不会发生。

### 2.2 显示输入的内容

现在让我们显示用户输入的内容：

```r
library(shiny)

ui <- fluidPage(
  textInput("name", "请输入你的名字："),

  # 添加一个显示文字的地方
  textOutput("greeting")
)

server <- function(input, output) {
  # 现在我们要处理输入了
  output$greeting <- renderText({
    input$name  # 获取用户输入的内容
  })
}

shinyApp(ui = ui, server = server)
```

试试输入你的名字，它会立即显示出来！

### 2.3 让输出更友好

我们可以加工一下输出的内容：

```r
library(shiny)

ui <- fluidPage(
  textInput("name", "请输入你的名字："),
  textOutput("greeting")
)

server <- function(input, output) {
  output$greeting <- renderText({
    # 如果没输入，显示提示
    if(input$name == "") {
      "请在上方输入你的名字"
    } else {
      # 如果输入了，显示问候语
      paste("你好，", input$name, "！欢迎使用 Shiny！")
    }
  })
}

shinyApp(ui = ui, server = server)
```

### 2.4 textInput 的更多选项

#### `verbatimTextOutput()` 用法详解

在 Shiny 的 UI 中，`verbatimTextOutput(outputId)` 用于创建一个“逐字输出”区域（等宽字体），可以完整保留空格、换行和控制台风格的格式，适合展示：

- R 对象的打印结果（如 `summary()`、`str()` 等）
- 调试信息或日志
- 任意需要保留原始格式的文本

它通常与服务器端的 `renderPrint({ ... })` 配合使用：

- **UI 端**

```text
  verbatimTextOutput("allText")
```

- **Server 端**

```r
  output$allText <- renderPrint({
      # 这里写需要“打印”的 R 代码
      summary(some_data)
  })
```

---

下面是一个完整示例：演示四种不同的 `textInput()` 用法，并将所有输入汇总到一个 `verbatimTextOutput` 区域中。

#### 代码示例

```r
library(shiny)

ui <- fluidPage(
  h3("textInput 的各种用法"),

  # 1. 基础用法
  textInput("text1", "基础输入框："),

  # 2. 带默认值
  textInput("text2", "带默认值：", value = "我是默认文字"),

  # 3. 带占位符（提示文字）
  textInput("text3", "带提示文字：", placeholder = "请输入邮箱地址"),

  # 4. 限制宽度
  textInput("text4", "窄一点的输入框：", width = "200px"),

  hr(),

  h4("你输入的内容："),
  # 创建一个等宽文本输出区域，用于显示服务器端 renderPrint 的结果
  verbatimTextOutput("allText")
)

server <- function(input, output) {
  # 将所有四个输入框的值拼接，并“打印”到 verbatimTextOutput 区域
  output$allText <- renderPrint({
    paste(
      "输入框1:", input$text1, "\n",
      "输入框2:", input$text2, "\n",
      "输入框3:", input$text3, "\n",
      "输入框4:", input$text4
    )
  })
}

shinyApp(ui = ui, server = server)
```

## 3. 数字输入框：numericInput()

### 3.1 基础数字输入

当我们需要用户输入数字时，用 `numericInput()`：

```r
library(shiny)

ui <- fluidPage(
  # 创建数字输入框
  numericInput("age", "请输入你的年龄：", value = 18)
)

server <- function(input, output) {
}

shinyApp(ui = ui, server = server)
```

注意：这个输入框只能输入数字！

### 3.2 设置数字范围

我们可以限制输入的范围：

```r
library(shiny)

ui <- fluidPage(
  numericInput("age",
               "请输入你的年龄：",
               value = 18,      # 默认值
               min = 0,         # 最小值
               max = 150,       # 最大值
               step = 1)        # 步长（点击箭头时增减多少）
)

server <- function(input, output) {
}

shinyApp(ui = ui, server = server)
```

### 3.3 用数字输入做计算

让我们做个 BMI 计算器：

```r
library(shiny)

ui <- fluidPage(
  h3("BMI 计算器"),

  # 第一步：添加身高输入
  numericInput("height", "身高（厘米）：",
               value = 170, min = 50, max = 250),

  # 第二步：添加体重输入
  numericInput("weight", "体重（公斤）：",
               value = 60, min = 20, max = 200),

  # 第三步：显示结果的地方
  h4("你的 BMI 是："),
  textOutput("bmi"),
  textOutput("status")
)

server <- function(input, output) {
  # 计算 BMI
  output$bmi <- renderText({
    # BMI = 体重(kg) / (身高(m))^2
    height_m <- input$height / 100  # 厘米转米
    bmi_value <- input$weight / (height_m ^ 2)
    round(bmi_value, 1)  # 保留一位小数
  })

  # 显示健康状态
  output$status <- renderText({
    height_m <- input$height / 100
    bmi_value <- input$weight / (height_m ^ 2)

    if(bmi_value < 18.5) {
      "体重偏轻"
    } else if(bmi_value < 24) {
      "体重正常"
    } else if(bmi_value < 28) {
      "体重偏重"
    } else {
      "需要减重"
    }
  })
}

shinyApp(ui = ui, server = server)
```

## 4. 滑块输入：sliderInput()

### 4.1 基础滑块

滑块是一种直观的数字选择方式：

```r
library(shiny)

ui <- fluidPage(
  h3("滑块演示"),

  # 基础滑块
  sliderInput("slider1", "选择一个数字：",
              min = 0,
              max = 100,
              value = 50),

  # 显示选中的值
  textOutput("value1")
)

server <- function(input, output) {
  output$value1 <- renderText({
    paste("你选择了：", input$slider1)
  })
}

shinyApp(ui = ui, server = server)
```

### 4.2 滑块的各种形式

滑块有很多种用法，让我们逐一尝试：

```r
library(shiny)

ui <- fluidPage(
  h3("滑块的各种形式"),

  # 1. 基础滑块
  sliderInput("basic", "基础滑块：",
              min = 0, max = 100, value = 50),

  # 2. 带步长的滑块
  sliderInput("step", "每次移动5（步长=5）：",
              min = 0, max = 100, value = 50,
              step = 5),

  # 3. 范围滑块（选择区间）
  sliderInput("range", "选择范围：",
              min = 0, max = 100,
              value = c(25, 75)),  # 注意：这里是两个值！

  # 4. 带动画的滑块
  sliderInput("animate", "可以自动播放：",
              min = 1, max = 10, value = 1,
              animate = TRUE),  # 添加播放按钮

  hr(),
  verbatimTextOutput("allValues")
)

server <- function(input, output) {
  output$allValues <- renderPrint({
    paste("基础滑块:", input$basic, "\n",
          "步长滑块:", input$step, "\n",
          "范围滑块:", input$range[1], "-", input$range[2], "\n",
          "动画滑块:", input$animate)
  })
}

shinyApp(ui = ui, server = server)
```

### 4.3 用滑块控制图形

这是最常见的用法：

```r
library(shiny)

ui <- fluidPage(
  titlePanel("滑块控制图形"),

  sidebarLayout(
    sidebarPanel(
      # 控制数据点数量
      sliderInput("n_points", "数据点数量：",
                  min = 10, max = 500, value = 100),

      # 控制点的大小
      sliderInput("point_size", "点的大小：",
                  min = 0.5, max = 5, value = 2,
                  step = 0.5),

      # 控制透明度
      sliderInput("alpha", "透明度：",
                  min = 0.1, max = 1, value = 0.7,
                  step = 0.1)
    ),

    mainPanel(
      plotOutput("scatter")
    )
  )
)

server <- function(input, output) {
  output$scatter <- renderPlot({
    # 生成随机数据
    x <- rnorm(input$n_points)
    y <- rnorm(input$n_points)

    # 画散点图
    plot(x, y,
         pch = 19,  # 实心圆点
         cex = input$point_size,  # 点的大小
         col = rgb(0, 0, 1, input$alpha),  # 蓝色，可变透明度
         main = paste(input$n_points, "个数据点"))
  })
}

shinyApp(ui = ui, server = server)
```

## 5. 下拉选择框：selectInput()

### 5.1 基础下拉框

当用户需要从几个选项中选择时：

```r
library(shiny)

ui <- fluidPage(
  h3("下拉框演示"),

  # 创建下拉框
  selectInput("fruit", "选择你喜欢的水果：",
              choices = c("苹果", "香蕉", "橙子", "葡萄")),

  textOutput("selected")
)

server <- function(input, output) {
  output$selected <- renderText({
    paste("你选择了：", input$fruit)
  })
}

shinyApp(ui = ui, server = server)
```

### 5.2 设置选项的值

有时候显示给用户的文字和实际使用的值不一样：

```r
library(shiny)

ui <- fluidPage(
  h3("选项的显示值和实际值"),

  # 方式1：显示和值相同
  selectInput("simple", "简单选项：",
              choices = c("红色", "蓝色", "绿色")),

  # 方式2：显示和值不同
  selectInput("advanced", "高级选项：",
              choices = c("红色" = "red",
                          "蓝色" = "blue",
                          "绿色" = "green")),

  verbatimTextOutput("values")
)

server <- function(input, output) {
  output$values <- renderPrint({
    paste("简单选项的值:", input$simple, "\n",
          "高级选项的值:", input$advanced)
  })
}

shinyApp(ui = ui, server = server)
```

### 5.3 多选下拉框

允许用户选择多个选项：

```r
library(shiny)

ui <- fluidPage(
  h3("多选下拉框"),

  selectInput("skills", "选择你会的编程语言：",
              choices = c("R", "Python", "JavaScript",
                          "Java", "C++", "SQL"),
              multiple = TRUE),  # 允许多选！

  textOutput("selected")
)

server <- function(input, output) {
  output$selected <- renderText({
    if(length(input$skills) == 0) {
      "你还没有选择"
    } else {
      paste("你会：", paste(input$skills, collapse = ", "))
    }
  })
}

shinyApp(ui = ui, server = server)
```

## 6. 单选按钮：radioButtons()

### 6.1 基础单选按钮

当选项不多，想全部显示出来时：

```r
library(shiny)

ui <- fluidPage(
  h3("单选按钮"),

  radioButtons("gender", "选择性别：",
               choices = c("男", "女", "其他")),

  textOutput("selected")
)

server <- function(input, output) {
  output$selected <- renderText({
    paste("你选择了：", input$gender)
  })
}

shinyApp(ui = ui, server = server)
```

### 6.2 横向排列和设置默认值

```r
library(shiny)

ui <- fluidPage(
  h3("单选按钮的更多选项"),

  # 竖向排列（默认）
  radioButtons("size1", "衣服尺码（竖向）：",
               choices = c("S", "M", "L", "XL"),
               selected = "M"),  # 默认选中 M

  # 横向排列
  radioButtons("size2", "衣服尺码（横向）：",
               choices = c("S", "M", "L", "XL"),
               selected = "M",
               inline = TRUE),  # 横向排列！

  verbatimTextOutput("sizes")
)

server <- function(input, output) {
  output$sizes <- renderPrint({
    paste("竖向选择:", input$size1, "\n",
          "横向选择:", input$size2)
  })
}

shinyApp(ui = ui, server = server)
```

## 7. 复选框：checkboxInput() 和 checkboxGroupInput()

### 7.1 单个复选框

用于是/否的选择：

```r
library(shiny)

ui <- fluidPage(
  h3("单个复选框"),

  checkboxInput("agree", "我同意用户协议"),

  # 根据是否勾选显示不同内容
  uiOutput("nextStep")
)

server <- function(input, output) {
  output$nextStep <- renderUI({
    if(input$agree) {
      actionButton("continue", "继续", class = "btn-success")
    } else {
      p("请先同意用户协议", style = "color:red;")
    }
  })
}

shinyApp(ui = ui, server = server)
```

### 7.2 复选框组

多个选项可以同时选择：

```r
library(shiny)

ui <- fluidPage(
  h3("复选框组"),

  checkboxGroupInput("hobbies", "选择你的爱好（可多选）：",
                     choices = c("运动", "阅读", "音乐",
                                 "旅游", "美食", "电影")),

  textOutput("selected")
)

server <- function(input, output) {
  output$selected <- renderText({
    if(length(input$hobbies) == 0) {
      "你还没有选择任何爱好"
    } else {
      paste("你的爱好有：",
            paste(input$hobbies, collapse = "、"))
    }
  })
}

shinyApp(ui = ui, server = server)
```

## 8. 日期输入：dateInput() 和 dateRangeInput()

### 8.1 单个日期选择

```r
library(shiny)

ui <- fluidPage(
  h3("日期选择器"),

  dateInput("birthday", "选择你的生日：",
            value = "2000-01-01",  # 默认值
            format = "yyyy-mm-dd",  # 日期格式
            language = "zh-CN"),    # 中文界面

  textOutput("age")
)

server <- function(input, output) {
  output$age <- renderText({
    # 计算年龄
    today <- Sys.Date()
    age <- as.numeric(today - input$birthday) / 365.25
    paste("你大约", round(age, 1), "岁")
  })
}

shinyApp(ui = ui, server = server)
```

### 8.2 日期范围选择

```r
library(shiny)

ui <- fluidPage(
  h3("选择日期范围"),

  dateRangeInput("dateRange", "选择开始和结束日期：",
                 start = Sys.Date() - 30,  # 默认开始：30天前
                 end = Sys.Date(),         # 默认结束：今天
                 language = "zh-CN"),

  textOutput("days")
)

server <- function(input, output) {
  output$days <- renderText({
    # 计算天数
    days <- as.numeric(input$dateRange[2] - input$dateRange[1])
    paste("你选择了", days + 1, "天的数据")
  })
}

shinyApp(ui = ui, server = server)
```

## 9. 文件上传：fileInput()

### 9.1 基础文件上传

```r
library(shiny)

ui <- fluidPage(
  h3("文件上传"),

  fileInput("file", "选择一个文件：",
            accept = c(".csv", ".txt")),  # 限制文件类型

  tableOutput("contents")
)

server <- function(input, output) {
  output$contents <- renderTable({
    # 检查是否有文件上传
    if(is.null(input$file)) {
      return(NULL)
    }

    # 读取 CSV 文件
    read.csv(input$file$datapath)
  })
}

shinyApp(ui = ui, server = server)
```

### 9.2 显示文件信息

```r
library(shiny)

ui <- fluidPage(
  h3("文件上传详情"),

  fileInput("file", "选择任意文件："),

  h4("文件信息："),
  verbatimTextOutput("fileInfo"),

  h4("文件内容预览："),
  verbatimTextOutput("preview")
)

server <- function(input, output) {
  output$fileInfo <- renderPrint({
    if(is.null(input$file)) {
      "还没有上传文件"
    } else {
      paste("文件名:", input$file$name, "\n",
            "文件大小:", input$file$size, "字节\n",
            "文件类型:", input$file$type)
    }
  })

  output$preview <- renderPrint({
    if(is.null(input$file)) {
      return(NULL)
    }

    # 根据文件类型显示不同内容
    if(grepl("\\.csv$", input$file$name)) {
      head(read.csv(input$file$datapath), 5)
    } else if(grepl("\\.txt$", input$file$name)) {
      readLines(input$file$datapath, n = 5)
    } else {
      "不支持预览此文件类型"
    }
  })
}

shinyApp(ui = ui, server = server)
```

## 10 综合练习：一步步搭建鸢尾花数据筛选器

目标：让用户筛选 `iris` 数据集，选择显示的列、品种、花萼长度范围、行数，最后还能下载结果。

---

### 第一步：准备工作

```r
# 加载 Shiny 包
library(shiny)
```

---

### 第二步：构建用户界面（UI）

在 Shiny 应用中，**UI 是用户看到和操作的界面部分**。我们会使用 `fluidPage()` 来定义一个响应式布局，并用 `sidebarLayout()` 分为左侧的输入控件区和右侧的输出显示区。

我们不会直接把全部 UI 写死，而是通过**模块化、分步方式**搭建每个组件，最终组合成完整 UI。

---

#### 🎯 目标：构建一个交互式数据筛选面板，包含 5 个功能控件：

| 编号 | 控件类型 | 功能描述 |
| --- | --- | --- |
| 1 | 复选框组 | 用户选择要显示的变量列 |
| 2 | 下拉菜单 | 用户选择某一品种或全部数据 |
| 3 | 滑块 | 限定花萼长度的筛选范围 |
| 4 | 数值输入框 | 控制显示数据的前几行 |
| 5 | 下载按钮 | 下载筛选后的数据为 CSV 文件 |

---

#### 🧩 子模块1：选择要显示的列 `checkboxGroupInput()`

##### ✅ 设计思路：

用户可能不需要查看全部变量，我们用复选框列出 iris 的所有列名，让用户勾选自己感兴趣的字段。

##### ✅ 代码示例：

```text
checkboxGroupInput(
  inputId = "columns",                     # 控件的唯一 ID
  label = "选择要显示的列：",             # 显示在控件上方的提示文字
  choices = names(iris),                   # 可选项：iris 数据集的所有列名
  selected = names(iris)                   # 默认全部勾选
)
```

---

#### 🧩 子模块2：选择品种 `selectInput()`

##### ✅ 设计思路：

iris 数据集中有三类植物品种。我们允许用户选中某一类，也可以选择“全部”。

##### ✅ 代码示例：

```text
selectInput(
  inputId = "species",
  label = "选择品种：",
  choices = c("全部", unique(iris$Species)),  # 添加“全部”选项
  selected = "全部"                            # 默认显示全部品种
)
```

---

#### 🧩 子模块3：花萼长度范围筛选 `sliderInput()`

##### ✅ 设计思路：

使用滑块让用户选择花萼长度的筛选区间。滑块支持双端拖动，表示区间范围。

##### ✅ 代码示例：

```text
sliderInput(
  inputId = "sepalLength",
  label = "花萼长度范围：",
  min = min(iris$Sepal.Length),    # 左边界
  max = max(iris$Sepal.Length),    # 右边界
  value = c(min(iris$Sepal.Length), max(iris$Sepal.Length)),  # 初始范围
  step = 0.1                       # 每次移动的间隔
)
```

---

#### 🧩 子模块4：控制显示行数 `numericInput()`

##### ✅ 设计思路：

有时只想查看部分数据，因此允许用户指定“前几行”数据。

##### ✅ 代码示例：

```text
numericInput(
  inputId = "rows",
  label = "显示前几行：",
  value = 10,       # 默认显示10行
  min = 1, max = 150
)
```

---

#### 🧩 子模块5：下载筛选结果 `downloadButton()`

##### ✅ 设计思路：

允许用户将当前筛选的结果导出为 CSV 文件，方便保存与分享。

##### ✅ 代码示例：

```text
downloadButton(
  outputId = "download",     # 与 server 中的 downloadHandler 对应
  label = "下载筛选结果"
)
```

---

#### 🧩 组合：将所有控件放入 `sidebarPanel()` 中

```text
sidebarPanel(
  h4("筛选条件"),

  # 控件1：列选择
  checkboxGroupInput("columns", "选择要显示的列：",
                     choices = names(iris),
                     selected = names(iris)),

  hr(),  # 分割线

  # 控件2：品种选择
  selectInput("species", "选择品种：",
              choices = c("全部", unique(iris$Species)),
              selected = "全部"),

  # 控件3：花萼长度范围
  sliderInput("sepalLength", "花萼长度范围：",
              min = min(iris$Sepal.Length),
              max = max(iris$Sepal.Length),
              value = c(min(iris$Sepal.Length), max(iris$Sepal.Length)),
              step = 0.1),

  # 控件4：显示行数
  numericInput("rows", "显示前几行：",
               value = 10, min = 1, max = 150),

  hr(),

  # 控件5：下载按钮
  downloadButton("download", "下载筛选结果")
)
```

---

#### 📤 主面板 `mainPanel()`：显示结果

```text
mainPanel(
  h4("筛选结果"),
  tableOutput("table"),

  hr(),

  h4("数据摘要"),
  verbatimTextOutput("summary")
)
```

---

#### 🧱 完整 UI 构建

现在我们将侧边栏与主面板合并到 `fluidPage()` 中，组成完整的 `ui`：

```r
ui <- fluidPage(
  titlePanel("鸢尾花数据筛选器"),   # 应用标题

  sidebarLayout(
    sidebarPanel(
      h4("筛选条件"),
      checkboxGroupInput("columns", "选择要显示的列：",
                         choices = names(iris),
                         selected = names(iris)),
      hr(),
      selectInput("species", "选择品种：",
                  choices = c("全部", unique(iris$Species)),
                  selected = "全部"),
      sliderInput("sepalLength", "花萼长度范围：",
                  min = min(iris$Sepal.Length),
                  max = max(iris$Sepal.Length),
                  value = c(min(iris$Sepal.Length), max(iris$Sepal.Length)),
                  step = 0.1),
      numericInput("rows", "显示前几行：",
                   value = 10, min = 1, max = 150),
      hr(),
      downloadButton("download", "下载筛选结果")
    ),

    mainPanel(
      h4("筛选结果"),
      tableOutput("table"),
      hr(),
      h4("数据摘要"),
      verbatimTextOutput("summary")
    )
  )
)
```

---

#### ✅ 提示

- 所有控件的 `inputId` 值必须唯一；
- 输出部分的 `outputId` 会在 `server` 中用 `output$xxx <- renderXXX()` 配合；
- 想要美化界面可以使用 `theme`, `tags$style`, 或 `bslib` 等高级功能。

---

### 第三步：构建服务器逻辑 `server`

我们用 `server <- function(input, output) { ... }` 来定义**所有的计算与响应行为**。所有对 UI 控件的读取，都来自 `input$xxx`，而所有的输出，都通过 `output$xxx <- renderXXX(...)` 来完成。

---

### 🧩 模块1：数据筛选逻辑 `filteredData`

---

#### 🎯 目标

根据用户选择的：

- 品种（`input$species`）
- 花萼长度范围（`input$sepalLength`）
- 显示的列（`input$columns`）
- 显示的行数（`input$rows`）

动态生成筛选后的 `iris` 数据。

---

#### 🧠 思路说明

Shiny 中的 `reactive({...})` 是一个**响应式函数容器**，只要相关输入发生变化，它就会重新计算。

---

#### ✅ 代码实现

```r
filteredData <- reactive({
  data <- iris  # 从原始数据开始

  # 第一步：按品种筛选
  if (input$species != "全部") {
    data <- data[data$Species == input$species, ]
  }

  # 第二步：按花萼长度范围筛选
  data <- data[data$Sepal.Length >= input$sepalLength[1] &
               data$Sepal.Length <= input$sepalLength[2], ]

  # 第三步：按所选列筛选
  data <- data[, input$columns, drop = FALSE]

  # 第四步：限制显示的行数
  head(data, input$rows)
})
```

---

### 🧩 模块2：显示表格 `output$table`

---

#### 🎯 目标

把用户筛选出的数据以**表格形式**在主界面显示。

---

#### 🧠 思路说明

Shiny 中 `renderTable({...})` 会把一个 `data.frame` 转换为 HTML 表格，并自动更新。

---

#### ✅ 代码实现

```r
output$table <- renderTable({
  filteredData()  # 使用上面 reactive 对象
})
```

---

### 🧩 模块3：显示摘要信息 `output$summary`

---

#### 🎯 目标

展示用户筛选出数据的“摘要”，例如：

```text
共筛选出 25 行数据
```

---

#### 🧠 思路说明

- 使用 `renderPrint()` 显示纯文本；
- 使用 `cat()` 实现多行格式。

---

#### ✅ 代码实现

```r
output$summary <- renderPrint({
  data <- filteredData()
  cat("共筛选出", nrow(data), "行数据")
})
```

---

### 🧩 模块4：实现下载按钮 `output$download`

---

#### 🎯 目标

用户点击下载按钮后，将当前筛选结果保存为 CSV 文件。

---

#### 🧠 思路说明

- 用 `downloadHandler()`；
- `filename = function()` 指定文件名；
- `content = function(file)` 写入文件。

---

#### ✅ 代码实现

```r
output$download <- downloadHandler(
  filename = function() {
    paste("iris_filtered_", Sys.Date(), ".csv", sep = "")
  },
  content = function(file) {
    write.csv(filteredData(), file, row.names = FALSE)
  }
)
```

---

#### 🧱 完整 `server` 构建

```r
server <- function(input, output) {

  # 1. 响应式筛选数据
  filteredData <- reactive({
    data <- iris
    if (input$species != "全部") {
      data <- data[data$Species == input$species, ]
    }
    data <- data[data$Sepal.Length >= input$sepalLength[1] &
                 data$Sepal.Length <= input$sepalLength[2], ]
    data <- data[, input$columns, drop = FALSE]
    head(data, input$rows)
  })

  # 2. 显示数据表格
  output$table <- renderTable({
    filteredData()
  })

  # 3. 显示摘要信息
  output$summary <- renderPrint({
    data <- filteredData()
    cat("共筛选出", nrow(data), "行数据")
  })

  # 4. 下载功能
  output$download <- downloadHandler(
    filename = function() {
      paste("iris_filtered_", Sys.Date(), ".csv", sep = "")
    },
    content = function(file) {
      write.csv(filteredData(), file, row.names = FALSE)
    }
  )
}
```

---

#### ✅ 总结：完整项目结构

| 组成 | 功能说明 |
| --- | --- |
| `ui` | 定义界面布局和控件输入、输出位置 |
| `server` | 定义输入如何处理，如何生成输出 |
| `shinyApp(ui, server)` | 启动整个应用 |

---

#### 🚀 启动应用

```r
shinyApp(ui = ui, server = server)
```

## 11. 今日总结

### 11.1 输入控件清单

**文本类：**

- `textInput()` - 单行文本
- `textAreaInput()` - 多行文本（今天没讲）
- `passwordInput()` - 密码输入（今天没讲）

**数字类：**

- `numericInput()` - 数字输入框
- `sliderInput()` - 滑块

**选择类：**

- `selectInput()` - 下拉框
- `radioButtons()` - 单选按钮
- `checkboxInput()` - 单个复选框
- `checkboxGroupInput()` - 复选框组

**日期类：**

- `dateInput()` - 单个日期
- `dateRangeInput()` - 日期范围

**文件类：**

- `fileInput()` - 文件上传

### 11.2 记住这些要点

1. **所有输入控件都需要：**

   - `inputId` - 唯一标识符
   - `label` - 显示给用户的说明
2. **在 Server 中获取值：**

   - 使用 `input$控件ID`
   - 值会自动更新
3. **常见参数：**

   - `value` - 默认值
   - `selected` - 默认选中
   - `choices` - 选项列表
   - `min/max` - 最小/最大值

### 11.3 选择合适的控件

如何选择控件

- 输入文字 → textInput
- 输入数字 → numericInput（精确）或 sliderInput（快速）
- 选一个 → radioButtons（少）或 selectInput（多）
- 选多个 → checkboxGroupInput
- 是/否 → checkboxInput
- 日期 → dateInput
- 文件 → fileInput

恭喜完成 Day 3！

你已经掌握了 Shiny 的所有主要输入控件。
明天我们将学习如何展示各种输出结果！

作业

创建一个“个人信息表单”，包含：

- 姓名（文本）
- 年龄（数字）
- 性别（单选）
- 爱好（多选）
- 生日（日期）
- 简介（文本）
- 头像（文件上传）

并在右侧显示填写的所有信息。
