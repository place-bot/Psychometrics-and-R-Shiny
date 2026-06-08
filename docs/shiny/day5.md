# Day 5: 反应式编程基础 - Shiny 的核心思维

## 1. 理解反应式编程的思维

### 1.1 什么是反应式？

想象一个简单场景：

```text
温度计显示温度
温度变化 → 显示自动更新
```

这就是反应式的核心：**自动更新**。

### 1.2 在 Shiny 中体验反应式

先看最简单的例子：

```r
library(shiny)

ui <- fluidPage(
  sliderInput("x", "选择数字：", 1, 10, 5),
  textOutput("y")
)

server <- function(input, output) {
  output$y <- renderText({
    paste("你选了：", input$x)
  })
}

shinyApp(ui, server)
```

**思维重点：**

- 滑块变 → 文字自动变
- 我们没写任何"监听"代码
- Shiny 自动处理了

## 2. 为什么需要 reactive()？

### 2.1 先看一个问题

假设我们要显示一个数字的平方和立方：

```r
server <- function(input, output) {
  output$square <- renderText({
    input$x ^ 2
  })

  output$cube <- renderText({
    input$x ^ 3
  })
}
```

这样写没问题，但如果计算很复杂呢？

### 2.2 复杂计算的问题

```r
server <- function(input, output) {
  output$result1 <- renderText({
    # 假设这是个耗时计算
    Sys.sleep(2)  # 模拟耗时
    input$x * 100
  })

  output$result2 <- renderText({
    # 又算一遍！
    Sys.sleep(2)  # 又耗时
    input$x * 100
  })
}
```

**问题：** 同样的计算做了两遍！

### 2.3 reactive() 解决方案

```r
server <- function(input, output) {
  # 计算一次，存起来
  result <- reactive({
    Sys.sleep(2)  # 只耗时一次
    input$x * 100
  })

  output$result1 <- renderText({
    result()  # 注意括号！
  })

  output$result2 <- renderText({
    result()  # 重用结果
  })
}
```

**思维要点：**

- `reactive()` = 智能缓存
- 计算一次，多处使用
- 输入变化时自动重算

## 3. reactive() 的思维方式

### 3.1 第一步：识别重复

看这个例子：

```r
# 两个图都需要随机数据
output$hist <- renderPlot({
  data <- rnorm(input$n)  # 生成数据
  hist(data)
})

output$boxplot <- renderPlot({
  data <- rnorm(input$n)  # 又生成了不同的数据！
  boxplot(data)
})
```

### 3.2 第二步：提取共同部分

```r
# 把共同部分提出来
myData <- reactive({
  rnorm(input$n)
})
```

### 3.3 第三步：替换使用

```r
output$hist <- renderPlot({
  hist(myData())  # 用同一份数据
})

output$boxplot <- renderPlot({
  boxplot(myData())  # 用同一份数据
})
```

### 3.4 完整思维过程

```r
library(shiny)

ui <- fluidPage(
  sliderInput("n", "数据量：", 10, 100, 50),
  plotOutput("hist"),
  plotOutput("box")
)

server <- function(input, output) {
  # 思维1：数据只生成一次
  myData <- reactive({
    rnorm(input$n)
  })

  # 思维2：多处使用
  output$hist <- renderPlot({
    hist(myData(), col = "lightblue")
  })

  output$box <- renderPlot({
    boxplot(myData(), col = "lightgreen")
  })
}

shinyApp(ui, server)
```

## 4. observe() 的思维方式

### 4.1 reactive vs observe 的区别

```r
# reactive：计算值
calculated <- reactive({
  input$x * 2  # 返回一个值
})

# observe：执行动作
observe({
  print(input$x)  # 执行一个动作
})
```

**思维区别：**

- `reactive`：我要**算出**什么
- `observe`：我要**做**什么

### 4.2 什么时候用 observe？

当你想要"副作用"时：

```r
server <- function(input, output) {
  observe({
    # 打印日志（副作用）
    cat("用户选择了：", input$choice, "\n")
  })
}
```

### 4.3 实际例子：调试助手

```r
library(shiny)

ui <- fluidPage(
  textInput("name", "姓名："),
  sliderInput("age", "年龄：", 1, 100, 25)
)

server <- function(input, output) {
  # 用 observe 监控所有输入
  observe({
    cat("=== 输入变化 ===\n")
    cat("姓名：", input$name, "\n")
    cat("年龄：", input$age, "\n\n")
  })
}

shinyApp(ui, server)
```

运行后看控制台，每次改变输入都会打印！

## 5. observeEvent() 的思维方式

### 5.1 只在特定时刻执行

`observe()` 太敏感了，任何相关输入变化都会执行。
`observeEvent()` 只在你指定的时刻执行。

```text
# observe：name 或 age 变化都执行
observe({
  cat(input$name, input$age)
})

# observeEvent：只在点击按钮时执行
observeEvent(input$button, {
  cat(input$name, input$age)
})
```

### 5.2 典型用法：按钮事件

```r
library(shiny)

ui <- fluidPage(
  textInput("text", "输入文字："),
  actionButton("save", "保存")
)

server <- function(input, output) {
  observeEvent(input$save, {
    cat("保存了：", input$text, "\n")
  })
}

shinyApp(ui, server)
```

## 6. reactiveValues() 的思维方式

### 6.1 为什么需要存储变量？

在 Shiny 中，普通变量不会触发更新：

```r
# 这样不行！
server <- function(input, output) {
  count <- 0  # 普通变量

  observeEvent(input$add, {
    count <- count + 1  # 修改了，但界面不会更新
  })
}
```

### 6.2 使用 reactiveValues

```r
server <- function(input, output) {
  # 创建反应式变量
  values <- reactiveValues(count = 0)

  observeEvent(input$add, {
    values$count <- values$count + 1  # 这样界面会更新！
  })
}
```

### 6.3 简单计数器

```r
library(shiny)

ui <- fluidPage(
  actionButton("add", "+1"),
  actionButton("minus", "-1"),
  h3(textOutput("count"))
)

server <- function(input, output) {
  # 存储计数
  values <- reactiveValues(count = 0)

  # 加
  observeEvent(input$add, {
    values$count <- values$count + 1
  })

  # 减
  observeEvent(input$minus, {
    values$count <- values$count - 1
  })

  # 显示
  output$count <- renderText(values$count)
}

shinyApp(ui, server)
```

## 7. 构建复杂功能

### 7.1 思维步骤

1. **输入** → 用户能改变什么？
2. **状态** → 需要记住什么？（reactiveValues）
3. **计算** → 需要算什么？（reactive）
4. **动作** → 需要做什么？（observeEvent）
5. **输出** → 显示什么？（renderXXX）

### 7.2 例子：简单的购物车

**第一步：分析需求**

```text
# 需求：
# 1. 用户可以从下拉菜单中选择商品
# 2. 点击按钮将商品添加到购物车
# 3. 显示购物车中已选商品的列表及总价
# 4. 提供一个“清空购物车”的按钮
```

**第二步：设计状态**

```r
# 使用 reactiveValues 来保存购物车状态
# 这里我们同时记录商品名称和商品价格
values <- reactiveValues(
  cart = character(0),   # 存储商品代号（如 "apple"）
  prices = numeric(0)    # 存储对应价格
)
```

> 解释：虽然实际代码可以只存商品名并查表获取价格，但这里为了教学清晰，保留了显式记录价格的方式，让数据结构一一对应，便于观察。

**第三步：添加输入**

```r
ui <- fluidPage(
  selectInput("item", "选择商品：",
              choices = c("苹果-5元" = "apple",
                          "香蕉-3元" = "banana",
                          "橙子-4元" = "orange")),
  actionButton("add", "添加到购物车")
)
```

> 解释：使用 `selectInput()` 创建一个下拉框，显示商品及价格；用户选择后点击 `actionButton()` 来添加商品。

**第四步：处理动作**

```r
# 商品价格查找表
price_table <- c(apple = 5, banana = 3, orange = 4)

# 添加商品逻辑
observeEvent(input$add, {
  # 把商品名加入购物车
  values$cart <- c(values$cart, input$item)

  # 从价格表中查找价格并添加
  values$prices <- c(values$prices, price_table[input$item])
})
```

> 解释：`observeEvent` 在按钮被点击时触发，从输入中读取商品，并更新 `cart` 和 `prices`。

**第五步：计算总价**

```r
# 实时计算总价
total <- reactive({
  sum(values$prices)
})
```

> 解释：每当购物车中价格变化时，自动更新总价。

**第六步：完整组合**

```r
library(shiny)

ui <- fluidPage(
  h3("简单购物车"),

  # 商品选择输入
  selectInput("item", "选择商品：",
              choices = c("苹果-5元" = "apple",
                          "香蕉-3元" = "banana",
                          "橙子-4元" = "orange")),
  actionButton("add", "添加"),
  actionButton("clear", "清空"),

  hr(),

  # 显示购物车内容
  h4("购物车："),
  verbatimTextOutput("cart"),

  # 显示总价
  h4(textOutput("total"))
)

server <- function(input, output) {
  # 商品价格表（用于查找）
  prices <- c(apple = 5, banana = 3, orange = 4)
  # 商品名称映射（用于显示）
  names_cn <- c(apple = "苹果", banana = "香蕉", orange = "橙子")

  # 状态记录：商品代号和价格
  values <- reactiveValues(
    cart = character(0),
    prices = numeric(0)
  )

  # 添加商品到购物车
  observeEvent(input$add, {
    values$cart <- c(values$cart, input$item)
    values$prices <- c(values$prices, prices[input$item])
  })

  # 清空购物车
  observeEvent(input$clear, {
    values$cart <- character(0)
    values$prices <- numeric(0)
  })

  # 实时计算总价
  total <- reactive({
    sum(values$prices)
  })

  # 显示购物车内容
  output$cart <- renderPrint({
    if (length(values$cart) == 0) {
      "购物车是空的"
    } else {
      # 显示商品中文名称及数量
      table(names_cn[values$cart])
    }
  })

  # 显示总价
  output$total <- renderText({
    paste("总价：", total(), "元")
  })
}

shinyApp(ui, server)
```

## 8. 反应式编程的思维模式

### 8.1 三种思维模式

1. **值的传递**（reactive）

```text
A 变化 → B 自动重算 → C 自动更新
```

1. **事件响应**（observeEvent）

```text
按钮点击 → 执行特定动作
```

1. **状态管理**（reactiveValues）

```text
存储可变状态 → 状态改变 → 界面更新
```

### 8.2 选择指南

问自己这些问题：

- 我要**计算**什么？→ `reactive()`
- 我要**做**什么？→ `observeEvent()`
- 我要**记住**什么？→ `reactiveValues()`
- 我要**一直监视**什么？→ `observe()`

### 8.3 常见模式

**模式1：输入处理**

```r
# 处理用户输入
cleaned_input <- reactive({
  # 清理、验证、转换输入
  toupper(input$text)
})
```

**模式2：数据流水线**

```r
# 原始数据
raw_data <- reactive({
  read.csv(input$file$datapath)
})

# 清理数据
clean_data <- reactive({
  na.omit(raw_data())
})

# 分析结果
results <- reactive({
  summary(clean_data())
})
```

**模式3：用户交互**

```r
# 状态
values <- reactiveValues(step = 1)

# 下一步
observeEvent(input$next, {
  values$step <- values$step + 1
})

# 上一步
observeEvent(input$prev, {
  values$step <- values$step - 1
})
```

## 9. 调试反应式代码

### 9.1 使用 browser()

```r
my_reactive <- reactive({
  browser()  # 在这里暂停
  input$x * 2
})
```

### 9.2 打印中间值

```r
my_reactive <- reactive({
  cat("输入值是：", input$x, "\n")
  result <- input$x * 2
  cat("结果是：", result, "\n")
  result
})
```

### 9.3 使用 req() 避免错误

```r
my_reactive <- reactive({
  req(input$file)  # 确保文件已上传
  read.csv(input$file$datapath)
})
```

## 10. 今日总结

### 10.1 核心思维

反应式编程就是建立**自动更新链条**：

```text
输入变化 → 自动触发计算 → 自动更新显示
```

### 10.2 四个核心工具

1. **reactive()**：创建智能变量，自动重算
2. **observe()**：持续监听，执行副作用
3. **observeEvent()**：特定事件触发
4. **reactiveValues()**：存储可变状态

### 10.3 思维流程

1. 识别输入（input）
2. 设计状态（reactiveValues）
3. 定义计算（reactive）
4. 处理事件（observeEvent）
5. 生成输出（render）

恭喜掌握反应式思维！

反应式编程的关键不是记住函数，而是理解思维方式。
多练习，慢慢就会形成直觉。

练习建议

不要一开始就写复杂应用。从小功能开始：

1. 一个按钮改变一个数字
2. 两个输入计算一个结果
3. 保存用户的选择历史

每个小功能都是在练习反应式思维！
