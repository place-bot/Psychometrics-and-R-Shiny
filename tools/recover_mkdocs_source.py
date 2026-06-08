from __future__ import annotations

import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SITE = ROOT / ".work" / "gh-pages"
DOCS_DIR = ROOT / "docs"


CASUAL_REPLACEMENTS = {
    "7天搞定": "7 天学习路径",
    "为啥学这个": "为什么学习 Shiny",
    "需要啥基础": "需要哪些基础",
    "高大上": "复杂",
    "能跑起来，能用就行": "先建立可运行、可解释的最小应用",
    "搞个": "构建一个",
    "小抄": "速查表",
    "写在最后": "总结",
    "这份笔记适合谁": "适用对象",
    "这份笔记不适合谁": "不适用对象",
    "学完能做啥": "学习成果",
    "友情提醒": "学习建议",
    "不求甚解": "优先完成入门实践",
    "不想学 HTML/CSS/JavaScript 那些前端的东西": "希望主要使用 R 语言完成交互式数据展示",
    "被老板/导师催着要做个展示的": "需要快速完成数据展示原型的",
    "像我一样懒得看长篇大论的": "希望以短教程形式学习的",
    "复制粘贴代码是最快的学习方式": "从最小可运行示例开始，再逐步修改参数和结构",
    "不要求甚解": "优先完成入门实践",
    "真的很简单": "入门门槛较低",
    "坑": "常见问题",
    "恭喜你完成了 7 天的 Shiny 学习之旅！": "完成 7 天学习路径后，建议继续通过真实数据项目巩固。",
    "现在，去创造属于你的 Shiny 应用吧！": "后续可将示例扩展为可复用的数据分析应用。",
    "就这": "以上内容",
    "先跑起来再说": "先完成可运行示例，再逐步理解原理",
    "就行": "即可",
}


URL_REPLACEMENTS = {
    "https://shiny.rstudio.com/tutorial/": "https://shiny.posit.co/r/getstarted/shiny-basics/lesson1/",
    "https://shiny.rstudio.com/gallery/widget-gallery.html": "https://shiny.posit.co/r/gallery/widgets/widget-gallery/",
    "RStudio Community": "Posit Community",
    "actions/checkout@v2": "actions/checkout@v6",
    "r-lib/actions/setup-r@v1": "r-lib/actions/setup-r@v2",
}


def normalize_markdown(text: str) -> str:
    for old, new in CASUAL_REPLACEMENTS.items():
        text = text.replace(old, new)
    for old, new in URL_REPLACEMENTS.items():
        text = text.replace(old, new)

    text = text.replace("\\\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)

    # Keep Markdown headings readable after markdownify removes HTML anchors.
    text = re.sub(r"^(#{1,6})([^ #])", r"\1 \2", text, flags=re.MULTILINE)
    return text.strip() + "\n"


def page_to_markdown(html_path: Path, out_path: Path) -> str:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    article = soup.select_one("article.md-content__inner")
    if article is None:
        raise RuntimeError(f"Could not find article body in {html_path}")

    for tag in article.select("a.headerlink, script, style"):
        tag.decompose()

    for img in article.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        image_name = src.split("/")[-1]
        rel_target = Path("assets") / "images" / image_name
        relative_src = Path("../" * (len(out_path.relative_to(DOCS_DIR).parents) - 1)) / rel_target
        img["src"] = relative_src.as_posix()

    markdown = md(
        str(article),
        heading_style="ATX",
        bullets="-",
        strip=["span"],
    )
    return normalize_markdown(markdown)


def output_path_for(html_path: Path) -> Path:
    relative = html_path.relative_to(SOURCE_SITE)
    if relative == Path("index.html"):
        return DOCS_DIR / "index.md"
    parent = relative.parent
    return DOCS_DIR / parent.with_suffix(".md")


def main() -> None:
    if not SOURCE_SITE.exists():
        raise SystemExit(f"Missing source site: {SOURCE_SITE}")

    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)

    images_src = SOURCE_SITE / "assets" / "images"
    if images_src.exists():
        shutil.copytree(images_src, DOCS_DIR / "assets" / "images")

    pages = sorted(SOURCE_SITE.rglob("index.html"))
    for html_path in pages:
        out_path = output_path_for(html_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_to_markdown(html_path, out_path), encoding="utf-8")

    recovered = "\n".join(
        f"- {output_path_for(path).relative_to(ROOT).as_posix()} <- {path.relative_to(SOURCE_SITE).as_posix()}"
        for path in pages
    )
    (ROOT / "RECOVERED_SOURCE.md").write_text(
        "# Recovered MkDocs Source\n\n"
        "The original `main` branch only contained a minimal README. "
        "These source files were reconstructed from the deployed MkDocs HTML in `origin/gh-pages`.\n\n"
        f"Recovered pages:\n\n{recovered}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
