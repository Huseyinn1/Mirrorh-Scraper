from database import engine, Data
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
app = Flask(__name__)

Session = sessionmaker(bind=engine)


"""@app.route("/data", methods=["POST"])
def add_data():
    data = request.get_json()
    data_leaked = Data(
        attacker=data.get('attacker'),
        country=data.get('country'),
        url=data.get('url'),
        ip=data.get('ip'),
        date=data.get('date')
    )
    try:
        # Session nesnesini başlat
        session = Session()
        session.add(data_leaked)
        session.commit()
        # İşlem tamamlandıktan sonra session'ı kapat
        session.close()
        return jsonify({"message": f"Post with title '{data_leaked.url}' added successfully!"})
    except Exception as e:
        # Hata durumunda session'ı kapat ve hatayı döndür
        session.close()
        return jsonify({"error": str(e)}), 500"""

@app.route("/")
def index():
    return "Welcome to the dark side!"

@app.route("/data/<int:data_id>", methods=["GET"])
def get_data(data_id):
    with Session() as session:
        post = session.query(Data).filter_by(id=data_id).first()
    if post:
        post_data = {
            "id": post.id,
            "attacker": post.attacker,
            "country": post.country,
            "url": post.url,
            "ip": post.ip,
            "date":post.date
            
        }
        return jsonify(post_data)
    else:
        return jsonify({"message": f"Post with ID '{data_id}' not found!"})
    


@app.route("/data", methods=["GET"])
def get_all_posts():
    with Session() as session:
        posts = session.query(Data).all()
    post_list = []
    for post in posts:
        post_data = {
          "id": post.id,
            "attacker": post.attacker,
            "country": post.country,
            "url": post.url,
            "ip": post.ip,
            "date":post.date
        }
        post_list.append(post_data)
    return jsonify(post_list)




@app.route("/search", methods=["GET"])
def search_data():
    search_query = request.args.get('query')
    if search_query:
        with Session() as session:
            search_results = session.query(Data).filter(
                or_(
                    Data.attacker.like(f'%{search_query}%'),
                    Data.country.like(f'%{search_query}%'),
                    Data.url.like(f'%{search_query}%'),
                    Data.ip.like(f'%{search_query}%'),
                    Data.date.like(f'%{search_query}%')
                )
            ).all()

            # Arama sonuçlarını JSON formatında döndür
            results_list = []
            for result in search_results:
                result_data = {
                    "id": result.id,
                    "attacker": result.attacker,
                    "country": result.country,
                    "url": result.url,
                    "ip": result.ip,
                    "date": result.date
                }
                results_list.append(result_data)
                
            return jsonify(results_list)
    else:
        return jsonify({"message": "No search query provided!"}), 400


@app.route("/data/<int:data_id>", methods=["DELETE"])
def delete_data(data_id):
    try:
        session = Session()

        # Veritabanından silinecek veriyi bul
        data_to_delete = session.query(Data).filter_by(id=data_id).first()

        if data_to_delete:
            session.delete(data_to_delete)
            session.commit()
            session.close()
            return jsonify({"message": f"Data with ID {data_id} deleted successfully!"}), 200
        
        else:
            return jsonify({"error": f"Data with ID {data_id} not found!"}), 404
        
    except Exception as e:
        session.close()
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)