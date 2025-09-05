from werkzeug.security import generate_password_hash, check_password_hash

DEFAULT_METHOD = "pbkdf2:sha256:260000"
DEFAULT_SALT_LENGTH = 16

class Hashed:
    """
    Wrapper para armazenar e verificar senhas com segurança.
    Internamente guarda apenas o hash.
    """

    def __init__(self, value: str, already_hashed: bool = False,
                 method: str = DEFAULT_METHOD, salt_length: int = DEFAULT_SALT_LENGTH):
        if already_hashed:
            # já é um hash válido
            self._hash = value
        else:
            # gera hash a partir da senha em texto
            self._hash = generate_password_hash(
                value, method=method, salt_length=salt_length
            )

    def check(self, candidate: str) -> bool:
        """Verifica se a senha candidata confere com o hash."""
        return check_password_hash(self._hash, candidate)

    def __str__(self):
        return self._hash

    def __repr__(self):
        return f"HashedPassword('<hidden>')"
