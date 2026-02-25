import sqlite3, os, sys
db = "db.sqlite3"
if not os.path.exists(db):
    print("db.sqlite3 introuvable"); sys.exit(1)
conn = sqlite3.connect(db)
cur = conn.cursor()
print("Tables:", [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])
def show(name):
    try:
        cols = list(cur.execute(f"PRAGMA table_info({name})"))
        print(f"\nPRAGMA table_info({name}):", cols)
        try:
            print(f"Exemples {name} (limit 5):", list(cur.execute(f"SELECT * FROM {name} LIMIT 5")))
        except Exception as e:
            print(f"Can't SELECT from {name}:", e)
    except Exception as e:
        print(f"{name} absent or error:", e)
for t in ("core_exercice","core_matiere","core_utilisateur"):
    show(t)
conn.close()