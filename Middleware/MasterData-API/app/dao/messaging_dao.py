"""Messaging adapters — in-memory for tests; RabbitMQ for local stack."""

from __future__ import annotations

from typing import Protocol

from app.config import Settings, get_settings


class MessagingDao(Protocol):
    def publish(self, payload: str) -> None: ...
    def consume(self, max_messages: int = 10) -> list[str]: ...


class InMemoryMessagingDao:
    def __init__(self) -> None:
        self._q: list[str] = []

    def publish(self, payload: str) -> None:
        self._q.append(payload)

    def consume(self, max_messages: int = 10) -> list[str]:
        out = self._q[:max_messages]
        del self._q[: len(out)]
        return out


class RabbitMessagingDao:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def _channel(self):
        import pika

        s = self._settings
        params = pika.ConnectionParameters(
            host=s.rabbitmq_host,
            port=s.rabbitmq_port,
            virtual_host=s.rabbitmq_vhost,
            credentials=pika.PlainCredentials(s.rabbitmq_user, s.rabbitmq_password),
            connection_attempts=2,
            retry_delay=1,
            socket_timeout=3,
        )
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.queue_declare(queue=s.rabbitmq_queue, durable=True)
        return conn, ch

    def publish(self, payload: str) -> None:
        conn, ch = self._channel()
        try:
            import pika

            ch.basic_publish(
                exchange="",
                routing_key=self._settings.rabbitmq_queue,
                body=payload.encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2),
            )
        finally:
            conn.close()

    def consume(self, max_messages: int = 10) -> list[str]:
        conn, ch = self._channel()
        out: list[str] = []
        try:
            for _ in range(max_messages):
                method, _props, body = ch.basic_get(queue=self._settings.rabbitmq_queue, auto_ack=True)
                if method is None:
                    break
                out.append(body.decode("utf-8"))
        finally:
            conn.close()
        return out
