from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import os, json, random

app = Flask(__name__)
app.secret_key = 'emotune_bollywood_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotune.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ── User Model ────────────────────────────────────────────
class User(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(80), unique=True, nullable=False)
    email     = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(200), nullable=False)
    avatar    = db.Column(db.String(10), default='🎵')
    created_at= db.Column(db.DateTime, default=datetime.utcnow)

# ── Bollywood Music Library ───────────────────────────────
MUSIC = {
    "happy": {
        "label": "Happy / Khushi",
        "emoji": "😄",
        "gradient": "linear-gradient(135deg,#f7971e,#ffd200)",
        "songs": {
            "trending": [
                {"title":"Kesariya","artist":"Arijit Singh","film":"Brahmastra","year":"2022","youtube":"https://www.youtube.com/watch?v=BddP6PYo2gs","thumb":"🎶"},
                {"title":"Naatu Naatu","artist":"Rahul Sipligunj","film":"RRR","year":"2022","youtube":"https://www.youtube.com/watch?v=OsU0CGZoV8E","thumb":"🥁"},
                {"title":"Jhoome Jo Pathaan","artist":"Arijit Singh","film":"Pathaan","year":"2023","youtube":"https://www.youtube.com/watch?v=IdmHZge2fTs","thumb":"🎤"},
                {"title":"Besharam Rang","artist":"Shilpa Rao","film":"Pathaan","year":"2023","youtube":"https://www.youtube.com/watch?v=z7oFMGCCBFg","thumb":"💃"},
                {"title":"Tum Kya Mile","artist":"Arijit Singh","film":"Rocky Aur Rani","year":"2023","youtube":"https://www.youtube.com/watch?v=ZO93BQ63R8c","thumb":"🌟"},
            ],
            "90s": [
                {"title":"Chaiyya Chaiyya","artist":"Sukhwinder Singh","film":"Dil Se","year":"1998","youtube":"https://www.youtube.com/watch?v=5yYP5c6oFhw","thumb":"🚂"},
                {"title":"Kuch Kuch Hota Hai","artist":"Kumar Sanu","film":"KKHH","year":"1998","youtube":"https://www.youtube.com/watch?v=FqKxBBGpQao","thumb":"❤️"},
                {"title":"Dilwale Dulhania Le Jayenge","artist":"Lata Mangeshkar","film":"DDLJ","year":"1995","youtube":"https://www.youtube.com/watch?v=4NMHkCWp670","thumb":"🌾"},
                {"title":"Jai Ho","artist":"A.R. Rahman","film":"Slumdog","year":"1998","youtube":"https://www.youtube.com/watch?v=Hy1YVFHJhJY","thumb":"🙌"},
                {"title":"Didi","artist":"Udit Narayan","film":"Yeh Dillagi","year":"1994","youtube":"https://www.youtube.com/watch?v=fGxlzwJP_1k","thumb":"👫"},
            ],
            "2000s": [
                {"title":"Kajra Re","artist":"Alisha Chinai","film":"Bunty Aur Babli","year":"2005","youtube":"https://www.youtube.com/watch?v=WLZIe7wfB1c","thumb":"💫"},
                {"title":"Dhoom Machale","artist":"Sunidhi Chauhan","film":"Dhoom","year":"2004","youtube":"https://www.youtube.com/watch?v=P6lE24VKuCE","thumb":"🏍️"},
                {"title":"Rang De Basanti","artist":"A.R. Rahman","film":"Rang De Basanti","year":"2006","youtube":"https://www.youtube.com/watch?v=Nj3HWVbBfPk","thumb":"🎨"},
            ]
        }
    },
    "sad": {
        "label": "Sad / Udaas",
        "emoji": "😢",
        "gradient": "linear-gradient(135deg,#4b6cb7,#182848)",
        "songs": {
            "trending": [
                {"title":"Tum Hi Ho","artist":"Arijit Singh","film":"Aashiqui 2","year":"2013","youtube":"https://www.youtube.com/watch?v=IJq0yyWug04","thumb":"💔"},
                {"title":"Channa Mereya","artist":"Arijit Singh","film":"Ae Dil Hai Mushkil","year":"2016","youtube":"https://www.youtube.com/watch?v=zaYQMWAcGgE","thumb":"🌊"},
                {"title":"Raabta","artist":"Arijit Singh","film":"Agent Sai Srinivasa","year":"2017","youtube":"https://www.youtube.com/watch?v=1UjnKEcFrC8","thumb":"🌙"},
                {"title":"Agar Tum Saath Ho","artist":"Arijit Singh & Alka Yagnik","film":"Tamasha","year":"2015","youtube":"https://www.youtube.com/watch?v=sQMBoJtBDZg","thumb":"🕯️"},
                {"title":"Phir Bhi Tumko Chaahunga","artist":"Arijit Singh","film":"Half Girlfriend","year":"2017","youtube":"https://www.youtube.com/watch?v=lRJKqkUBBC8","thumb":"🥀"},
            ],
            "90s": [
                {"title":"Pehla Nasha","artist":"Udit Narayan","film":"Jo Jeeta Wohi Sikandar","year":"1992","youtube":"https://www.youtube.com/watch?v=RrBsxmL1myk","thumb":"🌹"},
                {"title":"Kabhi Alvida Naa Kehna","artist":"Sonu Nigam","film":"KANK","year":"2006","youtube":"https://www.youtube.com/watch?v=L8A1FJ7HKPI","thumb":"🚉"},
                {"title":"Tujhe Bhula Diya","artist":"Mohit Chauhan","film":"Anjaana Anjaani","year":"2010","youtube":"https://www.youtube.com/watch?v=4U0PkJKenB4","thumb":"❄️"},
                {"title":"Ek Ladki Ko Dekha","artist":"Kumar Sanu","film":"1942 A Love Story","year":"1994","youtube":"https://www.youtube.com/watch?v=LPcN0wQK4Vk","thumb":"🌸"},
            ],
            "2000s": [
                {"title":"Tu Hi Meri Shab Hai","artist":"Mohit Chauhan","film":"Gangster","year":"2006","youtube":"https://www.youtube.com/watch?v=bDGMJENY1SQ","thumb":"🌃"},
                {"title":"Woh Lamhe","artist":"Atif Aslam","film":"Zeher","year":"2005","youtube":"https://www.youtube.com/watch?v=bdJanPhMqmc","thumb":"⏳"},
            ]
        }
    },
    "angry": {
        "label": "Angry / Gussa",
        "emoji": "😠",
        "gradient": "linear-gradient(135deg,#c0392b,#e74c3c)",
        "songs": {
            "trending": [
                {"title":"Zinda","artist":"Benny Dayal","film":"Bhaag Milkha Bhaag","year":"2013","youtube":"https://www.youtube.com/watch?v=IZLFyuGmX5w","thumb":"🏃"},
                {"title":"Sultan","artist":"Sukhwinder Singh","film":"Sultan","year":"2016","youtube":"https://www.youtube.com/watch?v=8xKxOBpFt8A","thumb":"🥊"},
                {"title":"Dangal","artist":"Daler Mehndi","film":"Dangal","year":"2016","youtube":"https://www.youtube.com/watch?v=vhzlFhaxEUc","thumb":"💪"},
                {"title":"Sher Khul Gaye","artist":"Vishal-Shekhar","film":"Fighter","year":"2024","youtube":"https://www.youtube.com/watch?v=OqrTOyE-5DQ","thumb":"🦁"},
            ],
            "90s": [
                {"title":"Ek Do Teen","artist":"Alka Yagnik","film":"Tezaab","year":"1988","youtube":"https://www.youtube.com/watch?v=c4p6vn0Z8bQ","thumb":"🔥"},
                {"title":"Sarfaroshi Ki Tamanna","artist":"Udit Narayan","film":"The Legend of Bhagat Singh","year":"2002","youtube":"https://www.youtube.com/watch?v=v3NUMUKFThI","thumb":"✊"},
                {"title":"Main Aisa Hi Hoon","artist":"Udit Narayan","film":"Main Aisa Hi Hoon","year":"2005","youtube":"https://www.youtube.com/watch?v=D1IH_lXJC1g","thumb":"⚡"},
            ],
            "2000s": [
                {"title":"Rock On","artist":"Farhan Akhtar","film":"Rock On","year":"2008","youtube":"https://www.youtube.com/watch?v=L5kW-Y2sTJQ","thumb":"🎸"},
                {"title":"Jai Ho","artist":"Salman Khan","film":"Jai Ho","year":"2014","youtube":"https://www.youtube.com/watch?v=zx_BhgcPqSc","thumb":"🌟"},
            ]
        }
    },
    "surprised": {
        "label": "Surprised / Hairaan",
        "emoji": "😲",
        "gradient": "linear-gradient(135deg,#f093fb,#f5576c)",
        "songs": {
            "trending": [
                {"title":"Badtameez Dil","artist":"Benny Dayal","film":"Yeh Jawaani Hai Deewani","year":"2013","youtube":"https://www.youtube.com/watch?v=t9ZVbNmFNMY","thumb":"🎊"},
                {"title":"London Thumakda","artist":"Labh Janjua","film":"Queen","year":"2014","youtube":"https://www.youtube.com/watch?v=uddx6LCmCKo","thumb":"🎺"},
                {"title":"Ghungroo","artist":"Arijit Singh","film":"War","year":"2019","youtube":"https://www.youtube.com/watch?v=qFkNATtMHBM","thumb":"💃"},
                {"title":"Simmba","artist":"Mika Singh","film":"Simmba","year":"2018","youtube":"https://www.youtube.com/watch?v=dl_fOPdVDGY","thumb":"🥳"},
            ],
            "90s": [
                {"title":"Didi Tera Dewar Deewana","artist":"Kavita Krishnamurthy","film":"Hum Aapke Hain Koun","year":"1994","youtube":"https://www.youtube.com/watch?v=eTiL9l0_oRc","thumb":"🎶"},
                {"title":"Ole Ole","artist":"Abhijeet","film":"Yeh Dillagi","year":"1994","youtube":"https://www.youtube.com/watch?v=xXWxf_5TbO8","thumb":"😎"},
                {"title":"Woh Ladki Jo","artist":"Udit Narayan","film":"Raja Hindustani","year":"1996","youtube":"https://www.youtube.com/watch?v=jxQrMkA9bEo","thumb":"👀"},
            ],
            "2000s": [
                {"title":"Desi Girl","artist":"Vishal-Shekhar","film":"Dostana","year":"2008","youtube":"https://www.youtube.com/watch?v=01LBzFrZMDI","thumb":"🌺"},
                {"title":"Pareshaan","artist":"Shalmali Kholgade","film":"Ishaqzaade","year":"2012","youtube":"https://www.youtube.com/watch?v=U3vlEKBW0hM","thumb":"🌀"},
            ]
        }
    },
    "fearful": {
        "label": "Fear / Darr",
        "emoji": "😨",
        "gradient": "linear-gradient(135deg,#2d3561,#c05c7e)",
        "songs": {
            "trending": [
                {"title":"Darr Ke Aage Jeet Hai","artist":"Shaan","film":"Darr @ The Mall","year":"2014","youtube":"https://www.youtube.com/watch?v=nRhR97tlpE0","thumb":"🌟"},
                {"title":"Jeena Jeena","artist":"Atif Aslam","film":"Badlapur","year":"2015","youtube":"https://www.youtube.com/watch?v=gCMkRCKqgAA","thumb":"🌙"},
                {"title":"Raabta (Kehte Hain)","artist":"Arijit Singh","film":"Agent Sai","year":"2017","youtube":"https://www.youtube.com/watch?v=1UjnKEcFrC8","thumb":"🌊"},
            ],
            "90s": [
                {"title":"Darr Mujhe Darr Lagta Hai","artist":"Udit Narayan","film":"Darr","year":"1993","youtube":"https://www.youtube.com/watch?v=sRvtLGDoKAY","thumb":"💙"},
                {"title":"Koi Mil Gaya","artist":"Udit Narayan","film":"Koi Mil Gaya","year":"2003","youtube":"https://www.youtube.com/watch?v=FKBEuS1V3to","thumb":"👽"},
            ],
            "2000s": [
                {"title":"Teri Meri Kahaani","artist":"Udit Narayan","film":"Bodyguard","year":"2011","youtube":"https://www.youtube.com/watch?v=ooBxJ8BEXFE","thumb":"🌸"},
            ]
        }
    },
    "disgusted": {
        "label": "Neutral / Thoda Alag",
        "emoji": "😒",
        "gradient": "linear-gradient(135deg,#134e5e,#71b280)",
        "songs": {
            "trending": [
                {"title":"Bekhayali","artist":"Sachet Tandon","film":"Kabir Singh","year":"2019","youtube":"https://www.youtube.com/watch?v=k1pBnBbQGqk","thumb":"🍃"},
                {"title":"Tera Ban Jaunga","artist":"Akhil Sachdeva","film":"Kabir Singh","year":"2019","youtube":"https://www.youtube.com/watch?v=9KaRz5d2AjA","thumb":"🌿"},
                {"title":"Tujhse Bhi Zyada","artist":"Jubin Nautiyal","film":"Tadap","year":"2021","youtube":"https://www.youtube.com/watch?v=bY3ZQFR3W1A","thumb":"💚"},
            ],
            "90s": [
                {"title":"Aaj Mausam Bada Beimaan Hai","artist":"Lata Mangeshkar","film":"Loafer","year":"1973","youtube":"https://www.youtube.com/watch?v=yEv5D7rABU8","thumb":"☁️"},
                {"title":"Tere Bina Zindagi Se","artist":"Lata Mangeshkar","film":"Aandhi","year":"1975","youtube":"https://www.youtube.com/watch?v=0Fy4sDqRhYk","thumb":"🌧️"},
            ],
            "2000s": [
                {"title":"Jab Se Tere Naina","artist":"Udit Narayan","film":"Saawariya","year":"2007","youtube":"https://www.youtube.com/watch?v=Lch3L9eBxF4","thumb":"🌒"},
            ]
        }
    },
    "neutral": {
        "label": "Chill / Sukoon",
        "emoji": "😊",
        "gradient": "linear-gradient(135deg,#11998e,#38ef7d)",
        "songs": {
            "trending": [
                {"title":"Raataan Lambiyan","artist":"Jubin Nautiyal","film":"Shershaah","year":"2021","youtube":"https://www.youtube.com/watch?v=hZnFcVrxjpA","thumb":"🌌"},
                {"title":"Tera Fitoor","artist":"Arijit Singh","film":"Genius","year":"2018","youtube":"https://www.youtube.com/watch?v=OFMxo4VNJew","thumb":"🎵"},
                {"title":"Mann Bharrya","artist":"B Praak","film":"Qismat","year":"2018","youtube":"https://www.youtube.com/watch?v=SjoMvhbMUhk","thumb":"🌠"},
                {"title":"Heeriye","artist":"Arijit Singh","film":"Mission Raniganj","year":"2023","youtube":"https://www.youtube.com/watch?v=e8YBQQ3iuSs","thumb":"✨"},
            ],
            "90s": [
                {"title":"Ye Jo Des Hai Tera","artist":"A.R. Rahman","film":"Swades","year":"2004","youtube":"https://www.youtube.com/watch?v=Cjf9iExBoEU","thumb":"🇮🇳"},
                {"title":"Kal Ho Naa Ho","artist":"Sonu Nigam","film":"Kal Ho Naa Ho","year":"2003","youtube":"https://www.youtube.com/watch?v=0cDS2DTOJUU","thumb":"☀️"},
                {"title":"Tum Se Hi","artist":"Mohit Chauhan","film":"Jab We Met","year":"2007","youtube":"https://www.youtube.com/watch?v=pMWi5ZMknFM","thumb":"🌻"},
            ],
            "2000s": [
                {"title":"Kabhi Neem Neem","artist":"Sunidhi Chauhan","film":"Yuva","year":"2004","youtube":"https://www.youtube.com/watch?v=OwNchlcuWEA","thumb":"🍃"},
                {"title":"Mauja Hi Mauja","artist":"Mika Singh","film":"Jab We Met","year":"2007","youtube":"https://www.youtube.com/watch?v=Sj7fI50wuI0","thumb":"🎉"},
            ]
        }
    }
}

GROUP_ANTHEMS = [
    {"title":"Jai Ho","artist":"A.R. Rahman","film":"Slumdog Millionaire","year":"2008","youtube":"https://www.youtube.com/watch?v=Hy1YVFHJhJY","thumb":"🙌","mood":"Energetic"},
    {"title":"Rang De Basanti","artist":"A.R. Rahman","film":"Rang De Basanti","year":"2006","youtube":"https://www.youtube.com/watch?v=Nj3HWVbBfPk","thumb":"🎨","mood":"Patriotic"},
    {"title":"Naatu Naatu","artist":"Rahul Sipligunj","film":"RRR","year":"2022","youtube":"https://www.youtube.com/watch?v=OsU0CGZoV8E","thumb":"🥁","mood":"Dance"},
    {"title":"Sooraj Dooba Hai","artist":"Arijit Singh","film":"Roy","year":"2015","youtube":"https://www.youtube.com/watch?v=0WLNXZ-VFTU","thumb":"🌅","mood":"Romantic"},
    {"title":"Gallan Goodiyaan","artist":"Various","film":"Dil Dhadakne Do","year":"2015","youtube":"https://www.youtube.com/watch?v=0_ODFWZ_T8I","thumb":"🎊","mood":"Party"},
    {"title":"Balam Pichkari","artist":"Vishal Dadlani","film":"Yeh Jawaani Hai Deewani","year":"2013","youtube":"https://www.youtube.com/watch?v=mFWAlNcHQnk","thumb":"🎆","mood":"Fun"},
    {"title":"Tum Hi Ho","artist":"Arijit Singh","film":"Aashiqui 2","year":"2013","youtube":"https://www.youtube.com/watch?v=IJq0yyWug04","thumb":"❤️","mood":"Love"},
    {"title":"Ghoomar","artist":"Shreya Ghoshal","film":"Padmaavat","year":"2018","youtube":"https://www.youtube.com/watch?v=7PC_DEMKb-4","thumb":"👗","mood":"Cultural"},
]

# ── Routes ────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already registered!'})
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': 'Username already taken!'})
        pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        avatars = ['🎵','🎶','🎸','🎹','🎺','🎻','🥁','🎤','🎧','🎼']
        user = User(username=data['username'], email=data['email'], password=pw, avatar=random.choice(avatars))
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['username'] = user.username
        session['avatar'] = user.avatar
        return jsonify({'success': True, 'redirect': '/home'})
    return render_template('auth.html', mode='register')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            session['avatar'] = user.avatar
            return jsonify({'success': True, 'redirect': '/home'})
        return jsonify({'success': False, 'message': 'Invalid credentials!'})
    return render_template('auth.html', mode='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session.get('username'), avatar=session.get('avatar'))

@app.route('/detect')
def detect():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('detect.html', username=session.get('username'), avatar=session.get('avatar'))

@app.route('/api/songs/<emotion>')
def get_songs(emotion):
    era = request.args.get('era', 'trending')
    emotion = emotion.lower()
    if emotion not in MUSIC:
        emotion = 'neutral'
    data = MUSIC[emotion]
    songs = data['songs'].get(era, data['songs']['trending'])
    return jsonify({
        'emotion': emotion,
        'label': data['label'],
        'emoji': data['emoji'],
        'gradient': data['gradient'],
        'songs': songs,
        'era': era
    })

@app.route('/api/group_songs')
def group_songs():
    return jsonify({'songs': GROUP_ANTHEMS, 'title': '🎉 Group Anthems – Sab Ke Liye!'})

@app.route('/api/emotions')
def emotions():
    return jsonify({k: {'label': v['label'], 'emoji': v['emoji'], 'gradient': v['gradient']} for k, v in MUSIC.items()})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
