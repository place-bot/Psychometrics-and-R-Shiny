# Day 6: 实战项目 - 数据探索工具

## 1. 项目规划：我们要做什么

### 1.1 需求分析

我们要做一个数据探索工具，功能包括：

1. **上传功能**：用户上传 CSV 文件
2. **查看功能**：预览数据内容
3. **分析功能**：生成统计图表
4. **下载功能**：下载分析结果

### 1.2 开发思路

不要一次做完所有功能，而是：

```text
空壳 → 上传 → 显示 → 分析 → 下载 → 美化
```

每一步都要能运行！

## 2. 第一步：创建最简单的框架

### 2.1 最基础的 Shiny App

```r
library(shiny)

ui <- fluidPage(
  "Hello World"
)

server <- function(input, output) {
}

shinyApp(ui, server)
```

**思维要点：**

- 先确保 Shiny 正常工作
- 从最简单的开始

### 2.2 添加基本布局

```r
ui <- fluidPage(
  # 标题
  titlePanel("数据探索工具"),

  # 主体布局
  sidebarLayout(
    # 左侧面板
    sidebarPanel(
      "控制区域"
    ),

    # 右侧面板
    mainPanel(
      "显示区域"
    )
  )
)
```

**布局解释：**

- `titlePanel()`：页面标题
- `sidebarLayout()`：侧边栏布局（最常用）
- `sidebarPanel()`：放控件
- `mainPanel()`：放结果

## 3. 第二步：添加文件上传功能

### 3.1 理解 fileInput()

```text
fileInput(
  inputId = "file",      # ID，用于在server中引用
  label = "选择文件：",   # 显示的文字
  accept = ".csv"        # 限制文件类型
)
```

### 3.2 添加上传控件

```r
ui <- fluidPage(
  titlePanel("数据探索工具"),

  sidebarLayout(
    sidebarPanel(
      # 添加文件上传
      h4("步骤1：上传数据"),
      fileInput("file", "选择CSV文件：",
                accept = c(".csv", ".CSV")),

      # 分隔线
      hr(),

      # 占位符
      p("更多控件稍后添加...")
    ),

    mainPanel(
      h4("数据预览"),
      p("请先上传文件")
    )
  )
)
```

### 3.3 测试文件上传

在 server 中测试是否能接收到文件：

```r
server <- function(input, output) {
  # 监听文件上传
  observe({
    # 打印文件信息到控制台
    print(input$file)
  })
}
```

**测试方法：**

1. 运行 App
2. 上传一个 CSV 文件
3. 查看 RStudio 控制台

## 4. 第三步：读取 CSV 文件

### 4.1 理解 reactive()

为什么要用 `reactive()`？

```r
# 错误方式：直接读取
server <- function(input, output) {
  # 这样会报错！
  data <- read.csv(input$file$datapath)
}

# 正确方式：使用 reactive
server <- function(input, output) {
  data <- reactive({
    read.csv(input$file$datapath)
  })
}
```

### 4.2 安全地读取文件

```r
server <- function(input, output) {
  # 反应式读取数据
  data <- reactive({
    # 确保文件已上传
    req(input$file)

    # 读取CSV
    read.csv(input$file$datapath,
             stringsAsFactors = FALSE)
  })
}
```

**代码解释：**

- `req(input$file)`：要求文件存在，否则停止
- `stringsAsFactors = FALSE`：字符串不转因子

### 4.3 添加错误处理

```r
data <- reactive({
  req(input$file)

  # 尝试读取，捕获可能的错误
  tryCatch({
    df <- read.csv(input$file$datapath,
                   stringsAsFactors = FALSE)
    df
  },
  error = function(e) {
    # 如果出错，返回NULL
    showNotification(
      "文件读取失败，请检查文件格式",
      type = "error"
    )
    NULL
  })
})
```

## 5. 第四步：显示数据预览

### 5.1 添加表格输出

修改 UI 的主面板：

```text
mainPanel(
  h4("数据预览"),
  # 添加表格输出
  tableOutput("preview"),

  # 添加信息输出
  hr(),
  h4("数据信息"),
  verbatimTextOutput("info")
)
```

### 5.2 显示前几行数据

```r
# 在 server 中添加
output$preview <- renderTable({
  # 获取数据
  df <- data()

  # 显示前10行
  head(df, 10)
})
```

### 5.3 显示数据基本信息

```r
output$info <- renderPrint({
  df <- data()

  cat("📊 数据集信息\n")
  cat("=" , rep("=", 30), "\n", sep = "")
  cat("文件名：", input$file$name, "\n")
  cat("文件大小：",
      round(input$file$size / 1024, 2), "KB\n")
  cat("行数：", nrow(df), "\n")
  cat("列数：", ncol(df), "\n")
  cat("\n列名：\n")
  for(i in 1:ncol(df)) {
    cat(i, ". ", names(df)[i],
        " (", class(df[[i]]), ")\n", sep = "")
  }
})
```

## 6. 第五步：添加列选择功能

### 6.1 为什么需要动态 UI？

不同的 CSV 文件有不同的列名，所以选择框必须动态生成。

### 6.2 创建动态选择框

在侧边栏添加：

```text
sidebarPanel(
  h4("步骤1：上传数据"),
  fileInput("file", "选择CSV文件：",
            accept = c(".csv", ".CSV")),

  hr(),

  # 动态UI占位
  h4("步骤2：选择分析列"),
  uiOutput("column_ui")
)
```

### 6.3 生成选择框

```r
output$column_ui <- renderUI({
  # 需要先有数据
  req(data())

  # 获取所有列名
  choices <- names(data())

  # 创建选择框
  selectInput("column",
              "选择要分析的列：",
              choices = choices)
})
```

### 6.4 只显示数值列

```r
output$column_ui <- renderUI({
  req(data())

  df <- data()
  # 找出数值型列
  numeric_cols <- names(df)[sapply(df, is.numeric)]

  if(length(numeric_cols) == 0) {
    # 没有数值列
    p("⚠️ 没有找到数值型列",
      style = "color: red;")
  } else {
    selectInput("column",
                "选择要分析的列：",
                choices = numeric_cols)
  }
})
```

## 7. 第六步：添加统计分析

### 7.1 添加分析选项

继续在动态 UI 中添加：

```r
output$column_ui <- renderUI({
  req(data())

  df <- data()
  numeric_cols <- names(df)[sapply(df, is.numeric)]

  if(length(numeric_cols) == 0) {
    p("⚠️ 没有找到数值型列", style = "color: red;")
  } else {
    tagList(  # 组合多个UI元素
      selectInput("column",
                  "选择要分析的列：",
                  choices = numeric_cols),

      hr(),

      h4("步骤3：选择分析类型"),
      radioButtons("plot_type",
                   "图表类型：",
                   choices = c("直方图" = "hist",
                               "箱线图" = "box",
                               "密度图" = "density"))
    )
  }
})
```

### 7.2 使用标签页组织内容

修改主面板：

```text
mainPanel(
  tabsetPanel(
    # 数据标签
    tabPanel("数据预览",
             br(),
             tableOutput("preview"),
             hr(),
             verbatimTextOutput("info")),

    # 分析标签
    tabPanel("统计分析",
             br(),
             plotOutput("plot"),
             hr(),
             verbatimTextOutput("summary"))
  )
)
```

### 7.3 生成统计图表

```r
output$plot <- renderPlot({
  # 确保已选择列
  req(input$column)

  # 获取选中列的数据
  col_data <- data()[[input$column]]

  # 移除缺失值
  col_data <- na.omit(col_data)

  # 根据选择绘图
  if(input$plot_type == "hist") {
    hist(col_data,
         main = paste("直方图:", input$column),
         xlab = input$column,
         col = "skyblue",
         border = "white")

  } else if(input$plot_type == "box") {
    boxplot(col_data,
            main = paste("箱线图:", input$column),
            ylab = input$column,
            col = "lightgreen")

  } else if(input$plot_type == "density") {
    plot(density(col_data),
         main = paste("密度图:", input$column),
         xlab = input$column,
         lwd = 2,
         col = "red")
    polygon(density(col_data),
            col = rgb(1, 0, 0, 0.2))
  }
})
```

### 7.4 添加统计摘要

```r
output$summary <- renderPrint({
  req(input$column)

  col_data <- data()[[input$column]]

  cat("📈 统计摘要：", input$column, "\n")
  cat("=" , rep("=", 40), "\n", sep = "")

  # 基本统计
  cat("样本量：", length(col_data), "\n")
  cat("缺失值：", sum(is.na(col_data)),
      "(", round(mean(is.na(col_data)) * 100, 1), "%)\n")

  # 有效值统计
  valid_data <- na.omit(col_data)
  if(length(valid_data) > 0) {
    cat("\n有效值统计：\n")
    cat("最小值：", min(valid_data), "\n")
    cat("第一四分位数：", quantile(valid_data, 0.25), "\n")
    cat("中位数：", median(valid_data), "\n")
    cat("平均值：", round(mean(valid_data), 2), "\n")
    cat("第三四分位数：", quantile(valid_data, 0.75), "\n")
    cat("最大值：", max(valid_data), "\n")
    cat("标准差：", round(sd(valid_data), 2), "\n")
    cat("变异系数：",
        round(sd(valid_data)/mean(valid_data), 3), "\n")
  }
})
```

## 8. 第七步：添加下载功能

### 8.1 添加下载标签页

```text
tabPanel("下载结果",
         br(),
         h4("下载选项"),
         p("选择要下载的内容："),

         # 下载数据
         h5("📊 原始数据"),
         downloadButton("download_data",
                        "下载CSV文件"),

         br(), br(),

         # 下载报告
         h5("📄 分析报告"),
         downloadButton("download_report",
                        "下载分析报告"))
```

### 8.2 实现数据下载

```r
output$download_data <- downloadHandler(
  # 文件名
  filename = function() {
    paste0("data_", Sys.Date(), ".csv")
  },

  # 文件内容
  content = function(file) {
    write.csv(data(), file, row.names = FALSE)
  }
)
```

### 8.3 实现报告下载

```r
output$download_report <- downloadHandler(
  filename = function() {
    paste0("report_", Sys.Date(), ".txt")
  },

  content = function(file) {
    # 打开文件连接
    sink(file)

    # 写入报告内容
    cat("数据分析报告\n")
    cat("=" , rep("=", 50), "\n\n", sep = "")

    cat("生成时间：", as.character(Sys.time()), "\n")
    cat("分析文件：", input$file$name, "\n\n")

    # 数据概况
    df <- data()
    cat("数据概况\n")
    cat("-" , rep("-", 30), "\n", sep = "")
    cat("总行数：", nrow(df), "\n")
    cat("总列数：", ncol(df), "\n")
    cat("数值列：", sum(sapply(df, is.numeric)), "\n")
    cat("字符列：", sum(sapply(df, is.character)), "\n\n")

    # 如果选择了列，添加该列的分析
    if(!is.null(input$column)) {
      cat("列分析：", input$column, "\n")
      cat("-" , rep("-", 30), "\n", sep = "")

      col_data <- df[[input$column]]
      valid_data <- na.omit(col_data)

      cat("数据类型：", class(col_data), "\n")
      cat("缺失值：", sum(is.na(col_data)), "\n")
      cat("最小值：", min(valid_data), "\n")
      cat("最大值：", max(valid_data), "\n")
      cat("平均值：", mean(valid_data), "\n")
      cat("标准差：", sd(valid_data), "\n")
    }

    # 关闭文件连接
    sink()
  }
)
```

## 9. 第八步：添加数据筛选功能

### 9.1 添加筛选控件

在动态 UI 中添加：

```text
# 在选择列之后添加
hr(),

h4("步骤4：数据筛选（可选）"),
checkboxInput("enable_filter",
              "启用数据筛选"),

conditionalPanel(
  condition = "input.enable_filter == true",
  uiOutput("filter_ui")
)
```

### 9.2 生成筛选界面

```r
output$filter_ui <- renderUI({
  req(input$column)

  col_data <- data()[[input$column]]

  tagList(
    sliderInput("filter_range",
                "选择数值范围：",
                min = min(col_data, na.rm = TRUE),
                max = max(col_data, na.rm = TRUE),
                value = c(min(col_data, na.rm = TRUE),
                          max(col_data, na.rm = TRUE))),

    textOutput("filter_info")
  )
})
```

### 9.3 应用筛选

创建筛选后的数据：

```r
# 筛选后的数据
filtered_data <- reactive({
  df <- data()

  if(input$enable_filter && !is.null(input$filter_range)) {
    # 应用筛选
    df <- df[df[[input$column]] >= input$filter_range[1] &
             df[[input$column]] <= input$filter_range[2], ]
  }

  df
})

# 显示筛选信息
output$filter_info <- renderText({
  if(input$enable_filter) {
    paste("筛选后剩余", nrow(filtered_data()), "行")
  }
})
```

## 10. 完整代码（带详细注释）

```r
# 加载必要的包
library(shiny)

# ========== UI 部分 ==========
ui <- fluidPage(
  # 应用标题
  titlePanel("数据探索工具 v1.0"),

  # 添加说明信息
  tags$div(
    class = "alert alert-info",
    tags$strong("使用说明："),
    "上传CSV文件 → 选择分析列 → 查看统计图表 → 下载结果"
  ),

  # 主体布局：侧边栏布局
  sidebarLayout(
    # ===== 侧边栏面板 =====
    sidebarPanel(
      # 步骤1：文件上传
      tags$div(
        class = "well",
        h4("📁 步骤1：上传数据"),
        fileInput("file",
                  "选择CSV文件：",
                  accept = c(".csv", ".CSV"),
                  buttonLabel = "浏览...",
                  placeholder = "未选择文件")
      ),

      # 分隔线
      hr(),

      # 动态UI：根据上传的文件生成控件
      uiOutput("column_ui"),

      # 添加一些说明
      br(),
      tags$small(
        class = "text-muted",
        "提示：只有数值型列可以进行统计分析"
      )
    ),

    # ===== 主面板 =====
    mainPanel(
      # 使用标签页组织不同功能
      tabsetPanel(
        id = "tabs",

        # 标签1：数据预览
        tabPanel("数据预览",
                 value = "preview_tab",
                 br(),
                 # 显示数据基本信息
                 verbatimTextOutput("info"),
                 hr(),
                 # 显示数据表格
                 h4("数据前10行"),
                 tableOutput("preview")
        ),

        # 标签2：统计分析
        tabPanel("统计分析",
                 value = "analysis_tab",
                 br(),
                 # 统计图表
                 plotOutput("plot", height = "400px"),
                 hr(),
                 # 统计摘要
                 verbatimTextOutput("summary")
        ),

        # 标签3：下载结果
        tabPanel("下载结果",
                 value = "download_tab",
                 br(),
                 h4("📥 下载选项"),

                 # 下载原始数据
                 tags$div(
                   class = "well",
                   h5("原始数据"),
                   p("下载上传的CSV文件"),
                   downloadButton("download_data",
                                  "下载CSV",
                                  class = "btn-primary")
                 ),

                 # 下载分析报告
                 tags$div(
                   class = "well",
                   h5("分析报告"),
                   p("下载数据分析的文本报告"),
                   downloadButton("download_report",
                                  "下载报告",
                                  class = "btn-success")
                 )
        )
      )
    )
  )
)

# ========== Server 部分 ==========
server <- function(input, output, session) {

  # ===== 反应式表达式 =====

  # 读取上传的CSV文件
  data <- reactive({
    # 确保文件已上传
    req(input$file)

    # 显示进度条
    withProgress(message = '正在读取文件...', value = 0, {
      # 更新进度
      incProgress(0.3, detail = "读取中...")

      # 尝试读取文件，处理可能的错误
      tryCatch({
        # 读取CSV
        df <- read.csv(input$file$datapath,
                       stringsAsFactors = FALSE,
                       fileEncoding = "UTF-8")

        # 更新进度
        incProgress(0.7, detail = "处理中...")

        # 返回数据框
        df

      }, error = function(e) {
        # 如果出错，显示错误信息
        showNotification(
          paste("文件读取错误:", e$message),
          type = "error",
          duration = 5
        )
        return(NULL)
      })
    })
  })

  # ===== 输出部分 =====

  # 显示数据信息
  output$info <- renderPrint({
    # 确保数据已加载
    req(data())

    df <- data()

    cat("📊 数据集信息\n")
    cat(strrep("=", 50), "\n")
    cat("文件名：", input$file$name, "\n")
    cat("文件大小：",
        round(input$file$size / 1024, 2), "KB\n")
    cat("编码：UTF-8\n")
    cat("\n")
    cat("数据维度\n")
    cat(strrep("-", 30), "\n")
    cat("行数：", nrow(df), "\n")
    cat("列数：", ncol(df), "\n")
    cat("\n")
    cat("列信息\n")
    cat(strrep("-", 30), "\n")

    # 显示每列的信息
    for(i in 1:ncol(df)) {
      col_name <- names(df)[i]
      col_type <- class(df[[i]])[1]
      na_count <- sum(is.na(df[[i]]))
      na_pct <- round(na_count / nrow(df) * 100, 1)

      cat(sprintf("%2d. %-20s %-10s 缺失值: %d (%.1f%%)\n",
                  i, col_name, col_type, na_count, na_pct))
    }
  })

  # 显示数据预览
  output$preview <- renderTable({
    req(data())

    # 显示前10行，如果不足10行则显示全部
    head(data(), min(10, nrow(data())))
  },
  striped = TRUE,      # 条纹表格
  hover = TRUE,        # 鼠标悬停效果
  bordered = TRUE      # 边框
  )

  # 动态生成列选择UI
  output$column_ui <- renderUI({
    # 需要先有数据
    req(data())

    df <- data()

    # 找出所有数值型列
    numeric_cols <- names(df)[sapply(df, is.numeric)]

    # 检查是否有数值列
    if(length(numeric_cols) == 0) {
      # 没有数值列时的提示
      tags$div(
        class = "alert alert-warning",
        tags$strong("注意："),
        "数据中没有找到数值型列，无法进行统计分析。"
      )
    } else {
      # 有数值列时，生成选择界面
      tagList(
        tags$div(
          class = "well",
          h4("📊 步骤2：选择分析列"),
          selectInput("column",
                      "选择要分析的列：",
                      choices = numeric_cols,
                      selected = numeric_cols[1])
        ),

        hr(),

        tags$div(
          class = "well",
          h4("📈 步骤3：选择分析类型"),
          radioButtons("plot_type",
                       "图表类型：",
                       choices = list(
                         "直方图" = "hist",
                         "箱线图" = "box",
                         "密度图" = "density",
                         "QQ图" = "qq"
                       ),
                       selected = "hist")
        ),

        hr(),

        # 数据筛选选项
        tags$div(
          class = "well",
          h4("🔍 步骤4：数据筛选（可选）"),
          checkboxInput("enable_filter",
                        "启用数据筛选",
                        value = FALSE),

          # 条件面板：只在启用筛选时显示
          conditionalPanel(
            condition = "input.enable_filter == true",
            uiOutput("filter_ui")
          )
        )
      )
    }
  })

  # 生成筛选UI
  output$filter_ui <- renderUI({
    req(input$column)

    col_data <- data()[[input$column]]
    col_data <- na.omit(col_data)

    if(length(col_data) > 0) {
      tagList(
        sliderInput("filter_range",
                    "选择数值范围：",
                    min = min(col_data),
                    max = max(col_data),
                    value = c(min(col_data), max(col_data)),
                    step = (max(col_data) - min(col_data)) / 100),

        tags$small(
          class = "text-info",
          textOutput("filter_info")
        )
      )
    }
  })

  # 筛选后的数据
  filtered_data <- reactive({
    df <- data()

    # 如果启用了筛选且设置了范围
    if(!is.null(input$enable_filter) &&
       input$enable_filter &&
       !is.null(input$filter_range) &&
       !is.null(input$column)) {

      # 保留在范围内的数据
      keep_rows <- df[[input$column]] >= input$filter_range[1] &
                   df[[input$column]] <= input$filter_range[2]
      keep_rows[is.na(keep_rows)] <- FALSE

      df <- df[keep_rows, ]
    }

    df
  })

  # 显示筛选信息
  output$filter_info <- renderText({
    if(!is.null(input$enable_filter) && input$enable_filter) {
      total <- nrow(data())
      filtered <- nrow(filtered_data())
      paste0("筛选后: ", filtered, " / ", total, " 行 ",
             "(", round(filtered/total*100, 1), "%)")
    }
  })

  # 生成统计图表
  output$plot <- renderPlot({
    # 确保已选择列
    req(input$column)

    # 获取数据
    df <- filtered_data()
    col_data <- df[[input$column]]

    # 移除缺失值
    col_data <- na.omit(col_data)

    # 检查是否有有效数据
    if(length(col_data) == 0) {
      plot(1, type = "n", axes = FALSE,
           xlab = "", ylab = "")
      text(1, 1, "没有有效数据可以绘图",
           cex = 1.5, col = "gray")
      return()
    }

    # 设置图形参数
    par(mar = c(4, 4, 3, 2))

    # 根据选择的类型绘图
    if(input$plot_type == "hist") {
      # 直方图
      hist(col_data,
           breaks = "Sturges",  # 自动确定组数
           main = paste("直方图:", input$column),
           xlab = input$column,
           ylab = "频数",
           col = "skyblue",
           border = "white")

      # 添加正态分布曲线
      x <- seq(min(col_data), max(col_data), length.out = 100)
      y <- dnorm(x, mean = mean(col_data), sd = sd(col_data))
      y <- y * length(col_data) * diff(range(col_data)) / 30
      lines(x, y, col = "red", lwd = 2)

      # 添加均值线
      abline(v = mean(col_data), col = "red",
             lwd = 2, lty = 2)

      # 图例
      legend("topright",
             legend = c("数据", "正态曲线", "均值"),
             col = c("skyblue", "red", "red"),
             lty = c(0, 1, 2),
             pch = c(15, NA, NA),
             lwd = c(NA, 2, 2))

    } else if(input$plot_type == "box") {
      # 箱线图
      boxplot(col_data,
              main = paste("箱线图:", input$column),
              ylab = input$column,
              col = "lightgreen",
              border = "darkgreen",
              notch = TRUE,  # 显示凹槽
              outline = TRUE)  # 显示异常值

      # 添加均值点
      points(1, mean(col_data),
             col = "red", pch = 19, cex = 1.5)

      # 添加数据点（抖动）
      points(jitter(rep(1, length(col_data)), 0.2),
             col_data,
             col = rgb(0, 0, 0, 0.2),
             pch = 19, cex = 0.5)

    } else if(input$plot_type == "density") {
      # 密度图
      d <- density(col_data)
      plot(d,
           main = paste("密度图:", input$column),
           xlab = input$column,
           ylab = "密度",
           lwd = 2,
           col = "blue")

      # 填充区域
      polygon(d, col = rgb(0, 0, 1, 0.2))

      # 添加均值和中位数线
      abline(v = mean(col_data),
             col = "red", lwd = 2, lty = 2)
      abline(v = median(col_data),
             col = "green", lwd = 2, lty = 2)

      # 图例
      legend("topright",
             legend = c("密度曲线", "均值", "中位数"),
             col = c("blue", "red", "green"),
             lty = c(1, 2, 2),
             lwd = 2)

    } else if(input$plot_type == "qq") {
      # QQ图
      qqnorm(col_data,
             main = paste("QQ图:", input$column),
             xlab = "理论分位数",
             ylab = "样本分位数",
             pch = 19,
             col = "darkblue")
      qqline(col_data, col = "red", lwd = 2)

      # 添加说明
      legend("topleft",
             legend = c("数据点", "参考线"),
             col = c("darkblue", "red"),
             pch = c(19, NA),
             lty = c(NA, 1),
             lwd = c(NA, 2))
    }

    # 添加网格
    grid(col = "lightgray", lty = "dotted")
  })

  # 显示统计摘要
  output$summary <- renderPrint({
    req(input$column)

    # 获取数据
    df <- filtered_data()
    col_data <- df[[input$column]]

    cat("📈 统计摘要：", input$column, "\n")
    cat(strrep("=", 50), "\n\n")

    # 样本信息
    cat("样本信息\n")
    cat(strrep("-", 30), "\n")
    cat("总样本量：", length(col_data), "\n")
    cat("缺失值：", sum(is.na(col_data)),
        sprintf("(%.1f%%)", mean(is.na(col_data)) * 100), "\n")
    cat("有效值：", sum(!is.na(col_data)), "\n\n")

    # 计算有效数据的统计量
    valid_data <- na.omit(col_data)

    if(length(valid_data) > 0) {
      # 集中趋势
      cat("集中趋势\n")
      cat(strrep("-", 30), "\n")
      cat("最小值：", min(valid_data), "\n")
      cat("第一四分位数：", quantile(valid_data, 0.25), "\n")
      cat("中位数：", median(valid_data), "\n")
      cat("平均值：", mean(valid_data), "\n")
      cat("第三四分位数：", quantile(valid_data, 0.75), "\n")
      cat("最大值：", max(valid_data), "\n\n")

      # 离散程度
      cat("离散程度\n")
      cat(strrep("-", 30), "\n")
      cat("极差：", max(valid_data) - min(valid_data), "\n")
      cat("四分位距：", IQR(valid_data), "\n")
      cat("方差：", var(valid_data), "\n")
      cat("标准差：", sd(valid_data), "\n")
      cat("标准误：", sd(valid_data)/sqrt(length(valid_data)), "\n")
      cat("变异系数：", sd(valid_data)/mean(valid_data), "\n\n")

      # 分布形态
      cat("分布形态\n")
      cat(strrep("-", 30), "\n")

      # 计算偏度和峰度
      n <- length(valid_data)
      m <- mean(valid_data)
      s <- sd(valid_data)

      skew <- sum((valid_data - m)^3) / (n * s^3)
      kurt <- sum((valid_data - m)^4) / (n * s^4) - 3

      cat("偏度：", round(skew, 3),
          ifelse(abs(skew) < 0.5, "（近似对称）",
                 ifelse(skew > 0, "（右偏）", "（左偏）")), "\n")
      cat("峰度：", round(kurt, 3),
          ifelse(abs(kurt) < 0.5, "（近似正态）",
                 ifelse(kurt > 0, "（尖峰）", "（平峰）")), "\n")

      # 正态性检验（如果样本量合适）
      if(length(valid_data) >= 3 && length(valid_data) <= 5000) {
        sw_test <- shapiro.test(valid_data)
        cat("\nShapiro-Wilk正态性检验\n")
        cat(strrep("-", 30), "\n")
        cat("W统计量：", round(sw_test$statistic, 4), "\n")
        cat("p值：", round(sw_test$p.value, 4), "\n")
        cat("结论：", ifelse(sw_test$p.value > 0.05,
                           "不能拒绝正态性假设",
                           "拒绝正态性假设"), "\n")
      }
    } else {
      cat("没有有效数据进行统计分析\n")
    }
  })

  # ===== 下载功能 =====

  # 下载数据
  output$download_data <- downloadHandler(
    filename = function() {
      # 生成文件名：原文件名_filtered_日期.csv
      base_name <- tools::file_path_sans_ext(input$file$name)
      if(!is.null(input$enable_filter) && input$enable_filter) {
        paste0(base_name, "_filtered_", Sys.Date(), ".csv")
      } else {
        paste0(base_name, "_", Sys.Date(), ".csv")
      }
    },

    content = function(file) {
      # 写入CSV文件
      write.csv(filtered_data(),
                file,
                row.names = FALSE,
                fileEncoding = "UTF-8")

      # 显示成功通知
      showNotification("数据下载成功！",
                       type = "success",
                       duration = 3)
    }
  )

  # 下载报告
  output$download_report <- downloadHandler(
    filename = function() {
      # 生成报告文件名
      base_name <- tools::file_path_sans_ext(input$file$name)
      paste0("report_", base_name, "_", Sys.Date(), ".txt")
    },

    content = function(file) {
      # 创建报告内容
      sink(file)

      cat("数据分析报告\n")
      cat(strrep("=", 60), "\n\n")

      # 基本信息
      cat("报告信息\n")
      cat(strrep("-", 40), "\n")
      cat("生成时间：", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
      cat("分析工具：数据探索工具 v1.0\n")
      cat("操作系统：", Sys.info()["sysname"], "\n")
      cat("R版本：", R.version.string, "\n\n")

      # 文件信息
      cat("文件信息\n")
      cat(strrep("-", 40), "\n")
      cat("文件名：", input$file$name, "\n")
      cat("文件大小：", round(input$file$size / 1024, 2), "KB\n")
      cat("上传时间：",
          format(file.info(input$file$datapath)$mtime,
                 "%Y-%m-%d %H:%M:%S"), "\n\n")

      # 数据概况
      df <- data()
      cat("数据概况\n")
      cat(strrep("-", 40), "\n")
      cat("总行数：", nrow(df), "\n")
      cat("总列数：", ncol(df), "\n")
      cat("数值型列：", sum(sapply(df, is.numeric)), "\n")
      cat("字符型列：", sum(sapply(df, is.character)), "\n")
      cat("逻辑型列：", sum(sapply(df, is.logical)), "\n\n")

      # 列详情
      cat("列详细信息\n")
      cat(strrep("-", 40), "\n")
      for(i in 1:ncol(df)) {
        col_name <- names(df)[i]
        col_type <- class(df[[i]])[1]
        na_count <- sum(is.na(df[[i]]))
        na_pct <- round(na_count / nrow(df) * 100, 1)

        cat(sprintf("%2d. %-20s 类型:%-10s 缺失:%d(%.1f%%)\n",
                    i, col_name, col_type, na_count, na_pct))
      }

      # 如果选择了特定列，添加详细分析
      if(!is.null(input$column)) {
        cat("\n\n")
        cat("选定列分析：", input$column, "\n")
        cat(strrep("=", 60), "\n\n")

        col_data <- df[[input$column]]
        valid_data <- na.omit(col_data)

        # 基本统计
        cat("描述性统计\n")
        cat(strrep("-", 40), "\n")
        cat("样本量：", length(col_data), "\n")
        cat("缺失值：", sum(is.na(col_data)), "\n")
        cat("有效值：", length(valid_data), "\n\n")

        if(length(valid_data) > 0) {
          # 五数概括
          fivenum_vals <- fivenum(valid_data)
          cat("五数概括\n")
          cat(strrep("-", 40), "\n")
          cat("最小值：", fivenum_vals[1], "\n")
          cat("第一四分位数：", fivenum_vals[2], "\n")
          cat("中位数：", fivenum_vals[3], "\n")
          cat("第三四分位数：", fivenum_vals[4], "\n")
          cat("最大值：", fivenum_vals[5], "\n\n")

          # 其他统计量
          cat("其他统计量\n")
          cat(strrep("-", 40), "\n")
          cat("平均值：", mean(valid_data), "\n")
          cat("标准差：", sd(valid_data), "\n")
          cat("方差：", var(valid_data), "\n")
          cat("标准误：", sd(valid_data)/sqrt(length(valid_data)), "\n")
          cat("变异系数：", sd(valid_data)/mean(valid_data), "\n")
          cat("极差：", max(valid_data) - min(valid_data), "\n")
          cat("四分位距：", IQR(valid_data), "\n")

          # 如果启用了筛选，添加筛选信息
          if(!is.null(input$enable_filter) && input$enable_filter) {
            cat("\n筛选信息\n")
            cat(strrep("-", 40), "\n")
            cat("筛选范围：[", input$filter_range[1],
                ", ", input$filter_range[2], "]\n")
            cat("筛选前行数：", nrow(df), "\n")
            cat("筛选后行数：", nrow(filtered_data()), "\n")
            cat("保留比例：",
                round(nrow(filtered_data())/nrow(df)*100, 1), "%\n")
          }
        }
      }

      # 结束语
      cat("\n\n")
      cat(strrep("-", 60), "\n")
      cat("报告结束\n")

      sink()

      # 显示成功通知
      showNotification("报告生成成功！",
                       type = "success",
                       duration = 3)
    }
  )

  # ===== 其他功能 =====

  # 当文件上传后，自动切换到预览标签
  observeEvent(input$file, {
    updateTabsetPanel(session, "tabs", selected = "preview_tab")
  })

  # 当选择列后，自动切换到分析标签
  observeEvent(input$column, {
    if(!is.null(input$column)) {
      updateTabsetPanel(session, "tabs", selected = "analysis_tab")
    }
  })
}

# ========== 运行应用 ==========
shinyApp(ui = ui, server = server)
```

## 11. 项目总结

### 11.1 我们学到了什么

通过这个项目，我们掌握了：

1. **项目开发流程**：

   - 需求分析
   - 逐步实现
   - 测试优化
2. **核心技术点**：

   - 文件上传处理
   - 动态UI生成
   - 数据可视化
   - 下载功能
3. **实际问题处理**：

   - 错误处理
   - 用户体验
   - 代码组织

### 11.2 可以继续改进的地方

1. **支持更多文件格式**：

   - Excel文件（.xlsx）
   - JSON文件
   - 文本文件
2. **更多分析功能**：

   - 相关性分析
   - 多变量分析
   - 时间序列分析
3. **更好的用户体验**：

   - 数据预处理选项
   - 图表自定义
   - 批量处理

### 11.3 关键编程思维

1. **模块化思维**：每个功能独立实现
2. **用户思维**：站在用户角度设计
3. **健壮性思维**：处理各种异常情况
4. **迭代思维**：持续改进和优化

项目完成！

你已经创建了一个功能完整的数据探索工具。
这个工具可以真正用于日常的数据分析工作。

下一步建议

1. 用自己的数据测试这个工具
2. 根据需要添加新功能
3. 分享给需要的人使用
4. 在GitHub上开源你的改进版本
