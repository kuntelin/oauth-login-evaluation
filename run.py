#!/usr/bin/env python3

import logging
import logging.config
import os

import uvicorn
from fastapi import FastAPI

from oauth_login_evaluation.auth.keycloak.routers import router as keycloak_router
from oauth_login_evaluation.auth.line.routers import router as line_router

APP_NAME = "oauth_login_evaluation"

VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
TRACING = os.getenv("TRACING", "false").lower() == "true"

# * initialize logging

# add TRACE logging level
logging.addLevelName(5, "TRACE")

# set default logging config
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",  # noqa: E501
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            APP_NAME: {"handlers": ["default"], "level": "INFO", "propagate": False},
            # * uvicorn logging
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }
)

if TRACING:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("uvicorn").setLevel(logging.DEBUG)
    logging.getLogger(APP_NAME).setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)-30s - %(levelname)-7s - %(message)s")
    logging.getHandlerByName("default").setFormatter(formatter)
    logging.getHandlerByName("access").setFormatter(formatter)
elif DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("uvicorn").setLevel(logging.DEBUG)
    logging.getLogger(APP_NAME).setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)-7s - %(message)s")
    logging.getHandlerByName("default").setFormatter(formatter)
    logging.getHandlerByName("access").setFormatter(formatter)
elif VERBOSE:
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger(APP_NAME).setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s")
    logging.getHandlerByName("default").setFormatter(formatter)
    logging.getHandlerByName("access").setFormatter(formatter)
else:
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger(APP_NAME).setLevel(logging.WARNING)
    formatter = logging.Formatter("%(message)s")
    logging.getHandlerByName("default").setFormatter(formatter)
    logging.getHandlerByName("access").setFormatter(formatter)

# * initialize FastAPI app
app = FastAPI(title=APP_NAME)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# * include routers
app.include_router(keycloak_router, prefix="/auth/keycloak", tags=["keycloak"])
app.include_router(line_router, prefix="/auth/line", tags=["line"])


# * run FastAPI app
if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        access_log=True,
        reload=True,
        use_colors=True,
    )
