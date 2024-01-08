import datetime
import asyncio
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from my_data_base.my_data_base import init_db
from api.usersApi import users_router
from api.userAdditionalInfoApi import user_additional_info_router
from api.disciplinesApi import movies_router
from api.directorApi import directors_router
from models.generalModels import Tags

app = FastAPI(
    version="0.1.2",
    description="За выполнение задания отвечала Мозер М.О."
)

app.include_router(users_router)
app.include_router(user_additional_info_router)
app.include_router(movies_router)
app.include_router(directors_router)


class LogWriter:
    def __init__(self, filename: str):
        self.filename = filename

    async def write_log(self, event: str):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        with open(self.filename, mode="a") as file:
            file.write(f"{current_time}: {event}\n")


log_writer = LogWriter("log.txt")


async def startup_event():
    await log_writer.write_log("Begin")
    await init_db()


async def shutdown_event():
    await log_writer.write_log("End")


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


@app.get("/", response_class=PlainTextResponse, tags=[Tags.main])
def root_page():
    return "Hello!"


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()


if __name__ == "__main__":
    main()
