from datetime import datetime, timedelta
from prefect.schedules import IntervalSchedule

brt_pipeline_schedule = IntervalSchedule(
    start_date=datetime.utcnow(),
    end_date=datetime.utcnow() + timedelta(minutes=5),  # Para após 5 minutos
    interval=timedelta(minutes=1)
)