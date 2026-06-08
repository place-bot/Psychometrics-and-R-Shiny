# Day 7: 部署上线 - 让别人能访问你的 App

## 1. 为什么要部署？

### 1.1 现在的问题

你做好的 Shiny App 只能在自己电脑上运行：

- 别人看不到
- 不能分享链接
- 需要 R 环境才能运行

### 1.2 部署后的好处

部署后，你的 App：

- 有独立网址
- 任何人都能访问
- 不需要安装 R

## 2. 部署前的准备

### 2.1 检查你的代码

在部署前，确保代码没有问题：

```r
# 坏习惯：使用绝对路径
data <- read.csv("C:/Users/张三/Desktop/data.csv")

# 好习惯：使用相对路径
data <- read.csv("data.csv")
```

### 2.2 创建项目文件夹

整理你的文件结构：

```text
my_app/
├── app.R          # Shiny 应用代码
├── data/          # 数据文件夹
│   └── data.csv
└── www/           # 静态文件（图片、CSS等）
    └── logo.png
```

### 2.3 测试依赖包

列出你用到的所有包：

```r
# 在 app.R 开头列出所有包
library(shiny)
library(ggplot2)
library(DT)
# ... 其他包
```

## 3. 方法一：shinyapps.io

### 3.1 什么是 shinyapps.io？

- Posit 提供的 Shiny 应用托管服务
- 适合个人项目、教学演示和轻量级原型
- 免费层通常有应用数量、运行时长和资源限制，具体以账户页面的当前说明为准

### 3.2 注册账户

1. 访问 https://www.shinyapps.io/
2. 点击 "Sign Up"
3. 用邮箱注册（建议用 GitHub 账号）

### 3.3 安装 rsconnect 包

```r
install.packages("rsconnect")
library(rsconnect)
```

### 3.4 连接你的账户

在 shinyapps.io 上：

1. 登录后点击你的用户名
2. 选择 "Tokens"
3. 点击 "Show" 显示 Token

在 R 中运行显示的代码：

```r
rsconnect::setAccountInfo(
  name='你的用户名',
  token='你的token',
  secret='你的secret'
)
```

### 3.5 部署应用

最简单的部署命令：

```r
# 确保在应用目录下
setwd("path/to/my_app")

# 部署
rsconnect::deployApp()
```

### 3.6 部署时的输出

```text
Preparing to deploy application...
Uploading bundle for application: 1234567...
Deploying bundle: 1234567 for application: 1234567...
Building image: 1234567...
Starting instance...
Application successfully deployed to https://username.shinyapps.io/my_app/
```

部署成功后，控制台会输出公开访问地址；该地址就是应用的线上入口。

## 4. 处理部署问题

### 4.1 文件太大

如果出现错误：

```text
Error: The application is too large to be deployed.
```

解决方法：

```r
# 检查文件夹大小
# 免费账户限制 1GB

# 解决方案1：压缩数据
data <- read.csv("big_data.csv")
# 只保留需要的列
data_small <- data[, c("col1", "col2")]
write.csv(data_small, "data.csv")

# 解决方案2：使用数据采样
data_sample <- data[sample(nrow(data), 1000), ]
```

### 4.2 包的问题

如果某个包在服务器上安装失败，优先在项目中声明依赖，而不是在 `app.R` 运行时安装包：

```r
# 推荐：在本地初始化 renv，并提交 renv.lock
install.packages("renv")
renv::init()
renv::snapshot()
```

对于教学小项目，也可以在部署前确认所有依赖包已安装，并在 `app.R` 顶部只保留 `library()` 调用。

### 4.3 中文显示问题

```text
# 确保源文件以 UTF-8 保存
options(encoding = "UTF-8")

# 读取文件时显式指定编码
read.csv("data.csv", fileEncoding = "UTF-8")

# 绘图时指定可用字体
theme_set(theme_minimal(base_family = "sans"))
```

## 5. 管理已部署的应用

### 5.1 查看应用列表

```r
# 查看所有已部署的应用
rsconnect::applications()
```

### 5.2 更新应用

修改代码后重新部署：

```r
# 会自动覆盖原来的版本
rsconnect::deployApp()
```

### 5.3 停止应用

```r
# 暂时停止应用
rsconnect::terminateApp("my_app")
```

### 5.4 查看应用日志

在 shinyapps.io 网站上：

1. 进入 Dashboard
2. 点击你的应用
3. 选择 "Logs" 查看运行日志

## 6. 方法二：本地网络分享

### 6.1 适用场景

- 只想在办公室/家里分享
- 不想上传到互联网
- 数据比较敏感

### 6.2 获取本机 IP 地址

Windows:

```text
ipconfig
# 找到 IPv4 地址，如 192.168.1.100
```

Mac/Linux:

```text
ifconfig
# 找到 inet 地址
```

### 6.3 修改运行方式

```text
# 不要用这个
runApp()

# 改成这个
runApp(host = "0.0.0.0", port = 5678)
```

### 6.4 分享地址

告诉同事访问：

```text
http://你的IP地址:5678
例如：http://192.168.1.100:5678
```

**注意：** 必须在同一个网络下！

## 7. 方法三：打包成独立程序

### 7.1 使用 RInno 创建安装包

安装 RInno：

```r
install.packages("RInno")
library(RInno)
```

### 7.2 创建安装程序

```text
# 创建安装配置
create_app(
  app_name = "我的数据分析工具",
  app_dir = "path/to/my_app",
  dir_out = "installer"
)

# 编译安装程序
compile_iss()
```

### 7.3 分享 exe 文件

生成的 `.exe` 文件可以：

- 发给别人安装
- 不需要 R 环境
- 像普通软件一样使用

## 8. 优化部署的应用

### 8.1 添加加载动画

```r
# UI 端
ui <- fluidPage(
  # 添加加载提示
  tags$head(
    tags$style(
      ".shiny-busy {
        position: fixed;
        top: 50%;
        left: 50%;
        margin-top: -25px;
        margin-left: -50px;
        background-color: #000;
        color: white;
        padding: 10px;
        border-radius: 5px;
      }"
    )
  ),

  # 其他 UI 元素...
)
```

### 8.2 优化启动速度

```r
# 把数据读取放在 app 外面
# 这样只读取一次，不是每个用户都读

# 全局数据（app.R 开头）
global_data <- read.csv("data.csv")

ui <- fluidPage(...)

server <- function(input, output) {
  # 使用全局数据
  data <- reactive({
    global_data
  })
}
```

### 8.3 限制文件上传大小

```text
# 设置最大上传 10MB
options(shiny.maxRequestSize = 10*1024^2)
```

## 9. 实战：部署我们的数据探索工具

### 9.1 准备文件

创建文件夹结构：

```text
data_explorer/
├── app.R
├── sample_data.csv  # 示例数据
└── README.md       # 说明文档
```

### 9.2 添加示例数据

```r
# 在 app.R 中添加
ui <- fluidPage(
  # ... 其他代码

  # 添加示例数据按钮
  actionButton("use_sample", "使用示例数据"),

  # ... 其他代码
)

server <- function(input, output) {
  # 响应示例数据按钮
  observeEvent(input$use_sample, {
    # 使用内置数据集
    values$data <- iris

    showNotification(
      "已加载示例数据：鸢尾花数据集",
      type = "success"
    )
  })

  # ... 其他代码
}
```

### 9.3 添加使用说明

```r
ui <- fluidPage(
  titlePanel("数据探索工具"),

  # 添加说明
  tags$div(
    class = "well",
    h4("使用说明"),
    tags$ol(
      tags$li("点击'使用示例数据'快速体验"),
      tags$li("或上传自己的 CSV 文件"),
      tags$li("选择要分析的数值列"),
      tags$li("查看统计图表和摘要")
    )
  ),

  # ... 其他代码
)
```

### 9.4 部署命令

```r
# 设置应用名称
rsconnect::deployApp(
  appName = "data-explorer",
  appTitle = "数据探索工具"
)
```

## 10. 部署后的维护

### 10.1 监控使用情况

在 shinyapps.io 控制台可以看到：

- 访问次数
- 使用时长
- 错误日志

### 10.2 设置访问限制

下面的示例只适合教学演示。真实项目不要把密码写进源码；应使用 shinyapps.io 账户权限、反向代理认证、企业身份认证，或至少通过环境变量读取密钥。

```r
# 教学示例：使用环境变量提供演示密码
ui <- fluidPage(
  # 登录界面
  conditionalPanel(
    condition = "!output.authenticated",
    wellPanel(
      h3("请登录"),
      passwordInput("password", "密码："),
      actionButton("login", "登录")
    )
  ),

  # 主界面
  conditionalPanel(
    condition = "output.authenticated",
    # 你的应用内容
  )
)

server <- function(input, output, session) {
  # 认证状态
  authenticated <- reactiveVal(FALSE)

  # 登录逻辑
  observeEvent(input$login, {
    if (identical(input$password, Sys.getenv("APP_PASSWORD"))) {
      authenticated(TRUE)
    } else {
      showNotification("密码错误", type = "error")
    }
  })

  # 输出认证状态
  output$authenticated <- reactive({
    authenticated()
  })
  outputOptions(output, "authenticated",
                suspendWhenHidden = FALSE)
}
```

### 10.3 添加 Google Analytics

如果应用处理个人数据或课堂数据，加入统计脚本前应确认隐私告知和机构要求。

```text
# 在 UI 的 head 中添加
tags$head(
  tags$script(
    src = "https://www.googletagmanager.com/gtag/js?id=YOUR_ID"
  ),
  tags$script(
    HTML("
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'YOUR_ID');
    ")
  )
)
```

## 11. 不同部署方式对比

### 11.1 方式对比表

| 方式 | 优点 | 缺点 | 适用场景 |
| --- | --- | --- | --- |
| shinyapps.io | 简单快速 | 有时间限制 | 个人项目、演示 |
| 本地网络 | 数据安全 | 只能内网访问 | 办公室分享 |
| 打包 exe | 像软件一样 | 文件较大 | 分发给客户 |
| 自建服务器 | 完全控制 | 需要技术 | 企业应用 |

### 11.2 选择建议

**如果你是初学者：**
→ 使用 shinyapps.io

**如果你在公司内部使用：**
→ 本地网络分享

**如果你要给客户使用：**
→ 打包成 exe

**如果你是专业开发者：**
→ 考虑自建服务器

## 12. 常见问题解决

### 12.1 部署失败

```text
Error: HTTP 413
Request entity too large
```

解决：减小文件大小

### 12.2 应用很慢

原因和解决：

1. **数据太大** → 使用数据采样
2. **计算复杂** → 使用 reactive 缓存
3. **包太多** → 只加载必要的包

### 12.3 中文乱码

```text
# 确保脚本和数据文件保存为 UTF-8
options(encoding = "UTF-8")

# 读取外部文件时显式指定编码
read.csv("data.csv", fileEncoding = "UTF-8")
```

不建议用 `Sys.setlocale("LC_ALL", "C")` 解决中文问题；`C` locale 通常会使非 ASCII 文本处理更受限。

## 13. 部署清单

部署前检查：

- 代码在本地运行正常
- 没有使用绝对路径
- 数据文件在正确位置
- 所有包都已声明
- 文件总大小合理
- 添加了错误处理
- 有基本的使用说明
- 测试了不同浏览器

## 14. 进阶：自动化部署

### 14.1 使用 GitHub Actions

创建 `.github/workflows/deploy.yml`：

```r
name: Deploy to shinyapps.io

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      SHINY_NAME: ${{ secrets.SHINY_NAME }}
      SHINY_TOKEN: ${{ secrets.SHINY_TOKEN }}
      SHINY_SECRET: ${{ secrets.SHINY_SECRET }}
    steps:
    - uses: actions/checkout@v6

    - uses: r-lib/actions/setup-r@v2

    - name: Install packages
      run: |
        Rscript -e 'install.packages(c("rsconnect", "renv"), repos = "https://cloud.r-project.org")'
        Rscript -e 'renv::restore(prompt = FALSE)'

    - name: Deploy
      run: |
        Rscript -e 'rsconnect::setAccountInfo(name = Sys.getenv("SHINY_NAME"), token = Sys.getenv("SHINY_TOKEN"), secret = Sys.getenv("SHINY_SECRET")); rsconnect::deployApp()'
```

### 14.2 好处

- 推送代码自动部署
- 不用手动运行命令
- 部署凭据放在 GitHub Secrets 中，避免写进源码

## 15. 总结与展望

### 15.1 你学会了

1. **三种部署方式**：

   - 云端部署（shinyapps.io）
   - 本地分享
   - 打包分发
2. **部署技巧**：

   - 优化性能
   - 处理错误
   - 添加功能
3. **维护方法**：

   - 监控使用
   - 更新版本
   - 收集反馈

### 15.2 下一步

1. **完善应用**：

   - 添加更多功能
   - 改进用户体验
   - 优化性能
2. **学习进阶**：

   - Shiny Server 自建
   - Docker 容器化
   - 负载均衡
3. **建立作品集**：

   - GitHub 展示代码
   - 个人网站展示应用
   - 写博客分享经验

## 16. 一周学习总结

### 16.1 学习路径回顾

```text
Day 1: Hello World → 基础交互
Day 2: 布局美化 → 专业界面
Day 3: 输入控件 → 用户交互
Day 4: 展示结果 → 数据输出
Day 5: 反应式编程 → 核心概念
Day 6: 实战项目 → 综合应用
Day 7: 部署上线 → 分享成果
```

### 16.2 核心技能清单

**基础技能：**

- ✓ 创建 UI 和 Server
- ✓ 使用各种输入输出
- ✓ 掌握布局方法
- ✓ 理解反应式编程

**进阶技能：**

- ✓ 动态 UI 生成
- ✓ 文件上传下载
- ✓ 错误处理
- ✓ 部署发布

### 16.3 继续学习资源

**官方资源：**

- [Shiny 官网](https://shiny.posit.co/)
- [Shiny Gallery](https://shiny.posit.co/r/gallery/)
- [Mastering Shiny](https://mastering-shiny.org/)

**社区资源：**

- [Posit Community](https://community.rstudio.com/c/shiny)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/shiny)
- [GitHub 优秀项目](https://github.com/topics/shiny)

**视频教程：**

- YouTube: "Shiny Tutorial"
- Coursera: "Developing Data Products"
- DataCamp: "Building Web Applications with Shiny"

### 16.4 最后的话

完成 7 天学习路径后，建议继续通过真实数据项目巩固。

从第一天的 Hello World，到今天能够部署自己的应用，你已经掌握了 Shiny 开发的核心技能。

后续可将示例扩展为可复用的数据分析应用。
