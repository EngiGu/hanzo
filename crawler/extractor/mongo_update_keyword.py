from core.mongo_db import MongoDb


MT_cp = MongoDb("aizhaopin", "company_infos")

def company_update_func(resume):
    res = MT_cp.search({"jx_resume_id": resume["jx_resume_id"]})
    if not res:
        MT_cp.update({"jx_resume_id": resume["jx_resume_id"]}, resume)
    else:
        develop_old = res.get("develops", [])
        develop_new = resume.get("develops", [])
        resume["develops"] = develop_old + develop_new
        MT_cp.update({"jx_resume_id": resume["jx_resume_id"]}, resume)
    pass

def mongo_ur(resume:dict):
    source = resume.get("source", 0)
    if source > 200:
        company_update_func(resume)
    else:
        raise Exception(f"source num wrong:{resume}")

if __name__ == '__main__':
    run()