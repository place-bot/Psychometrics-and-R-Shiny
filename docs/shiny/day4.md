# Day 4: 展示结果 - 把分析结果优雅地呈现出来

## 1. 理解输出的基本概念

### 1.1 输入与输出的关系

在 Shiny 中，数据流是这样的：

```text
用户输入 → Server 处理 → 输出显示
```

昨天我们学了各种输入控件，今天来学习如何展示输出结果。

### 1.2 输出的两步走

每个输出都需要两步：

1. **在 UI 中占位置**：用 `XXXOutput()`
2. **在 Server 中生成内容**：用 `renderXXX()`

这两个必须配对使用！

## 2. 文本输出：最简单的开始

### 2.1 认识 textOutput() 和 renderText()

先来看看这两个函数的语法：

```r
# UI 端：占个位置
textOutput(outputId = "mytext")

# Server 端：生成内容
output$mytext <- renderText({
  # 这里写要显示的文字
})
```

**关键点：**

- `outputId` 必须和 `output$` 后面的名字一致
- `renderText()` 里面要用花括号 `{}`

### 2.2 第一个例子：显示当前时间

让我们从最简单的开始：

```r
library(shiny)

# 第一步：创建 UI
ui <- fluidPage(
  h3("显示当前时间"),
  textOutput("currentTime")  # 占个位置，ID 是 "currentTime"
)

# 第二步：创建 Server
server <- function(input, output) {
  # 生成要显示的内容
  output$currentTime <- renderText({
    paste("现在是：", Sys.time())
  })
}

# 第三步：运行
shinyApp(ui = ui, server = server)
```

### 2.3 让文本动起来：响应用户输入

现在加入用户交互：

```r
library(shiny)

ui <- fluidPage(
  h3("文本输出练习"),

  # 输入部分
  textInput("username", "你的名字："),
  sliderInput("age", "你的年龄：", 1, 100, 25),

  # 输出部分
  h4("生成的句子："),
  textOutput("sentence")
)

server <- function(input, output) {
  output$sentence <- renderText({
    # 构建句子
    # 注意：我们可以使用 input$username 和 input$age
    if(input$username == "") {
      "请输入你的名字"
    } else {
      paste(input$username, "今年", input$age, "岁了。")
    }
  })
}

shinyApp(ui = ui, server = server)
```

### 2.4 verbatimTextOutput：保持原始格式

有时我们想保持文本的原始格式（比如显示代码）：

```r
library(shiny)

ui <- fluidPage(
  h3("两种文本输出的区别"),

  h4("普通文本输出 textOutput："),
  textOutput("normal"),

  h4("原格式输出 verbatimTextOutput："),
  verbatimTextOutput("verbatim")
)

server <- function(input, output) {
  # 相同的内容
  text_content <- "第一行\n第二行\n   有缩进的第三行"

  output$normal <- renderText({
    text_content  # 换行和空格会被忽略
  })

  output$verbatim <- renderPrint({
    text_content  # 保持原格式
  })
}

shinyApp(ui = ui, server = server)
```

**什么时候用哪个？**

- `textOutput` + `renderText`：普通文字显示
- `verbatimTextOutput` + `renderPrint`：显示代码、数据结构、保持格式

## 3. 表格输出：展示数据

### 3.1 基础表格：tableOutput() 和 renderTable()

语法结构：

```r
# UI 端
tableOutput(outputId = "mytable")

# Server 端
output$mytable <- renderTable({
  # 返回一个 data.frame
})
```

### 3.2 第一个表格

让我们显示一些数据：

```r
library(shiny)

ui <- fluidPage(
  h3("基础表格展示"),

  # 用滑块控制显示多少行
  sliderInput("rows", "显示多少行：", 1, 10, 5),

  # 表格输出位置
  tableOutput("myTable")
)

server <- function(input, output) {
  output$myTable <- renderTable({
    # 使用内置的 iris 数据集
    # head() 函数取前几行
    head(iris, input$rows)
  })
}

shinyApp(ui = ui, server = server)
```

### 3.3 动态生成表格内容

让我们创建一个根据用户输入动态生成的表格：

```r
library(shiny)

ui <- fluidPage(
  h3("成绩单生成器"),

  # 输入学生信息
  textInput("name", "学生姓名：", "张三"),
  numericInput("chinese", "语文成绩：", 85, 0, 100),
  numericInput("math", "数学成绩：", 90, 0, 100),
  numericInput("english", "英语成绩：", 88, 0, 100),

  hr(),

  # 显示成绩单
  h4("成绩单："),
  tableOutput("report")
)

server <- function(input, output) {
  output$report <- renderTable({
    # 创建一个数据框
    scores <- data.frame(
      科目 = c("语文", "数学", "英语", "总分", "平均分"),
      成绩 = c(
        input$chinese,
        input$math,
        input$english,
        input$chinese + input$math + input$english,
        round((input$chinese + input$math + input$english) / 3, 1)
      )
    )

    scores
  })
}

shinyApp(ui = ui, server = server)
```

### 3.4 使用 DT 包创建交互式表格

普通表格功能有限，让我们用 DT 包创建更强大的表格：

```r
# 先安装 DT 包
install.packages("DT")
```

```r
library(shiny)
library(DT)

ui <- fluidPage(
  h3("交互式表格"),

  # 注意：使用 DT::dataTableOutput 而不是 tableOutput
  DT::dataTableOutput("interactiveTable")
)

server <- function(input, output) {
  # 注意：使用 DT::renderDataTable 而不是 renderTable
  output$interactiveTable <- DT::renderDataTable({
    iris
  }, options = list(
    pageLength = 5,  # 每页显示5行
    searching = TRUE  # 允许搜索
  ))
}

shinyApp(ui = ui, server = server)
```

**DT 表格的优势：**

- 可以搜索
- 可以排序
- 可以分页
- 可以选择显示多少行

## 4. 图形输出：数据可视化

### 4.1 基础图形：plotOutput() 和 renderPlot()

语法结构：

```r
# UI 端
plotOutput(outputId = "myplot",
           width = "100%",    # 可选：宽度
           height = "400px")  # 可选：高度

# Server 端
output$myplot <- renderPlot({
  # 这里写画图代码
  # 可以用 plot()、hist()、boxplot() 等
})
```

### 4.2 第一个图形：直方图

```r
library(shiny)

ui <- fluidPage(
  h3("直方图示例"),

  # 控制直方图的参数
  sliderInput("bins", "组数：", 5, 50, 30),
  selectInput("color", "颜色：",
              choices = c("红色" = "red",
                          "蓝色" = "blue",
                          "绿色" = "green")),

  # 图形输出
  plotOutput("histogram")
)

server <- function(input, output) {
  output$histogram <- renderPlot({
    # 生成随机数据
    data <- rnorm(1000)

    # 画直方图
    hist(data,
         breaks = input$bins,  # 使用用户选择的组数
         col = input$color,    # 使用用户选择的颜色
         main = "正态分布直方图",
         xlab = "值",
         ylab = "频数")
  })
}

shinyApp(ui = ui, server = server)
```

### 4.3 响应式数据处理

当多个输出使用相同的数据时，使用 `reactive()` 避免重复计算：

```r
library(shiny)

ui <- fluidPage(
  h3("数据分析仪表板"),

  sidebarLayout(
    sidebarPanel(
      sliderInput("n", "数据点数量：", 50, 500, 100),
      numericInput("mean", "均值：", 0),
      numericInput("sd", "标准差：", 1, min = 0.1)
    ),

    mainPanel(
      # 多个输出
      plotOutput("histogram"),
      hr(),
      verbatimTextOutput("summary")
    )
  )
)

server <- function(input, output) {
  # 使用 reactive() 创建响应式数据
  # 当输入改变时，数据会自动更新
  myData <- reactive({
    rnorm(input$n, mean = input$mean, sd = input$sd)
  })

  # 输出1：直方图
  output$histogram <- renderPlot({
    hist(myData(),  # 注意要加括号！
         col = "lightblue",
         main = paste("直方图 (n =", input$n, ")"))
  })

  # 输出2：统计摘要
  output$summary <- renderPrint({
    data <- myData()  # 获取数据
    cat("数据摘要：\n")
    cat("样本量：", length(data), "\n")
    cat("均值：", round(mean(data), 2), "\n")
    cat("标准差：", round(sd(data), 2), "\n")
    cat("最小值：", round(min(data), 2), "\n")
    cat("最大值：", round(max(data), 2), "\n")
  })
}

shinyApp(ui = ui, server = server)
```

**编程思维重点：**

- `reactive()` 创建的是一个"智能变量"
- 它会监听相关的输入变化
- 使用时记得加括号：`myData()`

### 4.4 使用 ggplot2 创建更美观的图形

```r
library(shiny)
library(ggplot2)  # 需要先加载 ggplot2

ui <- fluidPage(
  h3("ggplot2 图形"),

  sidebarLayout(
    sidebarPanel(
      selectInput("xvar", "X轴变量：",
                  choices = c("Sepal.Length", "Sepal.Width",
                              "Petal.Length", "Petal.Width")),
      selectInput("yvar", "Y轴变量：",
                  choices = c("Sepal.Length", "Sepal.Width",
                              "Petal.Length", "Petal.Width"),
                  selected = "Sepal.Width")
    ),

    mainPanel(
      plotOutput("scatterplot")
    )
  )
)

server <- function(input, output) {
  output$scatterplot <- renderPlot({
    # 使用 ggplot2 语法
    ggplot(iris, aes_string(x = input$xvar, y = input$yvar)) +
      geom_point(aes(color = Species), size = 3) +
      theme_minimal() +
      labs(title = paste(input$xvar, "vs", input$yvar))
  })
}

shinyApp(ui = ui, server = server)
```

## 5. 动态 UI：uiOutput() 和 renderUI()

### 5.1 为什么需要动态 UI？

有时候我们需要根据用户的选择动态改变界面元素。

语法结构：

```r
# UI 端
uiOutput(outputId = "myui")

# Server 端
output$myui <- renderUI({
  # 返回 UI 元素
})
```

### 5.2 根据条件显示不同内容

```r
library(shiny)

ui <- fluidPage(
  h3("动态界面示例"),

  radioButtons("choice", "你是：",
               choices = c("学生", "老师")),

  # 动态 UI 的位置
  uiOutput("dynamicUI"),

  # 显示结果
  textOutput("result")
)

server <- function(input, output) {
  # 根据选择生成不同的界面
  output$dynamicUI <- renderUI({
    if(input$choice == "学生") {
      # 学生看到的界面
      tagList(  # tagList 用来组合多个 UI 元素
        textInput("studentID", "学号："),
        selectInput("grade", "年级：",
                    choices = c("大一", "大二", "大三", "大四"))
      )
    } else {
      # 老师看到的界面
      tagList(
        textInput("teacherID", "工号："),
        selectInput("subject", "科目：",
                    choices = c("数学", "语文", "英语"))
      )
    }
  })

  # 显示输入的信息
  output$result <- renderText({
    if(input$choice == "学生") {
      # 检查学生界面的输入是否存在
      if(!is.null(input$studentID)) {
        paste("学生", input$studentID, "，", input$grade)
      }
    } else {
      # 检查老师界面的输入是否存在
      if(!is.null(input$teacherID)) {
        paste("老师", input$teacherID, "，教", input$subject)
      }
    }
  })
}

shinyApp(ui = ui, server = server)
```

**编程思维要点：**

1. 使用 `tagList()` 组合多个 UI 元素
2. 动态创建的输入可能不存在，要用 `is.null()` 检查
3. 界面会根据条件实时变化

## 6. 下载功能：downloadButton() 和 downloadHandler()

### 6.1 下载功能的语法

```r
# UI 端
downloadButton(outputId = "download",
               label = "下载")

# Server 端
output$download <- downloadHandler(
  filename = function() {
    # 生成文件名
  },
  content = function(file) {
    # 生成文件内容
  }
)
```

### 6.2 实现数据下载

让我们创建一个可以下载数据的应用：

```r
library(shiny)

ui <- fluidPage(
  h3("数据下载示例"),

  sidebarLayout(
    sidebarPanel(
      sliderInput("nrows", "选择行数：", 1, 150, 10),

      radioButtons("filetype", "文件格式：",
                   choices = c("CSV" = "csv",
                               "文本" = "txt")),

      br(),

      downloadButton("downloadData", "下载数据")
    ),

    mainPanel(
      h4("数据预览："),
      tableOutput("preview")
    )
  )
)

server <- function(input, output) {
  # 准备要下载的数据
  datasetInput <- reactive({
    head(iris, input$nrows)
  })

  # 预览数据
  output$preview <- renderTable({
    datasetInput()
  })

  # 下载处理
  output$downloadData <- downloadHandler(
    # 文件名
    filename = function() {
      paste("iris_data_", Sys.Date(), ".", input$filetype, sep = "")
    },

    # 文件内容
    content = function(file) {
      if(input$filetype == "csv") {
        write.csv(datasetInput(), file, row.names = FALSE)
      } else {
        write.table(datasetInput(), file, row.names = FALSE)
      }
    }
  )
}

shinyApp(ui = ui, server = server)
```

### 6.3 下载图形

不仅可以下载数据，还可以下载图形：

```r
library(shiny)
library(ggplot2)

ui <- fluidPage(
  h3("图形下载示例"),

  sidebarLayout(
    sidebarPanel(
      selectInput("plotType", "图形类型：",
                  choices = c("散点图", "箱线图", "直方图")),

      br(),

      downloadButton("downloadPlot", "下载图形")
    ),

    mainPanel(
      plotOutput("plot")
    )
  )
)

server <- function(input, output) {
  # 创建图形的函数
  makePlot <- function() {
    if(input$plotType == "散点图") {
      ggplot(iris, aes(x = Sepal.Length, y = Sepal.Width, color = Species)) +
        geom_point(size = 3) +
        theme_minimal()
    } else if(input$plotType == "箱线图") {
      ggplot(iris, aes(x = Species, y = Sepal.Length, fill = Species)) +
        geom_boxplot() +
        theme_minimal()
    } else {
      ggplot(iris, aes(x = Sepal.Length)) +
        geom_histogram(bins = 30, fill = "skyblue", color = "black") +
        theme_minimal()
    }
  }

  # 显示图形
  output$plot <- renderPlot({
    makePlot()
  })

  # 下载图形
  output$downloadPlot <- downloadHandler(
    filename = function() {
      paste("plot_", Sys.Date(), ".png", sep = "")
    },

    content = function(file) {
      ggsave(file, plot = makePlot(), width = 8, height = 6)
    }
  )
}

shinyApp(ui = ui, server = server)
```

## 7. 综合练习：数据分析报告生成器

让我们把今天学的所有内容整合起来：

```r
library(shiny)
library(ggplot2)
library(DT)

ui <- fluidPage(
  titlePanel("数据分析报告生成器"),

  sidebarLayout(
    sidebarPanel(
      h4("数据选择"),
      selectInput("dataset", "选择数据集：",
                  choices = c("鸢尾花" = "iris",
                              "汽车" = "mtcars")),

      uiOutput("variableUI"),

      hr(),

      h4("分析选项"),
      checkboxGroupInput("analysis", "选择分析内容：",
                         choices = c("数据摘要" = "summary",
                                     "相关性分析" = "correlation",
                                     "分布图" = "distribution",
                                     "散点图" = "scatter"),
                         selected = c("summary", "distribution")),

      hr(),

      downloadButton("downloadReport", "下载报告")
    ),

    mainPanel(
      tabsetPanel(
        tabPanel("数据预览",
                 DT::dataTableOutput("dataTable")
        ),

        tabPanel("分析结果",
                 uiOutput("analysisOutput")
        )
      )
    )
  )
)

server <- function(input, output) {
  # 获取选择的数据集
  getDataset <- reactive({
    if(input$dataset == "iris") {
      iris
    } else {
      mtcars
    }
  })

  # 动态生成变量选择界面
  output$variableUI <- renderUI({
    data <- getDataset()
    numeric_vars <- names(data)[sapply(data, is.numeric)]

    tagList(
      selectInput("xvar", "X轴变量：",
                  choices = numeric_vars),
      selectInput("yvar", "Y轴变量：",
                  choices = numeric_vars,
                  selected = numeric_vars[2])
    )
  })

  # 数据表格
  output$dataTable <- DT::renderDataTable({
    getDataset()
  }, options = list(pageLength = 10))

  # 分析输出
  output$analysisOutput <- renderUI({
    output_list <- list()

    # 数据摘要
    if("summary" %in% input$analysis) {
      output$summaryText <- renderPrint({
        summary(getDataset())
      })
      output_list <- append(output_list, list(
        h4("数据摘要"),
        verbatimTextOutput("summaryText"),
        hr()
      ))
    }

    # 相关性分析
    if("correlation" %in% input$analysis && !is.null(input$xvar)) {
      output$corPlot <- renderPlot({
        data <- getDataset()
        numeric_data <- data[sapply(data, is.numeric)]
        cor_matrix <- cor(numeric_data)

        # 相关性热力图
        heatmap(cor_matrix,
                main = "相关性热力图",
                margins = c(10, 10))
      })
      output_list <- append(output_list, list(
        h4("相关性分析"),
        plotOutput("corPlot"),
        hr()
      ))
    }

    # 分布图
    if("distribution" %in% input$analysis && !is.null(input$xvar)) {
      output$distPlot <- renderPlot({
        ggplot(getDataset(), aes_string(x = input$xvar)) +
          geom_histogram(bins = 30, fill = "skyblue", color = "black") +
          theme_minimal() +
          labs(title = paste(input$xvar, "的分布"))
      })
      output_list <- append(output_list, list(
        h4("分布图"),
        plotOutput("distPlot"),
        hr()
      ))
    }

    # 散点图
    if("scatter" %in% input$analysis && !is.null(input$xvar) && !is.null(input$yvar)) {
      output$scatterPlot <- renderPlot({
        ggplot(getDataset(), aes_string(x = input$xvar, y = input$yvar)) +
          geom_point(size = 3, alpha = 0.7) +
          geom_smooth(method = "lm", se = TRUE) +
          theme_minimal() +
          labs(title = paste(input$xvar, "vs", input$yvar))
      })
      output_list <- append(output_list, list(
        h4("散点图"),
        plotOutput("scatterPlot")
      ))
    }

    do.call(tagList, output_list)
  })

  # 下载报告
  output$downloadReport <- downloadHandler(
    filename = function() {
      paste("data_report_", Sys.Date(), ".txt", sep = "")
    },

    content = function(file) {
      # 创建报告内容
      sink(file)
      cat("数据分析报告\n")
      cat("生成日期：", as.character(Sys.Date()), "\n")
      cat("数据集：", input$dataset, "\n")
      cat("\n数据摘要：\n")
      print(summary(getDataset()))
      sink()
    }
  )
}

shinyApp(ui = ui, server = server)
```

## 8. 今日总结

### 8.1 输出函数配对

| UI 函数 | Server 函数 | 用途 |
| --- | --- | --- |
| `textOutput()` | `renderText()` | 显示文本 |
| `verbatimTextOutput()` | `renderPrint()` | 显示原格式文本 |
| `tableOutput()` | `renderTable()` | 显示静态表格 |
| `DT::dataTableOutput()` | `DT::renderDataTable()` | 显示交互式表格 |
| `plotOutput()` | `renderPlot()` | 显示图形 |
| `uiOutput()` | `renderUI()` | 动态生成 UI |
| `downloadButton()` | `downloadHandler()` | 下载功能 |

### 8.2 编程思维总结

1. **分解思维**：

   - 先在 UI 占位置
   - 再在 Server 生成内容
   - 最后连接起来
2. **响应式思维**：

   - 使用 `reactive()` 避免重复计算
   - 理解数据流向：输入 → 处理 → 输出
3. **动态思维**：

   - 界面可以根据条件变化
   - 内容可以根据输入更新

### 8.3 最佳实践

1. **命名一致**：UI 的 `outputId` 必须和 Server 的 `output$` 名称一致
2. **检查 NULL**：动态生成的输入可能不存在
3. **使用 reactive**：多个输出用同一数据时
4. **模块化**：把复杂的图形生成逻辑写成函数

Day 4 完成！

你已经掌握了 Shiny 的所有主要输出方式。
结合前三天的输入控件，你已经可以创建功能完整的 Shiny 应用了！

今日作业

创建一个"数据探索器"，要求：
1. 可以上传 CSV 文件
2. 显示数据的前几行（可调节）
3. 显示基本统计信息
4. 可以选择两个变量画散点图
5. 可以下载处理后的数据
