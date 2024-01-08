from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.disciplinesModels import DirectorEntity, Director
from my_data_base.my_data_base import get_session
from fastapi import HTTPException
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

directors_router = APIRouter(tags=[Tags.directors], prefix='/api/directors')


@directors_router.get("/", response_model=List[Director])
async def get_all_directors(my_data_base: Session = Depends(get_session)):
    """Получить всех преподавателей"""
    async with my_data_base.begin():
        query = select(DirectorEntity)
        final_data = await my_data_base.execute(query)
        disciplines = final_data.scalars().all()

    if disciplines is None:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return disciplines


@directors_router.get("/{id}", response_model=Director)
async def get_director(identifier: int, my_data_base: Session = Depends(get_session)):
    """Получить преподавателя по ID"""
    async with my_data_base.begin():
        query = select(DirectorEntity).where(DirectorEntity.id == identifier)
        final_data = await my_data_base.execute(query)
        discipline = final_data.scalar()

    if discipline is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return discipline


import logging


@directors_router.post("/", response_model=Director)
async def create_director(cr_director: Director, my_data_base: AsyncSession = Depends(get_session)):
    """Создать преподавателя"""
    try:
        director = DirectorEntity(
            name=cr_director.name,
            date_of_birth=cr_director.date_of_birth
        )
        if director is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        async with my_data_base.begin():
            my_data_base.add(director)
            await my_data_base.commit()

        await my_data_base.refresh(director)
        result = Director(name=director.name, date_of_birth=director.date_of_birth)
        return result
    except Exception as exc:
        logging.error(f"Error while adding discipline: {exc}")
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_director}")


@directors_router.delete("/", response_model=Director)
async def delete_director(identifier: int, my_data_base: AsyncSession = Depends(get_session)):
    """Удалить преподавателя"""
    try:
        async with my_data_base.begin():
            query = select(DirectorEntity).where(DirectorEntity.id == identifier)
            result = await my_data_base.execute(query)
            director = result.scalar()

            if director is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await my_data_base.delete(director)

        return director
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@directors_router.put("/{id}", response_model=Director)
async def update_director(identifier: int, updated_info: Director,
                          my_data_base: AsyncSession = Depends(get_session)):
    """Полное обновление преподавателя"""
    try:
        async with my_data_base.begin():
            query = select(DirectorEntity).where(DirectorEntity.id == identifier)
            result = await my_data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id = updated_info.id
            existing_info.name = updated_info.name
            existing_info.date_of_birth = updated_info.date_of_birth

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@directors_router.patch("/{id}", response_model=Director)
async def partial_update_director(identifier: int, updated_info: Director,
                                  my_data_base: AsyncSession = Depends(get_session)):
    """Частичное обновление преподавателя"""
    try:
        async with my_data_base.begin():
            query = select(DirectorEntity).where(DirectorEntity.id == identifier)
            result = await my_data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id:
                existing_info.id = updated_info.id
            if updated_info.name:
                existing_info.name = updated_info.name
            if updated_info.date_of_birth:
                existing_info.date_of_birth = updated_info.date_of_birth

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
