# Курс: Автоматизация тестирования на Python + pytest + Playwright (с GitLab CI + Docker)

Краткое описание

Этот курс предназначен для начинающих: пошагово объясняет основы автоматизации тестирования с использованием Python, `pytest` и `Playwright` (Python binding), и показывает как запускать тесты в GitLab CI в Docker‑окружении.

Целевая аудитория

- Новички в автоматизации тестирования
- Разработчики Python, которые хотят писать тесты UI/API
- QA инженеры, начинающие автоматизировать E2E тесты

Формат курса

- Папка `stages` содержит отдельные модули (этапы). Каждый этап — самостоятельный блок с теорией, примерами кода и практическими заданиями.
- В корне: `requirements.txt`, `Dockerfile`, `.gitlab-ci.yml` (пример).

Цели курса

- Научиться писать unit и end‑to‑end тесты на Python
- Освоить `pytest` и его лучшие практики
- Изучить Playwright для автоматизации браузера
- Научиться запускать тесты в GitLab CI и в Docker

---

Дерево курса

```
course_automation_pytest_playwright/
├─ README.md
├─ requirements.txt
├─ Dockerfile
├─ .gitlab-ci.yml
├─ stages/
│  ├─ 01_introduction/
│  ├─ 02_env_setup/
│  ├─ 03_pytest_basics/
│  ├─ 04_playwright_intro/
│  ├─ 05_e2e_tests/
│  ├─ 06_gitlab_ci/
│  └─ 07_advanced_topics/
```

Дальше откройте папку `stages` и начните с `01_introduction`.
