from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def data(self):
        data_1 = {i.name: getattr(self, i.name) for i in self.__table__.columns}
        return data_1






@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/random")
def random_cafe_1():
    all_cafe = db.session.query(Cafe).all()
    random_cafe=random.choice(all_cafe)

    print(all_cafe)
    print(random_cafe)



    return jsonify(cafe=random_cafe.data())

@app.route("/all")
def for_all():
    all_cafe = db.session.query(Cafe).all()

    print(all_cafe)
    return jsonify(cafe=[i.data()  for i in all_cafe])


@app.route("/search")
def for_search():
    get_args=request.args.get("loc")
    find_in_db=Cafe.query.filter_by(location=get_args).first()
    if find_in_db:
        return jsonify(cafe=find_in_db.data())
    else:
        return jsonify(error={"not found":"djedejedebd"})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_this(cafe_id):
    api_header=request.args.get("api_key")
    if api_header=="hola":
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted."}), 200
        else:
            # 404 = Resource not found
            return jsonify(error={"Unaurthorized": "Wrong APi key"}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403





@app.route("/add", methods=["POST"])
def post_new_cafe():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})




## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
