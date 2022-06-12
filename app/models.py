from app import db, login 
from flask_login import UserMixin 
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


user_poke = db.Table("user_poke",
    db.Column("poke_name", db.Integer, db.ForeignKey("pokemon.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on= db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    pokemen = db.relationship(
        "Pokemon",
        secondary=user_poke,
        backref="card_holders",
        lazy="dynamic" 
        )

    
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self,data):
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=self.hash_password(data['password'])
        self.icon = data['icon']

    def save(self):
        db.session.add(self) 
        db.session.commit()

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/croodles/{self.icon}.svg'


    def check_user_poke(self, poke_check):
        return poke_check in self.pokemon

    def add_poke(self, poke_add):
        if not self.check_user_poke(poke_add):
            self.pokemon.append(poke_add)
            db.session.commit()
    
    def release_poke(self, delete_poke):
        if self.check_user_poke(delete_poke): 
            self.pokemon.remove(delete_poke)
            db.session.commit()

    def collected_poke(self):
        pokemen = Pokemon.query.join(user_poke, (Pokemon.user_id ==user_poke.c.poke_name)).filter(user_poke.c.user_id == self.id)
        user_pokes = Pokemon.query.filter_by(user_id = self.id)
        collected_pokes = pokemen.union(user_pokes)
        return collected_pokes




@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String(100))
    attack_base_stat = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    defense_base_stat= db.Column(db.Integer)
    ability_name=db.Column(db.String(150))
    base_experience=db.Column(db.Integer)
    front_shiny=db.Column(db.String(150))
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Pokemon: {self.id} | Body: {self.poke_name}'

    def from_dict(self,poke_dict):
        self.poke_name=poke_dict["poke_name"]
        self.attack_base_stat=poke_dict["attack_base_stat"]
        self.hp_base_stat=poke_dict["hp_base_stat"]
        self.defense_base_stat=poke_dict["defense_base_stat"]
        self.ability_name=poke_dict["ability_name"]
        self.base_experience=poke_dict["base_experience"]
        self.front_shiny=poke_dict["front_shiny"]
    #poke_dict={
                #     "poke_name":poke['name'],
                #     "attack_base_stat":poke ["stats"][1]["base_stat"],
                #     "hp_base_stat": poke["stats"][0]["base_stat"],
                #     "defense_base_stat": poke["stats"][2]["base_stat"],
                #     "front_shiny": poke["sprites"]["front_shiny"],
                #     "ability_name": poke["abilities"][0]["ability"]["name"],
                #     "base_experience": poke["base_experience"],
                # }
    def to_dict(self):
        data={
            'id':self.id,
            'poke_name': self.poke_name,
            'attack_base_stat': self.attack_base_stat,
            'hp_base_stat': self.hp_base_stat,
            'defense_base_stat':self.defense_base_stat,
            'ability_name': self.ability_name,
            'base_experience': self.base_experience,
            'front_shiny': self.front_shiny
        }
        return data 

    def save(self):
        db.session.add(self)
        db.session.commit()
