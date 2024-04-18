
# shared_task - это декоратор Celery, который превращает обычную функцию в задачу, которую можно запускать асинхронно.
from celery import shared_task

from .email import send_activate_email_message, send_contact_email_message

from django.core.management import call_command


@shared_task
def send_activate_email_message_task(user_id):
    """
    1. Задача обрабатывается в представлении: UserRegisterView
    2. Отправка письма подтверждения осуществляется через функцию: send_activate_email_message
    """
    return send_activate_email_message(user_id)


@shared_task
def send_contact_email_message_task(subject, email, content, ip, user_id):
    """
    1. Задача обрабатывается в представлении: FeedbackCreateView
    2. Отправка письма из формы обратной связи осуществляется через функцию: send_contact_email_message
    """
    return send_contact_email_message(subject, email, content, ip, user_id)

"""
Выполнение резервного копирования базы данных
.\services\management\commands\dbackup.py
"""
# @shared_task()
# def dbackup_task():
#     call_command('dbackup')  # имя вызываемого файла  \services\management\commands\dbackup.py