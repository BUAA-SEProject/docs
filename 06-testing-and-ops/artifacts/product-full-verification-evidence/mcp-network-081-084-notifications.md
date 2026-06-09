2. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [200] OK
3. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count
31. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [FAILED] net::ERR_ABORTED
32. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [200] OK
33. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK
34. [GET] http://127.0.0.1:3000/api/v1/me/notifications?page=1&pageSize=20 => [200] OK
35. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [FAILED] net::ERR_ABORTED
36. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK

Note: 27 static requests not shown, run with "static" option to see them.