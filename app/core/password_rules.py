def check_password_strength(password: str) -> str:
    rules = {
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(c in "@$!%*?&." for c in password)
    }

    for rule, passed in rules.items():
        if not passed:
            raise ValueError(f"Password must contain at least one {rule}")

    return password


#print(">>> CARGANDO password_rules.py")