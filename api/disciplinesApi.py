from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.disciplinesModels import DisciplineEntity, Discipline
from my_data_base.my_data_base import get_session
from fastapi import HTTPException
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

disciplines_router = APIRouter(tags=[Tags.disciplines], prefix='/api/disciplines')


@disciplines_router.get("/", response_model=List[discipline])
async def get_all_disciplines(my_data_base: Session = Depends(get_session)):
    """Получить все дисциплины"""
    async with my_data_base.begin():
        query = select(DisciplineEntity)
        final_data = await my_data_base.execute(query)
        disciplines = final_data.scalars().all()

    if disciplines is None:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return disciplines


@disciplines_router.get("/{id}", response_model=discipline)
async def get_discipline(identifier: int, my_data_base: Session = Depends(get_session)):
    """Получить дисциплины по ID"""
    async with my_data_base.begin():
        query = select(DisciplineEntity).where(DisciplineEntity.id == identifier)
        final_data = await my_data_base.execute(query)
        discipline = final_data.scalar()

    if discipline is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return discipline


import logging


@disciplines_router.post("/", response_model=discipline)
async def create_discipline(cr_discipline: discipline, my_data_base: AsyncSession = Depends(get_session)):
    """Создать дисциплину"""
    try:
        discipline = DisciplineEntity(
            title=cr_discipline.title,
            release_year=cr_discipline.release_year,
            genre=cr_discipline.genre,
            rating=cr_discipline.rating,
            is_published=cr_discipline.is_published,
            director_id=cr_discipline.director_id
        )
        if discipline is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        async with my_data_base.begin():
            my_data_base.add(discipline)
            await my_data_base.commit()

        await my_data_base.refresh(discipline)
        result = discipline(id=discipline.id,
                       title=discipline.title,
                       release_year=discipline.release_year,
                       genre=discipline.genre,
                       rating=discipline.rating,
                       is_published=discipline.is_published,
                       director_id=discipline.director_id
                       )
        return result
    except Exception as exc:
        logging.error(f"Error while adding discipline: {exc}")
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_discipline}")


@disciplines_router.delete("/", response_model=discipline)
async def delete_discipline(identifier: int, my_data_base: AsyncSession = Depends(get_session)):
    """Удалить дисциплину"""
    try:
        async with my_data_base.begin():
            query = select(DisciplineEntity).where(DisciplineEntity.id == identifier)
            result = await my_data_base.execute(query)
            discipline = result.scalar()

            if discipline is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await my_data_base.delete(discipline)

        return discipline
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@disciplines_router.put("/{id}", response_model=discipline)
async def update_discipline(identifier: int, updated_info: discipline,
                       my_data_base: AsyncSession = Depends(get_session)):
    """Полное обновление дисциплины"""
    try:
        async with my_data_base.begin():
            query = select(DisciplineEntity).where(DisciplineEntity.id == identifier)
            result = await my_data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id = updated_info.id
            existing_info.title = updated_info.title
            existing_info.release_year = updated_info.release_year
            existing_info.genre = updated_info.genre
            existing_info.rating = updated_info.rating
            existing_info.is_published = updated_info.is_published
            existing_info.director_id = updated_info.director_id

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@disciplines_router.patch("/{id}", response_model=discipline)
async def partial_update_discipline(identifier: int, updated_info: discipline,
                               my_data_base: AsyncSession = Depends(get_session)):
    """Частичное обновление дисциплины"""
    try:
        async with my_data_base.begin():
            query = select(DisciplineEntity).where(DisciplineEntity.id == identifier)
            result = await my_data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id:
                existing_info.id = updated_info.id
            if updated_info.title:
                existing_info.title = updated_info.title
            if updated_info.release_year:
                existing_info.release_year = updated_info.release_year
            if updated_info.genre:
                existing_info.genre = updated_info.genre
            if updated_info.rating:
                existing_info.rating = updated_info.rating
            if updated_info.is_published:
                existing_info.is_published = updated_info.is_published
            if updated_info.director_id:
                existing_info.director_id = updated_info.director_id

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
