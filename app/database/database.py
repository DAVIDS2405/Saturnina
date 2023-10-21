from surrealdb import Surreal

async def Connection():
    conn = None  # Inicializa la variable de conexión
    try:
        conn = Surreal("http://localhost:8000")
        await conn.connect()
        await conn.signin({"user": "root", "pass": "root"})
        await conn.use("test", "test")
        print("Conexión lista", str(conn._validate_connection))
    except Exception as e:
        print("Ocurrió un error con surreal:", str(e))
    
        
