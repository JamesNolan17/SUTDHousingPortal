from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from markkk.logger import logger
from pymongo import ReturnDocument

from ..access_utils import Access
from ..auth import AuthHandler
from ..database import *
from ..error_msg import ErrorMsg as MSG
from ..functional import clean_dict, remove_none_value_keys
from ..models.application import ApplicationForm, ApplicationPeriod, TimePeriod
from ..models.event import Event
from ..models.lifestyle import LifestyleProfile
from ..models.record import DisciplinaryRecord
from ..models.room import Room, RoomProfile
from ..models.student import (
    StudentEditableProfile,
    StudentIdentityProfile,
    StudentProfile,
)

router = APIRouter(prefix="/api/students", tags=["Students"])
auth_handler = AuthHandler()


@router.get("/")
async def get_all_student_info(
    username=Depends(auth_handler.auth_wrapper), num: int = 30
):
    """
    Get all student info

    Require: Admin-read
    """
    logger.debug(f"User({username}) trying fetching all students info.")
    permission_ok: bool = Access.is_admin(username)
    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    student_info_list = []
    count = 0
    try:
        for student_info in students_collection.find():
            count += 1
            clean_dict(student_info)
            student_info_list.append(student_info)
            if count >= num:
                break
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    return student_info_list


@router.get("/{student_id}", response_model=StudentProfile)
async def get_a_student_info(
    student_id: str, username=Depends(auth_handler.auth_wrapper)
):
    """
    Set a particular Student info

    Require: Student-self or Admin-read
    """

    logger.debug(f"User({username}) trying fetching student({student_id}) info.")
    permission_ok = False
    if student_id == username or Access.is_admin(username):
        permission_ok = True

    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    try:
        student_info = students_collection.find_one({"student_id": student_id})
        clean_dict(student_info)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if student_info:
        logger.debug(f"student_info: {student_info}")
        return student_info
    else:
        raise HTTPException(status_code=404, detail=MSG.ITEM_NOT_FOUND)


@router.put("/{student_id}", response_model=StudentProfile)
async def update_a_student_profile(
    student_id: str,
    student_editable_profile: StudentEditableProfile,
    username=Depends(auth_handler.auth_wrapper),
):
    """
    Update (Overwrite) a particular Student info

    Require: Student-self or Admin-write
    """
    permission_ok = False
    if username == student_id:
        permission_ok = True
    if Access.is_admin_write(username):
        permission_ok = True

    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    student_update_dict = dict(student_editable_profile.dict())
    remove_none_value_keys(student_update_dict)

    try:
        # NOTE: there is a potential bug here, need to distinguish cases where
        # A: user wants to clear certain field (supply 'None' as new value)
        # B: user wants to preserve the value of certain field (Not changing anything, so supplying 'None')
        updated = students_collection.find_one_and_update(
            filter={"student_id": student_id},
            update={"$set": student_update_dict},
            return_document=ReturnDocument.AFTER,
        )
        logger.debug(f"{str(updated)}")
        clean_dict(updated)
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if updated:
        logger.debug(f"Updated: {updated}")
        return updated
    else:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)


@router.put("/{student_id}/identity", response_model=StudentProfile)
async def update_a_student_identity(
    student_id: str,
    student_identity_profile: StudentIdentityProfile,
    username=Depends(auth_handler.auth_wrapper),
):
    logger.debug(
        f"User({username}) trying to update Student({student_id})'s identity profile."
    )
    permission_ok = Access.is_admin_write(username)
    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    identity_dict = dict(student_identity_profile.dict())
    remove_none_value_keys(identity_dict)

    try:
        updated = students_collection.find_one_and_update(
            filter={"student_id": student_id},
            update={"$set": identity_dict},
            return_document=ReturnDocument.AFTER,
        )
        clean_dict(updated)
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if updated:
        logger.debug(f"Updated: {updated}")
        return updated
    else:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)


@router.put("/{student_id}/set_hg")
async def set_a_student_as_hg(
    student_id: str, username=Depends(auth_handler.auth_wrapper)
):
    """
    Set a Student as House Guardian

    Require: Admin-write
    """
    permission_ok = False
    if Access.is_admin_write(username):
        permission_ok = True

    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    try:
        updated = students_collection.find_one_and_update(
            filter={"student_id": student_id},
            update={"$set": {"is_house_guardian": True}},
            return_document=ReturnDocument.AFTER,
        )
        logger.debug(f"{str(updated)}")
        clean_dict(updated)
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if updated:
        logger.debug(f"Updated: {updated}")
        return updated
    else:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)


@router.put("/{student_id}/revoke_sg")
async def revoke_a_student_as_hg(
    student_id: str, username=Depends(auth_handler.auth_wrapper)
):
    """
    Revoke a Student as House Guardian

    Require: Admin-write
    """
    permission_ok = False
    if Access.is_admin_write(username):
        permission_ok = True

    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    try:
        updated = students_collection.find_one_and_update(
            filter={"student_id": student_id},
            update={"$set": {"is_house_guardian": False}},
            return_document=ReturnDocument.AFTER,
        )
        logger.debug(f"{str(updated)}")
        clean_dict(updated)
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if updated:
        logger.debug(f"Updated: {updated}")
        return updated
    else:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)


@router.put("/{student_id}/update_room_profile")
async def update_one_room_profile(
    student_id: str,
    room_profile: RoomProfile,
    username=Depends(auth_handler.auth_wrapper),
):
    """
    Update (Overwrite) a student's prefered Room Profile

    Require: Student-self or Admin-write
    """
    permission_ok = False
    if username == student_id:
        permission_ok = True
    if Access.is_admin_write(username):
        permission_ok = True
    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    data = dict(room_profile.dict())
    try:
        updated = students_collection.find_one_and_update(
            filter={"student_id": student_id},
            update={"$set": {"preference_room": data}},
            return_document=ReturnDocument.AFTER,
        )
        clean_dict(updated)
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if updated:
        logger.debug(f"Updated: {updated}")
        return updated
    else:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)


@router.put("/{student_id}/update_lifestyle_profile")
async def update_one_lifestyle_profile(
    student_id: str,
    lifestyle_profile: LifestyleProfile,
    username=Depends(auth_handler.auth_wrapper),
):
    """
    Update (Overwrite) a student's prefered Lifestyle Profile

    Require: Student-self or Admin-write
    """
    permission_ok = False
    if username == student_id:
        permission_ok = True
    if Access.is_admin_write(username):
        permission_ok = True
    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    data = dict(lifestyle_profile.dict())
    try:
        updated = students_collection.find_one_and_update(
            filter={"student_id": student_id},
            update={"$set": {"preference_lifestyle": data}},
            return_document=ReturnDocument.AFTER,
        )
        clean_dict(updated)
    except Exception as e:
        logger.error(MSG.DB_UPDATE_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_UPDATE_ERROR)

    if updated:
        logger.debug(f"Updated: {updated}")
        return updated
    else:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)


@router.get("/{student_id}/events", response_model=List[Event])
async def get_student_participated_events(
    student_id: str, username=Depends(auth_handler.auth_wrapper)
):
    """
    Get a list of Events that the student has signed up and/or attended.

    Require: Any authenticated user
    """
    logger.debug(f"User({username}) fetching student({student_id})'s Event list.")

    try:
        student_info = students_collection.find_one({"student_id": student_id})
        clean_dict(student_info)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not student_info:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)

    event_uids = student_info.get("registered_events", [])
    if not event_uids:
        return []
    else:
        event_uids = list(set(event_uids))

    event_info_list: List[dict] = []

    try:
        for uid in event_uids:
            if isinstance(uid, str):
                event_dict: dict = events_collection.find_one({"uid": uid})
                clean_dict(event_dict)
                if event_dict:
                    event_info_list.append(event_dict)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    return event_info_list


@router.get("/{student_id}/records", response_model=List[DisciplinaryRecord])
async def get_student_disciplinary_records(
    student_id: str, username=Depends(auth_handler.auth_wrapper)
):
    """
    Get all DisciplinaryRecords that belong to the particular student

    Require: Student-self or Admin-read
    """
    logger.debug(
        f"User({username}) trying fetching Student({student_id})'s DisciplinaryRecords"
    )

    permission_ok = Access.is_admin(username) or (username == student_id)
    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    # get DisciplinaryRecord uids from student profile
    try:
        student_info = students_collection.find_one({"student_id": student_id})
        clean_dict(student_info)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not student_info:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)

    record_uids: List[str] = student_info.get("disciplinary_records")
    if not record_uids:
        return []
    else:
        record_uids = list(set(record_uids))

    event_info_list: List[dict] = []
    try:
        for uid in record_uids:
            if isinstance(uid, str):
                _record_dict: dict = records_collection.find_one({"uid": uid})
                clean_dict(_record_dict)
                if _record_dict:
                    event_info_list.append(_record_dict)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    logger.debug(
        f"Fetched {len(event_info_list)} DisciplinaryRecord(s) that belong to Student({student_id})"
    )
    return event_info_list


@router.get("/{student_id}/applications", response_model=Dict[str, ApplicationForm])
async def get_student_submitted_applications(
    student_id: str, username=Depends(auth_handler.auth_wrapper)
):
    """
    Get a list of ApplicationForm that the student has submitted.

    Require: Student-self or Admin-read
    """
    logger.debug(
        f"User({username}) trying fetching Student({student_id})'s Applications"
    )

    permission_ok = Access.is_admin(username) or (username == student_id)
    if not permission_ok:
        logger.debug(MSG.permission_denied_msg(username))
        raise HTTPException(status_code=401, detail=MSG.PERMISSION_ERROR)

    application_list = []
    try:
        student_info = students_collection.find_one({"student_id": student_id})
        clean_dict(student_info)
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    if not student_info:
        raise HTTPException(status_code=404, detail=MSG.TARGET_ITEM_NOT_FOUND)

    AF_uids = student_info.get("application_uids", [])
    if not AF_uids:
        return {}
    else:
        AF_uids = list(set(AF_uids))

    submitted_applications: Dict[str, dict] = {}

    try:
        for uid in AF_uids:
            if isinstance(uid, str):
                ap_dict: dict = applications_collection.find_one({"uid": uid})
                clean_dict(ap_dict)
                if ap_dict:
                    submitted_applications[uid] = ap_dict
    except Exception as e:
        logger.error(MSG.DB_QUERY_ERROR)
        logger.error(e)
        raise HTTPException(status_code=500, detail=MSG.DB_QUERY_ERROR)

    return submitted_applications
