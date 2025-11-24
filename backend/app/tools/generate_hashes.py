# app/tools/generate_hashes.py

from app.core.security import get_password_hash

passwords = {
    "hash_lh123": "laura.h",
    "hash_pm123": "pedro.m",
    "hash_as123": "ana.s",
    "hash_lr123": "luis.r",
    "hash_sg123": "sofia.g",
    "hash_jp123": "juan.p",
    "hash_mg123": "maria.g",
    "hash_cl123": "carlos.l",
    "hash_cm123": "carlos.m",
    "hash_so123": "sandra.o",
    "hash_pr123": "paula.r",
    "hash_ac123": "andres.c",
}

for plain, user in passwords.items():
    h = get_password_hash(plain)
    print(f"{user}: {plain} -> {h}")
