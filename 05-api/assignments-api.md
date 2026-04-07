# [占位] 作业与实验接口

> [占位] 当前文档尚未进入正式编写阶段。本页仅保留结构化草案，不可直接作为课程提交稿、开发依据或答辩材料使用。

## 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/courses/{id}/assignments` | 查看课程作业/实验 | 已登录 |
| POST | `/courses/{id}/assignments` | 创建作业/实验 | 教师 |
| GET | `/assignments/{id}` | 查看作业/实验详情 | 已登录 |
| PUT | `/assignments/{id}` | 更新作业/实验 | 教师 |
| POST | `/assignments/{id}/submissions` | 提交作业/实验 | 学生 |
| GET | `/assignments/{id}/submissions` | 查看提交记录 | 已登录 |
| POST | `/submissions/{id}/rejudge` | 重新评测 | 教师 |

## 待补充内容

- 提交次数限制
- 截止时间与迟交策略
- 评测触发与状态回传
