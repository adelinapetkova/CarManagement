import calendar
from fastapi import HTTPException
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from car_management_backend.app.models.maintenance import MaintenanceRequest
from car_management_backend.app.models.garage import Garage


def get_requests_per_month(db: Session, garage_id: int, start_month: str, end_month: str):
    """ Get the number of maintenance requests per month for a given garage """
    start_date = datetime.strptime(start_month, "%Y-%m").date()
    end_date = datetime.strptime(end_month, "%Y-%m").date()

    # Get the last day of the month
    last_day = calendar.monthrange(end_date.year, end_date.month)[1]
    end_date = end_date.replace(day=last_day)

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


def get_daily_availability_report(db: Session, garage_id: int, start_date: str, end_date: str):
    """ Get the daily availability for a given garage """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    # Get all dates between start_date and end_date
    all_dates = []
    current_date = start_date
    while current_date <= end_date:
        all_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    results = (
        db.query(
            MaintenanceRequest.scheduled_date.label("date"),
            func.count(MaintenanceRequest.id).label("requests")
        )
            .filter(
            MaintenanceRequest.garage_id == garage_id,
            MaintenanceRequest.scheduled_date.between(start_date, end_date)
        )
            .group_by(MaintenanceRequest.scheduled_date)
            .all()
    )

    requests_dict = {row.date: row.requests for row in results}

    daily_report = []
    for date in all_dates:
        requests = requests_dict.get(date, 0)
        available_capacity = garage.capacity - requests
        daily_report.append({
            "date": date,
            "requests": requests,
            "availableCapacity": available_capacity
        })

    return daily_report
