# app/utils/utils.py
from datetime import datetime
from app import db
from ..models.bitacora_model import Bitacora
from flask import request

def registrar_en_bitacora(usuario_codigo: int, accion: str, descripcion: str = None):
    """Registra una acción realizada por un usuario en la bitácora."""
    ahora = datetime.now()
    nueva_bitacora = Bitacora(
        usuario_codigo=usuario_codigo,
        accion=accion,
        fecha=ahora.date(),
        hora=ahora.time(),
        descripcion=descripcion,
        ip=obtener_ip_cliente()
    )
    db.session.add(nueva_bitacora)
    db.session.commit()
    


def obtener_ip_cliente():
    if request.headers.get('X-Forwarded-For'):
        # Si está detrás de un proxy o balanceador
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    return ip