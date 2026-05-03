# API Mesa de Servicios - Laboratorios ITM

## Informacion del Taller

- Asignatura: Aplicaciones y Servicios Web
- Taller: Autenticacion JWT, autorizacion por scopes y flujo de tickets
- Proyecto: Mesa de servicios para laboratorios universitarios
- Version: 1.0.0

### Equipo de trabajo

- Juan Manuel Gallego Rojas
- Bryan Alejandro Ruiz Restrepo
- Santiago Arenas Herrera
---

## 1. Competencia, contenido e indicador de logro

| Competencia | Contenido tematico | Indicador de logro |
|---|---|---|
| Disenar y desarrollar servicios web seguros con FastAPI, PostgreSQL, JWT y scopes, aplicando reglas de autorizacion y control de acceso por rol. | Autenticacion JWT, autorizacion por scopes, proteccion de endpoints, persistencia con SQLAlchemy y PostgreSQL, reglas de negocio del flujo de tickets. | Implementar una API segura para crear, asignar, consultar, actualizar y finalizar tickets, segun rol, scope y relacion con el ticket. |

---

## 2. Fundamento teorico (resumen)

- La autenticacion valida la identidad del usuario.
- La autorizacion define que acciones puede ejecutar.
- JWT permite enviar identidad y permisos firmados en cada solicitud.
- Los scopes modelan permisos finos, por ejemplo `tickets:crear` o `tickets:finalizar`.
- FastAPI usa dependencias de seguridad para exigir token y scopes por endpoint.
- Ademas del scope, el sistema aplica reglas de negocio por relacion con el ticket y flujo de estados.
### Usuarios de prueba

| ID | Rol                    | Correo         | Contraseña |
|----|------------------------|----------------|------------|
| 5  | solicitante            | soli@test.com  | 12345678   |
| 6  | responsable_tecnico    | resp@test.com  | 12345678   |
| 3  | solicitante            | 13@example.com | prueba456  |
| 7  | auxiliar               | aux@test.com   | 12345678   |
| 13 | auxiliar               | aux1@test.com  | 12345678   |
| 8  | tecnico_especializado  | tec@test.com   | 12345678   |
| 1  | admin                  | 12@example.com | prueba123  |

### Observaciones

- Todos los usuarios fueron creados mediante el endpoint `POST /usuarios/` o `bootstrap-admin`.
- Las contraseñas están almacenadas como hash bcrypt en la base de datos.
- Cada usuario recibe sus scopes automáticamente según su rol al hacer login.

---

## 3. Objetivos

### Objetivo general

Desarrollar una API segura para la gestion de tickets de servicios en laboratorios universitarios usando FastAPI, PostgreSQL, JWT y scopes.

### Objetivos especificos

- Modelar usuarios, laboratorios, servicios y tickets.
- Implementar login con JWT.
- Definir roles y scopes.
- Proteger endpoints por scope.
- Aplicar reglas del flujo de estados del ticket.
- Validar visibilidad por rol y relacion con el ticket.
- Probar endpoints protegidos en Swagger.

---

## 4. Recursos requeridos

### Hardware y software

- Equipo con Windows o Linux.
- Python 3.10+.
- PostgreSQL.
- FastAPI, SQLAlchemy, Uvicorn.
- Git y GitHub.
- Visual Studio Code (recomendado).

### Dependencias Python requeridas

Minimo esperado en `requirements.txt`:

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart
- python-dotenv

---

## 5. Seguridad de la informacion

- No subir secretos al repositorio.
- Usar archivo `.env` local para variables sensibles.
- Mantener `.env` en `.gitignore`.
- No publicar credenciales de base de datos ni `SECRET_KEY` en capturas.
- Usar hash bcrypt para contrasenas.

Plantilla sugerida de `.env` local:

```env
DATABASE_URL=postgresql://USUARIO:PASSWORD@HOST:PUERTO/DB
SECRET_KEY=CAMBIAR_POR_UNA_CLAVE_LARGA_Y_SEGURA
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

---

## 6. Procedimiento de desarrollo

### Actividad 1: Configuracion inicial

1. Clonar repositorio.
2. Crear y activar entorno virtual.
3. Instalar dependencias.
4. Configurar `.env`.
5. Verificar `.gitignore`.

### Actividad 2: Comprension del problema

Roles del sistema:

- solicitante
- responsable_tecnico
- auxiliar
- tecnico_especializado
- admin

Scopes del sistema:

- tickets:crear
- tickets:ver_propios
- tickets:recibir
- tickets:asignar
- tickets:atender
- tickets:finalizar
- tickets:ver_todos
- usuarios:gestionar

Flujo de estados permitido:

1. solicitado -> recibido
2. recibido -> asignado
3. asignado -> en_proceso
4. en_proceso -> en_revision
5. en_revision -> terminado

### Actividad 3: Base de datos y modelos

- Definir modelos SQLAlchemy.
- Definir esquemas Pydantic.
- Crear endpoints base.

### Actividad 4: JWT y usuarios

- Login con `POST /auth/token`.
- Token con `sub`, `id_usuario`, `rol`, `scopes`, `exp`.
- Hash de contrasena y validacion de usuario activo.

### Actividad 5: Scopes y reglas de acceso

- Endpoint protegido por scopes.
- Regla adicional por rol/relacion con ticket.
- Rechazar accesos invalidos con 403.
- Rechazar transiciones invalidas con 422.

---

## 7. Endpoints implementados en este proyecto

### Autenticacion

- `POST /auth/token`

### Usuarios

- `POST /usuarios/bootstrap-admin` (solo primera inicializacion)
- `POST /usuarios/` (requiere `usuarios:gestionar`)
- `GET /usuarios/` (requiere `usuarios:gestionar`)
- `GET /usuarios/{id_usuario}` (requiere `usuarios:gestionar`)

### Laboratorios

- `POST /laboratorios/` (requiere `usuarios:gestionar`)
- `GET /laboratorios/` (requiere token)
- `GET /laboratorios/{id_laboratorio}` (requiere token)

### Servicios

- `POST /servicios/` (requiere `usuarios:gestionar`)
- `GET /servicios/` (requiere token)
- `GET /servicios/{id_servicio}` (requiere token)

### Tickets

- `POST /tickets/` (requiere `tickets:crear`)
- `GET /tickets/` (requiere `tickets:ver_propios`)
- `GET /tickets/{id_ticket}` (requiere `tickets:ver_propios` + visibilidad)
- `PATCH /tickets/{id_ticket}/estado` (requiere token + reglas de negocio)

---

## 8. Ejecucion del proyecto

### 8.1 Crear entorno e instalar dependencias

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 8.2 Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

### 8.3 Abrir documentacion

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

---

## 9. Matriz de evidencias

Colocar las imagenes en `docs/evidencias/` con los nombres sugeridos.

> Nota: Antes de capturar, ocultar o difuminar secretos/tokens completos.

### Evidencia 1 - solicitante crea ticket (permitido)

- Usuario: solicitante
- Accion: Crear ticket
- Resultado esperado: 200

![img.png](img.png)
![img_1.png](img_1.png)

### Evidencia 2 - solicitante intenta asignar ticket (denegado)

- Usuario: solicitante
- Accion: Asignar ticket
- Resultado esperado: 403

![img_6.png](img_6.png)
![img_7.png](img_7.png)

### Evidencia 3 - responsable recibe ticket (permitido)

- Usuario: responsable_tecnico
- Accion: solicitado -> recibido
- Resultado esperado: permitido

![img_4.png](img_4.png)
![img_5.png](img_5.png) 

### Evidencia 4 - responsable asigna ticket (permitido)

- Usuario: responsable_tecnico
- Accion: recibido -> asignado
- Resultado esperado: permitido

![img_8.png](img_8.png)
![img_9.png](img_9.png)

### Evidencia 5 - auxiliar pasa a en_proceso (solo si esta asignado)

- Usuario: auxiliar
- Accion: asignado -> en_proceso
- Resultado esperado: permitido solo si esta asignado

![img_10.png](img_10.png)
![img_11.png](img_11.png)

### Evidencia 6 - auxiliar intenta finalizar (denegado)

- Usuario: auxiliar
- Accion: finalizar ticket
- Resultado esperado: 403

![img_12.png](img_12.png)
![img_13.png](img_13.png)

### Evidencia 7 - tecnico especializado pasa a en_revision

- Usuario: tecnico_especializado
- Accion: en_proceso -> en_revision
- Resultado esperado: permitido solo si esta asignado
- Archivo sugerido: `docs/evidencias/07-tecnico-en-revision.png`

![img_31.png](img_31.png)
![img_32.png](img_32.png)

Espacio para observaciones:

### Evidencia 8 - responsable finaliza ticket

- Usuario: responsable_tecnico
- Accion: en_revision -> terminado
- Resultado esperado: permitido

![img_14.png](img_14.png)
![img_15.png](img_15.png)

### Evidencia 9 - solicitante intenta ver tickets de otros (denegado)

- Usuario: solicitante
- Accion: ver tickets de otros usuarios
- Resultado esperado: 403

![img_16.png](img_16.png)
![img_17.png](img_17.png)

### Evidencia 10 - admin ve todos los tickets

- Usuario: admin
- Accion: ver todos los tickets
- Resultado esperado: permitido

![img_18.png](img_18.png)
![img_19.png](img_19.png)

### Evidencia 11 - Login exitoso (JWT)

- Usuario: solicitante
- Accion: Autorizacion del token
- Resultado esperado: permitido

![img_20.png](img_20.png)
![img_21.png](img_21.png)

### Evidencia 12 - Uso de Authorize en Swagger

- Usuario: solicitante
- Accion: Logear como usuario autorizado
- Resultado esperado: permitido

![img_22.png](img_22.png)
![img_23.png](img_23.png)

### Evidencia 12 - Acceso sin token

- Usuario: solicitante
- Accion: Ejecutar la API sin autorizacion
- Resultado esperado: 401

![img_24.png](img_24.png)
![img_25.png](img_25.png)

### Evidencia 13 - Transición inválida

- Usuario: responsable_tecnico
- Accion: Cambiar estado de ticket a 'Terminado'
- Resultado esperado: 422

![img_26.png](img_26.png)
![img_27.png](img_27.png)

### Evidencia 13 - Usuario modifica ticket NO asignado

- Usuario: auxiliar
- Accion: Modificar ticket de auxiliar ajeno
- Resultado esperado: 403

![img_28.png](img_28.png)
![img_29.png](img_29.png)
---

## 10.   Checklist final de entrega

- [ ] Codigo fuente actualizado en repositorio GitHub.
- [ ] Base de datos configurada en el schema asignado.
- [ ] Modelos SQLAlchemy implementados.
- [ ] Esquemas Pydantic implementados.
- [ ] Endpoints funcionales en Swagger.
- [ ] JWT y scopes funcionando segun rol.
- [ ] Flujo de estados validado.
- [ ] 10 capturas de evidencia completadas.
- [ ] Sin secretos expuestos en README, capturas o commits.

---

## 12. Referencias

- FastAPI: https://fastapi.tiangolo.com
- OAuth2 scopes en FastAPI: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
- Pydantic: https://docs.pydantic.dev
- Python: https://docs.python.org
- python-jose: https://python-jose.readthedocs.io
- passlib: https://passlib.readthedocs.io

---

## 13. Nota para evaluacion

Este README se diseno para cumplir la guia del taller con:

- contexto teorico,
- objetivos,
- procedimiento,
- definicion de roles/scopes,
- flujo de estados,
- endpoints implementados,
- checklist,
- y espacios de evidencias listos para capturas.
