from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User


class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        await self.send_user_email({
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }, 'email_verification')


# test_email_service.py
import pytest
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
from app.utils.smtp_connection import SMTPClient
from unittest.mock import Mock


@pytest.fixture
def email_service():
    template_manager = TemplateManager()
    smtp_client = SMTPClient(
        server=settings.smtp_server,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password
    )
    return EmailService(template_manager, smtp_client)


@pytest.mark.asyncio
async def test_send_verification_email(email_service):
    user = User(first_name="Test", email="test@example.com", id=123, verification_token="token123")
    email_service.smtp_client.send_email = Mock()
    await email_service.send_verification_email(user)
    email_service.smtp_client.send_email.assert_called_once_with(
        "Verify Your Account",
        Mock(),
        "test@example.com"
    )
