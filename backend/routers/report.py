from __future__ import annotations
from fastapi import APIRouter, Header, HTTPException, Response
from fastapi.responses import JSONResponse
from datetime import datetime
import io
import logging

from models.schemas import NatalRequest
from services.astrology_service import AstrologyService

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except Exception:
    letter = None
    canvas = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Simple API key check for premium access; in production replace with real auth
PREMIUM_API_KEYS = {"demo-premium-key"}


@router.post("/report")
async def generate_report(request: NatalRequest, x_api_key: str | None = Header(default=None)):
    if x_api_key is None or x_api_key not in PREMIUM_API_KEYS:
        raise HTTPException(status_code=403, detail="Premium API key required")

    service = AstrologyService()

    # Attempt to build natal chart and v2 response
    try:
        # Resolve lat/lon via geocoding if needed (astrology_service may do this internally)
        chart = service.build_natal_chart(request.person, lat=None, lon=None, tz_name=None)
        response = service.build_v2_natal_response(chart, request.person)
    except Exception as e:
        logger.exception("Failed to build natal response")
        raise HTTPException(status_code=500, detail=str(e))

    # Try to produce a PDF if reportlab is available
    if canvas and letter:
        buf = io.BytesIO()
        try:
            c = canvas.Canvas(buf, pagesize=letter)
            width, height = letter
            y = height - 40

            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y, f"Natal Report: {chart.name or 'Unknown'}")
            y -= 24

            c.setFont("Helvetica", 10)
            meta = response.meta
            c.drawString(40, y, f"Version: {meta.version}  Locale: {meta.locale}  ChartType: {meta.chartType}")
            y -= 18

            c.drawString(40, y, f"Sun: {meta.zodiac.sun}  Moon: {meta.zodiac.moon or 'Unknown'}  Rising: {meta.zodiac.rising or 'Unknown'}")
            y -= 24

            for sec in response.sections:
                if y < 100:
                    c.showPage()
                    y = height - 40
                c.setFont("Helvetica-Bold", 12)
                c.drawString(40, y, sec.title_i18n)
                y -= 16
                c.setFont("Helvetica", 9)
                c.drawString(48, y, sec.summary)
                y -= 14
                for ins in sec.insights:
                    if y < 60:
                        c.showPage()
                        y = height - 40
                    line = f"- [{ins.type}] {ins.content}"
                    c.drawString(56, y, line[:120])
                    y -= 12

            c.save()
            buf.seek(0)
            return Response(content=buf.read(), media_type="application/pdf")
        except Exception as e:
            logger.exception("PDF generation failed, falling back to JSON")

    # Fall back to JSON response with the structured natal response
    return JSONResponse(content=response.model_dump())
