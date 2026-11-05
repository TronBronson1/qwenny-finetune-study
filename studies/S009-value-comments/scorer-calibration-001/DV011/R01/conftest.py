"""Trusted evaluator instrumentation; never provided to the model or optimizer."""
import copy,importlib.util,json,pathlib
import pytest
TRACE=[]
NODE=None
CONFIG=json.loads(pathlib.Path('trace-config.json').read_text(encoding='utf-8'))
def snapshot(v):
    typ=type(v)
    if isinstance(v,(tuple,list)):
        return {'type':typ.__name__,'items':[snapshot(x) for x in v]}
    if isinstance(v,dict):
        return {'type':typ.__name__,'items':[[snapshot(k),snapshot(x)] for k,x in v.items()]}
    if isinstance(v,(str,int,float,bool,bytes)) or v is None:
        return {'type':typ.__name__,'repr':repr(v)}
    return {'type':typ.__name__,'repr':repr(v),'unsupported':True}
def result(function,args,kwargs):
    try: return {'return':snapshot(function(*args,**kwargs))}
    except Exception as e: return {'exception':type(e).__name__}
def pytest_sessionstart(session):
    import subject
    spec=importlib.util.spec_from_file_location('trusted_reference',CONFIG['reference'])
    reference=importlib.util.module_from_spec(spec); spec.loader.exec_module(reference)
    correct=getattr(reference,CONFIG['function']); original=getattr(subject,CONFIG['function'])
    def wrapped(*args,**kwargs):
        item={'node':NODE,'args':snapshot(args),'kwargs':snapshot(kwargs)}
        ca,ck=copy.deepcopy((args,kwargs))
        item['expected']=result(correct,ca,ck)
        item['expected_after']=snapshot((ca,ck))
        try:
            value=original(*args,**kwargs); item['actual']={'return':snapshot(value)}; return value
        except Exception as e:
            item['actual']={'exception':type(e).__name__}; raise
        finally:
            item['actual_after']=snapshot((args,kwargs)); TRACE.append(item)
    setattr(subject,CONFIG['function'],wrapped)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item,nextitem):
    global NODE
    NODE=item.nodeid
    yield
    NODE=None
def pytest_sessionfinish(session,exitstatus):
    pathlib.Path('calls.json').write_text(json.dumps(TRACE,indent=2,ensure_ascii=True),encoding='utf-8')
