build-up:
	docker compose up -d --build

restart:
	docker compose down && docker compose up -d

logs:
	docker logs -f chat-backend