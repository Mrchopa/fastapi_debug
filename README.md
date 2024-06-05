# What's this
This is the event loop task capture code provided for debugging a server based on the Python asynchronous web framework FastAPI. (Anywhere there's an asyncio-based event loop..)
It allows you to identify the location of the function currently executing in tasks running in the event loop. 
It provides similar information to thread dumps in Java.

## Example code
```python
from fastapi import FastAPI, Query
from main import get_tasks

app = FastAPI()


@app.get("/debug")
async def debug(include_stacks: bool = Query(False, description="세부 스택 정보 포함 여부")):
    return await get_tasks(include_stacks)

```

## Example result

### without stack
```json
{
    "tasks": [
      {
        "task": "<Task pending name='Task-2' coro=<LifespanOn.main() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/lifespan/on.py:86> wait_for=<Future pending cb=[Task.task_wakeup()]>>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/queues.py",
          "lineno": 158,
          "name": "get",
          "line": "                await getter\n"
        },
        "function_executing": "LifespanOn.main"
      },
      {
        "task": "<Task pending name='Task-1' coro=<Server.serve() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/server.py:81> wait_for=<Future pending cb=[Task.task_wakeup()]> cb=[_run_until_complete_cb() at /opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py:181]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
          "lineno": 649,
          "name": "sleep",
          "line": "        return await future\n"
        },
        "function_executing": "Server.serve"
      },
      {
        "task": "<Task pending name='starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.close_recv_stream_on_response_sent' coro=<BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.close_recv_stream_on_response_sent() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py:55> wait_for=<Future pending cb=[Task.task_wakeup()]> cb=[TaskGroup._spawn.<locals>.task_done() at /Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py:661]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/locks.py",
          "lineno": 213,
          "name": "wait",
          "line": "            await fut\n"
        },
        "function_executing": "BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.close_recv_stream_on_response_sent"
      },
      {
        "task": "<Task pending name='Task-388' coro=<RequestResponseCycle.run_asgi() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py:408> cb=[set.discard()]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
          "lineno": 634,
          "name": "__sleep0",
          "line": "    yield\n"
        },
        "function_executing": "RequestResponseCycle.run_asgi"
      },
      {
        "task": "<Task pending name='starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro' coro=<BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py:70> cb=[TaskGroup._spawn.<locals>.task_done() at /Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py:661]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
          "lineno": 70,
          "name": "coro",
          "line": "                        await self.app(scope, receive_or_disconnect, send_no_error)\n"
        },
        "function_executing": "BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro"
      },
      {
        "task": "<Task pending name='Task-3' coro=<BasePoolManager._check_pool_task() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/hasql/base.py:492> wait_for=<Future pending cb=[Task.task_wakeup()]>>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
          "lineno": 649,
          "name": "sleep",
          "line": "        return await future\n"
        },
        "function_executing": "BasePoolManager._check_pool_task"
      }
    ]
  }
```

### with stack
```json
{
    "tasks": [
      {
        "task": "<Task pending name='Task-2' coro=<LifespanOn.main() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/lifespan/on.py:86> wait_for=<Future pending cb=[Task.task_wakeup()]>>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/queues.py",
          "lineno": 158,
          "name": "get",
          "line": "                await getter\n"
        },
        "function_executing": "LifespanOn.main",
        "stack": [
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/lifespan/on.py",
            "lineno": 86,
            "name": "main",
            "line": "            await app(scope, self.receive, self.send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py",
            "lineno": 84,
            "name": "__call__",
            "line": "        return await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/fastapi/applications.py",
            "lineno": 1106,
            "name": "__call__",
            "line": "        await super().__call__(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/applications.py",
            "lineno": 122,
            "name": "__call__",
            "line": "        await self.middleware_stack(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py",
            "lineno": 149,
            "name": "__call__",
            "line": "            await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette_context/middleware/raw_middleware.py",
            "lineno": 75,
            "name": "__call__",
            "line": "            await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/authentication.py",
            "lineno": 31,
            "name": "__call__",
            "line": "            await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
            "lineno": 26,
            "name": "__call__",
            "line": "            await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py",
            "lineno": 55,
            "name": "__call__",
            "line": "            await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py",
            "lineno": 17,
            "name": "__call__",
            "line": "                await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/routing.py",
            "lineno": 707,
            "name": "__call__",
            "line": "            await self.lifespan(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/routing.py",
            "lineno": 686,
            "name": "lifespan",
            "line": "                await receive()\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/lifespan/on.py",
            "lineno": 137,
            "name": "receive",
            "line": "        return await self.receive_queue.get()\n"
          },
          {
            "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/queues.py",
            "lineno": 158,
            "name": "get",
            "line": "                await getter\n"
          }
        ]
      },
      {
        "task": "<Task pending name='Task-1' coro=<Server.serve() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/server.py:81> wait_for=<Future pending cb=[Task.task_wakeup()]> cb=[_run_until_complete_cb() at /opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py:181]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
          "lineno": 649,
          "name": "sleep",
          "line": "        return await future\n"
        },
        "function_executing": "Server.serve",
        "stack": [
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/server.py",
            "lineno": 81,
            "name": "serve",
            "line": "        await self.main_loop()\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/server.py",
            "lineno": 232,
            "name": "main_loop",
            "line": "            await asyncio.sleep(0.1)\n"
          },
          {
            "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
            "lineno": 649,
            "name": "sleep",
            "line": "        return await future\n"
          }
        ]
      },
      {
        "task": "<Task pending name='starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.close_recv_stream_on_response_sent' coro=<BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.close_recv_stream_on_response_sent() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py:55> wait_for=<Future pending cb=[Task.task_wakeup()]> cb=[TaskGroup._spawn.<locals>.task_done() at /Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py:661]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/locks.py",
          "lineno": 213,
          "name": "wait",
          "line": "            await fut\n"
        },
        "function_executing": "BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.close_recv_stream_on_response_sent",
        "stack": [
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
            "lineno": 55,
            "name": "close_recv_stream_on_response_sent",
            "line": "                await response_sent.wait()\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py",
            "lineno": 1778,
            "name": "wait",
            "line": "        if await self._event.wait():\n"
          },
          {
            "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/locks.py",
            "lineno": 213,
            "name": "wait",
            "line": "            await fut\n"
          }
        ]
      },
      {
        "task": "<Task pending name='starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro' coro=<BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py:70> cb=[TaskGroup._spawn.<locals>.task_done() at /Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py:661]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
          "lineno": 70,
          "name": "coro",
          "line": "                        await self.app(scope, receive_or_disconnect, send_no_error)\n"
        },
        "function_executing": "BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro",
        "stack": [
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
            "lineno": 70,
            "name": "coro",
            "line": "                        await self.app(scope, receive_or_disconnect, send_no_error)\n"
          }
        ]
      },
      {
        "task": "<Task pending name='Task-3' coro=<BasePoolManager._check_pool_task() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/hasql/base.py:492> wait_for=<Future pending cb=[Task.task_wakeup()]>>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
          "lineno": 649,
          "name": "sleep",
          "line": "        return await future\n"
        },
        "function_executing": "BasePoolManager._check_pool_task",
        "stack": [
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/hasql/base.py",
            "lineno": 492,
            "name": "_check_pool_task",
            "line": "                await self._periodic_pool_check(pool, dsn, sys_connection)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/hasql/base.py",
            "lineno": 564,
            "name": "_periodic_pool_check",
            "line": "            await asyncio.sleep(self._refresh_delay)\n"
          },
          {
            "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
            "lineno": 649,
            "name": "sleep",
            "line": "        return await future\n"
          }
        ]
      },
      {
        "task": "<Task pending name='Task-495' coro=<RequestResponseCycle.run_asgi() running at /Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py:408> cb=[set.discard()]>",
        "current_state": "PENDING",
        "current_frame": {
          "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
          "lineno": 634,
          "name": "__sleep0",
          "line": "    yield\n"
        },
        "function_executing": "RequestResponseCycle.run_asgi",
        "stack": [
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py",
            "lineno": 408,
            "name": "run_asgi",
            "line": "            result = await app(  # type: ignore[func-returns-value]\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py",
            "lineno": 84,
            "name": "__call__",
            "line": "        return await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/fastapi/applications.py",
            "lineno": 1106,
            "name": "__call__",
            "line": "        await super().__call__(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/applications.py",
            "lineno": 122,
            "name": "__call__",
            "line": "        await self.middleware_stack(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py",
            "lineno": 162,
            "name": "__call__",
            "line": "            await self.app(scope, receive, _send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette_context/middleware/raw_middleware.py",
            "lineno": 92,
            "name": "__call__",
            "line": "            await self.app(scope, receive, send_wrapper)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/authentication.py",
            "lineno": 48,
            "name": "__call__",
            "line": "        await self.app(scope, receive, send)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
            "lineno": 108,
            "name": "__call__",
            "line": "            response = await self.dispatch_func(request, call_next)\n"
          },
          {
            "filename": "/Users/tester/workspace/app/web/middlewares.py",
            "lineno": 39,
            "name": "dispatch",
            "line": "            res = await call_next(request)\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/starlette/middleware/base.py",
            "lineno": 78,
            "name": "call_next",
            "line": "                message = await recv_stream.receive()\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/streams/memory.py",
            "lineno": 96,
            "name": "receive",
            "line": "        await checkpoint()\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/lowlevel.py",
            "lineno": 33,
            "name": "checkpoint",
            "line": "    await get_asynclib().checkpoint()\n"
          },
          {
            "filename": "/Users/tester/workspace/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py",
            "lineno": 447,
            "name": "checkpoint",
            "line": "    await sleep(0)\n"
          },
          {
            "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
            "lineno": 640,
            "name": "sleep",
            "line": "        await __sleep0()\n"
          },
          {
            "filename": "/opt/homebrew/Cellar/python@3.11/3.11.9/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/tasks.py",
            "lineno": 634,
            "name": "__sleep0",
            "line": "    yield\n"
          }
        ]
      }
    ]
  }
```
