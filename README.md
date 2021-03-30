## How to reproduce the error "sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_() here. Was IO attempted in an unexpected place? (Background on this error at: http://sqlalche.me/e/14/xd2s) sys:1: RuntimeWarning: coroutine 'AsyncAdapt_asyncpg_cursor._prepare_and_execute' was never awaited"

```
$ pip install -r requirements.txt

$ alembic upgrade head

$ python run_example.py
```

