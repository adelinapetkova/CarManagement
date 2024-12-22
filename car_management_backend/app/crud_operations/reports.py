from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from car_management_backend.app.models.maintenance import MaintenanceRequest


def get_requests_per_month(db: Session, garage_id: int, start_month: str, end_month: str):
    """ Get the number of maintenance requests per month for a given garage """
    start_date = datetime.strptime(start_month, "%Y-%m").date()
    end_date = datetime.strptime(end_month, "%Y-%m").date()

    # Get all months between start_date and end_date
    all_months = []
    current_date = start_date
    while current_date <= end_date:
        all_months.append(current_date.strftime("%Y-%m"))
        current_date += timedelta(days=31)
        current_date = current_date.replace(day=1)

    results = (
        db.query(
            func.strftime("%Y-%m", MaintenanceRequest.scheduled_date).label("month"),
            func.count(MaintenanceRequest.id).label("count")
        )
        .filter(
            MaintenanceRequest.garage_id == garage_id,
            func.date(MaintenanceRequest.scheduled_date) >= start_date,
            func.date(MaintenanceRequest.scheduled_date) <= end_date
        )
        .group_by(func.strftime("%Y-%m", MaintenanceRequest.scheduled_date))
        .order_by(func.strftime("%Y-%m", MaintenanceRequest.scheduled_date))
        .all()
    )

    monthly_counts = {row.month: row.count for row in results}

    # Set count for all months of the period including the ones where the requests are 0
    monthly_requests = {}
    for month in all_months:
        monthly_requests[month] = monthly_counts.get(month, 0)

    return dict(monthly_requests)



