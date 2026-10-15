PLATFORM_FEATURES = {
    "8.3.20": ["Расширения", "HTTP-сервисы", "REST"],
    "8.3.21": ["Работа с JSON", "Асинхронные методы"],
    "8.3.22": ["Мультиязычность", "Новые методы строк"],
    "8.3.23": ["Оптимизация запросов", "Новый механизм блокировок"],
    "8.3.24": ["Улучшения EDT", "Новый API для интеграций"],
    "8.3.25": ["Мобильная платформа", "Улучшения производительности"],
}

BREAKING_CHANGES = {
    ("8.3.20", "8.3.21"): ["Изменён механизм работы с JSON"],
    ("8.3.22", "8.3.23"): ["Устаревший механизм блокировок удалён"],
    ("8.3.23", "8.3.24"): ["Изменён формат HTTP-сервисов"],
}

def check_compatibility(current, target):
    if not is_upgrade(current, target):
        return {"ok": False, "reason": "downgrade not supported"}

    issues = []
    key = (current, target)
    if key in BREAKING_CHANGES:
        issues = BREAKING_CHANGES[key]

    return {
        "ok": len(issues) == 0,
        "current": current,
        "target": target,
        "breaking_changes": issues,
        "available_features": PLATFORM_FEATURES.get(target, []),
    }

def is_upgrade(current, target):
    from src.platform import version_tuple
    return version_tuple(target) >= version_tuple(current)
