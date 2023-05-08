
from apps import db
from apps.projects.models import ProjectsDetails


class projectsController:

    @staticmethod
    def getMaxPhase(project_id: int, tableName: object) -> int:
        # Получить запись с максимальным значением поля "phase" для заданного "project_id"
        max_phase_record = db.session.query(tableName).filter_by(project_id=project_id).order_by(tableName.phase.desc()).first()

        if max_phase_record:
            # Вернуть JSON-объект с данными найденной записи
            return max_phase_record.phase
        else:
            # если нет записей возвращаю 0, и будет записана единица
            return 0
