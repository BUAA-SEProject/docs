# [占位] 批改与成绩接口

> [占位] 当前文档尚未进入正式编写阶段。本页仅保留结构化草案，不可直接作为课程提交稿、开发依据或答辩材料使用。

## 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/submissions/{id}/review` | 查看批改信息 | 已登录 |
| POST | `/submissions/{id}/review` | 提交人工批改 | 教师 |
| GET | `/courses/{id}/grades` | 查看课程成绩 | 已登录 |
| POST | `/courses/{id}/grades/publish` | 发布成绩 | 教师 |
| GET | `/courses/{id}/grades/export` | 导出成绩 | 教师 |

## 待补充内容

- 评分组成
- 成绩可见性控制
- 人工评分与自动评测融合规则
