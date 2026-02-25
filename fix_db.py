import os, shutil, sqlite3, sys

proj = os.path.dirname(__file__)
db = os.path.join(proj, "db.sqlite3")
if not os.path.exists(db):
    print("db.sqlite3 introuvable dans le dossier du projet."); sys.exit(1)

# backup
shutil.copy2(db, db + ".bak")
print("Backup créé:", db + ".bak")

conn = sqlite3.connect(db)
cur = conn.cursor()

try:
    refs = [r[0] for r in cur.execute("SELECT DISTINCT matiere_id FROM core_exercice").fetchall()]
    print("matiere_id référencées:", refs)
except Exception as e:
    print("Erreur listing core_exercice:", e)
    conn.close()
    sys.exit(1)

try:
    existing = [r[0] for r in cur.execute("SELECT id FROM core_matiere").fetchall()]
    print("matiere.id existantes:", existing)
except Exception as e:
    print("Table core_matiere manquante :", e)
    conn.close()
    sys.exit(1)

orphan_ids = [i for i in refs if i is not None and i not in existing]
if not orphan_ids:
    print("Aucun exercice orphelin.")
else:
    print("Orphan matiere_ids:", orphan_ids)
    q = ",".join(str(int(i)) for i in orphan_ids)
    cur.execute(f"DELETE FROM core_exercice WHERE matiere_id IN ({q})")
    print("Lignes supprimées:", cur.rowcount)
    conn.commit()

conn.close()
print("Terminé. Lancez: python manage.py migrate")