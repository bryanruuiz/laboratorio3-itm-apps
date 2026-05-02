from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate
from app.security.auth import get_password_hash

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()


def count_usuarios(db: Session) -> int:
    return db.query(Usuario).count()

def get_usuario(db: Session, id_usuario: int):
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

def get_usuario_by_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    # Encriptamos la contraseña aquí
    hashed_password = get_password_hash(usuario.password)
    rol_valor = usuario.rol.value if hasattr(usuario.rol, "value") else usuario.rol
    
    db_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password_hash=hashed_password,
        rol=rol_valor,
        activo=usuario.activo
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario