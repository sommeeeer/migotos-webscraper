from sqlalchemy import create_engine, select
from models import KittenPictureImage, CatImage

DB_FILE = "migotos.db"

engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

connection = engine.connect()


stmt = select(CatImage.src).union(select(KittenPictureImage.src))


result = connection.execute(stmt)

with open('images.txt', 'w') as f:
    for row in result:
        if 'migotos' not in row[0]:
            f.write(f'/old/{row[0]}\n')
        else:
            f.write(f'{row[0]}\n')

connection.close()
