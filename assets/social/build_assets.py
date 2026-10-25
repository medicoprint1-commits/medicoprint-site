"""Build simple, ready-to-publish Medicoprint social visuals from official photos."""
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "ready-to-post"
OUT.mkdir(exist_ok=True)
INK, GREEN, MINT, PALE, WHITE, MUTED = "#172c32", "#007b70", "#c6e9de", "#f3f7f5", "#ffffff", "#687b7b"
ORANGE = "#ed9e66"
FONT_DIR = Path("C:/Windows/Fonts")


def font(size, bold=False):
    path = FONT_DIR / ("segoeuib.ttf" if bold else "segoeui.ttf")
    return ImageFont.truetype(str(path), size)


def brand(canvas, x, y, width=250):
    """Place the supplied official logo intact, with its original white background."""
    with Image.open(HERE / "logo-medicoprint-officiel.png") as source:
        logo = source.convert("RGB")
    height = round(width * logo.height / logo.width)
    logo = logo.resize((width, height), Image.Resampling.LANCZOS)
    canvas.paste(logo, (x, y))


def wrap(draw, text, xy, face, fill, maxw, gap=8):
    x, y = xy
    line = ""
    for word in text.split():
        candidate = (line + " " + word).strip()
        if line and draw.textbbox((0, 0), candidate, font=face)[2] > maxw:
            draw.text((x, y), line, font=face, fill=fill)
            y += face.size + gap
            line = word
        else:
            line = candidate
    if line:
        draw.text((x, y), line, font=face, fill=fill)
        y += face.size + gap
    return y


def photo(canvas, filename, box, cover=False):
    x0, y0, x1, y1 = box
    source = Image.open(HERE / filename).convert("RGBA")
    w, h = x1-x0-40, y1-y0-40
    factor = max(w/source.width, h/source.height) if cover else min(w/source.width, h/source.height)
    source = source.resize((round(source.width*factor), round(source.height*factor)), Image.Resampling.LANCZOS)
    if cover:
        left, top = (source.width-w)//2, (source.height-h)//2
        source = source.crop((left, top, left+w, top+h))
    panel = Image.new("RGBA", (x1-x0, y1-y0), WHITE)
    panel.alpha_composite(source, ((panel.width-source.width)//2, (panel.height-source.height)//2))
    canvas.paste(panel.convert("RGB"), (x0, y0))


def card(size, title, subtitle, filename, layout):
    canvas = Image.new("RGB", size, PALE)
    d = ImageDraw.Draw(canvas)
    w, h = size
    if layout == "landscape":
        d.ellipse((w*.66, -h*.35, w*1.15, h*.62), fill=MINT)
        d.ellipse((w*.73, -h*.22, w*1.08, h*.48), outline="#aacfc0", width=2)
        brand(canvas, 65, 12)
        d.text((65, 145), "EXPERTISE EN HÉMODIALYSE · DEPUIS 2005", font=font(19, True), fill=GREEN)
        d.rounded_rectangle((65, 178, 93, 182), radius=2, fill=ORANGE)
        title_end = wrap(d, title, (65, 195), font(48, True), INK, 535, 6)
        wrap(d, subtitle, (65, title_end+18), font(28), MUTED, 535, 6)
        photo(canvas, filename, (660, 70, w-45, h-65), filename == "traitement-eau.jpg")
        d = ImageDraw.Draw(canvas)
        d.rounded_rectangle((65, h-110, 615, h-40), radius=12, fill=GREEN)
        d.text((86, h-91), "+212 661 979 898  |  medicoprint.ma", font=font(24, True), fill=WHITE)
    elif layout == "square":
        d.rectangle((0, 0, w, 400), fill=INK)
        brand(canvas, 60, 20)
        d.text((65, 155), "SOLUTIONS D’HÉMODIALYSE", font=font(29, True), fill="#9bd1bd")
        wrap(d, title, (65, 210), font(54, True), WHITE, w-125, 6)
        photo(canvas, filename, (55, 430, w-55, h-165))
        d = ImageDraw.Draw(canvas)
        d.rounded_rectangle((60, h-135, w-60, h-63), radius=15, fill=GREEN)
        d.text((86, h-115), "+212 661 979 898  |  medicoprint.ma", font=font(32, True), fill=WHITE)
    else:
        d.rectangle((0, 0, w, 390), fill=INK)
        brand(canvas, 60, 15)
        wrap(d, title, (60, 155), font(54, True), WHITE, w-120, 6)
        photo(canvas, filename, (55, 420, w-55, h-190), filename == "traitement-eau.jpg")
        d = ImageDraw.Draw(canvas)
        wrap(d, subtitle, (60, h-170), font(30, True), INK, w-120, 4)
        d.rounded_rectangle((55, h-100, w-55, h-35), radius=14, fill=GREEN)
        d.text((78, h-84), "+212 661 979 898  |  medicoprint.ma", font=font(28 if w < 900 else 34, True), fill=WHITE)
    return canvas


def make_cards():
    cards = [
        ((1200, 627), "Des solutions pour les professionnels de la dialyse", "Consommables | Traitement de l’eau | Matériel médical", "machine-dialyse.png", "landscape", "linkedin-presentation.png"),
        ((1080, 1350), "Des consommables d’hémodialyse pour les équipes de santé", "Informations produits auprès de Medicoprint", "lifemed-module.png", "square", "instagram-consommables.png"),
        ((1280, 720), "Aux côtés des professionnels de santé", "Hémodialyse | Traitement de l’eau | Matériel médical", "machine-dialyse.png", "landscape", "youtube-thumbnail.png"),
        ((1200, 1200), "Équipements et consommables médicaux à Casablanca", "Hémodialyse | Traitement de l’eau | Matériel médical", "traitement-eau.jpg", "square", "facebook-presentation.png"),
        ((1080, 1920), "Les solutions Medicoprint pour les professionnels de santé", "Hémodialyse | Traitement de l’eau", "traitement-eau.jpg", "vertical", "tiktok-cover.png"),
    ]
    for size, title, subtitle, image, layout, name in cards:
        card(size, title, subtitle, image, layout).save(OUT/name, optimize=True)


def video_frame(size, scene):
    w, h = size
    if h > w:
        layout = "vertical"
        title = ["Medicoprint | Maroc", "Consommables d’hémodialyse", "Traitement de l’eau", "Matériel médical", "Contactez notre équipe"][scene]
        image = ["lifemed-module.png", "lifemed-module.png", "traitement-eau.jpg", "machine-dialyse.png", "machine-dialyse.png"][scene]
        sub = "Au service des professionnels de santé"
    else:
        layout = "landscape"
        title = ["Medicoprint | Maroc", "Consommables d’hémodialyse", "Traitement de l’eau", "Matériel médical", "Contactez notre équipe"][scene]
        image = ["lifemed-module.png", "lifemed-module.png", "traitement-eau.jpg", "machine-dialyse.png", "machine-dialyse.png"][scene]
        sub = "Au service des professionnels de santé"
    return card(size, title, sub, image, layout)


def make_video(size, name):
    import imageio_ffmpeg
    w, h, fps = size[0], size[1], 20
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [exe, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "25", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT/name)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for scene in range(5):
        frame = video_frame(size, scene).convert("RGB").tobytes()
        for _ in range(fps*2):
            proc.stdin.write(frame)
    proc.stdin.close()
    err = proc.stderr.read().decode("utf-8", errors="replace")
    if proc.wait():
        raise RuntimeError(err[-2000:])


if __name__ == "__main__":
    make_cards()
    if "--no-video" not in sys.argv:
        make_video((720, 1280), "vertical-launch.mp4")
        make_video((1280, 720), "youtube-linkedin-launch.mp4")
    print(f"Created social assets in {OUT}")
