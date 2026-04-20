#!/usr/bin/env python3
import subprocess, sys, os, tempfile, shutil

SABLON_DUR  = 1.0
FADE_DUR    = 0.5
BLUR_STR    = 15
OUTPUT      = "cizgi_roman_v2.mp4"
FPS         = 30

PANELS = [
    (1348, 922,    0,   0),
    (1404, 922, 1348,   0),
    (2752, 614,    0, 922),
]

HAS_KALEM = os.path.exists("kalem.wav")
HAS_SAYFA = os.path.exists("sayfa.wav")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Hata:\n" + r.stderr[-2000:])
        sys.exit(1)
    return r

def get_duration(filepath):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except:
        return None

def get_dimensions(filepath):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", filepath],
        capture_output=True, text=True)
    try:
        w, h = r.stdout.strip().split(",")
        return int(w), int(h)
    except:
        return None, None

def find_pages():
    pages = []
    idx = 1
    while True:
        img  = f"{idx}.png"
        wavs = [f"{idx}.{p+1}.wav" for p in range(len(PANELS))]
        if not os.path.exists(img):
            break
        for w in wavs:
            if not os.path.exists(w):
                print(f"Eksik: {w}"); sys.exit(1)
        pages.append((img, wavs))
        idx += 1
    return pages

pages = find_pages()
if not pages:
    print("Hic sayfa bulunamadi."); sys.exit(1)

SW, SH = get_dimensions(pages[0][0])
print(f"Boyut: {SW}x{SH}  |  {len(pages)} sayfa")

sx, sy = SW / 2752, SH / 1536
PS = [(int(pw*sx), int(ph*sy), int(px*sx), int(py*sy)) for pw,ph,px,py in PANELS]
PS[1] = (SW - PS[0][0], PS[1][1], PS[0][0], PS[1][3])
PS[2] = (SW, SH - PS[0][1], 0, PS[0][1])

KALEM_DUR = get_duration("kalem.wav") if HAS_KALEM else 0.0
SAYFA_DUR = get_duration("sayfa.wav") if HAS_SAYFA else 0.0

timeline = []
for page_idx, (img, wavs) in enumerate(pages):
    pinfo = []
    for wav in wavs:
        dur = get_duration(wav)
        if dur is None:
            print(f"Ses okunamadi: {wav}"); sys.exit(1)
        pinfo.append((wav, dur))
    timeline.append((img, pinfo))
    print(f"  Sayfa {page_idx+1}: " + " | ".join(f"{w}={d:.2f}s" for w,d in pinfo))

tmpdir = tempfile.mkdtemp()
page_clips  = []
all_audio   = []
global_t    = 0.0

for page_idx, (img, pinfo) in enumerate(timeline):
    page_dur = SABLON_DUR + sum(d for _, d in pinfo)
    print(f"\nSayfa {page_idx+1} render ({page_dur:.2f}s)...")

    blur_png = os.path.join(tmpdir, f"blur{page_idx}.png")
    clip_out = os.path.join(tmpdir, f"page{page_idx}.mp4")

    run(["ffmpeg", "-y", "-i", img,
         "-vf", f"scale={SW}:{SH},boxblur={BLUR_STR}:5",
         "-frames:v", "1", blur_png])

    if HAS_SAYFA:
        all_audio.append(("sayfa.wav", global_t))

    local_t = SABLON_DUR
    panel_events = []
    for panel_idx, (wav, dur) in enumerate(pinfo):
        t_on  = local_t
        t_off = local_t + dur
        panel_events.append((t_on, t_off, panel_idx))
        if HAS_KALEM:
            all_audio.append(("kalem.wav", global_t + t_on))
        all_audio.append((wav, global_t + t_on))
        local_t += dur

    pad = page_dur + 0.1
    vf  = []

    vf.append(
        f"[0:v]loop=loop=-1:size=1:start=0,"
        f"trim=duration={pad:.3f},"
        f"setpts=PTS-STARTPTS[base]"
    )

    current = "[base]"
    for pidx, (t_on, t_off, pj) in enumerate(panel_events):
        pw, ph, px, py = PS[pj]
        dur_p = t_off - t_on
        cl    = f"[c{pidx}]"
        out   = f"[v{pidx}]"

        vf.append(
            f"[1:v]scale={SW}:{SH},"
            f"crop={pw}:{ph}:{px}:{py},"
            f"loop=loop=-1:size=1:start=0,"
            f"trim=duration={dur_p + 0.1:.3f},"
            f"setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d={FADE_DUR}"
            f"{cl}"
        )
        vf.append(
            f"{current}{cl}"
            f"overlay=x={px}:y={py}:enable='gte(t,{t_on:.3f})'"
            f"{out}"
        )
        current = out

    vf.append(f"{current}format=yuv420p[vout]")

    cmd = (
        ["ffmpeg", "-y", "-i", blur_png, "-i", img]
        + ["-filter_complex", ";".join(vf)]
        + ["-map", "[vout]"]
        + ["-c:v", "libx264", "-preset", "fast", "-crf", "20"]
        + ["-r", str(FPS)]
        + ["-t", f"{page_dur:.3f}"]
        + ["-an", clip_out]
    )
    run(cmd)
    page_clips.append(clip_out)
    global_t += page_dur

TOTAL_DUR = global_t
print(f"\nToplam: {TOTAL_DUR:.3f} sn")

print("Concat ediliyor...")
concat_list = os.path.join(tmpdir, "concat.txt")
with open(concat_list, "w") as f:
    for clip in page_clips:
        f.write(f"file '{clip}'\n")

video_only = os.path.join(tmpdir, "video.mp4")
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
     "-i", concat_list, "-c:v", "copy", video_only])

print("Ses karistiriliyor...")
audio_inputs  = []
audio_filters = []
audio_labels  = []

for idx, (wav, t_start) in enumerate(all_audio):
    audio_inputs += ["-i", wav]
    delay_ms = round(t_start * 1000)
    lbl = f"[da{idx}]"
    audio_filters.append(
        f"[{idx}:a]aresample=44100,adelay={delay_ms}|{delay_ms}{lbl}"
    )
    audio_labels.append(lbl)

n = len(audio_labels)
audio_filters.append(
    "".join(audio_labels) +
    f"amix=inputs={n}:duration=longest:normalize=0:dropout_transition=0[aout]"
)

audio_only = os.path.join(tmpdir, "audio.aac")
run(["ffmpeg", "-y"] + audio_inputs
    + ["-filter_complex", ";".join(audio_filters)]
    + ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k",
       "-t", f"{TOTAL_DUR:.3f}", audio_only])

print("Son birlesim...")
run(["ffmpeg", "-y", "-i", video_only, "-i", audio_only,
     "-c:v", "copy", "-c:a", "copy",
     "-t", f"{TOTAL_DUR:.3f}", OUTPUT])

shutil.rmtree(tmpdir, ignore_errors=True)

size_mb = os.path.getsize(OUTPUT) / 1_048_576
print(f"\nOK: {OUTPUT}  ({size_mb:.1f} MB)")