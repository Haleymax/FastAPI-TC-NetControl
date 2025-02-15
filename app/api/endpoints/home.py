from fastapi import APIRouter
from starlette.responses import HTMLResponse

# 创建 APIRouter 类的实例
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def read_root():
    html_content = "<h1>欢迎使用弱网测试环境</h1>"
    return html_content