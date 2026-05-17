import os

try:
    import pyodbc # pyright: ignore[reportMissingImports]
except ImportError:
    pyodbc = None

try:
    import flask # type: ignore
except ImportError:
    raise RuntimeError("Flask is not installed or could not be imported. Install it with: pip install flask")

app = flask.Flask(__name__)

# Configuración de la base de datos desde variables de entorno
server = "servidores.database.windows.net"
database = "proyecto_tareas"
username = "Servidor"
password = "Jroman7108"

driver = "{ODBC Driver 18 for SQL Server}"


if pyodbc is None:
    raise RuntimeError("pyodbc is not installed or could not be imported. Install it with: pip install pyodbc")

# Cadena de conexión global
CONNECTION_STRING = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_db():
    print(CONNECTION_STRING)
    conn = pyodbc.connect(CONNECTION_STRING)
    return conn
  


@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    tasks = cursor.fetchall()
    conn.close() # Siempre cierra la conexión al terminar la petición
    return flask.render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = flask.request.form.get("title")
    if title:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, 0))
        conn.commit()
        conn.close()
    return flask.redirect("/")

@app.route("/done/<int:task_id>")
def mark_done(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return flask.redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return flask.redirect("/")

if __name__ == "__main__":
    # Asegúrate de reiniciar tu terminal por completo antes de ejecutar
    app.run(debug=True)

