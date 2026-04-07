# 课程接口

## 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/courses` | 课程列表 | 已登录 |
| POST | `/courses` | 创建课程 | 教师 |
| GET | `/courses/{id}` | 课程详情 | 已登录 |
| PUT | `/courses/{id}` | 更新课程 | 教师 |
| POST | `/courses/{id}/members` | 加入课程 | 学生 |
| GET | `/courses/{id}/resources` | 课程资源列表 | 已登录 |
| POST | `/courses/{id}/announcements` | 发布公告 | 教师 |

## 待补充内容

- 分页与筛选规则
- 课程状态定义
- 加课方式与邀请码逻辑
