---
title: "แก้ Codex Voice Mode ใช้ไมค์ไม่ได้บน WSL: WSLg, ALSA และ PulseAudio"
notetype: feed
date: 2026-09-24 02:00:00 +0700
last_modified: 2026-09-24
tags: [Codex, WSL, WSLg, Linux, ALSA, PulseAudio, troubleshooting]
status: published
permalink: /notes/codex-voice-mode-wsl-audio-fix
---

เปิด Codex และพิมพ์คุยได้ตามปกติ แต่พอเริ่ม Voice Mode กลับเจอข้อความนี้:

```text
Failed to connect voice mode: voice audio devices could not open;
check microphone and speaker setup
```

กรณีนี้ไม่ได้จบแค่เปิดสิทธิ์ไมค์บน Windows หรือรีสตาร์ต WSL เพราะมีปัญหาซ้อนกันทั้ง **ช่องทางเสียงของ WSLg**, **การตั้งค่า ALSA** และ **บั๊กในปลั๊กอิน ALSA–PulseAudio ระหว่างเริ่มสตรีม** บทความนี้บันทึกวิธีแยกสาเหตุและแก้ทีละชั้นจากการทดสอบจริง

> ทดสอบเมื่อ 24 กันยายน 2026 บน Debian ใน WSL 2, Codex CLI 0.156.1, CPAL 0.18.2 และ `libasound2-plugins` 1.2.7.1-1 ขั้นตอนแพตช์ท้ายบทความเป็น workaround เฉพาะอาการที่ตรวจพบ ไม่ใช่อัปเดตทางการของ Codex และไม่จำเป็นสำหรับทุกเครื่อง

## สรุปวิธีแก้

1. ถ้า WSLg ถูกปิด ให้เปิด `guiApplications=true` ใน `.wslconfig` แล้วรีสตาร์ต WSL
2. ถ้า PulseAudio ทำงานแล้วแต่ ALSA ยังเปิด `default` ไม่ได้ ให้ติดตั้งปลั๊กอินและตั้ง `~/.asoundrc`
3. ถ้าเปิดอุปกรณ์ได้แต่สตรีมหยุดพร้อม `snd_pcm_avail_delay ... I/O error (5)` ให้ตรวจบั๊ก latency ของปลั๊กอินรุ่นที่ใช้อยู่ก่อนพิจารณาแพตช์
4. ทดสอบทั้งการเปิดอุปกรณ์และการทำงานต่อเนื่อง การเห็นชื่อไมค์หรือผ่านครั้งเดียวไม่พอ

**หยุดที่ขั้นที่แก้ปัญหาได้ ไม่ต้องคอมไพล์ปลั๊กอินใหม่ถ้าตั้งค่าเสียงแล้วใช้งานได้ปกติ**

## เสียงเดินทางผ่านอะไรบ้าง

```text
Codex Voice Mode
        ↕
Native voice helper / CPAL
        ↕
ALSA default PCM
        ↕
ALSA PulseAudio plugin
        ↕
WSLg PulseAudio server
        ↕
ไมโครโฟนและลำโพงของ Windows
```

WSLg ไม่ได้มีแค่หน้าต่าง GUI แต่มี PulseAudio สำหรับเชื่อมเสียงเข้าและออกกับ Windows ด้วย ดังนั้นการปิด WSLg อาจตัดเส้นทางเสียงที่โปรแกรม Linux ต้องใช้ แม้ตัวโปรแกรมจะทำงานใน terminal ก็ตาม [1][2]

## แยกปัญหา login ออกจากปัญหาเสียง

ในกรณีที่ตรวจพบ log แสดงว่า realtime conversation เริ่มได้แล้ว ก่อนล้มที่ขั้นเปิดอุปกรณ์:

```text
phase=Some(OpenDevices) exit_code=Some(25)
stage=AudioDevices kind="closed"
```

หลักฐานนี้ชี้ไปที่อุปกรณ์เสียงฝั่งเครื่อง ไม่ใช่เหตุผลให้ logout/login ซ้ำ ส่วน HTTP `401`, `token_expired` หรือ `invalid_refresh_token` เป็นอีกปัญหาหนึ่ง ต้องแก้ authentication แยกกัน

ควรอ่านเฉพาะ error และสถานะที่จำเป็นจาก log ไม่เผยแพร่ไฟล์ `auth.json`, token, realtime TRACE หรือ SDP ทั้งก้อน เพราะอาจมีข้อมูลรับรองและข้อมูลเซสชัน

## 1. ตรวจ WSLg และอุปกรณ์ฝั่ง Windows

### ตรวจใน WSL

```bash
codex --version
printf 'PULSE_SERVER=%s\n' "${PULSE_SERVER:-<unset>}"
test -S /mnt/wslg/PulseServer && printf 'PulseServer socket exists\n'
```

ถ้ามี `pactl` อยู่แล้ว ตรวจต่อได้ด้วย:

```bash
pactl info
pactl list short sources
pactl list short sinks
```

WSLg โดยปกติจะให้ `PULSE_SERVER` ชี้ไปที่ `unix:/mnt/wslg/PulseServer` การมี socket อย่างเดียวไม่ยืนยันว่าเชื่อมต่อสำเร็จ ต้องดูผล `pactl` และทดสอบเปิดอุปกรณ์ต่อด้วย หากยังไม่มี `pactl` ให้ติดตั้ง `pulseaudio-utils` ตามขั้นที่ 2

ฝั่ง Windows ให้ตรวจว่าไมค์และลำโพงที่ต้องการใช้งานเป็นอุปกรณ์เริ่มต้น และอนุญาตการเข้าถึงไมค์สำหรับ desktop apps แล้ว การเห็นอุปกรณ์สถานะ OK บน Windows ยังไม่ยืนยันว่าเส้นทางเสียงใน WSL ใช้งานได้

### ถ้า `.wslconfig` ปิด WSLg ไว้

เปิด **Windows PowerShell** แล้วสำรองไฟล์ก่อนแก้:

```powershell
$config = Join-Path $env:USERPROFILE '.wslconfig'
if (Test-Path $config) {
    Copy-Item $config "$config.before-codex-voice-$(Get-Date -Format yyyyMMdd-HHmmss)"
}
notepad.exe $config
```

เพิ่มหรือแก้เฉพาะค่านี้ใน section `[wsl2]` โดยเก็บค่า memory, processors และการตั้งค่าอื่นไว้ตามเดิม ไม่สร้าง `[wsl2]` ซ้ำ:

```ini
[wsl2]
guiApplications=true
```

จากนั้นบันทึกงานและหยุดงานสำคัญใน WSL ก่อนสั่งจาก **Windows PowerShell**:

```powershell
wsl --shutdown
```

คำสั่งนี้ปิดทุก WSL distribution ที่กำลังทำงาน รวมถึงงานที่อาศัย WSL เช่น Docker ไม่ใช่รีสตาร์ต Codex อย่างเดียว เปิด WSL ใหม่แล้วตรวจ socket และ `pactl` ซ้ำ [1]

ถ้า WSLg เปิดอยู่แล้วหรือไม่มีการปิดไว้ แต่ยังไม่มี PulseServer ให้ตรวจการติดตั้ง/รุ่น WSLg ตามเอกสารก่อน ไม่ต้องติดตั้ง PulseAudio daemon อีกตัวหรือ hardcode IP เพื่อข้ามปัญหา

## 2. ให้ ALSA ใช้ PulseAudio ของ WSLg

หลังเปิด WSLg แล้ว กรณีนี้ PulseAudio เปิด input และ output ได้ แต่ ALSA ยังหาอุปกรณ์ `default` ที่ใช้งานได้ไม่เจอ

บน Debian/Ubuntu ตรวจรายการที่จะติดตั้งก่อน:

```bash
sudo apt-get update
apt-get --simulate --no-install-recommends install libasound2-plugins pulseaudio-utils
sudo apt-get install --no-install-recommends libasound2-plugins pulseaudio-utils
```

ใช้ PulseAudio server ของ WSLg เดิม ไม่ต้องเริ่ม sound server ตัวที่สอง

### สำรองและแก้ `~/.asoundrc`

```bash
if test -e "$HOME/.asoundrc"; then
    cp -p "$HOME/.asoundrc" "$HOME/.asoundrc.before-codex-voice-$(date +%Y%m%d-%H%M%S)"
fi
```

เปิด `~/.asoundrc` ด้วย editor แล้วเพิ่มหรือปรับ default PCM/control เป็น:

```text
pcm.!default {
    type pulse
    hint {
        show on
        description "WSLg PulseAudio default input and output"
    }
}
ctl.!default {
    type pulse
}
```

ถ้ามี config เดิม ให้รวมเข้ากับของเดิม ไม่วางทับทั้งไฟล์หรือสร้าง block ชื่อเดียวกันซ้ำ ค่า `hint` ช่วยให้เครื่องมือ enumerate อุปกรณ์ได้พร้อมคำอธิบาย

**ขอบเขตของการเปลี่ยนแปลง:** `~/.asoundrc` เป็นค่าเสียงของบัญชี Linux นี้ โปรแกรม ALSA อื่นที่ใช้ `default` จะได้รับผลด้วย ไม่ได้จำกัดเฉพาะ Codex

### กรณีโหลดปลั๊กอินไม่พบ

ตรวจตำแหน่งปลั๊กอินที่แพ็กเกจติดตั้งจริง:

```bash
dpkg -L libasound2-plugins
```

ถ้า error ระบุว่าโหลด `libasound_module_pcm_pulse.so` ไม่พบ สามารถระบุ library path ใน `~/.asoundrc` เพิ่มได้ ตัวอย่างนี้สำหรับ Debian **x86_64** เท่านั้น:

```text
pcm_type.pulse {
    lib "/usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_pcm_pulse.so"
}
ctl_type.pulse {
    lib "/usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_ctl_pulse.so"
}
```

ใช้ path จากเครื่องจริง หากเป็น ARM64 หรือ distro อื่น path อาจต่างกัน ที่สำคัญคือการเรียก voice helper ตรง ๆ กับเรียกผ่าน Codex มี environment ไม่เหมือนกัน ใน Codex 0.156.1 ตัว launcher มีการเลือก ALSA plugin directory ให้ child process อยู่แล้ว จึงไม่ควรสรุปจาก direct-helper test เพียงอย่างเดียวว่า Codex หา path ผิด [5]

ปิด Codex แล้วเปิดใหม่และลอง Voice Mode หากใช้งานได้ต่อเนื่องแล้ว **ไม่ต้องทำขั้นแพตช์ด้านล่าง** การเปลี่ยน `.asoundrc` ไม่ต้องรีสตาร์ต WSL อีก

## 3. เปิดอุปกรณ์ได้แล้ว แต่เสียงยังหยุด: ตรวจ latency error

การทดสอบซ้ำพบว่าบางครั้ง voice helper เปิดอุปกรณ์ได้ แต่หยุดระหว่างเริ่มสตรีมด้วย device error ใน build นี้พบ helper exit code `37` ต่างจาก exit `25` ตอนเปิดอุปกรณ์ไม่ได้ [5]

เมื่อทดสอบผ่าน CPAL รุ่นเดียวกับ Codex จึงเห็น error ที่เจาะจงขึ้น:

```text
ALSA function 'snd_pcm_avail_delay' failed with error 'I/O error (5)'
```

ใน source ของ `alsa-plugins` รุ่น `v1.2.7.1` ฟังก์ชัน `pulse_delay()` มีเงื่อนไขนี้ [3]:

```c
err = pa_stream_get_latency(pcm->stream, &lat, NULL);
if (err) {
    if (err != PA_ERR_NODATA) {
        err = -EIO;
        goto finish;
    }
}
```

ปัญหาคือเอา return status เมื่อฟังก์ชันล้มเหลวไปเทียบกับ error enum `PA_ERR_NODATA` โดยตรง แทนที่จะอ่าน error ของ context เมื่อข้อมูล timing ยังไม่พร้อม จึงอาจรายงานเป็น I/O error ทั้งที่มีทางรอ latency update อยู่แล้ว ใน implementation ของ PulseAudio 16.1 เส้นทางนี้คืนสถานะติดลบและตั้ง error ไว้ใน context [4]

แพตช์ที่ทดสอบเปลี่ยนเฉพาะการอ่าน error:

```diff
- if (err != PA_ERR_NODATA) {
+ if (pa_context_errno(pcm->p->context) != PA_ERR_NODATA) {
```

การรอข้อมูล timing และการจัดการ error จริงยังอยู่เหมือนเดิม ไม่ได้ปิด error handling ทั้งหมด และไม่ได้แทนไมค์ด้วยอุปกรณ์ `null` เพื่อให้ test ผ่าน

> ใช้ส่วนนี้เฉพาะเมื่อพิสูจน์ได้ว่าเป็นอาการและ source แบบเดียวกัน ถ้าใช้ปลั๊กอินรุ่นใหม่ที่แก้แล้ว ไม่ควรย้อนรุ่นมาคอมไพล์ตามบทความเพียงเพราะใช้ Voice Mode ไม่ได้

## 4. สร้างปลั๊กอินที่แก้แล้วเป็นสำเนาแยก

ส่วนนี้เป็น **local workaround ที่คอมไพล์จาก upstream source** ไม่ใช่แพ็กเกจที่ OpenAI หรือ distro แจกให้ และไม่ทับไฟล์ใน `/usr/lib` หรือตัว Codex

### เตรียมเครื่องมือ build

ตรวจว่ามี `gcc`, `git`, `python3` และ ALSA development headers แล้ว หากขาด ให้ตรวจรายการและติดตั้ง:

```bash
apt-get --simulate --no-install-recommends install build-essential git python3 libasound2-dev
sudo apt-get install --no-install-recommends build-essential git python3 libasound2-dev
```

คำสั่ง build ด้านล่างใช้ PulseAudio headers ที่แตกจาก `.deb` รุ่นตรงกับ `libpulse0` ที่ติดตั้ง จึงไม่ต้องติดตั้ง dependency ทั้งชุดของ `libpulse-dev` หาก repository ไม่มีรุ่นที่ตรงกันแล้ว ให้หยุดและจัดรุ่นแพ็กเกจให้สอดคล้องกันก่อน

### ดาวน์โหลด แพตช์ และ build

รัน block นี้ใน Bash ของ WSL ผลลัพธ์อยู่ใน directory ใหม่และยังไม่เปลี่ยน config เสียง:

```bash
(
    set -eu
    mkdir -p "$HOME/.cache"
    work="$(mktemp -d "$HOME/.cache/codex-pulse-build.XXXXXX")"
    export CODEX_PULSE_WORK="$work"

    git clone --depth 1 --branch v1.2.7.1 \
        https://github.com/alsa-project/alsa-plugins.git "$work/upstream"
    git -C "$work/upstream" rev-parse HEAD

    mkdir -p "$work/headers"
    cd "$work"
    pulse_version="$(dpkg-query -W -f='${Version}' libpulse0)"
    apt-get download "libpulse-dev=$pulse_version"
    dpkg-deb --extract ./libpulse-dev_*.deb "$work/headers"

    python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["CODEX_PULSE_WORK"]) / "upstream/pulse/pcm_pulse.c"
source = path.read_text()
old = "if (err != PA_ERR_NODATA) {"
new = "if (pa_context_errno(pcm->p->context) != PA_ERR_NODATA) {"
if source.count(old) != 1:
    raise SystemExit("Source differs from the tested version; stop and review it.")
path.write_text(source.replace(old, new, 1))
PY

    gcc -shared -fPIC -DPIC -D_GNU_SOURCE -O2 -Wall \
        -I "$work/headers/usr/include" \
        -o "$work/libasound_module_pcm_pulse.so" \
        "$work/upstream/pulse/pcm_pulse.c" \
        "$work/upstream/pulse/pulse.c" \
        -lasound -Wl,-l:libpulse.so.0 -pthread

    git -C "$work/upstream" diff -- pulse/pcm_pulse.c
    printf '\nCandidate library: %s\n' "$work/libasound_module_pcm_pulse.so"
)
```

ควรเห็น diff เปลี่ยนเฉพาะเงื่อนไขข้างต้น และคำสั่ง compile ต้องจบโดยไม่มี error สำเนา source เก็บ copyright และ license ของ upstream ไว้ตามเดิม

### วิธีที่ใช้ยืนยันแพตช์ในกรณีนี้

การ build ผ่านยังไม่แปลว่าสตรีมเสียงทำงาน จึงเปรียบเทียบปลั๊กอินระบบเดิมกับสำเนาที่แพตช์แล้วผ่าน CPAL 0.18.2 โดยใช้ HOME ชั่วคราวและ `.asoundrc` แยกสำหรับ process ทดสอบ ไม่เปลี่ยน HOME ของ Codex ที่ใช้งานจริง

การทดสอบเปิด input/output จริง ทิ้ง input ในเครื่องและส่ง silence ไป output ตรวจว่ามี callbacks ต่อเนื่อง ไม่มี fatal backend/device error และปิดสตรีมได้ตามปกติ จากนั้นตรวจ native voice helper ของ Codex กับ local WebRTC peer โดย mute ไมค์และ suppress speaker ไม่มีการเรียก OpenAI API ผลอยู่ในหัวข้อถัดไป

นี่เป็นบันทึกวิธีตรวจและผลที่ได้ ไม่ได้แนบโปรแกรม diagnostic มาด้วย สำหรับการใช้งานจริงยังต้องลองพูดและฟังผ่าน Voice Mode หลังตั้งค่า หากสตรีมหยุดหรือยังมี error ให้ย้อน config ตามหัวข้อวิธีถอยกลับ ไม่ถือว่าการ compile สำเร็จเพียงอย่างเดียวคือแก้ครบแล้ว

### ติดตั้งหลัง candidate ผ่าน

คัดลอก `.so` ที่ทดสอบแล้วไป directory ถาวร เช่น `~/.local/lib/codex-audio/` อย่าชี้ config ไปที่ cache หรือ temporary directory ที่อาจถูกล้างภายหลัง

ตัวอย่างต่อไปนี้ให้แทน `/absolute/path/to/tested/candidate.so` ด้วย path ที่ทดสอบแล้ว ใช้ชื่อไฟล์ใหม่เพื่อไม่ทับปลั๊กอิน local ที่มีอยู่:

```bash
(
    set -eu
    candidate='/absolute/path/to/tested/candidate.so'
    test -f "$candidate"
    mkdir -p "$HOME/.local/lib/codex-audio"
    target="$HOME/.local/lib/codex-audio/libasound_module_pcm_pulse-fixed.so"
    if test -e "$target"; then
        printf 'Target already exists; review it before replacing.\n' >&2
        exit 1
    fi
    install -m 755 "$candidate" "$target"
    printf 'Use this absolute library path in .asoundrc: %s\n' "$target"
)
```

สำรอง `.asoundrc` อีกครั้งก่อนเปิดใช้แพตช์ แล้วแก้เฉพาะ `pcm_type.pulse.lib` ให้เป็น **absolute path ที่คำสั่งด้านบนพิมพ์ออกมา** ไม่ใช้ `$HOME` หรือ `~` ตรง ๆ ในช่อง `lib` และไม่เพิ่ม block ซ้ำ

คง `ctl_type.pulse.lib` เป็นปลั๊กอินระบบได้ เพราะแพตช์นี้แก้ PCM module ไม่ได้แก้ control module ส่วน `pcm.!default` และ `ctl.!default` ยังคงเป็น `type pulse` ตามเดิม

ปิด Codex แล้วเปิดใหม่ ไม่ต้องรีสตาร์ต WSL สำหรับการสลับปลั๊กอินระดับผู้ใช้นี้

## 5. ผลที่ตรวจยืนยันได้ และสิ่งที่ยังไม่ได้ยืนยัน

| การตรวจ | ผลที่พบในเครื่องทดสอบ |
|---|---|
| ใช้ปลั๊กอินระบบเดิมผ่าน CPAL | ทำซ้ำอาการ `snd_pcm_avail_delay` I/O error ได้ |
| ใช้แพตช์แล้วเปิด/สตรีม/ปิดผ่าน CPAL | ผ่าน 5 รอบ มี callbacks ทั้ง input/output และไม่พบ I/O error |
| ใช้ native voice helper เดิมของ Codex กับ local WebRTC peer | ผ่าน 5/5 รอบ แต่ละรอบ exit code 0 |
| ตรวจไฟล์ปลั๊กอินที่ distro ติดตั้งด้วย `dpkg --verify libasound2-plugins` | ไม่พบการแก้ไฟล์แพ็กเกจ |
| เทียบ SHA-256 ของ voice helper กับ manifest ที่ติดมากับ Codex | ตรงกัน ไม่ได้แพตช์ executable ของ Codex |
| พูดคุยจริงกับบริการ OpenAI | ยังไม่ได้ยืนยันในการทดสอบชุดนี้ |

สถานะสำคัญของ helper ที่ผ่าน:

```text
ready → runtimeReady → offer → transportReady → devicesOpened
      → audioControlsApplied → audioState → audioState → closed
helper exit code: 0
```

ตัวเลขนี้เป็นผลทดสอบเฉพาะ environment ที่ระบุ ไม่ใช่การรับประกันทุกเวอร์ชันหรือทุกอุปกรณ์ การทดสอบแบบ local ไม่บันทึกเสียงและไม่ส่งเสียงไป OpenAI แต่เมื่อเปิด Voice Mode จริง เสียงจะถูกใช้งานโดยบริการตามการทำงานปกติของ Codex

หลังแก้ ให้ลองพูดและฟังคำตอบจริง รวมทั้งเปิด/ปิด Voice Mode ซ้ำ เพื่อยืนยัน microphone, speaker, network และพฤติกรรมหน้าใช้งานให้ครบ

## วิธีถอยกลับ

### ยกเลิกเฉพาะแพตช์ แต่ยังใช้ WSLg ต่อ

ปิด Codex แล้วแก้ `pcm_type.pulse.lib` ใน `~/.asoundrc` กลับไปยังปลั๊กอินของ distro ตัวอย่าง Debian x86_64:

```text
pcm_type.pulse {
    lib "/usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_pcm_pulse.so"
}
```

อีกทางคือคืน `.asoundrc` จาก backup ที่ทำไว้ **ก่อนเปิดใช้แพตช์** จากนั้นเปิด Codex ใหม่ ไม่ต้องถอนแพ็กเกจหรือสั่ง `wsl --shutdown` และยังไม่ต้องลบไฟล์ local plugin ทั้งนี้การกลับไปปลั๊กอินเดิมอาจทำให้ I/O error เดิมกลับมา

### ยกเลิกการเปลี่ยนค่า ALSA ทั้งหมด

คืน `.asoundrc` จาก backup ก่อนเริ่มแก้เสียง หากแต่เดิมไม่มีไฟล์นี้ ให้ย้ายไฟล์ที่สร้างขึ้นไปเก็บชื่ออื่นแทนการลบทิ้ง แล้วเริ่มโปรแกรมเสียงใหม่ โปรแกรม ALSA อื่นในบัญชีจะกลับไปใช้การตั้งค่าก่อนแก้ด้วย

การย้อน `.asoundrc` ไม่ได้ย้อน `.wslconfig` หากต้องการคืนการตั้งค่า WSLg ให้ใช้ backup ของ `.wslconfig` แยกต่างหาก และนัดรีสตาร์ต WSL หลังบันทึกงาน การกลับไป `guiApplications=false` จะปิดช่องทาง WSLg อีกครั้ง

## ข้อคิดจากการแก้ปัญหานี้

- Windows เห็นไมค์ ไม่ได้แปลว่า WSL เห็นไมค์
- PulseAudio เปิดได้ ไม่ได้แปลว่า ALSA `default` ถูกตั้งค่าแล้ว
- เปิดอุปกรณ์ได้ ไม่ได้แปลว่าสตรีมจะทำงานต่อเนื่อง
- `null` เป็นอุปกรณ์ทิ้ง/สร้างตัวอย่างเสียง ไม่ใช่หลักฐานว่าไมค์จริงใช้งานได้
- ทดสอบแบบมี control ที่ทำซ้ำ error เดิมได้ แล้วเปลี่ยนทีละจุด จะช่วยแยกการแก้ต้นเหตุออกจากการทำให้ error เงียบ
- แพตช์ระดับผู้ใช้และ backup ทำให้ย้อนกลับได้โดยไม่ทับไลบรารีของระบบ แต่ต้องจำไว้ว่า override นี้ยังมีผลหลังอัปเดตแพ็กเกจ เมื่อ upstream/distro แก้แล้วควรทดสอบกลับไปใช้ปลั๊กอินทางการ

## Related Notes

- [[Claude Code]]
- [[Agent Harness Engineering]]

## อ้างอิง

1. [Microsoft Learn — Advanced settings configuration in WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config): ตำแหน่ง `.wslconfig`, `guiApplications` และผลของ `wsl --shutdown`
2. [Microsoft WSLg](https://github.com/microsoft/wslg): การเชื่อม PulseAudio sink/source กับ Windows
3. [ALSA plugins v1.2.7.1 — pulse/pcm_pulse.c](https://github.com/alsa-project/alsa-plugins/blob/v1.2.7.1/pulse/pcm_pulse.c): implementation ของ `pulse_delay()` ที่นำมาแก้
4. [PulseAudio v16.1 — stream.c](https://github.com/pulseaudio/pulseaudio/blob/v16.1/src/pulse/stream.c) และ [internal.h](https://github.com/pulseaudio/pulseaudio/blob/v16.1/src/pulse/internal.h): `pa_stream_get_latency()` และ macro ตรวจ error ที่ตั้งค่า context
5. Codex source ตรงกับ build ที่ตรวจ: [realtime-webrtc](https://github.com/openai/codex/tree/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/realtime-webrtc/src) และ [voice-host](https://github.com/openai/codex/tree/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/voice-host/src)
