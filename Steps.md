1. Project Structure : 
    - Network-Data,networksecurity,notebooks,venv,requirements.txt,.env,.gitignore

2. `setup.py`
3. `networksecurity/logging/logger.py`
4. `networksecurity/exception/exception.py`
5. Data - Ingestion Pipeline Building : `constant(training_pipeline/__init__) -> entity(config_entity,artifact_entity) -> components(data_ingestion.py)`.
6. Data - Validation Pipeline Building : `constant(training_pipeline/__init__),utils/main_utils/utils.py,data_schema/schema.yaml -> entity(config_entity,artifact_entity) -> components(data_validation.py)`.
7. Data - Transformation Pipeline Building : `constant(training_pipeline/__init__),utils/main_utils/utils.py -> entity(config_entity,artifact_entity) -> components(data_transformation.py)`.
8. Model - Trainer : 
