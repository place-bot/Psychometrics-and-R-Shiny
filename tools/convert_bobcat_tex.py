#!/usr/bin/env python3
"""Convert the BOBCAT Chinese LaTeX handout into MkDocs Markdown pages.

This is intentionally a narrow converter for BOBCAT_chinese_notes.tex.  It
preserves the prose and TeX math, maps the custom teaching boxes to Material
admonitions, converts the hand-written tables, and omits the exercise chapter.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "cat" / "bobcat"


CITATIONS = {
    "finn2017maml": "[Finn et al. (2017)](references.md#finn2017maml)",
    "rajeswaran2019meta": "[Rajeswaran et al. (2019)](references.md#rajeswaran2019meta)",
    "bengio2013estimating": "[Bengio et al. (2013)](references.md#bengio2013estimating)",
    "ghosh2021bobcat": "[Ghosh & Lan (2021)](references.md#ghosh2021bobcat)",
    "feng2023cbobcat": "[Feng et al. (2023)](references.md#feng2023cbobcat)",
}


CREFS = {
    "eq:1pl": "1PL 作答概率公式",
    "eq:bce": "二元交叉熵公式",
    "eq:irt-gradient": "IRT 梯度公式",
    "eq:irt-hessian": "IRT Hessian 公式",
    "eq:gd": "梯度下降公式",
    "eq:generic-outer": "双层优化外层公式",
    "eq:generic-inner": "双层优化内层公式",
    "eq:hypergradient-general": "hypergradient 公式",
    "eq:implicit-general": "隐式求导公式",
    "eq:meta-one-student": "单个学生的 meta 损失公式",
    "eq:bobcat-outer": "式（3）",
    "eq:bobcat-inner": "式（4）",
    "eq:bobcat-policy": "式（5）",
    "eq:bobcat-gd": "式（6）",
    "eq:bobcat-policy-objective": "式（7）",
    "eq:bobcat-reinforce": "式（8）",
    "eq:bobcat-chain": "式（9）",
    "eq:bobcat-weighted-inner": "式（10）",
    "eq:theta-weight-influence": "局部最优参数对题目权重的导数",
    "eq:bobcat-influence": "式（11）",
    "eq:approx-policy-gradient": "近似策略梯度公式",
}


ADMONITIONS = {
    "intuition": ("note", "直觉"),
    "warningbox": ("warning", "容易误解"),
    "examplebox": ("example", "小例子"),
    "checkpoint": ("tip", "读到这里应当记住"),
    "derivation": ("info", "推导"),
    "tcolorbox": ("note", "要点"),
}


DIAGRAMS = [
    """```text
选题器给出下一题
        ↓
读取该学生的历史作答
        ↓
内层适应学生参数
        ↓
在 meta 题上计算损失
        ↓
反向更新全局模型与选题器
        └──────────────→ 下一轮选题
```""",
    """```text
全部历史学生
├── 训练学生
│   ├── 学生内 training 候选题
│   └── 学生内 meta 题
├── 验证学生
└── 测试学生
```""",
]


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        out = []
        for char in line:
            if char == "%" and not escaped:
                break
            out.append(char)
            escaped = char == "\\" and not escaped
            if char != "\\":
                escaped = False
        lines.append("".join(out).rstrip())
    return "\n".join(lines)


def extract_braced(text: str, start: int) -> tuple[str, int]:
    if start >= len(text) or text[start] != "{":
        raise ValueError(f"Expected '{{' at {start}: {text[start:start + 30]!r}")
    depth = 0
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if char == "{" and not escaped:
            depth += 1
        elif char == "}" and not escaped:
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    raise ValueError("Unclosed braced argument")


def replace_command(
    text: str,
    command: str,
    nargs: int,
    formatter: Callable[[list[str]], str],
) -> str:
    token = "\\" + command
    cursor = 0
    pieces: list[str] = []
    while True:
        index = text.find(token, cursor)
        if index < 0:
            pieces.append(text[cursor:])
            break
        end_name = index + len(token)
        if end_name < len(text) and text[end_name].isalpha():
            pieces.append(text[cursor:end_name])
            cursor = end_name
            continue
        pos = end_name
        while pos < len(text) and text[pos].isspace():
            pos += 1
        args: list[str] = []
        try:
            for _ in range(nargs):
                arg, pos = extract_braced(text, pos)
                args.append(arg)
                while pos < len(text) and text[pos].isspace():
                    pos += 1
        except ValueError:
            pieces.append(text[cursor:end_name])
            cursor = end_name
            continue
        pieces.append(text[cursor:index])
        pieces.append(formatter(args))
        cursor = pos
    return "".join(pieces)


def replace_optional_title(command_text: str) -> tuple[str, str]:
    match = re.match(r"\\begin\{[^}]+\}(?:\[([^\]]*)\])?", command_text.strip())
    return (match.group(1) if match and match.group(1) else "", command_text)


def clean_inline(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = replace_command(text, "texorpdfstring", 2, lambda a: a[0])
        text = replace_command(text, "textbf", 1, lambda a: f"**{a[0]}**")
        text = replace_command(text, "emph", 1, lambda a: f"*{a[0]}*")
        text = replace_command(text, "texttt", 1, lambda a: f"`{a[0]}`")
        text = replace_command(text, "textcolor", 2, lambda a: f"**{a[1]}**")
        text = replace_command(text, "href", 2, lambda a: f"[{a[1]}]({a[0]})")
        text = replace_command(text, "url", 1, lambda a: f"<{a[0]}>")
        text = replace_command(
            text,
            "cite",
            1,
            lambda a: "; ".join(CITATIONS.get(k.strip(), k.strip()) for k in a[0].split(",")),
        )
        text = replace_command(
            text,
            "cref",
            1,
            lambda a: CREFS.get(a[0], a[0]),
        )

    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = text.replace(r"\E", r"\mathbb{E}")
    text = text.replace(r"\R", r"\mathbb{R}")
    text = text.replace(r"\ind", r"\mathbb{I}")
    text = text.replace(r"\given", r"\,\middle|\,")
    text = text.replace(r"\trans", r"\mathsf{T}")
    text = text.replace(r"\argmin", r"\operatorname*{arg\,min}")
    text = text.replace(r"\argmax", r"\operatorname*{arg\,max}")
    text = text.replace(r"\softmax", r"\operatorname{softmax}")
    text = text.replace(r"\logit", r"\operatorname{logit}")
    text = text.replace(r"\diag", r"\operatorname{diag}")
    text = text.replace(r"\%", "%")
    text = text.replace(r"\_", "_")
    text = text.replace(r"\#", "#")
    text = text.replace("``", "“")
    text = text.replace("''", "”")
    text = re.sub(r"\\(?:small|large|Large|LARGE|Huge|normalsize|centering)\b", "", text)
    text = re.sub(r"\\vspace\*?\{[^}]*\}", "", text)
    # Match the standalone paragraph command only.  A plain string replacement
    # would also remove the ``\par`` prefix from ``\partial``.
    text = re.sub(r"\\par\b", "", text)
    return text.strip()


def split_cells(row: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    depth = 0
    escaped = False
    for char in row:
        if char == "{" and not escaped:
            depth += 1
        elif char == "}" and not escaped:
            depth -= 1
        if char == "&" and depth == 0 and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    cells.append("".join(current).strip())
    return cells


def convert_table(block: str) -> str:
    caption = ""
    caption_pos = block.find(r"\caption")
    if caption_pos >= 0:
        brace = block.find("{", caption_pos)
        caption, caption_end = extract_braced(block, brace)
        block = block[:caption_pos] + block[caption_end:]

    tabular_match = re.search(r"\\begin\{(tabularx|tabular|longtable)\}", block)
    if not tabular_match:
        return ""
    env = tabular_match.group(1)
    pos = tabular_match.end()
    argument_count = 2 if env == "tabularx" else 1
    try:
        for _ in range(argument_count):
            while pos < len(block) and block[pos].isspace():
                pos += 1
            _, pos = extract_braced(block, pos)
    except ValueError:
        return ""
    end_token = rf"\end{{{env}}}"
    end = block.rfind(end_token)
    body = block[pos:end]

    body = re.sub(
        r"\\(?:toprule|midrule|bottomrule|endfirsthead|endhead|hline)\b",
        r"\\\\",
        body,
    )
    raw_rows = re.split(r"\\\\(?:\[[^\]]*\])?", body)
    rows: list[list[str]] = []
    seen_header: list[str] | None = None
    for raw in raw_rows:
        raw = raw.strip()
        if not raw:
            continue
        cells = [clean_inline(cell.replace("\n", " ")) for cell in split_cells(raw)]
        if not any(cells):
            continue
        if seen_header is None:
            seen_header = cells
        elif cells == seen_header:
            continue
        rows.append(cells)

    if not rows:
        return ""
    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    for row in normalized:
        for index, cell in enumerate(row):
            row[index] = re.sub(r"(?<!\\)\|", r"\\vert", cell)

    header = normalized[0]
    output = []
    if caption:
        output.append(f"**表：{clean_inline(caption)}**")
        output.append("")
    output.append("| " + " | ".join(header) + " |")
    output.append("| " + " | ".join(["---"] * width) + " |")
    for row in normalized[1:]:
        output.append("| " + " | ".join(row) + " |")
    return "\n".join(output)


def collect_environment(lines: list[str], start: int, env: str) -> tuple[str, int]:
    depth = 0
    collected: list[str] = []
    begin_token = rf"\begin{{{env}}}"
    end_token = rf"\end{{{env}}}"
    for index in range(start, len(lines)):
        line = lines[index]
        depth += line.count(begin_token)
        depth -= line.count(end_token)
        collected.append(line)
        if depth == 0:
            return "\n".join(collected), index + 1
    raise ValueError(f"Unclosed environment: {env}")


def heading_text(command: str) -> str:
    brace = command.find("{")
    content, _ = extract_braced(command, brace)
    if content.startswith(r"\texorpdfstring"):
        brace2 = content.find("{")
        first, pos = extract_braced(content, brace2)
        while pos < len(content) and content[pos].isspace():
            pos += 1
        if pos < len(content) and content[pos] == "{":
            second, _ = extract_braced(content, pos)
            content = second or first
        else:
            content = first
    return clean_inline(content)


def collect_heading(lines: list[str], start: int) -> tuple[str, int]:
    collected = [lines[start]]
    balance = lines[start].count("{") - lines[start].count("}")
    index = start + 1
    while balance > 0 and index < len(lines):
        collected.append(lines[index])
        balance += lines[index].count("{") - lines[index].count("}")
        index += 1
    return " ".join(line.strip() for line in collected), index


def indent_block(text: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else prefix for line in text.splitlines())


def convert_body(text: str) -> str:
    global _diagram_index
    text = strip_comments(text)
    lines = text.splitlines()
    output: list[str] = []
    list_stack: list[str] = []
    index = 0

    def emit(value: str = "", *, item: bool = False) -> None:
        if not value:
            output.append("")
            return
        if item:
            depth = max(len(list_stack) - 1, 0)
            output.append("    " * depth + list_stack[-1] + " " + value)
        elif list_stack:
            output.append("    " * len(list_stack) + value)
        else:
            output.append(value)

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()

        heading_match = re.match(r"\\(chapter\*?|section|subsection\*?|subsubsection|part)\b", stripped)
        if heading_match:
            command, index = collect_heading(lines, index)
            kind = heading_match.group(1)
            if kind == "part":
                continue
            level = {
                "chapter": 2,
                "chapter*": 2,
                "section": 3,
                "subsection": 4,
                "subsection*": 4,
                "subsubsection": 5,
            }[kind]
            emit("")
            emit("#" * level + " " + heading_text(command))
            emit("")
            continue

        begin_match = re.match(r"\\begin\{([^}]+)\}", stripped)
        if begin_match:
            env = begin_match.group(1)
            if env in ("itemize", "enumerate"):
                list_stack.append("-" if env == "itemize" else "1.")
                index += 1
                continue
            if env in ADMONITIONS:
                block, index = collect_environment(lines, index, env)
                inner_lines = block.splitlines()[1:-1]
                title, _ = replace_optional_title(block.splitlines()[0])
                kind, default_title = ADMONITIONS[env]
                converted = convert_body("\n".join(inner_lines)).strip()
                heading = default_title + (f"：{clean_inline(title)}" if title else "")
                emit(f'!!! {kind} "{heading}"')
                emit(indent_block(converted, 4))
                emit("")
                continue
            if env in ("equation", "align", "align*"):
                block, index = collect_environment(lines, index, env)
                inner = "\n".join(block.splitlines()[1:-1])
                inner = re.sub(r"\\label\{[^}]+\}", "", inner)
                inner = inner.replace(r"\notag", "")
                inner = clean_inline(inner)
                if env.startswith("align"):
                    tag_match = re.search(r"\\tag\{[^}]+\}", inner)
                    tag = tag_match.group(0) if tag_match else ""
                    if tag_match:
                        inner = inner[: tag_match.start()] + inner[tag_match.end() :]
                    inner = "\\begin{aligned}\n" + inner + "\n\\end{aligned}"
                    if tag:
                        inner += "\n" + tag
                emit("")
                emit("\\[\n" + inner + "\n\\]")
                emit("")
                continue
            if env == "lstlisting":
                block, index = collect_environment(lines, index, env)
                first = block.splitlines()[0]
                language = "python" if "Python" in first else "text"
                caption_match = re.search(r"caption=\{([^}]*)\}", first)
                if caption_match:
                    emit(f"**代码：{clean_inline(caption_match.group(1))}**")
                    emit("")
                code = "\n".join(block.splitlines()[1:-1])
                emit(f"```{language}\n{code}\n```")
                emit("")
                continue
            if env in ("table", "longtable"):
                block, index = collect_environment(lines, index, env)
                emit("")
                emit(convert_table(block))
                emit("")
                continue
            if env == "tikzpicture":
                _, index = collect_environment(lines, index, env)
                diagram = DIAGRAMS[_diagram_index] if _diagram_index < len(DIAGRAMS) else ""
                _diagram_index += 1
                emit(diagram)
                emit("")
                continue
            if env in ("center", "quote"):
                block, index = collect_environment(lines, index, env)
                converted = convert_body("\n".join(block.splitlines()[1:-1])).strip()
                if env == "quote":
                    converted = "\n".join("> " + row if row else ">" for row in converted.splitlines())
                emit(converted)
                emit("")
                continue

        if re.match(r"\\end\{(itemize|enumerate)\}", stripped):
            if list_stack:
                list_stack.pop()
            emit("")
            index += 1
            continue

        if stripped.startswith(r"\item"):
            item_text = clean_inline(stripped[len(r"\item") :].strip())
            emit(item_text, item=True)
            index += 1
            continue

        if stripped in {
            r"\mainmatter",
            r"\frontmatter",
            r"\backmatter",
            r"\appendix",
            r"\tableofcontents",
            r"\centering",
        }:
            index += 1
            continue

        if stripped.startswith(r"\addcontentsline"):
            index += 1
            continue

        emit(clean_inline(line))
        index += 1

    result = "\n".join(output)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"


def between(text: str, start: str, end: str) -> str:
    left = text.index(start) + len(start)
    right = text.index(end, left)
    return text[left:right]


def write_page(filename: str, title: str, source: str, intro: str = "") -> None:
    content = f"# {title}\n\n"
    if intro:
        content += intro.strip() + "\n\n"
    content += convert_body(source)
    (OUTPUT / filename).write_text(content, encoding="utf-8")


def convert_references(text: str) -> str:
    entries = re.split(r"\\bibitem\{([^}]+)\}", text)
    output = ["# CAT 与 BOBCAT 参考文献", ""]
    for index in range(1, len(entries), 2):
        key = entries[index]
        body = entries[index + 1]
        body = body.split(r"\end{thebibliography}", 1)[0]
        body = body.replace(r"\newblock", " ")
        body = clean_inline(body)
        body = re.sub(r"\s+", " ", body).strip()
        if body:
            output.extend([f'<a id="{key}"></a>', "", f"- {body}", ""])
    return "\n".join(output).strip() + "\n"


def main() -> None:
    arguments = sys.argv[1:]
    force = "--force" in arguments
    arguments = [argument for argument in arguments if argument != "--force"]
    if len(arguments) != 1:
        raise SystemExit(
            "Usage: convert_bobcat_tex.py [--force] /path/to/BOBCAT_chinese_notes.tex"
        )
    source_path = Path(arguments[0]).expanduser().resolve()
    text = source_path.read_text(encoding="utf-8")
    OUTPUT.mkdir(parents=True, exist_ok=True)

    generated_pages = [
        "01-foundations.md",
        "02-bilevel.md",
        "03-framework.md",
        "04-worked-example.md",
        "05-experiments.md",
        "06-symbols-and-derivations.md",
        "07-implementation.md",
        "08-summary.md",
        "references.md",
    ]
    existing_pages = [name for name in generated_pages if (OUTPUT / name).exists()]
    if existing_pages and not force:
        raise SystemExit(
            "Refusing to overwrite edited Markdown pages. "
            "Use --force only when a full regeneration is intended."
        )

    part1 = r"\part{先看清 BOBCAT 要解决的任务}"
    part2 = r"\part{bilevel 到底是什么意思}"
    part3 = r"\part{完整拆开 BOBCAT framework}"
    part4 = r"\part{把每一个数都算出来}"
    part5 = r"\part{怎样理解论文结果与方法边界}"
    appendix = "\n" + r"\appendix" + "\n"
    implementation = r"\chapter{代码实现与数学量对照}"
    exercises = r"\chapter{练习与完整答案}"
    recap = r"\chapter{最后一次总复盘}"
    backmatter = r"\backmatter"

    write_page(
        "01-foundations.md",
        "BOBCAT 基础：CAT、概率、梯度与学习范式",
        between(text, part1, part2),
    )
    write_page(
        "02-bilevel.md",
        "BOBCAT 的双层优化",
        between(text, part2, part3),
    )
    write_page(
        "03-framework.md",
        "BOBCAT Framework：式（3）至式（11）与 Algorithm 1",
        between(text, part3, part4),
    )
    write_page(
        "04-worked-example.md",
        "BOBCAT 手算：从选题到影响函数",
        between(text, part4, part5),
    )
    write_page(
        "05-experiments.md",
        "BOBCAT 实验、方法边界与扩展",
        between(text, part5, appendix),
    )
    write_page(
        "06-symbols-and-derivations.md",
        "BOBCAT 符号表与必要推导",
        between(text, appendix, implementation),
    )
    write_page(
        "07-implementation.md",
        "BOBCAT 代码实现与数学量对照",
        between(text, implementation, exercises),
    )
    write_page(
        "08-summary.md",
        "BOBCAT 总结",
        between(text, recap, backmatter),
    )

    references = text[text.index(r"\begin{thebibliography}") :]
    (OUTPUT / "references.md").write_text(convert_references(references), encoding="utf-8")


if __name__ == "__main__":
    _diagram_index = 0
    main()
