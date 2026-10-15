# Migration-Toolkit
Описание: миграции 1С: обновление типовых, переход между версиями платформы, миграция данных между базами, ETL.
# Migration Toolkit для 1С

Инструменты миграции 1С:
- Проверка совместимости версий платформы
- Миграция данных между базами (mapping YAML)
- ETL pipeline (extract/transform/load)
- Резервное копирование и восстановление

## Запуск
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
pytest -v
```
