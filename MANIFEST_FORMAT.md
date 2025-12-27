# Анализ формата manifest.json для HyperBox Launcher

## Общая структура
На основе анализа кода `launcher.py` и `loader.py`, модпак получает manifest.json с сервера API по URL:
```
https://Api.Hyperbox.world/modpacks/{modpack_name}
```

---

## 🔍 Основная структура Manifest.json

```json
{
  "java": {
    "version": "string (e.g., '17.0.5')",
    "windowsUrl": "string (URL to java manifest)"
  },
  "assets": {
    "urls": "string (URL to assets manifest)",
    "index": {},
    "id": "string (assets identifier)"
  },
  "libraries": [],
  "resources": {
    "requiredResources": [],
    "staticResources": []
  },
  "command": []
}
```

---

## 📦 Подробное описание полей

### 1. **java** объект
Содержит информацию для скачивания Java Runtime:

| Поле | Тип | Описание |
|------|-----|---------|
| `version` | string | Версия Java (напр., "17.0.5", "21.0.1") |
| `windowsUrl` | string | URL до JSON с файлами Java для загрузки |

**Java Manifest** (получаемый по `windowsUrl`):
```json
[
  {
    "path": "string (relative path)",
    "url": "string (download URL)",
    "size": number (bytes),
    "sha1": "string (SHA-1 hash)"
  }
]
```

---

### 2. **assets** объект
Содержит информацию для скачивания игровых ассетов:

| Поле | Тип | Описание |
|------|-----|---------|
| `urls` | string | URL до JSON массива ассетов |
| `index` | object | Object с индексом ассетов (тоже file_info) |
| `id` | string | Уникальный идентификатор ассетов |

**Assets Index** (в поле `index`):
```json
{
  "path": "string",
  "url": "string",
  "size": number,
  "sha1": "string"
}
```

**Assets Array** (получаемый по `urls`):
```json
[
  {
    "path": "string (относительный путь в objects/)",
    "url": "string (download URL)",
    "size": number,
    "sha1": "string"
  }
]
```

---

### 3. **libraries** массив
Список библиотек Minecraft/Forge для скачивания:

```json
[
  {
    "path": "string (relative path в libraries/)",
    "url": "string (download URL)",
    "size": number,
    "sha1": "string"
  }
]
```

**Примеры paths:**
- `net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar`
- `org/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar`

---

### 4. **resources** объект
Содержит два типа ресурсов:

```json
{
  "requiredResources": [
    {
      "path": "string",
      "url": "string",
      "size": number,
      "sha1": "string"
    }
  ],
  "staticResources": [
    {
      "path": "string",
      "url": "string",
      "size": number,
      "sha1": "string"
    }
  ]
}
```

**Разница:**
- **requiredResources** - скачиваются всегда при каждом запуске
- **staticResources** - скачиваются только если нет `config.bin` файла (первый запуск)

---

### 5. **command** массив
JVM команда запуска с плейсхолдерами:

```json
[
  "-XX:+UnlockCommercialFeatures",
  "-XX:+FlightRecorder",
  "-cp",
  "{libraries_path}/*",
  "-Djava.library.path={natives_path}",
  "-Dlog4j.configurationFile={assets_path}/log4j2.xml",
  "-Dminecraft.launcher.brand=minecraft-launcher",
  "-Dminecraft.launcher.version={launcher_version}",
  "-Dminecraft.client.jar={game_path}/versions/1.20.1/1.20.1.jar",
  "-Duser.language=en",
  "-Duser.country=US",
  "net.minecraft.client.main.Main",
  "--username={username}",
  "--uuid={uuid}",
  "--accessToken={token}",
  "--assetIndex={assets_id}",
  "--assetsDir={assets_path}",
  "--gameDir={game_path}",
  "--clientId={something}",
  "--xuid={something}",
  "--clientSecret={something}",
  "--features",
  "is_demo_user=false,has_cosmetics=false",
  "--quickPlayPath={game_path}",
  "--quickPlaySingleplayer=",
  "--width=1024",
  "--height=768"
]
```

**Доступные плейсхолдеры** (в `Command.get()`):
| Плейсхолдер | Значение |
|------------|----------|
| `{natives_path}` | `{main_dir}/natives` |
| `{libraries_path}` | `{game_dir}/libraries` |
| `{username}` | Имя пользователя из auth |
| `{game_path}` | Путь к модпаку |
| `{assets_path}` | Путь к ассетам |
| `{uuid}` | UUID токен |
| `{token}` | Токен доступа |

---

## 📋 Полный пример Manifest.json

```json
{
  "java": {
    "version": "17.0.5",
    "windowsUrl": "https://launcher-api.example.com/java/17.0.5/manifest.json"
  },
  "assets": {
    "urls": "https://launcher-api.example.com/assets/1.20.1/list.json",
    "index": {
      "path": "indexes/1.20.1.json",
      "url": "https://launcher-api.example.com/assets/1.20.1/index.json",
      "size": 524288,
      "sha1": "abc123def456..."
    },
    "id": "1.20.1"
  },
  "libraries": [
    {
      "path": "net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar",
      "url": "https://libraries.example.com/net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar",
      "size": 32768,
      "sha1": "hash1..."
    }
  ],
  "resources": {
    "requiredResources": [
      {
        "path": "config/somemod.cfg",
        "url": "https://resources.example.com/config/somemod.cfg",
        "size": 2048,
        "sha1": "hash2..."
      }
    ],
    "staticResources": [
      {
        "path": "mods/mymod-1.0.jar",
        "url": "https://resources.example.com/mods/mymod-1.0.jar",
        "size": 1048576,
        "sha1": "hash3..."
      }
    ]
  },
  "command": [
    "-XX:+UnlockCommercialFeatures",
    "-cp",
    "{libraries_path}/*",
    "-Djava.library.path={natives_path}",
    "net.minecraft.client.main.Main",
    "--username={username}",
    "--uuid={uuid}",
    "--accessToken={token}",
    "--assetIndex={assets_id}",
    "--assetsDir={assets_path}",
    "--gameDir={game_path}"
  ]
}
```

---

## 🔄 Процесс загрузки (из launcher.py)

1. **Получить manifest модпака:**
   ```
   GET /modpacks/{modpack_name}
   ```

2. **Загрузить Java** (по `java.windowsUrl`)
   - Получить список файлов Java
   - Скачать все файлы в `{main_dir}/java/{version}/`
   - Вернуть путь к `java.exe`

3. **Загрузить Assets** (по `assets.urls`)
   - Скачать индекс ассетов
   - Скачать все ассеты в `objects/` директорию

4. **Загрузить Libraries** (массив `libraries`)
   - Скачать все в `{game_dir}/libraries/`

5. **Загрузить Resources** (массив `resources`)
   - Скачать `requiredResources` всегда
   - Скачать `staticResources` только если нет `config.bin`

6. **Построить команду запуска** (из массива `command`)
   - Заменить все плейсхолдеры на реальные значения
   - Запустить как subprocess

---

## ⚙️ Проверка целостности файлов

Каждый файл проверяется:
1. **Размер:** `file.size == expected_size`
2. **SHA-1 хеш:** `sha1(file) == expected_sha1`

Если файл не совпадает - перекачивается.

---

## 📍 Директорийная структура после загрузки

```
{main_dir}/
├── java/
│   └── {version}/
│       ├── bin/
│       │   └── java.exe
│       └── ...
├── assets/
│   └── {assets_id}/
│       ├── objects/
│       │   └── [ассеты по хешам]
│       └── indexes/
│           └── {assets_id}.json
└── updates/
    └── {modpack_name}/
        ├── libraries/
        ├── mods/
        ├── config/
        └── ...

{main_dir}/config.bin  # Флаг "первый запуск"
```

---

## 🎯 Ключевые моменты

### Структура File Info
Везде используется единая структура:
```json
{
  "path": "относительный путь для скачивания",
  "url": "https://... прямая ссылка на файл",
  "size": "точный размер в байтах",
  "sha1": "контрольная сумма SHA-1"
}
```

### URL маршруты для подмножеств
- `java.windowsUrl` - возвращает массив file_info для Java
- `assets.urls` - возвращает массив file_info для ассетов
- Остальное (libraries, resources) - напрямую в manifest.json

### Типы ресурсов
- **requiredResources** - мены на кожи, мелкие файлы конфига (скачиваются каждый раз)
- **staticResources** - тяжелые моды, текстуры (только первый раз)

### Плейсхолдеры
Все плейсхолдеры в command заменяются в методе `Command.get()` с использованием `.format_map()`
