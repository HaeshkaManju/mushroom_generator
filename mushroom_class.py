# mushroom_class
import sqlite3
import random

##############################################################################
# Database Management for Mushroom Info #
##############################################################################

dbname = 'C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\mushroom_data.db'

class MushroomDatabase:
    def __init__(self, dbname):
        print(f"Connecting to database: {dbname}")  # print out which database you're attempting to connect to
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")  
        print("Tables in the database:", self.cur.fetchall())  # print out all the table names in the database
        
    def get_single_option(self, tablename, id):
        self.cur.execute(f"SELECT * FROM {tablename} WHERE roll = ?", (id,))
        return self.cur.fetchone()

    def get_range_option(self, tablename, roll):
        self.cur.execute(f"SELECT * FROM {tablename} WHERE roll_min <= ? AND roll_max >= ?", (roll, roll))
        return self.cur.fetchone()
    
    def get_highest_roll(self, tablename):
        try:
            self.cur.execute(f"SELECT MAX(roll) FROM {tablename}")
            return self.cur.fetchone()[0]
        except sqlite3.OperationalError as e:
            print(f"Error executing SQL: {e}")
            raise

    def get_max_roll(self, tablename):
        try:
            self.cur.execute(f"SELECT MAX(roll_max) FROM {tablename};")
            return self.cur.fetchone()[0]
        except sqlite3.OperationalError as e:
            print(f"Error executing SQL: {e}")
            raise

##############################################################################
# Database Management for Mushroom Info #
##############################################################################

class Mushroom:
    def __init__(self, db):
        self.db = db

    def get_highest_roll(self, tablename):
        return self.db.get_highest_roll(tablename)  # use MushroomDatabase's method

    def get_max_roll(self, tablename):
        return self.db.get_max_roll(tablename)  # use MushroomDatabase's method
    
    def generate(self):
        # Have randomized #s ready to go for the DB calls.
        adjective_max_roll = self.get_highest_roll('adjective')
        noun_max_roll = self.get_highest_roll('noun')
        
        id_adjective = random.randint(1, adjective_max_roll)
        id_noun = random.randint(1, noun_max_roll)
        
        shape_max_roll = self.get_highest_roll('cap_shape')
        texture_max_roll = self.get_highest_roll('cap_texture')
        margin_max_roll = self.get_highest_roll('cap_margin')
        color_max_roll = self.get_highest_roll('color')
        stem_max_roll = self.get_highest_roll('stem')
        
        id_shape = random.randint(1, shape_max_roll)
        id_texture = random.randint(1, texture_max_roll)
        id_margin = random.randint(1, margin_max_roll)
        id_color = random.randint(1, color_max_roll)
        id_stem = random.randint(1, stem_max_roll)
        
        special_max_roll = self.get_highest_roll('special')
        growth_number_max_roll = self.get_max_roll('growth_number')
        growth_biome_max_roll = self.get_max_roll('growth_biome')
        property_max_roll = self.get_max_roll('property')
        mycelium_max_roll = self.get_max_roll('mycelium')
        
        id_special = random.randint(1, special_max_roll)
        id_growth_number = random.randint(1, growth_number_max_roll)
        id_growth_biome = random.randint(1, growth_biome_max_roll)
        id_property = random.randint(1, property_max_roll)
        id_mycelium = random.randint(1, mycelium_max_roll)
        # Single Option Calls
        self.adjective = self.db.get_single_option('adjective', id_adjective)
        self.noun = self.db.get_single_option('noun', id_noun)
        
        self.cap_shape = self.db.get_single_option('cap_shape', id_shape)
        self.cap_texture = self.db.get_single_option('cap_texture', id_texture)
        self.cap_margin = self.db.get_single_option('cap_margin', id_margin)
        self.color = self.db.get_single_option('color', id_color)
        self.stem = self.db.get_single_option('stem', id_stem)
        
        self.special = self.db.get_single_option('special', id_special)
        # Range Option Calls
        self.growth_number = self.db.get_range_option('growth_number', id_growth_number)
        self.growth_biome = self.db.get_range_option('growth_biome', id_growth_biome)
        self.property = self.db.get_range_option('property', id_property)
        self.mycelium = self.db.get_range_option('mycelium', id_mycelium)
        
    def __str__(self):
        return f"Name: {self.adjective} {self.noun}\n" \
               f"Description:\n" \
                f"- Cap Shape: {self.cap_shape}\n" \
                f"- Cap Texture: {self.cap_texture}\n" \
                f"- Cap Margin: {self.cap_margin}\n" \
                f"- Color: {self.color}\n" \
                f"- Stem: {self.stem}\n" \
               f"Special Properties: \n" \
                f"- Special: {self.special}\n" \
                f"- Growth Number: {self.growth_number}\n" \
                f"- Growth Biome: {self.growth_biome}\n" \
                f"- Property: {self.property}\n" \
                f"- Mycelium: {self.mycelium}\n"

    def export_description(self):
        desc_str = str(self)
        
        # Convert the description into markdown syntax
        desc_markdown = desc_str.replace('\n', '<br>')
        
        return desc_str, desc_markdown