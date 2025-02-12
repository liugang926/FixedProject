from django.core.mail import send_mail
from django.conf import settings
import random
import string

def generate_verification_code(length=6):
    """生成数字验证码"""
    return ''.join(random.choices(string.digits, k=length))

def send_email(to_email, subject, message):
    """发送邮件"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return False

def send_sms(phone_number, message):
    """发送短信（需要集成短信服务）"""
    # TODO: 实现短信发送逻辑
    print(f"发送短信到 {phone_number}: {message}")
    return True 