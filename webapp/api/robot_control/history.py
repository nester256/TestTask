from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.robot_control.router import robot_router
from webapp.db.operations.history import get_history_page
from webapp.db.postgres import get_session
from webapp.schema.robot import HistoryInfo, ResponseDefault, RobotHistoryInfo, RobotHistoryInfoList


@robot_router.post(
    '/history',
    description='Endpoint for viewing the history of starting/stopping robots',
    responses={
        status.HTTP_200_OK: {'model': RobotHistoryInfoList, 'description': 'Will return the robots work history'},
        status.HTTP_404_NOT_FOUND: {'model': ResponseDefault, 'description': 'Robots work history not found'},
    },
)
async def history(
    body: HistoryInfo,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_history = [
        RobotHistoryInfo.model_validate(robot).model_dump() for robot in await get_history_page(session, body.page)
    ]
    if serialized_history:
        return ORJSONResponse({'products': serialized_history}, status_code=status.HTTP_200_OK)
    else:
        return ORJSONResponse({'message': 'No history found for robots'}, status_code=status.HTTP_404_NOT_FOUND)
