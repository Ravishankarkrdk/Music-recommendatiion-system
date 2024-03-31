from flask import Flask, request, render_template
import pickle

# flask app
app = Flask(__name__)

# loading models
try:
    with open('df.pkl', 'rb') as f:
        df = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
except Exception as e:
    print("list loading pickle files:", e)

def recommendation(song_df):
    idx = df[df['Song-Name'] == song_df].index[0]
    distance = sorted(list(enumerate(similarity[0])), reverse=False, key=lambda x: x[1])
    songs = []
    for i in distance[1:10]:
        songs.append(df.iloc[i[0]]['Song-Name'])
    return songs


# path
@app.route('/')
def index():
    try:
        names = df['Song-Name'].to_list()
        return render_template('index.html', name=names)
    except Exception as e:
        print("Error in index route:", e)
        return "An error occurred while loading data."

@app.route('/recom', methods=['POST'])
def mysong():
    try:
        user_song = request.form['names']
        songs = recommendation(user_song)
        return render_template('index.html', songs=songs)
    except Exception as e:
        print("list of mysong route:", e)
        return

# python
if __name__ == "__main__":
    app.run(debug=True)
