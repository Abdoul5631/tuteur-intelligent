import sqlite3, os, sys
db = "db.sqlite3"
if not os.path.exists(db):
    print("db.sqlite3 introuvable"); sys.exit(1)
conn = sqlite3.connect(db)
cur = conn.cursor()
for t in ("core_resultat","core_exercice","core_lecon"):
    try:
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t} rows before:", n)
    except Exception as e:
        print(f"{t} unavailable:", e)
for q in ("DELETE FROM core_resultat","DELETE FROM core_exercice","DELETE FROM core_lecon"):
    try:
        cur.execute(q)
        print("Executed:", q)
    except Exception as e:
        print("Failed:", q, e)
conn.commit()
conn.close()
print("Terminé — maintenant: python manage.py migrate")