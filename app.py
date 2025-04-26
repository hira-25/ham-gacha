# app.py  ─ Hamu-Gacha Capsule Edition (single-folder)
import streamlit as st, random, datetime, json, time
from streamlit_lottie import st_lottie
import base64

# ----------------- 設定 -----------------
DAILY_LIMIT = 1
HAMSTERS = [
    ("Kinkuma", "https://placekitten.com/200/200?image=1", "common"),
    ("Sable",   "https://placekitten.com/200/200?image=2", "common"),
    ("Winter",  "https://placekitten.com/200/200?image=3", "rare"),
    ("Robo",    "https://placekitten.com/200/200?image=4", "epic"),
]
WEIGHT = {"common": 70, "rare": 25, "epic": 5}

# Lottie files（同階層）
ANIM_SHAKE    = json.load(open("capsule_open.json"))
ANIM_CONFETTI = json.load(open("gold_confetti.json"))
ANIM_RAINBOW  = json.load(open("rainbow_burst.json"))
ANIM_OPEN     = {"common": ANIM_SHAKE, "rare": ANIM_CONFETTI, "epic": ANIM_RAINBOW}

# 効果音（オプション）
def play_sound(file="epic_win.mp3"):
    try:
        audio_bytes = open(file, "rb").read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
    except:
        pass

# ----------------- ヘルパ -----------------
today = lambda: datetime.date.today().isoformat()
def spins_left():
    return DAILY_LIMIT - st.session_state.get("spins", {}).get(today(), 0)
def add_spin():
    st.session_state.setdefault("spins", {}).setdefault(today(), 0)
    st.session_state["spins"][today()] += 1
def add_ham(h):
    st.session_state.setdefault("collection", []).append(h)

def gacha_roll():
    hamsters, weights = zip(*[(h, WEIGHT[h[2]]) for h in HAMSTERS])
    return random.choices(hamsters, weights)[0]

# ----------------- UI -----------------
st.set_page_config("Hamu-Gacha", "🐹")
st.title("🐹 Hamu-Gacha – Capsule Edition")

with st.expander("📜 My Collection"):
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.get("collection", [])):
        with cols[i % 4]:
            st.image(item[1], width=80)
            st.caption(f"{item[0]} ({item[2]})")

st.divider()

if spins_left() > 0:
    if st.button("✨ Spin Capsule!"):
        ham = gacha_roll()
        name, img, rare = ham
        st_lottie(ANIM_OPEN[rare], height=300, key=f"anim_{time.time()}")
        time.sleep(1.5)
        if rare == "epic":
            st.balloons()
            play_sound()
        elif rare == "rare":
            st.snow()
        st.success(f"🎉 {rare.upper()} → **{name}** GET!")
        st.image(img, width=200)
        add_spin()
        add_ham(ham)
else:
    st.warning("今日はもう回し切ったよ！また明日🐹")

st.caption("Single-folder edition · Data is session-only")
