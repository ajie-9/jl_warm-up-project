from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
VERSION = "doodle-cat-unified-v1"
W, H = 841, 1870

BG = "#ffffff"
INK = "#151918"
MUTED = "#737978"
SUBTLE = "#f4f6f5"
LINE = "#e6ebe8"
GREEN = "#22d47a"
GREEN_DARK = "#0aa85a"
RED = "#e65358"
YELLOW = "#fff8e8"
ORANGE = "#d99013"
BLUE = "#151918"
PINK = "#151918"


def font(size, weight="regular"):
    paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc" if weight in {"bold", "heavy"} else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


F = {
    "display": font(62, "heavy"),
    "h1": font(50, "heavy"),
    "h2": font(38, "bold"),
    "h3": font(30, "bold"),
    "body": font(25),
    "body_b": font(25, "bold"),
    "small": font(20),
    "small_b": font(20, "bold"),
    "tiny": font(17),
    "tiny_b": font(17, "bold"),
    "num": font(58, "heavy"),
}


def asset(name):
    return Image.open(ASSETS / name).convert("RGBA")


def sportify_cat(src):
    out = src.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a < 12:
                continue
            is_green_cloth = g > 75 and g > r * 1.08 and g > b * 1.05
            if not is_green_cloth:
                continue
            lum = (r + g + b) / 3
            if lum > 210:
                nr, ng, nb = 236, 241, 238
            elif g > 160 and lum > 120:
                nr, ng, nb = 30, 216, 123
            else:
                t = max(0, min(1, (lum - 45) / 160))
                nr = int(18 + 48 * t)
                ng = int(22 + 54 * t)
                nb = int(21 + 50 * t)
            px[x, y] = (nr, ng, nb, a)
    return out


CAT_AVATAR = sportify_cat(asset("orange-cat-avatar-cutout.png"))
CAT_READY = sportify_cat(asset("orange-cat-ready-cutout.png"))
CAT_COACH = sportify_cat(asset("orange-cat-coach-cutout.png"))
CAT_WORKOUT = sportify_cat(asset("orange-cat-workout-cutout.png"))
LOGO = asset("warmup-logo-256.png")
GYM = Image.open(ASSETS / "gym-follow-bg.png").convert("RGB")


def new_page():
    return Image.new("RGBA", (W, H), BG)


def draw_wrapped(d, xy, text, fnt, fill=MUTED, width=620, line_height=None):
    x, y = xy
    line_height = line_height or int(fnt.size * 1.42)
    for raw in text.split("\n"):
        line = ""
        for ch in raw:
            test = line + ch
            if d.textlength(test, font=fnt) <= width or not line:
                line = test
            else:
                d.text((x, y), line, font=fnt, fill=fill)
                y += line_height
                line = ch
        if line:
            d.text((x, y), line, font=fnt, fill=fill)
            y += line_height
    return y


def paste_fit(base, image, box, contain=True, radius=0):
    x1, y1, x2, y2 = map(int, box)
    bw, bh = x2 - x1, y2 - y1
    src = image.convert("RGBA")
    ratio = min(bw / src.width, bh / src.height) if contain else max(bw / src.width, bh / src.height)
    src = src.resize((max(1, int(src.width * ratio)), max(1, int(src.height * ratio))), Image.LANCZOS)
    if not contain:
        left = max(0, (src.width - bw) // 2)
        top = max(0, (src.height - bh) // 2)
        src = src.crop((left, top, left + bw, top + bh))
    layer = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    layer.alpha_composite(src, ((bw - src.width) // 2, (bh - src.height) // 2))
    if radius:
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), radius=radius, fill=255)
        layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (bw, bh), 0), mask))
    base.alpha_composite(layer, (x1, y1))


def draw_cat(base, box, pose="stand"):
    x1, y1, x2, y2 = map(int, box)
    bw, bh = x2 - x1, y2 - y1
    s = 4
    w, h = 330, 340
    art = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(art)

    def q(v):
        return int(round(v * s))

    def bx(coords):
        return tuple(q(v) for v in coords)

    def pts(items):
        return [(q(x), q(y)) for x, y in items]

    ink = "#111111"
    white = "#fffdf8"
    orange = "#f49a28"
    orange_dark = "#bd6417"
    soft = "#f4f2ed"

    def sketch_line(items, fill=ink, width=4):
        p = pts(items)
        d.line(p, fill=fill, width=q(width), joint="curve")
        jitter = [(x + q(1.1), y - q(0.7)) for x, y in p]
        d.line(jitter, fill=fill, width=max(1, q(width - 2)), joint="curve")

    def sketch_poly(items, fill=white, width=4):
        p = pts(items)
        d.polygon(p, fill=fill)
        d.line(p + [p[0]], fill=ink, width=q(width), joint="curve")
        d.line([(x + q(1), y - q(1)) for x, y in p + [p[0]]], fill=ink, width=max(1, q(width - 2)), joint="curve")

    def sketch_ellipse(box_, fill=white, width=4):
        d.ellipse(bx(box_), fill=fill, outline=ink, width=q(width))
        x0, y0, x3, y3 = box_
        d.arc(bx((x0 + 2, y0 - 1, x3 + 2, y3 - 1)), 8, 352, fill=ink, width=max(1, q(width - 2)))

    def sketch_round(box_, radius=22, fill=white, width=4):
        d.rounded_rectangle(bx(box_), radius=q(radius), fill=fill, outline=ink, width=q(width))
        x0, y0, x3, y3 = box_
        d.arc(bx((x0 + 2, y0 - 1, x3 + 2, y3 - 1)), 8, 352, fill=ink, width=max(1, q(width - 2)))

    def draw_tail():
        curve = [(224, 214), (252, 212), (280, 190), (278, 158), (260, 138)]
        sketch_line(curve, ink, 20)
        sketch_line(curve, orange, 12)
        sketch_line([(256, 151), (272, 144)], orange_dark, 4)
        sketch_line([(266, 176), (284, 168)], orange_dark, 4)

    def draw_head(cx=160, cy=88):
        sketch_poly([(94, cy - 22), (106, cy - 76), (132, cy - 28)], orange, 3)
        sketch_poly([(226, cy - 22), (214, cy - 76), (188, cy - 28)], orange, 3)
        sketch_poly([(106, cy - 26), (112, cy - 58), (126, cy - 30)], "#ffd4ab", 2)
        sketch_poly([(214, cy - 26), (208, cy - 58), (194, cy - 30)], "#ffd4ab", 2)
        sketch_ellipse((82, cy - 48, 238, cy + 76), white, 4)
        d.pieslice(bx((86, cy - 42, 154, cy + 58)), 115, 248, fill=orange)
        d.pieslice(bx((168, cy - 42, 236, cy + 58)), 292, 65, fill=orange)
        sketch_line([(112, cy - 12), (133, cy - 20)], orange_dark, 3)
        sketch_line([(111, cy + 6), (133, cy - 2)], orange_dark, 3)
        sketch_line([(188, cy - 20), (209, cy - 12)], orange_dark, 3)
        sketch_line([(187, cy - 2), (209, cy + 6)], orange_dark, 3)
        d.ellipse(bx((125, cy + 2, 137, cy + 14)), fill=ink)
        d.ellipse(bx((184, cy + 2, 196, cy + 14)), fill=ink)
        d.polygon(pts([(160, cy + 24), (151, cy + 16), (169, cy + 16)]), fill=ink)
        d.arc(bx((141, cy + 24, 160, cy + 44)), 12, 80, fill=ink, width=q(3))
        d.arc(bx((160, cy + 24, 179, cy + 44)), 100, 168, fill=ink, width=q(3))
        sketch_line([(117, cy + 28), (74, cy + 18)], ink, 2)
        sketch_line([(118, cy + 38), (74, cy + 42)], ink, 2)
        sketch_line([(203, cy + 28), (246, cy + 18)], ink, 2)
        sketch_line([(202, cy + 38), (246, cy + 42)], ink, 2)

    d.ellipse(bx((62, 303, 268, 325)), fill=(190, 190, 180, 80))
    draw_tail()

    if pose == "stretch":
        sketch_poly([(118, 135), (202, 138), (220, 250), (180, 258), (164, 212), (144, 260), (102, 250)], white, 4)
        sketch_line([(198, 143), (225, 92), (205, 44), (172, 38)], ink, 18)
        sketch_line([(198, 143), (225, 92), (205, 44), (172, 38)], white, 11)
        sketch_line([(118, 148), (78, 110), (64, 74)], ink, 18)
        sketch_line([(118, 148), (78, 110), (64, 74)], white, 11)
        sketch_line([(122, 244), (78, 292), (52, 302)], ink, 15)
        sketch_line([(122, 244), (78, 292), (52, 302)], white, 9)
        sketch_line([(198, 244), (252, 292), (285, 302)], ink, 15)
        sketch_line([(198, 244), (252, 292), (285, 302)], white, 9)
        d.polygon(pts([(88, 235), (118, 239), (108, 264), (80, 258)]), fill=orange)
        d.polygon(pts([(202, 238), (232, 232), (240, 258), (210, 264)]), fill=orange)
        draw_head(160, 88)
        sketch_line([(206, 142), (238, 88), (210, 34), (155, 48), (126, 82)], ink, 15)
        sketch_line([(206, 142), (238, 88), (210, 34), (155, 48), (126, 82)], white, 9)
        sketch_line([(98, 104), (214, 74)], ink, 3)
    elif pose == "point":
        sketch_round((116, 138, 204, 256), 35, white, 4)
        sketch_line([(197, 158), (252, 118), (288, 110)], ink, 16)
        sketch_line([(197, 158), (252, 118), (288, 110)], white, 10)
        sketch_line([(122, 162), (86, 214)], ink, 16)
        sketch_line([(122, 162), (86, 214)], white, 10)
        sketch_line([(132, 250), (118, 306)], ink, 13)
        sketch_line([(132, 250), (118, 306)], white, 8)
        sketch_line([(188, 250), (204, 306)], ink, 13)
        sketch_line([(188, 250), (204, 306)], white, 8)
        draw_head(160, 82)
    elif pose == "hold":
        sketch_round((116, 138, 204, 256), 35, white, 4)
        sketch_round((240, 132, 270, 210), 9, "#f5fbf8", 3)
        d.rectangle(bx((240, 162, 270, 190)), fill=GREEN)
        sketch_line([(196, 160), (238, 184)], ink, 16)
        sketch_line([(196, 160), (238, 184)], white, 10)
        sketch_line([(122, 162), (86, 214)], ink, 16)
        sketch_line([(122, 162), (86, 214)], white, 10)
        sketch_line([(132, 250), (118, 306)], ink, 13)
        sketch_line([(132, 250), (118, 306)], white, 8)
        sketch_line([(188, 250), (204, 306)], ink, 13)
        sketch_line([(188, 250), (204, 306)], white, 8)
        draw_head(160, 82)
    elif pose == "sit":
        sketch_ellipse((103, 142, 217, 270), white, 4)
        sketch_line([(108, 218), (66, 282), (120, 300)], ink, 16)
        sketch_line([(108, 218), (66, 282), (120, 300)], white, 10)
        sketch_line([(212, 218), (254, 282), (200, 300)], ink, 16)
        sketch_line([(212, 218), (254, 282), (200, 300)], white, 10)
        sketch_line([(122, 160), (92, 222)], ink, 16)
        sketch_line([(122, 160), (92, 222)], white, 10)
        sketch_line([(198, 160), (228, 222)], ink, 16)
        sketch_line([(198, 160), (228, 222)], white, 10)
        draw_head(160, 82)
    else:
        sketch_round((116, 138, 204, 256), 35, white, 4)
        sketch_line([(122, 160), (88, 222)], ink, 16)
        sketch_line([(122, 160), (88, 222)], white, 10)
        sketch_line([(198, 160), (232, 222)], ink, 16)
        sketch_line([(198, 160), (232, 222)], white, 10)
        sketch_line([(134, 250), (125, 306)], ink, 13)
        sketch_line([(134, 250), (125, 306)], white, 8)
        sketch_line([(186, 250), (195, 306)], ink, 13)
        sketch_line([(186, 250), (195, 306)], white, 8)
        draw_head(160, 82)

    sketch_line([(154, 180), (162, 190), (176, 172)], GREEN_DARK, 4)
    d.arc(bx((18, 42, 42, 65)), 250, 350, fill=ink, width=q(3))
    d.line(bx((37, 28, 42, 42)), fill=ink, width=q(3))

    scale = min(bw / art.width, bh / art.height)
    art = art.resize((max(1, int(art.width * scale)), max(1, int(art.height * scale))), Image.LANCZOS)
    base.alpha_composite(art, (x1 + (bw - art.width) // 2, y1 + (bh - art.height) // 2))


def header(d, title, subtitle="", step=None, progress=None, back=False):
    if back:
        d.text((78, 80), "‹", font=font(50, "bold"), fill=INK, anchor="mm")
    if step:
        d.text((760, 78), step, font=F["small_b"], fill=GREEN_DARK, anchor="ra")
    d.text((82, 170), title, font=F["h1"], fill=INK)
    if subtitle:
        draw_wrapped(d, (82, 238), subtitle, F["small"], width=650, line_height=30)
    if progress is not None:
        d.rounded_rectangle((82, 318, 760, 326), radius=5, fill=SUBTLE)
        d.rounded_rectangle((82, 318, 82 + int(678 * progress), 326), radius=5, fill=GREEN)


def row(d, box, title, subtitle="", lead=None, trailing=None, selected=False, danger=False):
    x1, y1, x2, y2 = box
    fill = "#ffffff" if not selected else "#fbfffd"
    outline = GREEN if selected else LINE
    d.rounded_rectangle((x1, y1 + 6, x2, y2 + 6), radius=14, fill="#edf2ef")
    d.rounded_rectangle(box, radius=14, fill=fill, outline=outline, width=3 if selected else 2)
    tx = x1 + 34
    if lead:
        d.rounded_rectangle((x1 + 24, y1 + 28, x1 + 76, y1 + 80), radius=10, fill=SUBTLE)
        d.text((x1 + 50, y1 + 54), lead, font=F["tiny_b"], fill=GREEN_DARK if selected else MUTED, anchor="mm")
        tx = x1 + 98
    d.text((tx, y1 + 25), title, font=F["body_b"], fill=RED if danger else INK)
    if subtitle:
        d.text((tx, y1 + 65), subtitle, font=F["small"], fill=MUTED)
    if trailing:
        d.text((x2 - 30, (y1 + y2) / 2), trailing, font=F["small_b"], fill=GREEN_DARK, anchor="rm")


def button(d, text, y=1718, outline=False, color=GREEN):
    if outline:
        d.rounded_rectangle((82, y, 760, y + 70), radius=14, fill=BG, outline=color, width=3)
        d.text((421, y + 35), text, font=F["body_b"], fill=color, anchor="mm")
    else:
        d.rounded_rectangle((82, y, 760, y + 70), radius=14, fill=color)
        d.text((421, y + 35), text, font=F["body_b"], fill="#ffffff", anchor="mm")
    home_indicator(d)


def home_indicator(d):
    d.rounded_rectangle((335, 1830, 506, 1838), radius=4, fill="#111111")


def tabbar(d, active):
    y = 1698
    d.line((82, y - 28, 760, y - 28), fill=LINE, width=2)
    tabs = ["热身", "日程", "饮食", "我的"]
    for i, label in enumerate(tabs):
        cx = 124 + i * 198
        is_active = label == active
        fill = GREEN_DARK if is_active else MUTED
        if is_active:
            d.rounded_rectangle((cx - 34, y + 42, cx + 34, y + 48), radius=3, fill=GREEN)
        d.text((cx, y + 15), label, font=F["body_b"], fill=fill, anchor="mm")
    home_indicator(d)


def note(d, box, title, text, color=GREEN_DARK):
    x1, y1, x2, y2 = box
    d.rounded_rectangle((x1, y1 + 6, x2, y2 + 6), radius=14, fill="#edf2ef")
    d.rounded_rectangle(box, radius=14, fill="#ffffff", outline=LINE, width=2)
    d.text((x1 + 28, y1 + 22), title, font=F["small_b"], fill=color)
    draw_wrapped(d, (x1 + 28, y1 + 58), text, F["tiny"], fill=MUTED, width=x2 - x1 - 56, line_height=25)


def splash():
    im = new_page()
    d = ImageDraw.Draw(im)
    paste_fit(im, LOGO, (342, 245, 500, 403), radius=34)
    d.text((421, 510), "热身 App", font=F["display"], fill=INK, anchor="mm")
    d.text((421, 575), "AI 私教陪伴每次热身", font=F["body"], fill=MUTED, anchor="mm")
    d.rounded_rectangle((120, 726, 722, 1251), radius=26, fill="#edf2ef")
    d.rounded_rectangle((120, 720, 722, 1245), radius=26, fill="#ffffff", outline=LINE, width=2)
    draw_cat(im, (292, 770, 550, 1138), "stand")
    d.text((421, 1320), "饮食计划 · 身体自检 · AI 跟练", font=F["small_b"], fill=GREEN_DARK, anchor="mm")
    button(d, "开始")
    return im.convert("RGB")


def gender():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "选择性别", "用于计算基础身体指标。", "1 / 5", 0.2, True)
    for cx, symbol, color in [(260, "♂", BLUE), (582, "♀", PINK)]:
        d.ellipse((cx - 118, 575, cx + 118, 811), fill="#ffffff", outline=INK, width=4)
        d.text((cx, 694), symbol, font=font(108, "bold"), fill=color, anchor="mm")
    note(d, (148, 1045, 694, 1170), "提示", "后续可以修改，先完成入门计划。")
    draw_cat(im, (112, 1048, 178, 1134), "stand")
    button(d, "下一步")
    return im.convert("RGB")


def body():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "身体指标", "身高体重用于计算 BMI、BMR、TDEE。", "2 / 5", 0.4, True)
    for yy, label, val, unit, pct in [(440, "身高", "170", "cm", 0.58), (720, "体重", "62", "kg", 0.48)]:
        d.text((82, yy), label, font=F["body_b"], fill=INK)
        d.text((82, yy + 54), val, font=F["num"], fill=GREEN)
        d.text((210, yy + 86), unit, font=F["body_b"], fill=GREEN_DARK)
        d.rounded_rectangle((82, yy + 150, 760, yy + 160), radius=6, fill=SUBTLE)
        d.rounded_rectangle((82, yy + 150, 82 + int(678 * pct), yy + 160), radius=6, fill=GREEN)
        d.ellipse((82 + int(678 * pct) - 18, yy + 134, 82 + int(678 * pct) + 18, yy + 176), fill="#ffffff", outline=GREEN, width=3)
    d.line((82, 1045, 760, 1045), fill=LINE, width=2)
    for x, k, v, sub in [(82, "BMI", "21.5", "标准"), (308, "BMR", "1311", "基础代谢"), (548, "TDEE", "1804", "日消耗")]:
        d.text((x, 1100), k, font=F["small_b"], fill=MUTED)
        d.text((x, 1140), v, font=F["h2"], fill=INK)
        d.text((x, 1190), sub, font=F["tiny"], fill=MUTED)
    button(d, "下一步：饮食")
    return im.convert("RGB")


def diet_choice():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "定制饮食计划？", "可根据身体指标和运动目标生成具体食谱。", "3 / 5", 0.6, True)
    row(d, (82, 465, 760, 595), "需要，生成具体食谱", "早餐、午餐、加餐、晚餐和克数", "食", "已选", True)
    row(d, (82, 640, 760, 770), "暂时不用，直接训练", "训练后也可以补充饮食计划", "练")
    d.line((82, 930, 760, 930), fill=LINE, width=2)
    draw_cat(im, (570, 930, 720, 1135), "point")
    note(d, (82, 1010, 520, 1138), "说明", "第一版用规则引擎生成，不依赖 OpenAI API key。")
    button(d, "下一步")
    return im.convert("RGB")


def risk():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "疾病风险", "选择常见情况，并补充其他疾病史。", "4 / 5", 0.8, True)
    items = [("高血压", "控盐", True), ("糖尿病", "控糖", False), ("高血脂", "少油", False), ("痛风", "低嘌呤", False), ("胃肠问题", "清淡", False), ("食物过敏", "避开过敏源", True), ("肾脏疾病", "蛋白谨慎", False), ("无以上情况", "跳过", False)]
    for i, (title, sub, selected) in enumerate(items):
        x = 82 if i % 2 == 0 else 436
        y = 430 + (i // 2) * 110
        row(d, (x, y, x + 324, y + 82), title, sub, "选" if selected else "+", selected=selected)
    d.text((82, 910), "补充疾病史", font=F["h2"], fill=INK)
    d.text((82, 960), "有其他疾病、手术、过敏或忌口，可以写在这里。", font=F["small"], fill=MUTED)
    d.rounded_rectangle((82, 1028, 760, 1320), radius=18, fill="#ffffff", outline=LINE, width=2)
    draw_wrapped(d, (120, 1070), "例如：\n轻度胃炎，不能吃太辣；\n乳糖不耐受；\n医生建议控制盐分。", F["body"], fill="#4f625b", width=560, line_height=42)
    d.rounded_rectangle((82, 1405, 760, 1515), radius=18, fill=YELLOW, outline="#f0cf70", width=2)
    d.text((116, 1435), "风险提示", font=F["small_b"], fill=ORANGE)
    d.text((116, 1473), "饮食建议仅供参考，必要时咨询专业人士。", font=F["tiny"], fill=MUTED)
    button(d, "下一步：目标")
    return im.convert("RGB")


def goal():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "运动计划目标", "我们将根据运动计划推荐饮食计划。", "5 / 5", 1.0, True)
    row(d, (82, 470, 760, 590), "减肥", "控制热量缺口，保证蛋白质", "瘦", "已选", True)
    row(d, (82, 635, 760, 755), "增肌", "提高蛋白和训练后补给", "肌")
    row(d, (82, 800, 760, 920), "保持体态", "稳定摄入和规律饮食", "稳")
    note(d, (82, 1090, 760, 1210), "当前选择：减肥", "下一步选择慢慢瘦或快速刷脂。")
    draw_cat(im, (588, 1270, 724, 1495), "point")
    button(d, "下一步：速度")
    return im.convert("RGB")


def speed():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "减脂速度", "选择适合自己的热量缺口。", "5 / 5", 1.0, True)
    for cx, label, title, sub, color, selected in [
        (260, "慢", "慢慢瘦", "更稳，推荐长期坚持", GREEN, True),
        (582, "快", "快速刷脂", "更严格，关注疲劳", INK, False),
    ]:
        d.ellipse((cx - 112, 560, cx + 112, 784), fill="#ffffff", outline=color, width=5 if selected else 3)
        d.text((cx, 672), label, font=font(74, "heavy"), fill=color, anchor="mm")
        d.text((cx, 840), title, font=F["body_b"], fill=INK, anchor="mm")
        d.text((cx, 880), sub, font=F["tiny"], fill=MUTED, anchor="mm")
    note(d, (82, 1080, 760, 1210), "推荐", "先从慢慢瘦开始，避免影响训练状态。", ORANGE)
    button(d, "生成饮食计划")
    return im.convert("RGB")


def diet_plan():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "饮食计划", "由身体指标、风险和目标生成。", "已生成", None, True)
    d.rounded_rectangle((82, 345, 760, 615), radius=20, fill="#edf2ef")
    d.rounded_rectangle((82, 338, 760, 608), radius=20, fill="#ffffff", outline=GREEN, width=3)
    d.text((122, 390), "饮食计划", font=F["h3"], fill=INK)
    d.text((122, 470), "1564", font=F["display"], fill=GREEN)
    d.text((302, 492), "kcal", font=F["h2"], fill=GREEN_DARK)
    d.text((122, 550), "推荐摄入 · 目标 1800 kcal", font=F["small"], fill=MUTED)
    draw_cat(im, (570, 355, 742, 590), "hold")
    d.text((82, 690), "今日食谱", font=F["h2"], fill=INK)
    meals = [("早", "燕麦 40g + 鸡蛋 1 个 + 低脂牛奶 250ml", "335 kcal"), ("午", "鸡胸肉 120g + 米饭 120g + 西兰花 200g", "406 kcal"), ("加", "无糖酸奶 150g + 蓝莓 50g", "124 kcal"), ("晚", "虾仁 120g + 红薯 150g + 生菜 200g", "285 kcal")]
    y = 765
    for lead, title, kcal in meals:
        row(d, (82, y, 760, y + 104), title, "", lead, kcal)
        y += 134
    d.rounded_rectangle((82, 1345, 760, 1465), radius=18, fill=YELLOW, outline="#f0cf70", width=2)
    d.text((116, 1378), "风险提示", font=F["small_b"], fill=ORANGE)
    d.text((116, 1418), "已勾选高血压/食物过敏，建议少盐并避开过敏食物。", font=F["tiny"], fill=MUTED)
    tabbar(d, "饮食")
    return im.convert("RGB")


def home():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "今天练什么", "先完成 3-5 分钟动态热身。")
    d.rounded_rectangle((82, 354, 760, 665), radius=22, fill="#edf2ef")
    d.rounded_rectangle((82, 345, 760, 656), radius=22, fill="#ffffff", outline=GREEN, width=3)
    d.text((122, 395), "今日热身", font=F["h2"], fill=INK)
    d.text((122, 456), "肩胸激活", font=F["body_b"], fill=INK)
    d.text((122, 510), "4 分钟", font=F["h2"], fill=GREEN)
    d.rounded_rectangle((122, 560, 290, 620), radius=18, fill=GREEN)
    d.text((206, 590), "开始热身", font=F["small_b"], fill="#ffffff", anchor="mm")
    draw_cat(im, (500, 370, 735, 640), "stretch")
    d.text((82, 740), "热身方向", font=F["h2"], fill=INK)
    plans = [("1", "练胸日", "启胸椎 · 唤肩胛", True), ("2", "练背日", "开上背 · 找背阔", False), ("3", "练肩日", "热肩袖 · 稳关节", False), ("4", "练腿日", "开髋膝 · 稳步态", False), ("5", "练全身", "轻快升温 · 醒节奏", False)]
    y = 805
    for lead, title, sub, selected in plans:
        row(d, (82, y, 760, y + 96), title, sub, lead, selected=selected)
        y += 118
    note(d, (82, 1460, 760, 1555), "训练前自检", "开始前确认心率、关节、呼吸和身体感觉。")
    button(d, "开始热身", y=1578)
    tabbar(d, "热身")
    return im.convert("RGB")


def schedule():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "日程", "训练记录、完成情况和最近热身。")
    row(d, (82, 365, 760, 485), "胸日动态热身", "今日完成 · 肩胸激活 + 弹力带外旋", "成", "4 分钟", True)
    stats = [("本周", "3 次"), ("累计", "18 分钟"), ("准备度", "82"), ("完成率", "92%")]
    for i, (k, v) in enumerate(stats):
        x = 82 + (i % 2) * 340
        y = 585 + (i // 2) * 130
        d.text((x, y), k, font=F["small"], fill=MUTED)
        d.text((x, y + 42), v, font=F["h2"], fill=INK)
    d.line((82, 895, 760, 895), fill=LINE, width=2)
    d.text((82, 965), "最近热身记录", font=F["h2"], fill=INK)
    records = [
        ("今天", "胸日动态热身", "肩胸激活 · 弹力带外旋", "4 分钟"),
        ("昨日", "背日热身", "猫牛伸展 · 胸椎开书", "4 分钟"),
        ("周一", "全身热身", "轻快踏步 · 侧向滑步", "5 分钟"),
        ("周日", "腿日热身", "髋部环绕 · 前后腿摆", "4 分钟"),
    ]
    y = 1045
    for day, title, sub, mins in records:
        d.text((82, y), day, font=F["small_b"], fill=GREEN_DARK)
        d.text((185, y), title, font=F["small_b"], fill=INK)
        d.text((760, y), mins, font=F["small_b"], fill=MUTED, anchor="ra")
        d.text((185, y + 36), sub, font=F["tiny"], fill=MUTED)
        y += 96
    d.rounded_rectangle((82, 1430, 760, 1608), radius=22, fill="#edf2ef")
    d.rounded_rectangle((82, 1422, 760, 1600), radius=22, fill="#f8fcf8", outline=LINE, width=2)
    draw_cat(im, (105, 1400, 260, 1600), "point")
    d.text((315, 1475), "继续加油！", font=F["h2"], fill=INK)
    d.text((315, 1535), "你已经连续运动 3 天", font=F["body"], fill=MUTED)
    tabbar(d, "日程")
    return im.convert("RGB")


def dynamic():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "胸日热身", "肩胸激活 + 弹力带外旋", "AI 识别预备", None, True)
    draw_cat(im, (106, 360, 230, 535), "stretch")
    d.text((280, 390), "4 分钟", font=F["h2"], fill=GREEN)
    d.text((280, 445), "2 个动作 · MediaPipe 看动作", font=F["body"], fill=INK)
    d.text((280, 492), "小猫只在动作需要调整时提示。", font=F["small"], fill=MUTED)
    d.line((82, 615, 760, 615), fill=LINE, width=2)
    d.text((82, 685), "流程", font=F["h2"], fill=INK)
    row(d, (82, 755, 760, 875), "肩胸激活", "2 分钟 · 打开胸椎", "1", "识别")
    row(d, (82, 915, 760, 1035), "弹力带外旋", "2 分钟 · 稳肩关节", "2", "识别")
    note(d, (82, 1180, 760, 1308), "动作提示", "动作慢一点，肩胛先收紧。")
    button(d, "开始动态热身")
    return im.convert("RGB")


def readiness():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "热身前自检", "确认今天身体是否适合进入跟练。", "准备度 82", None, True)
    d.text((82, 390), "82", font=F["display"], fill=GREEN)
    d.text((190, 420), "可以进入热身", font=F["h2"], fill=INK)
    d.text((190, 470), "四项状态正常", font=F["small"], fill=MUTED)
    d.line((82, 560, 760, 560), fill=LINE, width=2)
    checks = ["心率微微升高", "关节活动顺畅", "呼吸节奏稳定", "身体感觉良好"]
    y = 635
    for item in checks:
        row(d, (82, y, 760, y + 92), item, "正常", "正", selected=True)
        y += 112
    d.rounded_rectangle((82, 1130, 760, 1260), radius=18, fill=YELLOW, outline="#f0cf70", width=2)
    d.text((116, 1165), "安全边界", font=F["small_b"], fill=ORANGE)
    draw_wrapped(d, (116, 1202), "胸痛、头晕、呼吸不稳或关节疼痛时，优先休息。", F["tiny"], width=560)
    button(d, "开始动态热身")
    return im.convert("RGB")


def rest():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "今天先休息", "检测到不适反馈。", None, None, True)
    draw_cat(im, (576, 306, 722, 526), "sit")
    d.text((82, 410), "身体状态比完成训练更重要", font=F["h2"], fill=INK)
    draw_wrapped(d, (82, 470), "建议休息并择日再练。这个分支只做运动风险提醒，不做医疗诊断。", F["body"], width=500, line_height=38)
    d.line((82, 690, 760, 690), fill=LINE, width=2)
    row(d, (82, 770, 760, 880), "关节不适", "建议暂停训练", "!")
    row(d, (82, 910, 760, 1020), "呼吸不稳", "建议先休息观察", "!")
    button(d, "记录并返回计划", y=1540)
    button(d, "我还想继续训练", y=1640, outline=True, color=RED)
    return im.convert("RGB")


def workout():
    im = new_page()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((82, 64, 760, 74), radius=6, fill=SUBTLE)
    d.rounded_rectangle((82, 64, 300, 74), radius=6, fill=GREEN)
    d.text((82, 135), "1/2 肩胸激活", font=F["h1"], fill=INK)
    d.text((82, 198), "00:32    2 千卡", font=F["h2"], fill=GREEN)
    frame = (82, 320, 760, 1588)
    paste_fit(im, GYM, frame, contain=False, radius=22)
    d.rounded_rectangle(frame, radius=22, outline=LINE, width=3)
    d.rounded_rectangle((118, 360, 226, 400), radius=20, fill=GREEN)
    d.text((172, 380), "小猫", font=F["tiny_b"], fill="#ffffff", anchor="mm")
    draw_cat(im, (98, 382, 288, 650), "stretch")
    d.text((500, 388), "当前动作", font=F["tiny_b"], fill="#ffffff")
    d.text((500, 428), "肩胸激活", font=F["h2"], fill="#ffffff")
    d.ellipse((348, 1010, 494, 1156), fill=GREEN, outline="#ffffff", width=6)
    d.text((421, 1084), "25''", font=font(52, "heavy"), fill="#ffffff", anchor="mm")
    d.rounded_rectangle((126, 1474, 716, 1530), radius=28, fill="#ffffff")
    d.text((421, 1502), "反馈  动作感觉怎么样～", font=F["small"], fill=INK, anchor="mm")
    button(d, "完成当前动作")
    return im.convert("RGB")


def profile():
    im = new_page()
    d = ImageDraw.Draw(im)
    header(d, "我的", "")
    d.rounded_rectangle((82, 286, 760, 515), radius=22, fill="#edf2ef")
    d.rounded_rectangle((82, 278, 760, 507), radius=22, fill="#ffffff", outline=LINE, width=2)
    d.rounded_rectangle((112, 314, 244, 468), radius=22, fill="#f3f8f4")
    draw_cat(im, (120, 306, 238, 470), "stand")
    d.text((290, 330), "小暖同学", font=F["h2"], fill=INK)
    d.text((290, 382), "新手热身 · 连续 3 天", font=F["small"], fill=MUTED)
    d.text((290, 430), "经验值 82 / 200", font=F["small_b"], fill=GREEN_DARK)
    d.rounded_rectangle((290, 462, 620, 470), radius=5, fill=SUBTLE)
    d.rounded_rectangle((290, 462, 430, 470), radius=5, fill=GREEN)
    row(d, (82, 585, 760, 690), "个人资料", "头像、昵称、性别、身高体重", "人", "›")
    row(d, (82, 720, 760, 825), "健康档案", "疾病史、过敏、忌口和风险提示", "档", "›")
    row(d, (82, 855, 760, 960), "目标设置", "减脂、增肌、保持体态", "标", "›")
    row(d, (82, 990, 760, 1095), "通知提醒", "食谱提醒、训练提醒", "铃", "›")
    row(d, (82, 1125, 760, 1230), "隐私与数据", "摄像头权限、数据导出、隐私控制", "锁", "›")
    row(d, (82, 1260, 760, 1365), "设备连接", "健康 App、手表和体重秤", "连", "›")
    row(d, (82, 1395, 760, 1500), "帮助与反馈", "使用说明、问题反馈、联系客服", "?", "›")
    note(d, (82, 1545, 760, 1628), "账户状态", "MVP 先保留基础资料和设置入口，会员与社区暂不进入 P0。")
    tabbar(d, "我的")
    return im.convert("RGB")


SCREENS = {
    "splash-screen.png": splash,
    "onboarding-gender.png": gender,
    "onboarding-height-weight.png": body,
    "onboarding-diet-choice.png": diet_choice,
    "diet-risk-check.png": risk,
    "diet-goal-choice.png": goal,
    "diet-speed-choice.png": speed,
    "diet-plan-page.png": diet_plan,
    "app-home.png": home,
    "schedule-page.png": schedule,
    "dynamic-warmup-v2.png": dynamic,
    "readiness-check.png": readiness,
    "rest-advice.png": rest,
    "warmup-start.png": workout,
    "profile-home.png": profile,
}


def update_versions():
    path = ROOT / "index.html"
    html = path.read_text()
    html = re.sub(r"\?v=[a-zA-Z0-9_.-]+", f"?v={VERSION}", html)
    path.write_text(html)


def main():
    for name, renderer in SCREENS.items():
        renderer().save(ASSETS / name, quality=95)
    update_versions()
    print(f"generated {len(SCREENS)} minimal screens with version {VERSION}")


if __name__ == "__main__":
    main()
