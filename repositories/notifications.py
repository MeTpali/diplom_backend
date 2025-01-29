from typing import List, Optional
import logging
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.notifications import Notification
from core.schemas.notifications import NotificationCreate, NotificationUpdate, NotificationResponse

logger = logging.getLogger(__name__)

class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, notification: Notification) -> NotificationResponse:
        return NotificationResponse.model_validate(notification)

    async def get_notification_by_id(self, notification_id: int) -> Optional[NotificationResponse]:
        logger.info(f"Getting notification by id: {notification_id}")
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(query)
        notification = result.scalar_one_or_none()
        if notification is None:
            logger.warning(f"Notification with id {notification_id} not found")
        return self._model_to_schema(notification) if notification else None

    async def get_all_notifications(self) -> List[NotificationResponse]:
        logger.info("Getting all notifications")
        query = select(Notification)
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return [self._model_to_schema(notification) for notification in notifications]

    async def create_notification(self, notification_data: NotificationCreate) -> NotificationResponse:
        logger.info(f"Creating new notification for user {notification_data.user_id}")
        notification = Notification(**notification_data.model_dump())
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        logger.info(f"Successfully created notification with id: {notification.id}")
        return self._model_to_schema(notification)

    async def update_notification(
        self, notification_id: int, notification_data: NotificationUpdate
    ) -> Optional[NotificationResponse]:
        logger.info(f"Updating notification with id: {notification_id}")
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(query)
        notification = result.scalar_one_or_none()

        if notification is None:
            logger.warning(f"Notification with id {notification_id} not found for update")
            return None

        update_data = notification_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(notification, field, value)

        await self.session.commit()
        await self.session.refresh(notification)
        logger.info(f"Successfully updated notification with id: {notification_id}")
        return self._model_to_schema(notification)

    async def delete_notification(self, notification_id: int) -> bool:
        logger.info(f"Deleting notification with id: {notification_id}")
        query = delete(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted notification with id: {notification_id}")
        else:
            logger.warning(f"Notification with id {notification_id} not found for deletion")
        return success

    async def get_user_notifications(self, user_id: int) -> List[NotificationResponse]:
        logger.info(f"Getting notifications for user: {user_id}")
        query = select(Notification).where(Notification.user_id == user_id)
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return [self._model_to_schema(notification) for notification in notifications]

    async def get_exam_notifications(self, exam_id: int) -> List[NotificationResponse]:
        logger.info(f"Getting notifications for exam: {exam_id}")
        query = select(Notification).where(Notification.exam_id == exam_id)
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return [self._model_to_schema(notification) for notification in notifications]

    async def get_notifications_by_type(self, notification_type: str) -> List[NotificationResponse]:
        logger.info(f"Getting notifications by type: {notification_type}")
        query = select(Notification).where(Notification.type == notification_type)
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return [self._model_to_schema(notification) for notification in notifications]

    async def search_notifications(self, search_term: str) -> List[NotificationResponse]:
        logger.info(f"Searching notifications with term: {search_term}")
        query = select(Notification).where(
            or_(
                Notification.message.ilike(f"%{search_term}%"),
                Notification.type.ilike(f"%{search_term}%")
            )
        )
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return [self._model_to_schema(notification) for notification in notifications] 