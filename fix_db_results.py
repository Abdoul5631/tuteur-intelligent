import os, shutil, sqlite3, sys

proj = os.path.dirname(__file__)
db = os.path.join(proj, "db.sqlite3")
if not os.path.exists(db):
    print("db.sqlite3 introuvable"); sys.exit(1)

shutil.copy2(db, db + ".bak")
print("Backup créé:", db + ".bak")

conn = sqlite3.connect(db)
cur = conn.cursor()

try:
    refs = [r[0] for r in cur.execute("SELECT DISTINCT exercice_id FROM core_resultat").fetchall()]
    print("exercice_id référencés dans core_resultat:", refs)
except Exception as e:
    print("Erreur listing core_resultat:", e); conn.close(); sys.exit(1)

try:
    existing = [r[0] for r in cur.execute("SELECT id FROM core_exercice").fetchall()]
    print("exercice.id existants:", existing)
except Exception as e:
    print("Table core_exercice manquante :", e); conn.close(); sys.exit(1)

orphan_ids = [i for i in refs if i is not None and i not in existing]
if not orphan_ids:
    print("Aucun resultat orphelin trouvé.")
else:
    print("Orphan exercice_ids à supprimer des résultats:", orphan_ids)
    q = ",".join(str(int(i)) for i in orphan_ids)
    cur.execute(f"DELETE FROM core_resultat WHERE exercice_id IN ({q})")
    print("Lignes supprimées:", cur.rowcount)
    conn.commit()

conn.close()
print("Terminé. Lancez: python manage.py migrate")