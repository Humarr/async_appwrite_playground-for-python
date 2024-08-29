import asyncio
from time import sleep
from random import randrange
from sys import maxsize

from async_appwrite.async_client import AsyncClient
from async_appwrite.services.async_users import AsyncUsers
from async_appwrite.services.async_databases import AsyncDatabases
from async_appwrite.services.async_storage import AsyncStorage
from async_appwrite.services.async_account import AsyncAccount
from async_appwrite.services.async_functions import AsyncFunctions
from appwrite.input_file import InputFile
from appwrite.permission import Permission
from appwrite.role import Role
from appwrite.id import ID


# Helper method to print green colored output.
def p(info):
    print("\033[32;1m" + str(info) + "\033[0m")


# Read the docs at https://appwrite.io/docs to get more information
# about API keys and Project IDs
client = AsyncClient()
client.set_endpoint("http://YOUR_HOST/v1")
client.set_project("YOUR_PROJECT_ID")
client.set_key("YOU_API_KEY")
client.set_self_signed()
# client.set_jwt('JWT') # Use this to authenticate with JWT instead of API_KEY

databases = AsyncDatabases(client)
storage = AsyncStorage(client)
functions = AsyncFunctions(client)
users = AsyncUsers(client)

database_id = None
collection_id = None
document_id = None
user_id = None
bucket_id = None
file_id = None
document_id = None


async def create_database():
    global database_id

    p("Running Create Database API")
    response = await databases.create(
        database_id=ID.unique(),
        name="Movies",
    )
    database_id = response["$id"]
    print(response)


async def create_collection():
    global collection_id

    p("Running Create Collection API")
    response = await databases.create_collection(
        database_id,
        collection_id=ID.unique(),
        name="Movies",
        document_security=True,
        permissions=[
            Permission.read(Role.any()),
            Permission.create(Role.users()),
            Permission.update(Role.users()),
            Permission.delete(Role.users()),
        ],
    )

    collection_id = response["$id"]
    print(response)

    response = await databases.create_string_attribute(
        database_id,
        collection_id,
        key="name",
        size=255,
        required=True,
    )
    print(response)

    response = await databases.create_integer_attribute(
        database_id, collection_id, key="release_year", required=True, min=0, max=9999
    )
    print(response)

    response = await databases.create_float_attribute(
        database_id, collection_id, key="rating", required=True, min=0.0, max=99.99
    )
    print(response)

    response = await databases.create_boolean_attribute(
        database_id, collection_id, key="kids", required=True
    )
    print(response)

    response = await databases.create_email_attribute(
        database_id, collection_id, key="email", required=False, default=""
    )
    print(response)

    # Wait for attributes to be created
    sleep(2)

    response = await databases.create_index(
        database_id,
        collection_id,
        key="name_email_idx",
        type="fulltext",
        attributes=["name", "email"],
    )
    print(response)


async def list_collections():
    p("Running List Collection API")
    response = await databases.list_collections(database_id)
    print(response)


async def get_account():
    account = AsyncAccount(client)
    p("Running Get Account API")
    response = account.get()
    print(response)


async def add_doc():
    global document_id

    p("Running Add Document API")
    response = await databases.create_document(
        database_id,
        collection_id,
        document_id=ID.unique(),
        data={
            "name": "Spider Man",
            "release_year": 1920,
            "rating": 98.5,
            "kids": False,
        },
        permissions=[
            Permission.read(Role.users()),
            Permission.update(Role.users()),
            Permission.delete(Role.users()),
        ],
    )
    document_id = response["$id"]
    print(response)


async def list_doc():
    p("Running List Document API")
    response = await databases.list_documents(database_id, collection_id)
    print(response)


async def delete_doc():
    p("Running Delete Database API")
    response = await databases.delete_document(database_id, collection_id, document_id)
    print(response)


async def delete_collection():
    p("Running Delete Collection API")
    response = await databases.delete_collection(database_id, collection_id)
    print(response)


async def delete_database():
    p("Running Delete Database API")
    response = await databases.delete(database_id)
    print(response)


async def create_bucket():
    global bucket_id

    p("Running Create Bucket API")
    response = await storage.create_bucket(
        bucket_id=ID.unique(),
        name="awesome bucket",
        file_security=True,
        permissions=[
            Permission.read(Role.any()),
            Permission.create(Role.users()),
            Permission.update(Role.users()),
            Permission.delete(Role.users()),
        ],
    )
    bucket_id = response["$id"]
    print(response)


async def list_buckets():
    p("Running List Buckets API")
    response = await storage.list_buckets()
    print(response)


async def upload_file():
    global file_id

    p("Running Upload File API")
    response = await storage.create_file(
        bucket_id,
        file_id=ID.unique(),
        file=InputFile.from_path("./resources/nature.jpg"),
    )
    file_id = response["$id"]
    print(response)


async def list_files():
    p("Running List Files API")
    response = await storage.list_files(bucket_id)
    print(response)


async def delete_file():
    p("Running Delete File API")
    response = await storage.delete_file(bucket_id, file_id)
    print(response)


async def delete_bucket():
    p("Running Delete Bucket API")
    response = await storage.delete_bucket(bucket_id)
    print(response)


async def create_user():
    global user_id

    name = str(randrange(1, maxsize))
    p("Running Create User API")
    response = await users.create(
        user_id=ID.unique(), email=f"{name}@test.com", password=f"{name}@123", name=name
    )
    user_id = response["$id"]
    print(response)


async def list_user():
    p("Running List User API")
    response = await users.list()
    print(response)


async def delete_user():
    p("Running Delete User API")
    response = await users.delete(user_id)
    print(response)


async def create_function():
    global function_id

    p("Running Create Function API")
    response = await functions.create(
        function_id=ID.unique(),
        name="Test Function",
        execute=[Role.any()],
        runtime="python-3.9",
    )
    function_id = response["$id"]
    print(response)


async def list_function():
    p("Running List Function API")
    response = await functions.list()
    print(response)


async def delete_function():
    p("Running Delete Function API")
    response = await functions.delete(function_id)
    print(response)


async def run_all_tasks():
    # Databases
    await asyncio.gather(
        create_database(),
        create_collection(),
        list_collections(),
        add_doc(),
        list_doc(),
        delete_doc(),
        delete_collection(),
        delete_database(),
    )

    # Storage
    await asyncio.gather(
        create_bucket(),
        list_buckets(),
        upload_file(),
        list_files(),
        delete_file(),
        delete_bucket(),
    )

    # Users
    await asyncio.gather(create_user(), list_user(), delete_user())

    # Functions
    await asyncio.gather(create_function(), list_function(), delete_function())


if __name__ == "__main__":
    try:
        asyncio.run(run_all_tasks())
        print("Successfully ran playground!")
    except Exception as e:
        print(f"An error occurred: {e}")
