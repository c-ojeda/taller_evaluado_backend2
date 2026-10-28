from app.shared.database import get_connection
from app.students.students_schemas import Student
import psycopg 


class StudentsRepository:
    _SELECT = '''
        SELECT id, name, username, email, age, "createdAt", "updatedAt"
        FROM students
    '''

    @staticmethod
    def _to_student(row: tuple) -> Student:
        return Student(
            id=str(row[0]),
            name=row[1],
            username=row[2],
            email=row[3],
            age=row[4],
            createdAt=row[5],
            updatedAt=row[6],
        )

    def find_all(self) -> list[Student]:
        with get_connection() as connection:
            rows = connection.execute(self._SELECT).fetchall()
        return [self._to_student(row) for row in rows]

    def find_by_id(self, student_id: str) -> Student | None:
        with get_connection() as connection:
            row = connection.execute(
                f"{self._SELECT} WHERE id = %s", (student_id,)
            ).fetchone()
        return self._to_student(row) if row else None

    def find_by_email(self, email: str) -> Student | None:
        with get_connection() as connection:
            row = connection.execute(
                f"{self._SELECT} WHERE email = %s", (email,)
            ).fetchone()
        return self._to_student(row) if row else None

    def find_by_username(self, username: str) -> Student | None:
        with get_connection() as connection:
            row = connection.execute(
                f"{self._SELECT} WHERE username = %s", (username,)
            ).fetchone()
        return self._to_student(row) if row else None

    def save(self, student: Student) -> Student:
        query = '''
            INSERT INTO students (id, name, username, email, age, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                username = EXCLUDED.username,
                email = EXCLUDED.email,
                age = EXCLUDED.age,
                "updatedAt" = EXCLUDED."updatedAt"
            RETURNING id, name, username, email, age, "createdAt", "updatedAt"
        '''
        values = (
            student.id,
            student.name,
            student.username,
            str(student.email),
            student.age,
            student.createdAt,
            student.updatedAt,
        )
        with get_connection() as connection:
            row = connection.execute(query, values).fetchone()
        return self._to_student(row)

    def delete(self, student_id: str) -> None:
        with get_connection() as connection:
            connection.execute("DELETE FROM students WHERE id = %s", (student_id,))

    def save_tx(self, student: Student, connection: psycopg.Connection) -> Student:
        """Guarda un estudiante utilizando una conexión existente (para transacciones)."""
        query = '''
            INSERT INTO students (id, name, username, email, age, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                username = EXCLUDED.username,
                email = EXCLUDED.email,
                age = EXCLUDED.age,
                "updatedAt" = EXCLUDED."updatedAt"
            RETURNING id, name, username, email, age, "createdAt", "updatedAt"
        '''
        values = (
            student.id,
            student.name,
            student.username,
            str(student.email),
            student.age,
            student.createdAt,
            student.updatedAt,
        )
        row = connection.execute(query, values).fetchone()
        return self._to_student(row)
