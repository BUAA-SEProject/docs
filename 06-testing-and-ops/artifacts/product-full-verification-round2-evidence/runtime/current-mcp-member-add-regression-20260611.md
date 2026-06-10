# 当前会话成员添加 MCP 回归

- 时间：2026-06-11 01:24-01:29 CST
- 工具：Playwright MCP 浏览器
- 账号：教师 `U-TA1`
- 页面：`/teacher/courses/2/members`
- 临时数据：用户 `e2e-mcp-member-20260610172354`，用户 ID `496`，教学班 `A1`
- 步骤：
  1. 打开成员管理页，点击“添加成员”。
  2. 输入用户 ID `496`，保持角色“学生”，选择教学班 `A1 (A1)`。
  3. 点击“添加”。
  4. 使用成员页搜索框查询 `e2e-mcp-member-20260610172354`。
- 页面结果：添加对话框关闭；成员表显示该用户，教学班 `A1`，角色“学生”，状态“已激活”。
- Console：当前 MCP 会话 `Errors: 0, Warnings: 0`。
- Network：`POST /api/v1/teacher/course-offerings/2/members/batch` 200；随后 `GET /api/v1/teacher/course-offerings/2/members` 200；搜索 `keyword=e2e-mcp-member-20260610172354` 返回 200。
- 备注：首次打开 `/teacher/courses/32/members` 使用默认教师账号被拒绝，属于账号无该开课权限；未计入产品缺陷。
