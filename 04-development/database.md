# [占位] 数据库设计

> [占位] 当前文档尚未进入正式编写阶段。本页仅保留结构化草案，不可直接作为课程提交稿、开发依据或答辩材料使用。

## 设计目标

支持课程教学主链路的数据建模，并为评测、批改、统计和通知提供可靠存储。

## 建议核心实体

- User
- Role
- Permission
- Course
- CourseMember
- CourseSection
- Assignment
- Submission
- JudgeResult
- ReviewRecord
- Grade
- Notification
- FileAsset

## 建议建模原则

- 核心对象主键统一
- 状态字段和时间字段完整
- 关联关系清晰，避免隐式耦合
- 对评测结果、提交记录和通知保留历史

## 待补充内容

- ER 图
- 表结构定义
- 索引设计
- 初始化数据方案
