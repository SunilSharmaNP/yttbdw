import time
from datetime import datetime
import config

MONGO_URI = getattr(config, "MONGO_URI", "")
OWNER_ID = getattr(config, "OWNER_ID", 2032446867)
SUDO_USERS = getattr(config, "SUDO_USERS", [OWNER_ID])

sudo_users_set = set(SUDO_USERS)
if OWNER_ID not in sudo_users_set:
    sudo_users_set.add(OWNER_ID)

banned_users_set = set()
registered_users_set = set()
bot_start_time = time.time()

mongo_client = None
db = None

if MONGO_URI:
    try:
        import pymongo
        mongo_client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = mongo_client["ss_downloader_bot"]
        print("[MONGODB] Connected to MongoDB database successfully.")

        try:
            for s in db.sudo_users.find({}, {"user_id": 1}):
                if "user_id" in s:
                    sudo_users_set.add(int(s["user_id"]))
        except Exception:
            pass

        try:
            for b in db.banned_users.find({}, {"user_id": 1}):
                if "user_id" in b:
                    banned_users_set.add(int(b["user_id"]))
        except Exception:
            pass

        try:
            for u in db.users.find({}, {"user_id": 1}):
                if "user_id" in u:
                    registered_users_set.add(int(u["user_id"]))
        except Exception:
            pass
    except Exception as e:
        print(f"[MONGODB NOTE] Connection failed or skipped: {e}")

def is_admin(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in sudo_users_set

def is_banned(user_id: int) -> bool:
    return user_id in banned_users_set

def add_sudo_user(user_id: int):
    sudo_users_set.add(user_id)
    if db is not None:
        try:
            db.sudo_users.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "added_at": time.time()}},
                upsert=True
            )
        except Exception:
            pass

def remove_sudo_user(user_id: int):
    sudo_users_set.discard(user_id)
    if db is not None:
        try:
            db.sudo_users.delete_one({"user_id": user_id})
        except Exception:
            pass

def ban_user(user_id: int, reason: str = "", admin_id: int = 0):
    banned_users_set.add(user_id)
    if db is not None:
        try:
            db.banned_users.update_one(
                {"user_id": user_id},
                {"$set": {
                    "user_id": user_id,
                    "reason": reason,
                    "banned_by": admin_id,
                    "banned_at": time.time()
                }},
                upsert=True
            )
        except Exception:
            pass

def unban_user(user_id: int):
    banned_users_set.discard(user_id)
    if db is not None:
        try:
            db.banned_users.delete_one({"user_id": user_id})
        except Exception:
            pass

def db_add_user(user_id: int, user_name: str, username: str = "") -> bool:
    is_new = user_id not in registered_users_set
    registered_users_set.add(user_id)
    if db is not None:
        try:
            existing = db.users.find_one({"user_id": user_id})
            if existing is None:
                is_new = True
            db.users.update_one(
                {"user_id": user_id},
                {"$set": {
                    "name": user_name,
                    "username": username,
                    "last_active": time.time()
                }},
                upsert=True
            )
        except Exception:
            pass
    return is_new

def db_log_download(user_id: int, provider: str, file_name: str, size: str):
    if db is not None:
        try:
            db.downloads.insert_one({
                "user_id": user_id,
                "provider": provider,
                "file_name": file_name,
                "size": size,
                "timestamp": time.time()
            })
        except Exception:
            pass

# In-memory thumbnails storage (fallback)
user_thumbnails: dict[int, str] = {}

def set_user_thumbnail(user_id: int, file_id: str):
    """Saves user custom thumbnail photo file_id."""
    user_thumbnails[user_id] = file_id
    if db is not None:
        try:
            db.thumbnails.update_one(
                {"user_id": user_id},
                {"$set": {"file_id": file_id, "updated_at": time.time()}},
                upsert=True
            )
        except Exception:
            pass

def get_user_thumbnail(user_id: int) -> str | None:
    """Retrieves user custom thumbnail file_id."""
    if user_id in user_thumbnails:
        return user_thumbnails[user_id]
    if db is not None:
        try:
            rec = db.thumbnails.find_one({"user_id": user_id})
            if rec and "file_id" in rec:
                user_thumbnails[user_id] = rec["file_id"]
                return rec["file_id"]
        except Exception:
            pass
    return None

def del_user_thumbnail(user_id: int) -> bool:
    """Deletes user custom thumbnail."""
    existed = user_id in user_thumbnails
    user_thumbnails.pop(user_id, None)
    if db is not None:
        try:
            res = db.thumbnails.delete_one({"user_id": user_id})
            if res.deleted_count > 0:
                existed = True
        except Exception:
            pass
    return existed

def get_all_broadcast_users() -> list[int]:
    """Returns list of all unique registered user IDs for broadcast."""
    all_users = set(registered_users_set)
    if db is not None:
        try:
            for u in db.users.find({}, {"user_id": 1}):
                if "user_id" in u:
                    all_users.add(int(u["user_id"]))
        except Exception:
            pass
    return list(all_users)

