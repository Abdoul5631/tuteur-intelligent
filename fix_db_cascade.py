import os, shutil, sqlite3, sys

proj = os.path.dirname(__file__)
db = os.path.join(proj, "db.sqlite3")
if not os.path.exists(db):
    print("db.sqlite3 introuvable"); sys.exit(1)

# backup
shutil.copy2(db, db + ".bak")
print("Backup créé:", db + ".bak")

conn = sqlite3.connect(db)
cur = conn.cursor()

def ids(table, col):
    try:
        return [r[0] for r in cur.execute(f"SELECT DISTINCT {col} FROM {table}").fetchall()]
    except Exception as e:
        print(f"Impossible de lister {table}.{col}:", e)
        return []

# existant
matiere_exist = [r[0] for r in cur.execute("SELECT id FROM core_matiere").fetchall()] if any(t[0]=='core_matiere' for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")) else []
print("matiere.id existantes:", matiere_exist)

# référencés
lecon_matiere_refs = ids("core_lecon", "matiere_id")
exercice_lecon_refs = ids("core_exercice", "lecon_id")
resultat_exercice_refs = ids("core_resultat", "exercice_id")

print("core_lecon.matiere_id référencés:", lecon_matiere_refs)
print("core_exercice.lecon_id référencés:", exercice_lecon_refs)
print("core_resultat.exercice_id référencés:", resultat_exercice_refs)

# supprimer lecons dont matiere_id n'existe pas
orphan_lecons = [i for i in lecon_matiere_refs if i is not None and i not in matiere_exist]
if orphan_lecons:
    q = ",".join(str(int(i)) for i in orphan_lecons)
    cur.execute(f"DELETE FROM core_lecon WHERE matiere_id IN ({q})")
    print("Leçons supprimées (matiere manquante):", cur.rowcount)
    conn.commit()
else:
    print("Aucune leçon orpheline par matiere.")

# recalculer lecon ids existants et supprimer exercices orphelins
lecon_exist = [r[0] for r in cur.execute("SELECT id FROM core_lecon").fetchall()]
orphan_exercices = [i for i in exercice_lecon_refs if i is not None and i not in lecon_exist]
if orphan_exercices:
    q = ",".join(str(int(i)) for i in orphan_exercices)
    cur.execute(f"DELETE FROM core_exercice WHERE lecon_id IN ({q})")
    print("Exercices supprimés (leçon manquante):", cur.rowcount)
    conn.commit()
else:
    print("Aucun exercice orphelin par leçon.")

# recalculer exercice ids existants et supprimer resultats orphelins
exercice_exist = [r[0] for r in cur.execute("SELECT id FROM core_exercice").fetchall()]
orphan_resultats = [i for i in resultat_exercice_refs if i is not None and i not in exercice_exist]
if orphan_resultats:
    q = ",".join(str(int(i)) for i in orphan_resultats)
    cur.execute(f"DELETE FROM core_resultat WHERE exercice_id IN ({q})")
    print("Résultats supprimés (exercice manquant):", cur.rowcount)
    conn.commit()
else:
    print("Aucun résultat orphelin par exercice.")

conn.close()
print("Terminé. Relancer: python manage.py migrate")