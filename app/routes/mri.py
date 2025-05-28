from fastapi import APIRouter, Depends, Request, Query, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app import crud, schemas
from app.templates import templates
from app.auth import get_current_user

router = APIRouter()
ALLOWED_ROLES = ['missanoguga', 'sebastianmartinezarias']

def check_role(user):
    role = user["userinfo"].get("nickname")
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=403, detail=f"Unauthorized User: role is '{role}'")

@router.get("/", response_class=HTMLResponse)
async def mri_list_html(
    request: Request,
    page: int = Query(1, ge=1),
    user=Depends(get_current_user),
):
    check_role(user)
    limit = 10
    skip = (page - 1) * limit
    mris = await crud.get_mris_by_user(user["userinfo"]["sub"], skip=skip, limit=limit)
    pagination = {"page": page, "total_pages": 10, "has_previous": page > 1, "has_next": True}
    return templates.TemplateResponse("mri_list.html", {"request": request, "mris": mris, "pagination": pagination})

@router.get("/create", response_class=HTMLResponse)
async def mri_create_form(request: Request, user=Depends(get_current_user)):
    check_role(user)
    return templates.TemplateResponse("mri_create.html", {"request": request, "errors": []})

@router.post("/create", response_class=HTMLResponse)
async def mri_create_post(
    request: Request,
    fecha: str = Form(...),
    hora: str = Form(...),
    descripcion: str = Form(...),
    user=Depends(get_current_user),
):
    check_role(user)
    errors = []
    try:
        data = schemas.MRICreate(fecha=fecha, hora=hora, descripcion=descripcion)
        await crud.create_mri(data, user["userinfo"]["sub"])
        return RedirectResponse(url="/mris/html", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        errors.append(str(e))
        return templates.TemplateResponse("mri_create.html", {"request": request, "errors": errors})
