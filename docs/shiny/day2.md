# Day 2: 布局和主题 - 让你的 App 结构更清晰

## 1. 先复习昨天的内容

### 1.1 昨天学过的函数清单

先整理上一节使用过的函数，并明确各参数的作用：

#### UI 端函数

**1. actionButton() - 创建按钮**

```text
actionButton(inputId = "button1",    # ID，给这个按钮起个名字
             label = "运行示例")      # 按钮上显示的文字
```

**2. sliderInput() - 创建滑块**

```text
sliderInput(inputId = "slider1",      # ID，滑块的名字
            label = "选择一个数字：",   # 滑块上方的说明文字
            min = 1,                  # 最小值
            max = 100,                # 最大值
            value = 50)               # 默认值
```

**3. textInput() - 创建文本输入框**

```text
textInput(inputId = "text1",          # ID，输入框的名字
          label = "请输入文字：",      # 输入框上方的说明
          value = "")                 # 默认值（可选）
```

**4. textOutput() - 显示文字的位置**

```text
textOutput(outputId = "output1")      # ID，要和 server 里对应
```

**5. plotOutput() - 显示图形的位置**

```text
plotOutput(outputId = "plot1",        # ID，要和 server 里对应
           width = "100%",            # 宽度（可选）
           height = "400px")          # 高度（可选）
```

#### Server 端函数

**1. renderText() - 生成文字输出**

```r
output$output1 <- renderText({
  # 这里写要显示的文字
  "Hello World"
})
```

**2. renderPlot() - 生成图形输出**

```r
output$plot1 <- renderPlot({
  # 这里写画图的代码
  plot(1:10)
})
```

**3. observeEvent() - 监听事件**

```r
# 示例：监听按钮点击，点击后更新 text1 的内容
observeEvent(
  input$button1,        # （1）监听哪个输入——用户点击次数 input$button1
  {                      # （2）事件发生时要做什么
    output$text1 <- renderText({
      "你点击了按钮！"
    })
  }
)
```

### 1.2 括号、引号、逗号的使用规则

这部分超级重要！很多错误都是因为这些符号用错了。

#### 圆括号 () 的规则

```text
# 规则1：函数调用必须有圆括号
sliderInput()  # 对的
sliderInput    # 错的！

# 规则2：参数都写在圆括号里，用逗号分隔
sliderInput("id1", "标签", 1, 100, 50)  # 对的
sliderInput "id1" "标签" 1 100 50       # 错的！

# 规则3：圆括号要成对
sliderInput(         # 开始
  "id1",
  "标签"
)                    # 结束，必须对应
```

#### 花括号 {} 的规则

```r
# 规则1：花括号用来包含多行代码
server <- function(input, output) {    # 开始
  # 可以写很多行代码
  output$text1 <- renderText({
    "Hello"
  })
}                                      # 结束

# 规则2：renderXXX 函数里必须有花括号
renderText({         # 对的
  "Hello"
})

renderText("Hello")  # 错的！即使只有一行也要花括号
```

#### 引号的规则

```text
# 规则1：所有 ID 都要加引号
sliderInput("slider1", ...)    # 对的
sliderInput(slider1, ...)      # 错的！

# 规则2：所有显示的文字都要加引号
"选择一个数字："               # 对的
选择一个数字：                 # 错的！

# 规则3：数字不用加引号
min = 1                        # 对的
min = "1"                      # 能用但不推荐

# 规则4：input$ 和 output$ 后面不加引号
input$slider1                  # 对的
input$"slider1"                # 错的！
```

#### 逗号的规则

```r
# 规则1：函数参数之间用逗号分隔
sliderInput("id", "label", 1, 100, 50)  # 对的

# 规则2：最后一个参数后面不要逗号
sliderInput(
  "id",
  "label",
  1,
  100,
  50      # 最后一个，不要逗号
)

# 规则3：列表中的元素也要逗号分隔
fluidPage(
  h1("标题"),           # 要逗号
  p("段落"),            # 要逗号
  sliderInput(...)      # 最后一个不要逗号
)
```

### 1.3 常见的嵌套结构

Shiny 代码经常有很多层嵌套，我们来看看怎么理解：

```r
# 第一层：整个 App
shinyApp(
  # 第二层：UI 定义
  ui = fluidPage(
    # 第三层：布局
    sidebarLayout(
      # 第四层：侧边栏
      sidebarPanel(
        # 第五层：具体控件
        sliderInput("id", "label", 1, 100, 50)
      ),
      # 第四层：主面板
      mainPanel(
        # 第五层：输出
        plotOutput("plot")
      )
    )
  ),
  # 第二层：Server 定义
  server = function(input, output) {
    # 第三层：输出定义
    output$plot <- renderPlot({
      # 第四层：具体代码
      plot(1:10)
    })
  }
)
```

缩进技巧

每深入一层，就多缩进 2 个空格
这样代码结构一目了然

## 2. 布局基础：让 App 有条理

### 2.1 最简单的布局：fluidPage

昨天我们用过 `fluidPage()`，它是最基础的布局：

```r
library(shiny)

ui <- fluidPage(
  h1("这是标题"),
  p("这是第一段"),
  p("这是第二段"),
  sliderInput("slider", "滑块", 1, 100, 50),
  plotOutput("plot")
)

server <- function(input, output) {
  output$plot <- renderPlot({
    plot(1:input$slider)
  })
}

shinyApp(ui = ui, server = server)
```

问题：所有内容都堆在一起，信息层级不清晰。

### 2.2 侧边栏布局：sidebarLayout

这是最常用的布局，左边放控件，右边放结果：

```r
library(shiny)

ui <- fluidPage(
  # 添加标题
  titlePanel("我的数据分析 App"),

  # 侧边栏布局
  sidebarLayout(
    # 左侧：放控件
    sidebarPanel(
      h3("控制面板"),
      sliderInput("num", "选择数据点数量：",
                  min = 10,
                  max = 100,
                  value = 50),

      br(),  # 空行

      selectInput("color", "选择颜色：",
                  choices = c("红色" = "red",
                              "蓝色" = "blue",
                              "绿色" = "green"),
                  selected = "blue")
    ),

    # 右侧：放输出
    mainPanel(
      h3("分析结果"),
      plotOutput("scatter")
    )
  )
)

server <- function(input, output) {
  output$scatter <- renderPlot({
    # 生成随机数据
    x <- rnorm(input$num)
    y <- rnorm(input$num)

    # 画散点图
    plot(x, y,
         col = input$color,
         pch = 19,
         main = paste("散点图 (", input$num, "个点)"))
  })
}

shinyApp(ui = ui, server = server)
```

- `fluidPage(...)`
  创建一个响应式网页布局的最顶层容器。所有 UI 元素都要放在这里面。
- `titlePanel(title)`
  在页面顶部插入一个应用标题。参数 `title` 为字符串。
- `sidebarLayout(sidebar, main)`
  定义一行两列布局：左侧为 `sidebarPanel()`，右侧为 `mainPanel()`。
- `sidebarPanel(...)`
  用于放置各种输入控件（如滑块、下拉框等）的侧边栏区域。
- `mainPanel(...)`
  用于放置输出控件（如图形、表格、文字等）的主显示区域。
- `h3(text)`
  插入一个三级标题标签，参数 `text` 为字符串。
- `br()`
  插入一个 HTML 换行，相当于 `<br>`。
- `sliderInput(inputId, label, min, max, value, ...)`
  滑块控件，用于选择数值。

  - `inputId`：控件的唯一标识（如 `"num"`）。
  - `label`：滑块上方的文字说明。
  - `min`, `max`：取值范围。
  - `value`：初始默认值。
  - 其它可选参数：`step`（步长）、`animate`（动画播放）等。
- `selectInput(inputId, label, choices, selected, ...)`
  下拉选择框。

  - `choices`：一个命名向量，名字是要显示给用户的标签，值是实际返回给 `input$…` 的字符串。
  - `selected`：默认选中的项。
- `plotOutput(outputId, ...)`
  在 UI 中预留一个绘图输出区域。

  - `outputId`：对应服务器端 `output$…`。
  - 可选参数：`height`, `width` 等。
- `renderPlot(expr, ...)`
  在服务器端生成图形输出。

  - `expr`：绘图代码块。
  - 可选参数：`res`（分辨率）、`height`, `width` 等。
- `rnorm(n, mean = 0, sd = 1)`
  生成 `n` 个符合正态分布（平均值 `mean`，标准差 `sd`）的随机数。
- `plot(x, y, col, pch, main, ...)`
  基本绘图函数，绘制散点图。

  - `col`：点的颜色；
  - `pch`：点的形状；
  - `main`：图形标题。
- `paste(..., sep = " ", collapse = NULL)`
  字符串拼接函数，将多个值合并成一个字符串。

  - `sep`：各部分之间的分隔符。
- `shinyApp(ui, server)`
  将 UI 和 server 组装成一个完整的 Shiny 应用并启动它。

### 2.3 流式布局：`fluidRow` 与 `column`

在本示例中，我们使用了以下新函数，请先了解它们的基本用法和参数：

#### 相关函数及用法

- **`fluidPage(...)`**
  创建一个响应式页面容器，所有 UI 元素都要放在这里面。
- **`titlePanel(title)`**
  在页面顶部显示一个大标题。`title` 为字符串。
- **`fluidRow(...)`**
  定义一个“流式”行容器，内部可以放若干个 `column()`，自动适应不同屏幕宽度。
- **`column(width, ...)`**
  在 `fluidRow()` 中定义一列。

  - `width`：占用 12 列网格系统中的份数（1~12）。
  - 例如 `column(6, ...)` 表示占一半宽度，`column(4, ...)` 表示占三分之一宽度。
- **`h3(text)`**
  插入三级标题，`text` 为字符串。
- **`sliderInput(inputId, label, min, max, value, ...)`**
  滑块控件：

  - `inputId`：唯一标识符，用于在服务器端读 `input$inputId`。
  - `label`：显示在滑块上方的文字说明。
  - `min`、`max`：取值范围。
  - `value`：默认值。
- **`plotOutput(outputId, ...)`**
  在 UI 中预留一个绘图区域。`outputId` 对应服务器端的 `output$outputId`。
- **`renderPlot(expr, ...)`**
  在服务器端执行绘图代码，生成图形输出。

  - `expr`：一段 R 代码块，用 `{ … }` 包裹。
- **`rnorm(n, mean = 0, sd = 1)`**
  生成 `n` 个符合正态分布的随机数。
- **`hist(x, ...)`**
  绘制直方图。`x` 为数值向量。
- **`plot(x, y, type, col, main, ...)`**
  绘制散点图或折线图。

  - `type = "l"` 表示折线；默认是散点。
- **`shinyApp(ui, server)`**
  将 UI 和 server 组合并启动整个 Shiny 应用。

下面示例将第一行分为三列，各放一个滑块；第二行分为两列，各放一幅图表：

```r
library(shiny)

ui <- fluidPage(
  titlePanel("灵活的网格布局"),

  # 第一行：三个并列的滑块
  fluidRow(
    column(4,  # 占 4/12 宽度 (1/3)
           h3("第一列"),
           sliderInput("slider1", "滑块1", min = 1, max = 100, value = 50)
    ),
    column(4,  # 占 4/12 宽度 (1/3)
           h3("第二列"),
           sliderInput("slider2", "滑块2", min = 1, max = 100, value = 50)
    ),
    column(4,  # 占 4/12 宽度 (1/3)
           h3("第三列"),
           sliderInput("slider3", "滑块3", min = 1, max = 100, value = 50)
    )
  ),

  # 第二行：两个并列的图表
  fluidRow(
    column(6,  # 占 6/12 宽度 (1/2)
           plotOutput("plot1")
    ),
    column(6,  # 占 6/12 宽度 (1/2)
           plotOutput("plot2")
    )
  )
)

server <- function(input, output) {
  output$plot1 <- renderPlot({
    hist(rnorm(input$slider1),
         col = "lightblue",
         main = paste("直方图1 (n =", input$slider1, ")"))
  })

  output$plot2 <- renderPlot({
    plot(1:input$slider2,
         rnorm(input$slider2),
         type = "l",
         col = "red",
         main = paste("折线图 (n =", input$slider2, ")"))
  })
}

shinyApp(ui = ui, server = server)
```

12 列系统说明

- 每行 (`fluidRow`) 总宽度分成 12 份
- `column(n, ...)` 的 `n` 表示占用其中的几份
- 例如：`column(4)` 占三分之一，`column(6)` 占二分之一，`column(12)` 占整行

## 3. 多标签页：tabsetPanel

在学习多标签页布局之前，我们先了解几个新的 Shiny 函数和概念：

- **`tabsetPanel(...)`**
  创建一个标签页控件容器，用于在同一位置显示多个面板（Tabs）。
- **`tabPanel(title, ...)`**
  定义单个标签页。

  - `title`：标签页上显示的文字。
  - 后续的 `...` 部分是该页要展示的 UI 元素。
- **`sidebarLayout(sidebarPanel, mainPanel)`**
  经典的侧边栏布局，左边放输入控件，右边放输出和内容。
- **`sidebarPanel(...)`** 与 **`mainPanel(...)`**
  分别放置在 `sidebarLayout()` 的左右两侧，用于组织输入（左）和输出或其他内容（右）。
- **`reactive({ ... })`**
  定义一个响应式表达式，当其内部依赖的 `input$…` 发生变化时，自动重新计算并缓存结果。
- **输出函数**

  - `plotOutput("id")` 对应服务器端的 `renderPlot({ ... })`，用于绘图。
  - `tableOutput("id")` 对应服务器端的 `renderTable({ ... })`，用于显示数据表格。
- **UI 布局函数**

  - `fluidPage(...)`：页面顶层容器。
  - `titlePanel("标题")`：页面标题。
  - `h3("文本")`、`p("段落")`：分别插入三级标题和段落文字。

掌握了以上组件，就可以在同一个应用中用标签页灵活地切换不同视图。

### 3.1 基础标签页

```r
library(shiny)

ui <- fluidPage(
  titlePanel("多标签页示例"),

  sidebarLayout(
    sidebarPanel(
      sliderInput("n", "数据点数量：", 10, 100, 50)
    ),

    mainPanel(
      # 标签页面板
      tabsetPanel(
        # 第一个标签
        tabPanel("直方图",
                 h3("数据分布"),
                 plotOutput("hist")
        ),

        # 第二个标签
        tabPanel("散点图",
                 h3("数据散点"),
                 plotOutput("scatter")
        ),

        # 第三个标签
        tabPanel("数据",
                 h3("原始数据"),
                 tableOutput("table")
        ),

        # 第四个标签
        tabPanel("说明",
                 h3("关于这个 App"),
                 p("这是一个演示多标签页的例子。"),
                 p("你可以在不同标签之间切换查看不同内容。")
        )
      )
    )
  )
)

server <- function(input, output) {
  # 生成数据（所有标签共享）
  data <- reactive({
    data.frame(
      x = rnorm(input$n),
      y = rnorm(input$n)
    )
  })

  output$hist <- renderPlot({
    hist(data()$x,
         col = "lightgreen",
         main = "X 变量的分布")
  })

  output$scatter <- renderPlot({
    plot(data()$x, data()$y,
         col = "blue",
         pch = 19,
         main = "X vs Y")
  })

  output$table <- renderTable({
    head(data(), 10)  # 只显示前10行
  })
}

shinyApp(ui = ui, server = server)
```

### 3.2 导航栏页面：`navbarPage`

在 Shiny 中，如果你想要网站顶端就能切换不同“页面”的效果，可以使用 **导航栏布局**。核心函数有：

- **`navbarPage(title, ...)`**
  创建一个带有导航栏的应用框架。

  - `title`：应用名称，显示在最左侧。
- **`tabPanel(title, ...)`**
  定义导航栏中的一个标签页（页面）。

  - `title`：该页在导航栏上的文字。
- **`sidebarLayout(sidebarPanel, mainPanel)`**
  经典的左右结构：左侧是输入控件，右侧是输出。
- **`fileInput(inputId, label, ...)`**
  文件上传控件：

  - `inputId`：用于 `input$inputId` 读取。
  - `label`：显示的说明文字。
- **`checkboxInput(inputId, label, value = TRUE/FALSE)`**
  单个复选框控件：

  - `value`：默认是否选中。
- **`selectInput(inputId, label, choices, ...)`**
  下拉选择框：

  - `choices`：可选项向量或命名向量。
- **`tableOutput(outputId)`** 与 **`renderTable({ ... })`**
  在 UI 里预留表格区域，并在 server 里生成它。
- **`plotOutput(outputId)`** 与 **`renderPlot({ ... })`**
  在 UI 里预留绘图区域，并在 server 里生成图形。

---

**完整示例代码（含完整注释）**

```r
library(shiny)

# UI 部分
ui <- navbarPage(
  title = "我的数据分析平台",  # 应用名称显示在导航栏最左侧

  # ---- 第一个页面：数据导入 ----
  tabPanel("数据导入",
    sidebarLayout(
      # 左侧：文件上传和选项
      sidebarPanel(
        # 上传 CSV 文件
        fileInput(
          inputId = "file",
          label   = "选择 CSV 文件："
        ),
        br(),  # 换行间隔

        # 是否包含表头
        checkboxInput(
          inputId = "header",
          label   = "文件包含表头",
          value   = TRUE
        )
      ),

      # 右侧：显示上传的内容
      mainPanel(
        tableOutput("contents")
      )
    )
  ),

  # ---- 第二个页面：数据可视化 ----
  tabPanel("数据可视化",
    sidebarLayout(
      # 左侧：图表类型选择
      sidebarPanel(
        selectInput(
          inputId = "plotType",
          label   = "选择图表类型：",
          choices = c("直方图", "箱线图", "散点图"),
          selected = "直方图"
        )
      ),

      # 右侧：根据选择绘图
      mainPanel(
        plotOutput("plot")
      )
    )
  ),

  # ---- 第三个页面：关于 ----
  tabPanel("关于",
    h2("关于这个应用"),
    p("版本：1.0"),
    p("作者：你的名字"),
    p("这是一个数据分析演示应用。")
  )
)

# Server 部分
server <- function(input, output) {

  # 渲染表格：演示时使用静态数据，实际可替换为 read.csv(input$file$datapath, header = input$header)
  output$contents <- renderTable({
    # 简化示例：返回两列数据
    data.frame(
      列1 = 1:5,
      列2 = letters[1:5]
    )
  })

  # 渲染图表：根据下拉框选择绘制不同图形
  output$plot <- renderPlot({
    if (input$plotType == "直方图") {
      # 绘制直方图
      hist(
        rnorm(100),               # 随机数据
        col  = "lightblue",       # 填充颜色
        main = "直方图示例"
      )

    } else if (input$plotType == "箱线图") {
      # 绘制箱线图
      boxplot(
        rnorm(100),
        col  = "lightgreen",
        main = "箱线图示例"
      )

    } else {
      # 绘制散点图
      plot(
        rnorm(100), rnorm(100),   # 两组随机数据
        pch  = 19,                # 点的形状
        col  = "red",             # 点的颜色
        main = "散点图示例"
      )
    }
  })
}

# 启动 Shiny 应用
shinyApp(ui = ui, server = server)
```

## 4. 添加 HTML 元素美化

### 4.1 常用 HTML 标签

```r
library(shiny)

ui <- fluidPage(
  # 各种文字格式
  h1("一级标题 - 最大"),
  h2("二级标题"),
  h3("三级标题"),
  h4("四级标题"),

  p("这是一个普通段落。"),

  p("这个段落有", strong("加粗文字"), "和", em("斜体文字"), "。"),

  # 分隔线
  hr(),

  # 带颜色的文字
  p(style = "color:red;", "这是红色文字"),
  p(style = "color:blue; font-size:20px;", "这是蓝色大号文字"),

  # 列表
  tags$ul(
    tags$li("列表项目 1"),
    tags$li("列表项目 2"),
    tags$li("列表项目 3")
  ),

  # 链接
  tags$a(href = "https://shiny.posit.co/", "访问 Shiny 官网"),

  br(),
  br(),

  # 图片（如果有的话）
  # tags$img(src = "logo.png", height = 100)
)

server <- function(input, output) {
}

shinyApp(ui = ui, server = server)
```

### 4.2 使用 wellPanel 创建面板

```r
library(shiny)

ui <- fluidPage(
  titlePanel("使用面板组织内容"),

  fluidRow(
    column(6,
           wellPanel(
             h4("控制面板"),
             sliderInput("n1", "参数 1：", 1, 100, 50),
             sliderInput("n2", "参数 2：", 1, 100, 30),
             p("这些控件在一个灰色面板里")
           )
    ),

    column(6,
           wellPanel(
             h4("信息面板"),
             p("当前时间：", Sys.time()),
             p("R 版本：", R.version.string),
             tags$ul(
               tags$li("这样看起来更整洁"),
               tags$li("内容被组织在一起"),
               tags$li("视觉上更清晰")
             )
           )
    )
  )
)

server <- function(input, output) {
}

shinyApp(ui = ui, server = server)
```

## 5. 使用主题美化：shinythemes

### 5.1 安装和使用主题

#### 前置知识

- **`shinythemes` 包**
  提供多种 Bootstrap 主题，可以快速为你的 Shiny 应用换肤。
- **`theme = shinytheme("…")`**
  在 `fluidPage()` 中通过 `theme` 参数指定启动时的主题。
- **`themeSelector()`**
  内置的主题预览下拉菜单，允许在运行时立即切换主题。
- **按钮样式类（`class`）**

  - `btn-primary`：表示“主要”按钮（蓝色背景）。
  - `btn-warning`：表示“警告”按钮（橙黄色背景）。
  - 这些类都来自 Bootstrap，可通过 `class` 参数传给 `actionButton()` 等函数。

---

#### 完整示例代码

```r
library(shiny)
library(shinythemes)

ui <- fluidPage(
  theme = shinytheme("cerulean"),  # 默认主题
  themeSelector(),                 # 运行时可切换主题

  titlePanel("使用主题的 Shiny App"),

  sidebarLayout(
    sidebarPanel(
      h3("控制面板"),

      sliderInput(
        inputId = "num",
        label   = "数据点数量：",
        min     = 50,
        max     = 200,
        value   = 100
      ),

      # 主要按钮：蓝色背景
      actionButton(
        inputId = "action",
        label   = "点击我",
        class   = "btn-primary"
      ),

      br(), br(),  # 两个换行

      # 警告按钮：橙黄色背景
      actionButton(
        inputId = "action2",
        label   = "次要操作",
        class   = "btn-warning"
      )
    ),

    mainPanel(
      tabsetPanel(
        tabPanel("图表",
                 plotOutput("plot")
        ),
        tabPanel("数据",
                 tableOutput("table")
        ),
        tabPanel("说明",
                 h3("不同主题的外观"),
                 p("切换主题后，你会看到："),
                 tags$ul(
                   tags$li("配色方案变化"),
                   tags$li("字体与间距变化"),
                   tags$li("按钮样式变化"),
                   tags$li("整体视觉效果差异")
                 )
        )
      )
    )
  )
)

server <- function(input, output, session) {
  # 响应式数据
  data <- reactive({
    data.frame(
      x = rnorm(input$num),
      y = rnorm(input$num)
    )
  })

  # 渲染散点图
  output$plot <- renderPlot({
    plot(
      data()$x, data()$y,
      col  = "darkblue",
      pch  = 19,
      main = "随机散点图"
    )
  })

  # 渲染表格
  output$table <- renderTable({
    head(iris, 10)
  })
}

shinyApp(ui = ui, server = server)
```

### 5.2 主题效果对比

不同主题的特点：

- **cerulean**: 蓝色调，专业感
- **cosmo**: 扁平化设计，现代感
- **flatly**: 极简风格，清爽
- **journal**: 新闻风格，正式
- **readable**: 重视可读性
- **spacelab**: 科技感
- **united**: 橙色调，活力
- **yeti**: 蓝灰色调，冷静

## 6. 综合练习：构建结构清晰的 App

这一节我们一步步来完成一个「个人信息管理系统」小练习，通过以下几个步骤：

1. **搭建项目骨架**
2. **添加输入控件**
3. **根据提交按钮渲染个人信息卡片**
4. **绘制年龄分布统计图**
5. **美化布局与主题**

---

### 6.1 搭建项目骨架

首先，创建一个最简 `app.R`，加载必要的包并定义空的 `ui` 和 `server`：

```r
library(shiny)
library(shinythemes)

ui <- fluidPage(
  # 这里先留空
)

server <- function(input, output, session) {
  # 这里先留空
}

shinyApp(ui, server)
```

保存后运行，确认能正常启动一个空白的 Shiny 应用。

---

### 6.2 添加输入控件

在 `ui` 中，我们将左右分两列：左侧放「输入信息面板」，右侧放「输出区域」。

```r
ui <- fluidPage(
  theme = shinytheme("flatly"),  # 设置整体主题

  titlePanel("个人信息管理系统"),

  fluidRow(
    # 左侧：4/12 宽度，放输入控件
    column(4,
      wellPanel(
        h3("输入信息"),
        textInput("name",   "姓名：",    value = ""),
        numericInput("age", "年龄：",    value = 25, min = 1, max = 100),
        selectInput("gender", "性别：",
                    choices = c("男", "女", "其他")),
        selectInput("hobby",  "爱好：",
                    choices = c("运动", "阅读", "音乐", "旅游", "美食")),
        actionButton("submit", "提交",
                     class = "btn-success btn-block")
      )
    ),

    # 右侧：8/12 宽度，放 Tab 输出
    column(8,
      tabsetPanel(
        tabPanel("信息卡片", br(), uiOutput("card")),
        tabPanel("统计",      br(), plotOutput("stats"))
      )
    )
  )
)
```

- `wellPanel()` 用于给输入区域加背景框。
- `actionButton(..., class = "btn-success btn-block")` 指定了「成功绿色」和「铺满宽度」样式。

---

### 6.3 渲染个人信息卡片

在 `server` 里，监听 `input$submit` 的提交事件，使用 `renderUI()` 动态生成信息卡片：

```r
server <- function(input, output, session) {
  output$card <- renderUI({
    # 如果还没输入姓名，提示用户先填写
    if (input$name == "") {
      wellPanel(
        h4("请在左侧输入信息"),
        p("填写完成后点击“提交”按钮")
      )
    } else {
      # 已经输入后，显示详细信息
      wellPanel(
        h3("个人信息卡"),
        hr(),
        p(strong("姓名："), input$name),
        p(strong("年龄："), paste0(input$age, " 岁")),
        p(strong("性别："), input$gender),
        p(strong("爱好："), input$hobby),
        br(),
        p(em("信息提交时间："), Sys.time())
      )
    }
  })
}
```

- `uiOutput("card")` 与 `renderUI({...})` 配合使用，能在 UI 中插入任意 HTML 元素。

---

### 6.4 绘制年龄分布统计图

在前面，我们已经在 UI 中为“统计”标签页预留了一个 `plotOutput("stats")`。现在我们要在服务器端用 `renderPlot()` 填充它，步骤如下：

1. **准备数据**

   - 用户输入的年龄是一个固定值 `input$age`。
   - 为了让图更有“对比性”，我们再生成 50 个随机年龄样本：`sample(20:60, 50, replace = TRUE)`。
   - 最终把两部分合并到一个向量 `ages` 中。
2. **绘制直方图**

```text
   hist(ages,
         col   = "skyblue",     # 柱子的填充色
         main  = "年龄分布",     # 图表标题
         xlab  = "年龄",         # x 轴标签
         ylab  = "人数"          # y 轴标签
   )
   ```
3. `hist()` 会自动把 `ages` 按照区间分箱，并统计每个箱子的频数。
4. **标出用户年龄**
5. 调用 `abline(v = input$age, col = "red", lwd = 2)`：

   - `v = input$age` 表示在 x 轴的该位置画一条垂直线。
   - `col = "red"` 设置颜色为红色，突出显示。
   - `lwd = 2` 设置线的宽度，让它更醒目。
6. **添加文字说明**

```r
   # 先用 hist(..., plot = FALSE)$counts 拿到每个箱子的频数
   counts <- hist(ages, plot = FALSE)$counts
   ymax   <- max(counts) * 0.8    # 取最高频数的 80% 作为文字 y 坐标

   text(input$age,       # x 坐标：用户年龄
         ymax,           # y 坐标：我们计算好的位置
         labels = "您在此", # 要显示的文字
         col    = "red",    # 文字颜色
         pos    = 4         # 文字摆放方向：4 = 文字在坐标点的右侧
   )
   ```

   - `hist(..., plot = FALSE)`：先执行一次不绘图的直方图计算，用来获取原始频数。
   - `text(x, y, labels, col, pos)`：在指定坐标 `(x, y)` 处画文字。
   - `pos = 4` 表示文字放在点的右侧。

---

把以上逻辑放进 `server` 函数中，完整示例如下：

```r
server <- function(input, output, session) {
  # … 上面是个人信息卡片的 renderUI …

  output$stats <- renderPlot({
    # 1. 准备数据
    ages <- c(input$age,
              sample(20:60, 50, replace = TRUE))

    # 2. 绘制直方图
    hist(ages,
         col   = "skyblue",
         main  = "年龄分布",
         xlab  = "年龄",
         ylab  = "人数")

    # 3. 标出用户年龄
    abline(v = input$age, col = "red", lwd = 2)

    # 4. 计算合适的文字位置并添加文字
    counts <- hist(ages, plot = FALSE)$counts
    ymax   <- max(counts) * 0.8
    text(input$age, ymax,
         labels = "您在此",
         col    = "red",
         pos    = 4)
  })
}
```

这样，当用户切换到“统计”标签页，点击“提交”按钮后，就会看到包含用户年龄标记的直方图了。

---

### 6.5 完整代码

将上述各部分整合，得到最终可运行的 `app.R`：

```r
library(shiny)
library(shinythemes)

ui <- fluidPage(
  theme = shinytheme("flatly"),

  titlePanel("个人信息管理系统"),

  fluidRow(
    column(4,
      wellPanel(
        h3("输入信息"),
        textInput("name",   "姓名：",    value = ""),
        numericInput("age", "年龄：",    value = 25, min = 1, max = 100),
        selectInput("gender", "性别：",
                    choices = c("男", "女", "其他")),
        selectInput("hobby",  "爱好：",
                    choices = c("运动", "阅读", "音乐", "旅游", "美食")),
        actionButton("submit", "提交",
                     class = "btn-success btn-block")
      )
    ),
    column(8,
      tabsetPanel(
        tabPanel("信息卡片", br(), uiOutput("card")),
        tabPanel("统计",      br(), plotOutput("stats"))
      )
    )
  )
)

server <- function(input, output, session) {
  output$card <- renderUI({
    if (input$name == "") {
      wellPanel(
        h4("请在左侧输入信息"),
        p("填写完成后点击“提交”按钮")
      )
    } else {
      wellPanel(
        h3("个人信息卡"),
        hr(),
        p(strong("姓名："), input$name),
        p(strong("年龄："), paste0(input$age, " 岁")),
        p(strong("性别："), input$gender),
        p(strong("爱好："), input$hobby),
        br(),
        p(em("信息提交时间："), Sys.time())
      )
    }
  })

  output$stats <- renderPlot({
    ages <- c(input$age, sample(20:60, 50, replace = TRUE))
    hist(ages,
         col   = "skyblue",
         main  = "年龄分布",
         xlab  = "年龄",
         ylab  = "人数")
    abline(v = input$age, col = "red", lwd = 2)
    text(input$age,
         max(hist(ages, plot = FALSE)$counts) * 0.8,
         labels = "您在此", col = "red", pos = 4)
  })
}

shinyApp(ui = ui, server = server)
```

完成后，运行 `shinyApp(ui, server)`，即可体验一个交互式、结构清晰的个人信息管理小应用。

## 7. 今日总结

### 7.1 布局方法总结

1. **基础布局：**

   - `fluidPage()` - 响应式页面容器
   - `titlePanel()` - 添加标题
2. **常用布局：**

   - `sidebarLayout()` - 侧边栏布局（最常用）
   - `fluidRow()` + `column()` - 网格布局（灵活）
   - `wellPanel()` - 内容面板（组织内容）
3. **多页面：**

   - `tabsetPanel()` + `tabPanel()` - 标签页
   - `navbarPage()` - 导航栏页面

### 7.2 美化方法总结

1. **HTML 标签：**

   - 标题：`h1()` 到 `h6()`
   - 文字：`p()`, `strong()`, `em()`
   - 其他：`hr()`, `br()`, `tags$ul()`
2. **样式：**

   - 行内样式：`style = "color:red;"`
   - 按钮类：`class = "btn-primary"`
3. **主题：**

   - 使用 `shinythemes` 包
   - `theme = shinytheme("主题名")`

### 7.3 重要提醒

常见错误

1. 忘记加载 `shinythemes` 包
2. column 的宽度总和超过 12
3. 嵌套层级混淆（优先检查缩进和括号配对）
4. 逗号位置错误（最后一个元素不要逗号）

你学会了

- 使用专业的布局让 App 更有条理
- 用标签页组织复杂内容
- 添加 HTML 元素丰富界面
- 一键切换主题改变外观

明天我们将学习更多输入控件，让用户能以各种方式与你的 App 交互！
