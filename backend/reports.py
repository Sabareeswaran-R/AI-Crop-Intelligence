from io import BytesIO, StringIO
import csv

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import PredictionHistory, Farmer, Farm

router = APIRouter(tags=["Reports & Downloads"])


def get_prediction_rows(db: Session):
    rows = (
        db.query(PredictionHistory, Farmer, Farm)
        .join(Farmer, PredictionHistory.farmer_id == Farmer.id)
        .join(Farm, PredictionHistory.farm_id == Farm.id)
        .order_by(PredictionHistory.id.desc())
        .all()
    )

    data = []
    for prediction, farmer, farm in rows:
        data.append({
            "Prediction ID": prediction.id,
            "Farmer ID": prediction.farmer_id,
            "Farmer Name": farmer.name,
            "Farm ID": prediction.farm_id,
            "Farm Name": farm.farm_name,
            "Crop": prediction.crop,
            "Crop Year": prediction.crop_year,
            "Season": prediction.season,
            "State": prediction.state,
            "Area": prediction.area,
            "Rainfall (mm)": prediction.rainfall,
            "Fertilizer": prediction.fertilizer,
            "Pesticide": prediction.pesticide,
            "Predicted Yield (t/ha)": prediction.predicted_yield,
            "Created At": prediction.created_at.isoformat() if prediction.created_at else "",
        })
    return data


@router.get("/reports/predictions/csv")
def download_predictions_csv(db: Session = Depends(get_db)):
    data = get_prediction_rows(db)

    output = StringIO()
    headers = list(data[0].keys()) if data else [
        "Prediction ID", "Farmer ID", "Farmer Name", "Farm ID", "Farm Name",
        "Crop", "Crop Year", "Season", "State", "Area", "Rainfall (mm)",
        "Fertilizer", "Pesticide", "Predicted Yield (t/ha)", "Created At"
    ]

    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

    content = output.getvalue().encode("utf-8-sig")

    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": "attachment; filename=crop_prediction_report.csv"
        },
    )


@router.get("/reports/predictions/excel")
def download_predictions_excel(db: Session = Depends(get_db)):
    data = get_prediction_rows(db)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Prediction Report"

    headers = list(data[0].keys()) if data else [
        "Prediction ID", "Farmer ID", "Farmer Name", "Farm ID", "Farm Name",
        "Crop", "Crop Year", "Season", "State", "Area", "Rainfall (mm)",
        "Fertilizer", "Pesticide", "Predicted Yield (t/ha)", "Created At"
    ]

    sheet.append(headers)
    for item in data:
        sheet.append([item.get(header, "") for header in headers])

    for cell in sheet[1]:
        cell.font = cell.font.copy(bold=True)

    for column_cells in sheet.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            value = "" if cell.value is None else str(cell.value)
            max_length = max(max_length, len(value))
        sheet.column_dimensions[column_letter].width = min(max(max_length + 2, 12), 35)

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=crop_prediction_report.xlsx"
        },
    )


@router.get("/reports/predictions/json")
def download_predictions_json(db: Session = Depends(get_db)):
    return {
        "status": "success",
        "count": len(get_prediction_rows(db)),
        "predictions": get_prediction_rows(db),
    }
