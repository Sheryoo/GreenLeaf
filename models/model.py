from models.user import create_connection


def create_model_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    predictions TEXT NOT NULL,
    confidence TEXT NOT NULL,
    image TEXT NOT NULL,
    discription TEXT NOT NULL,
    temperature TEXT NOT NULL,
    sunlight TEXT NOT NULL,
    watering TEXT NOT NULL,
    userEmail INTEGER NOT NULL,
    FOREIGN KEY(userEmail) REFERENCES users(email)
    )
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("Model table created successfully")
    except Exception as e:
        print(e)
        print("Error creating model table")


def add_model_data(predictions, confidence, image, discription, temperature, sunlight, watering, userEmail):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO models (predictions, confidence, image, discription, temperature, sunlight, watering, userEmail) VALUES (?,?,?,?,?,?,?,?)",
                   (predictions, confidence, image, discription, temperature, sunlight, watering, userEmail))
    conn.commit()
    cursor.close()
    conn.close()