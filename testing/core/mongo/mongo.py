from datetime import datetime, timezone
from bson import ObjectId
from typing import Dict, Any, Mapping, List
from pymongo import MongoClient

from testing.config.read_config import app_config

global_session = None

mongo_database = 'weaknet'

mongo_config = app_config['mongo']


class Session:
    def __init__(self, uri: str, database_name: str = mongo_database):
        """初始化MongoDB连接"""
        self.client = MongoClient(uri)
        self.db = self.client[database_name]

    def c(self, collection):
        return self.db.get_collection(collection)

    def find_one(self, collection: str, query: Dict[str, Any]) -> Mapping[str, Any] | Any:
        result = self.c(collection).find_one(query)
        return result

    def find_all(self, collection: str, query: Dict[str, Any] = {}) -> List[Mapping[str, Any]] | Any:
        result = self.c(collection).find(query)
        return result

    def find_id(self, collection: str, id: str) -> Mapping[str, Any] | Any:
        result = self.c(collection).find_one({"_id": ObjectId(id)})
        return result

    def find_iter_sort(self, collection: str, query: Dict[str, Any] = {}, *sort: Any) -> List[Mapping[str, Any]] | Any:
        result = self.c(collection).find(query).sort(*sort)
        return result

    def find_count(self, collection: str, query: Dict[str, Any] = {}) -> int:
        result = self.c(collection).count_documents(query)
        return result

    def find_with_options(self, collection: str, query: Dict[str, Any] = {}, options: Dict[str, Any] = {}) \
            -> List[Mapping[str, Any]] | Any:
        result = self.c(collection).find(query, projection=options.get("projection"))
        if options.get("sort", None) is not None:
            result = result.sort(options["sort"])
        if options.get("offset", None) is not None:
            result = result.skip(options["offset"])
        if options.get("limit", None) is not None:
            result = result.limit(options["limit"])
        return result

    def find_distinct(self, collection: str, query: Dict[str, Any] = {}, key: str = "") -> list[Mapping[str, Any]]:
        result = self.c(collection).find(query).distinct(key)
        return result

    def insert(self, collection, data: Dict[str, Any]) -> str:
        """插入一条数据"""
        result = self.c(collection).insert_one(data)
        return str(result.inserted_id)

    def insert_many(self, collection: str, data: List[Dict[str, Any]]):
        """批量插入多条数据"""
        result = self.c(collection).insert_many(data)
        return str(result)

    def update(self, collection, query: Dict[str, Any], new_data: Dict[str, Any]) -> int:
        """更新数据"""
        result = self.c(collection).update_one(query, {'$set': new_data})
        return result.modified_count

    def update_id(self, collection: str, id: str, update: Dict[str, Any]) -> int:
        """通过id更新"""
        result = self.c(collection).update_one({"_id": id}, update)
        return int(result.modified_count)

    def update_all(self, collection: str, query: Dict[str, Any] = {}, update: Dict[str, Any] = {}):
        """根据查询条件批量更新"""
        result = self.c(collection).update_many(query, update)
        return result

    def update_ids(self, collection: str, ids: List[str], update: Dict[str, Any]) -> int:
        """通过id列表批量更新"""
        query = {"_id": {"$in": [ObjectId(id) for id in ids]}}
        result = self.c(collection).update_many(query, update)
        return result.modified_count

    def upsert(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """更新时不存在就插入一条"""
        result = self.c(collection).update_one(query, update, upsert=True)
        return int(result.modified_count)

    def upsert_id(self, collection: str, id: str, update: Dict[str, Any]):
        """通过id更新，不存在就插入一条数据"""
        result = self.c(collection).update_one({"_id": id}, {"$set": update}, upsert=True)
        return int(result.modified_count)

    def upsert_ids(self, collection: str, ids: list, update: Dict[str, Any]) -> int:
        """通过id批量更新，不存在就插入"""
        query = {"_id": {"$in": [ObjectId(id) for id in ids]}}
        result = self.c(collection).update_many(query, update, upsert=True)
        return int(result.modified_count)

    def partial_update(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """更新部分"""
        result = self.c(collection).update_many(query, update)
        return int(result.modified_count)

    def remove_one(self, collection: str, query: Dict[str, Any]) -> int:
        """删除一条"""
        result = self.c(collection).delete_one(query)
        return int(result.deleted_count)

    def remove_all(self, collection: str, query: Dict[str, Any]) -> int:
        """删除多条"""
        result = self.c(collection).delete_many(query)
        return int(result.deleted_count)

    def remove_id(self, collection: str, id: str) -> int:
        """根据id删除"""
        query = {"_id": id}
        result = self.c(collection).delete_one(query)
        return int(result.deleted_count)

    def remove_ids(self, collection: str, ids: list) -> int:
        """删除多条"""
        query = {"_id": {"$in": [ObjectId(id) for id in ids]}}
        result = self.c(collection).delete_many(query)
        return int(result.deleted_count)

    def archive_id(self, collection: str, id: str) -> int:
        """根据id做逻辑删除"""
        now = datetime.now(timezone.utc).isoformat()
        query = {"_id": id}
        update = {"$set": {"deletedTime": now}}
        result = self.c(collection).update_one(query, update)
        return int(result.modified_count)

    def un_archive_id(self, collection: str, id: str) -> int:
        """根据id恢复逻辑删除"""
        query = {"_id": id}
        update = {"$set": {"deletedTime": None}}
        result = self.c(collection).update_one(query, update)
        return int(result.modified_count)

    def pipe(self, collection: str, pipline: List[Dict[str, Any]]) -> list[Mapping[str, Any]] | Any:
        result = self.c(collection).aggregate(pipline)
        return result

    def exists(self, collection: str, query: Dict[str, Any]) -> bool:
        result = self.c(collection).find_one(query)
        return result is not None

    def close(self):
        """关闭数据库连接"""
        self.client.close()


def get():
    global global_session
    if global_session is None:
        mongo_auth = bool(mongo_config['auth'])
        mongo_host = mongo_config['host']
        mongo_port = mongo_config['port']
        if mongo_auth:
            mongo_user = mongo_config['user']
            mongo_password = mongo_config['password']
            mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
        else:
            mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"
        session = Session(mongo_uri)
        global_session = session
        return global_session
    else:
        return global_session
