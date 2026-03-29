## Run Tasks

### run-001: 构建完整的 RESTful API 服务

**Context**: 一个在线书店需要一个后端图书管理服务。团队使用 Go 语言，数据存储用 SQLite（轻量级，不需要外部数据库服务）。团队没有现成的项目框架，需要从零搭建。

**Requirements**:
- 使用 Go 标准库 + 第三方路由库（如 chi 或 gorilla/mux）构建 HTTP 服务
- 实现以下 API 端点：
  - `GET /api/books` — 分页列出图书，支持 `?page=1&limit=10&author=xxx` 筛选
  - `GET /api/books/{id}` — 获取单本图书详情
  - `POST /api/books` — 创建图书（title, author, isbn, price, stock）
  - `PUT /api/books/{id}` — 更新图书信息
  - `DELETE /api/books/{id}` — 删除图书
- SQLite 数据库初始化（包含建表语句和种子数据，至少 5 条）
- 输入验证：所有字段都有类型和范围校验
- 错误处理：返回具体的 HTTP 状态码和 JSON 错误消息
- 项目结构清晰：main.go、handlers/、models/、database/ 分层
- 提供 Makefile 或 go run 启动方式
- 代码能编译通过且逻辑正确

**Output**: 完整的 Go 项目目录结构，所有源代码文件。保存到 `output/run-001/` 目录下。

---

### run-002: 构建完整的单页 Web 应用

**Context**: 一个团队需要一个内部使用的任务看板（类似简化的 Trello）。纯前端实现，数据保存在 localStorage，不需要后端。需要从零创建一个完整的 HTML+CSS+JS 项目。

**Requirements**:
- 单个 `index.html` 文件（内联 CSS 和 JS）或拆分为 html/css/js 三个文件
- 三列看板布局：待办(Todo)、进行中(In Progress)、已完成(Done)
- 功能需求：
  - 添加新任务卡片（标题 + 描述 + 优先级标签）
  - 拖拽或点击移动卡片到不同列
  - 删除卡片
  - 卡片计数显示
  - 数据持久化到 localStorage，刷新页面不丢失
- UI 要求：
  - 响应式布局，移动端可用
  - 卡片有优先级颜色标记（高/中/低）
  - 添加任务有表单验证（标题必填）
  - 空状态提示（"暂无任务，点击添加"）
- 无外部依赖（不使用 React/Vue，原生 JS 实现）

**Output**: 完整的前端项目文件。保存到 `output/run-002/` 目录下。

---

### run-003: 重构现有代码并添加测试

**Context**: 一个初级开发者写了一个用户管理的 Python 模块，代码能用但质量很差。需要重构并添加单元测试。

以下是需要重构的原始代码（保存在 `output/run-003/original/user_manager.py`）：

```python
import json
import os

users = []

def load_users():
    global users
    if os.path.exists('users.json'):
        f = open('users.json', 'r')
        users = json.load(f)
        f.close()

def save_users():
    global users
    f = open('users.json', 'w')
    json.dump(users, f)
    f.close()

def add_user(name, email, age):
    for u in users:
        if u['email'] == email:
            return False
    user = {'name': name, 'email': email, 'age': age}
    users.append(user)
    save_users()
    return True

def get_user(email):
    for u in users:
        if u['email'] == email:
            return u
    return None

def delete_user(email):
    for i, u in enumerate(users):
        if u['email'] == email:
            users.pop(i)
            save_users()
            return True
    return False

def get_adults():
    result = []
    for u in users:
        if u['age'] >= 18:
            result.append(u)
    return result
```

**Requirements**:
- 重构为面向对象设计（UserManager 类）
- 添加完整的类型标注
- 添加输入验证（name 非空、email 格式合法、age 为正整数）
- 使用 dataclass 或 Pydantic 定义 User 模型
- 文件操作使用 context manager（with 语句）
- 消除全局变量
- 编写完整的 pytest 单元测试，覆盖：
  - 正常流程（增删查）
  - 边界情况（空列表、不存在的用户）
  - 异常情况（无效 email、重复 email、非法 age）
- 重构后的代码行数不应超过原始代码的 2 倍

**Output**: 重构后的 Python 模块和测试文件。保存到 `output/run-003/` 目录下，包含 `user_manager.py` 和 `test_user_manager.py`。
