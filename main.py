import linecache
import inspect
import asyncio

from typing import Dict


def _get_coroutine_stack_trace(task):
    """
    asyncio Task에서 실행 중인 coroutine 객체의 콜 스택을 반환 한다.
    Args:
        task (asyncio.Task): asyncio Task

    Returns:
        (List[Tuple]): [(파일명, 라인 번호, 함수 이름, 라인 코드)]
    """

    extracted_list = []
    coro = task._coro
    while True:
        coro_name = coro.__name__
        try:
            frame = coro.cr_frame
        except AttributeError:
            frame = coro.gi_frame
        coro_filename = frame.f_code.co_filename
        await_line_number = frame.f_lineno

        linecache.checkcache(coro_filename)
        line = linecache.getline(coro_filename, await_line_number, frame.f_globals)

        extracted_list.append((coro_filename, await_line_number, coro_name, line))

        try:
            coro = coro.cr_await
        except AttributeError:
            coro = coro.gi_yieldfrom
        if not inspect.isawaitable(coro):
            break

    return extracted_list


async def get_tasks(include_stacks: bool = False) -> Dict:
    """
    현재 이벤트 루프에서 실행 중인 전체 task의 실행 정보를 조회 한다.

    Args:
        include_stacks (bool): 세부 스택 정보 포함 여부

    Returns:
        (Dict): task 실행 정보
    """

    loop = asyncio.get_running_loop()
    tasks = asyncio.all_tasks(loop)
    result = []

    for task in tasks:
        stack_info = []

        coroutine_frames = _get_coroutine_stack_trace(task)

        current_frame = coroutine_frames[-1]
        current_frame_info = {
            'filename': current_frame[0],
            'lineno': current_frame[1],
            'name': current_frame[2],
            'line': current_frame[3]
        }

        if include_stacks:
            for frame in coroutine_frames:
                frame_info = {
                    'filename': frame[0],
                    'lineno': frame[1],
                    'name': frame[2],
                    'line': frame[3]
                }
                stack_info.append(frame_info)

        # 해당 task의 실행 함수 정보 가져오기
        task_function = task._coro.__qualname__

        task_info = {
            "task": str(task),
            "current_state": task._state,
            "current_frame": current_frame_info,
            "function_executing": task_function
        }

        if include_stacks:
            task_info["stack"] = stack_info

        result.append(task_info)

    return {"tasks": result}


async def main():
    # stack 정보 출력 하지 않음
    print(await get_tasks())

    # stack 정보 출력
    print(await get_tasks(True))


if __name__ == "__main__":
    asyncio.run(main())
