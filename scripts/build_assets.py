#!/usr/bin/env python3
"""Rebuild the images the profile README uses.

    python scripts/build_assets.py

Writes:
    assets/banner-{dark,light}.svg            animated banner: agent graph and a typing line
    assets/emoji/*.webp                       small animated Fluent emoji for the headings
    assets/toolbox/<group>-{dark,light}.svg   one row of icon tiles per toolbox group

Every source is pinned below and allows reuse: Skill Icons (MIT), Microsoft Fluent
Emoji (MIT) and Simple Icons (CC0). See assets/CREDITS.md. Needs Pillow.
"""

from __future__ import annotations

import hashlib
import re
import tempfile
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CACHE = Path(tempfile.gettempdir()) / "nilupul-profile-assets"

SKILL_ICONS = "https://raw.githubusercontent.com/tandpfun/skill-icons/7f7e691e71aec64e8354bf697835e009d1ad80f8/icons/{}"
SIMPLE_ICONS = "https://cdn.jsdelivr.net/npm/simple-icons@{}/icons/{}.svg"
SIMPLE_ICONS_VERSION = "16.37.0"
SIMPLE_ICONS_LEGACY = "9.21.0"  # the last release that still ships the OpenAI logo
FLUENT_ANIMATED = "https://media.githubusercontent.com/media/microsoft/fluentui-emoji-animated/daa0365c09795789ed2bc6e8b228c97736cb6669/assets/{}"
FLUENT_STATIC = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/1ffb34c752ecf5d402f04cfb4b392c77f57c54bc/assets/{}"

THEMES = {
    "dark": {
        "card": "#161b22", "border": "#30363d", "text": "#e6edf3", "muted": "#8b949e",
        "typed": "#c9d1d9", "accent": "#9d9bff", "dot": "#e0dfff", "edge": "#4a525c",
        "tile": "#242938", "tile_fg": "#ffffff",
    },
    "light": {
        "card": "#f6f8fa", "border": "#d0d7de", "text": "#1f2328", "muted": "#59636e",
        "typed": "#424a53", "accent": "#5e5ce6", "dot": "#5e5ce6", "edge": "#9aa4ae",
        "tile": "#f4f2ed", "tile_fg": "#242938",
    },
}


def fetch(url: str) -> bytes:
    """Download a URL once and keep it in a temp-dir cache."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / hashlib.sha1(url.encode()).hexdigest()
    if not path.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "profile-readme-build"})
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    return path.read_bytes()


# --------------------------------------------------------------------------- banner

FONT_SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
FONT_MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'

PHRASES = [
    "building agentic systems",
    "retrieval over long manuals",
    "document AI for invoices",
    "tools for AI coding agents",
]
TYPE_SIZE = 22
CHAR_W = TYPE_SIZE * 0.6  # textLength pins every glyph to this pitch, whatever the monospace font
TYPE_X, TYPE_Y = 112, 240
TYPE_STEP, DELETE_STEP, HOLD, GAP = 0.075, 0.03, 2.2, 0.4

GRAPH_LOOP = 6  # seconds for one pass through the agent graph


def typing_timelines() -> tuple[float, list[list[tuple[float, int]]]]:
    """For each phrase, a list of (time, visible characters) events on one shared clock."""
    timelines, clock = [], 0.0
    for phrase in PHRASES:
        n, events = len(phrase), []
        events += [(clock + k * TYPE_STEP, k) for k in range(n + 1)]
        delete_start = clock + n * TYPE_STEP + HOLD
        events += [(delete_start + (n - k) * DELETE_STEP, k) for k in range(n - 1, -1, -1)]
        timelines.append(events)
        clock = delete_start + n * DELETE_STEP + GAP
    return clock, timelines


def discrete(attribute: str, total: float, events: list[tuple[float, float]]) -> str:
    if events[0][0] > 0:
        events = [(0.0, events[0][1] if attribute == "x" else 0)] + events
    key_times = ";".join(f"{t / total:.4f}" for t, _ in events)
    values = ";".join(f"{v:g}" for _, v in events)
    return (f'<animate attributeName="{attribute}" dur="{total:.2f}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="{key_times}" values="{values}"/>')


def glow(cx: int, cy: int, key_times: str, opacity: str, radius: str, color: str) -> str:
    animate = f'dur="{GRAPH_LOOP}s" repeatCount="indefinite" keyTimes="{key_times}"'
    return (f'<circle cx="{cx}" cy="{cy}" r="16" fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" {animate} values="{opacity}"/>'
            f'<animate attributeName="r" {animate} values="{radius}"/></circle>')


def dot(path: str, key_times: str, opacity_times: str, opacity: str, c: dict) -> str:
    return (f'<g opacity="0"><circle r="12" fill="{c["accent"]}" opacity="0.28"/><circle r="5.5" fill="{c["dot"]}"/>'
            f'<animateMotion dur="{GRAPH_LOOP}s" repeatCount="indefinite" path="{path}" '
            f'keyPoints="0;0;1;1" keyTimes="{key_times}" calcMode="linear"/>'
            f'<animate attributeName="opacity" dur="{GRAPH_LOOP}s" repeatCount="indefinite" '
            f'keyTimes="{opacity_times}" values="{opacity}"/></g>')


def banner(c: dict) -> str:
    total, timelines = typing_timelines()

    clips, texts, cursor_events = [], [], []
    for i, (phrase, events) in enumerate(zip(PHRASES, timelines)):
        width_events = [(t, k * CHAR_W + (2 if k else 0)) for t, k in events]
        clips.append(f'<clipPath id="type-{i}"><rect x="{TYPE_X}" y="{TYPE_Y - 24}" width="0" height="32">'
                     f'{discrete("width", total, width_events)}</rect></clipPath>')
        texts.append(f'<text class="typed" x="{TYPE_X}" y="{TYPE_Y}" textLength="{len(phrase) * CHAR_W:g}" '
                     f'lengthAdjust="spacing" clip-path="url(#type-{i})">{escape(phrase)}</text>')
        cursor_events += [(t, TYPE_X + k * CHAR_W + 2) for t, k in events]

    style = f"""
      .name {{ font: 700 72px {FONT_SANS}; fill: {c["text"]}; letter-spacing: -1px; }}
      .role {{ font: 600 34px {FONT_SANS}; fill: {c["accent"]}; }}
      .prompt {{ font: 700 {TYPE_SIZE}px {FONT_MONO}; fill: {c["accent"]}; }}
      .typed {{ font: 500 {TYPE_SIZE}px {FONT_MONO}; fill: {c["typed"]}; }}
      .label {{ font: 500 17px {FONT_MONO}; fill: {c["muted"]}; }}
      .edge {{ stroke: {c["edge"]}; stroke-width: 2.5; fill: none; }}
      .loop {{ stroke: {c["edge"]}; stroke-width: 2.5; fill: none; stroke-dasharray: 6 7; }}
      .node {{ fill: {c["card"]}; stroke: {c["accent"]}; stroke-width: 3; }}
    """

    # One pass: two signals leave "understand" (t=0), reach retrieve and memory (~0.17),
    # meet at "answer" (0.33), then one signal returns through "reflect" (0.38 to 0.72).
    graph = "\n  ".join([
        glow(852, 160, "0;0.1;0.11;0.72;0.82;1", "0.45;0;0;0.45;0;0", "16;30;16;16;30;30", c["accent"]),
        glow(984, 94, "0;0.16;0.17;0.27;1", "0;0;0.45;0;0", "16;16;16;30;30", c["accent"]),
        glow(984, 226, "0;0.16;0.17;0.27;1", "0;0;0.45;0;0", "16;16;16;30;30", c["accent"]),
        glow(1120, 160, "0;0.32;0.33;0.45;1", "0;0;0.55;0;0", "16;16;16;32;32", c["accent"]),
        '<path class="edge" d="M866,160 L966,104" marker-end="url(#arrow)"/>',
        '<path class="edge" d="M866,160 L966,216" marker-end="url(#arrow)"/>',
        '<path class="edge" d="M1002,96 L1102,152" marker-end="url(#arrow)"/>',
        '<path class="edge" d="M1002,224 L1102,168" marker-end="url(#arrow)"/>',
        '<path class="loop" d="M1120,182 C1120,290 852,290 852,186" marker-end="url(#arrow)"/>',
        '<circle class="node" cx="852" cy="160" r="15"/>',
        '<circle class="node" cx="984" cy="94" r="15"/>',
        '<circle class="node" cx="984" cy="226" r="15"/>',
        f'<circle cx="1120" cy="160" r="15" fill="{c["accent"]}"/>',
        dot("M852,160 L984,94 L1120,160", "0;0.02;0.33;1", "0;0.03;0.31;0.35;1", "0;1;1;0;0", c),
        dot("M852,160 L984,226 L1120,160", "0;0.02;0.33;1", "0;0.03;0.31;0.35;1", "0;1;1;0;0", c),
        dot("M1120,160 L1120,182 C1120,290 852,290 852,186 L852,160", "0;0.38;0.72;1",
            "0;0.37;0.39;0.70;0.74;1", "0;0;1;1;0;0", c),
        '<text class="label" x="852" y="128" text-anchor="middle">understand</text>',
        '<text class="label" x="984" y="62" text-anchor="middle">retrieve</text>',
        '<text class="label" x="1046" y="232">memory</text>',
        '<text class="label" x="1120" y="128" text-anchor="middle">answer</text>',
        '<text class="label" x="986" y="286" text-anchor="middle">reflect</text>',
    ])

    cursor = (f'<rect x="{TYPE_X}" y="{TYPE_Y - 19}" width="3" height="24" rx="1" fill="{c["accent"]}">'
              f'{discrete("x", total, cursor_events)}'
              '<animate attributeName="opacity" dur="1.1s" repeatCount="indefinite" calcMode="discrete" '
              'keyTimes="0;0.55" values="1;0"/></rect>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320" role="img" aria-labelledby="title desc">
  <title id="title">Nilupul Nishan, AI Engineer</title>
  <desc id="desc">An agent graph where signals flow from understand to retrieve and memory, meet at answer, and return through reflect. A typing line cycles through: {escape(", ".join(PHRASES))}.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{c["edge"]}"/>
    </marker>
    {"".join(clips)}
    <style>{style}</style>
  </defs>

  <rect x="1" y="1" width="1278" height="318" rx="18" fill="{c["card"]}" stroke="{c["border"]}" stroke-width="2"/>

  <text class="name" x="80" y="134">Nilupul Nishan</text>
  <text class="role" x="82" y="186">AI Engineer</text>
  <text class="prompt" x="82" y="{TYPE_Y}">&#8250;</text>
  {"".join(texts)}
  {cursor}

  {graph}
</svg>
"""


# --------------------------------------------------------------------------- emoji

EMOJI = {
    "waving-hand": "Waving hand/Default/animated/waving_hand_animated_default.png",
    "brain": "Brain/animated/brain_animated.png",
    "rocket": "Rocket/animated/rocket_animated.png",
    "glowing-star": "Glowing star/animated/glowing_star_animated.png",
    "high-voltage": "High voltage/animated/high_voltage_animated.png",
    "handshake": "Handshake/Default/animated/handshake_animated_default.png",
}
EMOJI_SIZE, EMOJI_FRAME_STEP, EMOJI_QUALITY = 56, 2, 80


def build_emoji() -> None:
    from PIL import Image, ImageSequence

    out_dir = ASSETS / "emoji"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, path in EMOJI.items():
        source = Image.open(BytesIO(fetch(FLUENT_ANIMATED.format(quote(path)))))
        frames, durations = [], []
        for i, frame in enumerate(ImageSequence.Iterator(source)):
            duration = frame.info.get("duration", 33)
            if i % EMOJI_FRAME_STEP == 0:
                frames.append(frame.convert("RGBA").resize((EMOJI_SIZE, EMOJI_SIZE), Image.LANCZOS))
                durations.append(duration)
            else:
                durations[-1] += duration
        out = out_dir / f"{name}.webp"
        frames[0].save(out, save_all=True, append_images=frames[1:], duration=durations,
                       loop=0, quality=EMOJI_QUALITY, method=6)
        print(f"  {out.relative_to(ROOT)}  {len(frames)} frames, {out.stat().st_size // 1024} KB")


# --------------------------------------------------------------------------- toolbox

TILE, TILE_GAP, TILE_DISPLAY = 256, 44, 48


def luminance(hex_color: str) -> float:
    channels = [int(hex_color.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def svg_body(svg: str) -> tuple[str, str]:
    match = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', svg, re.S)
    if not match:
        raise ValueError("not an SVG with a viewBox")
    return match.group(1), match.group(2)


def prefix_ids(body: str, prefix: str) -> str:
    if "<style" in body:
        raise ValueError("an icon has its own <style>; its class names would clash")
    for old in sorted(set(re.findall(r'\bid="([^"]+)"', body)), key=len, reverse=True):
        new, o = f"{prefix}-{old}", re.escape(old)
        body = re.sub(rf'\bid="{o}"', f'id="{new}"', body)
        body = re.sub(rf"url\(#{o}\)", f"url(#{new})", body)
        body = re.sub(rf'href="#{o}"', f'href="#{new}"', body)
    return body


@dataclass
class Tile:
    name: str
    kind: str          # "skill", "simple" or "fluent"
    source: str        # file name, slug or Fluent path
    light: str = ""    # skill or fluent: the light-theme file when it differs
    color: str = ""    # simple: brand colour
    version: str = SIMPLE_ICONS_VERSION

    def render(self, theme: str, prefix: str) -> str:
        c = THEMES[theme]
        if self.kind == "skill":
            if self.light:
                file = self.source if theme == "dark" else self.light
            elif self.source.endswith(".svg"):
                file = self.source
            else:
                file = f"{self.source}-{theme.title()}.svg"
            view_box, body = svg_body(fetch(SKILL_ICONS.format(file)).decode())
            return f'<svg width="{TILE}" height="{TILE}" viewBox="{view_box}">{prefix_ids(body, prefix)}</svg>'
        backdrop = f'<rect width="{TILE}" height="{TILE}" rx="60" fill="{c["tile"]}"/>'
        if self.kind == "simple":
            path = re.search(r'<path d="([^"]+)"', fetch(SIMPLE_ICONS.format(self.version, self.source)).decode())
            color = f"#{self.color}" if contrast(f"#{self.color}", c["tile"]) >= 2.2 else c["tile_fg"]
            return f'{backdrop}<path transform="translate(56 56) scale(6)" fill="{color}" d="{path.group(1)}"/>'
        # Fluent's flat colours fade into the light tile, so light tiles use the one-colour
        # high-contrast version, recoloured to match the other monochrome logos.
        use_light = theme == "light" and self.light
        view_box, body = svg_body(fetch(FLUENT_STATIC.format(quote(self.light if use_light else self.source))).decode())
        if use_light:
            body = body.replace("#212121", c["tile_fg"])
        return f'{backdrop}<svg x="40" y="40" width="176" height="176" viewBox="{view_box}">{prefix_ids(body, prefix)}</svg>'


def skill(name: str, file: str = "", light: str = "") -> Tile:
    return Tile(name, "skill", file or name, light=light)


def simple(name: str, slug: str, color: str, version: str = SIMPLE_ICONS_VERSION) -> Tile:
    return Tile(name, "simple", slug, color=color, version=version)


GROUPS = {
    "ai": [
        simple("LangGraph", "langgraph", "7FC8FF"),
        simple("LangChain", "langchain", "7FC8FF"),
        Tile("LlamaIndex", "fluent", "Llama/Flat/llama_flat.svg", light="Llama/High Contrast/llama_high_contrast.svg"),
        simple("OpenAI", "openai", "412991", version=SIMPLE_ICONS_LEGACY),
        skill("Azure AI", "Azure"),
        simple("Anthropic", "anthropic", "191919"),
        simple("MCP", "modelcontextprotocol", "000000"),
        simple("Hugging Face", "huggingface", "FFD21E"),
        simple("Pydantic AI", "pydantic", "E92063"),
    ],
    "ml": [
        skill("Python"),
        skill("TensorFlow"),
        skill("scikit-learn", "ScikitLearn-Dark.svg", light="SciKitLearn-Light.svg"),
        skill("OpenCV"),
        simple("pandas", "pandas", "150458"),
        simple("NumPy", "numpy", "013243"),
        simple("Jupyter", "jupyter", "F37626"),
    ],
    "backend": [
        skill("FastAPI", "FastAPI.svg"),
        skill("Flask"),
        simple("Streamlit", "streamlit", "FF4B4B"),
        skill("PostgreSQL"),
        skill("SQLite", "SQLite.svg"),
    ],
    "web": [
        skill("TypeScript", "TypeScript.svg"),
        skill("React"),
        skill("Next.js", "NextJS"),
        skill("Vite"),
        skill("Tailwind CSS", "TailwindCSS"),
        simple("Payload CMS", "payloadcms", "000000"),
        skill("Vercel"),
    ],
    "mobile": [
        skill("Kotlin"),
        simple("Jetpack Compose", "jetpackcompose", "4285F4"),
        skill("Android", "AndroidStudio"),
        skill("Java"),
        skill("Firebase"),
        skill("C++", "CPP.svg"),
    ],
    "tools": [
        skill("Git", "Git.svg"),
        skill("GitHub", "Github"),
        simple("Claude Code", "claude", "D97757"),
    ],
}


def strip(tiles: list[Tile], theme: str) -> str:
    width = len(tiles) * TILE + (len(tiles) - 1) * TILE_GAP
    parts = [f'<g transform="translate({i * (TILE + TILE_GAP)} 0)">{tile.render(theme, f"t{i}")}</g>'
             for i, tile in enumerate(tiles)]
    names = escape(", ".join(tile.name for tile in tiles))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{round(width * TILE_DISPLAY / TILE)}" height="{TILE_DISPLAY}" viewBox="0 0 {width} {TILE}" '
            f'role="img"><title>{names}</title>{"".join(parts)}</svg>\n')


# --------------------------------------------------------------------------- main

def main() -> None:
    print("banners")
    for theme, colors in THEMES.items():
        out = ASSETS / f"banner-{theme}.svg"
        out.write_text(banner(colors), encoding="utf-8", newline="\n")
        print(f"  {out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")
    print("emoji")
    build_emoji()
    print("toolbox")
    (ASSETS / "toolbox").mkdir(parents=True, exist_ok=True)
    for group, tiles in GROUPS.items():
        for theme in THEMES:
            out = ASSETS / "toolbox" / f"{group}-{theme}.svg"
            out.write_text(strip(tiles, theme), encoding="utf-8", newline="\n")
        print(f"  assets/toolbox/{group}-*.svg  {len(tiles)} tiles")


if __name__ == "__main__":
    main()
