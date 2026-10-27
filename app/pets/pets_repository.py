from app.pets.pets_schemas import Pet
from app.shared.database import get_connection


class PetsRepository:
    @staticmethod
    def _to_pet(row: tuple) -> Pet:
        return Pet(
            id=str(row[0]),
            studentId=str(row[1]),
            name=row[2],
            species=row[3],
            age=row[4],
            createdAt=row[5],
            updatedAt=row[6],
        )

    def find_all_by_student(self, student_id: str) -> list[Pet]:
        query = '''
            SELECT id, "studentId", name, species, age, "createdAt", "updatedAt"
            FROM pets
            WHERE "studentId" = %s
        '''
        with get_connection() as connection:
            rows = connection.execute(query, (student_id,)).fetchall()
        return [self._to_pet(row) for row in rows]

    def find_by_id(self, pet_id: str) -> Pet | None:
        query = '''
            SELECT id, "studentId", name, species, age, "createdAt", "updatedAt"
            FROM pets
            WHERE id = %s
        '''
        with get_connection() as connection:
            row = connection.execute(query, (pet_id,)).fetchone()
        return self._to_pet(row) if row else None

    def find_by_student_and_name(self, student_id: str, name: str) -> Pet | None:
        query = '''
            SELECT id, "studentId", name, species, age, "createdAt", "updatedAt"
            FROM pets
            WHERE "studentId" = %s AND name = %s
        '''
        with get_connection() as connection:
            row = connection.execute(query, (student_id, name)).fetchone()
        return self._to_pet(row) if row else None

    def save(self, pet: Pet) -> Pet:
        query = '''
            INSERT INTO pets
                (id, "studentId", name, species, age, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                "studentId" = EXCLUDED."studentId",
                name = EXCLUDED.name,
                species = EXCLUDED.species,
                age = EXCLUDED.age,
                "updatedAt" = EXCLUDED."updatedAt"
            RETURNING id, "studentId", name, species, age, "createdAt", "updatedAt"
        '''
        values = (
            pet.id,
            pet.studentId,
            pet.name,
            pet.species,
            pet.age,
            pet.createdAt,
            pet.updatedAt,
        )
        with get_connection() as connection:
            row = connection.execute(query, values).fetchone()
        return self._to_pet(row)

    def delete(self, pet_id: str) -> None:
        with get_connection() as connection:
            connection.execute("DELETE FROM pets WHERE id = %s", (pet_id,))

    def delete_by_student(self, student_id: str) -> None:
        with get_connection() as connection:
            connection.execute(
                'DELETE FROM pets WHERE "studentId" = %s', (student_id,)
            )
