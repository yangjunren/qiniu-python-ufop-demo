# ufop demo

# 构建镜像
进入该目录，然后运行以下命令，获得名为 ufopdemo:v1 的 docker 镜像

```
docker build -t "ufopdemo:v1" .
```

# 验证镜像功能

## 运行镜像

```
docker run -p 9100:9100 ufopdemo:v1
```

## 测试数据处理接口

### 测试处理资源通过url参数来指定：
运行命令

```
curl -X POST "http://127.0.0.1:9100/handler?cmd=doraufoptest&url=http://qb8z8byyd.bkt.clouddn.com/4/a.jpg"

```

来自 http://qb8z8byyd.bkt.clouddn.com/4/a.jpg 的网页内容会被打印

### 测试处理资源通过请求body来指定：
运行命令

```
curl -d "{\"data\":\"this should be printed\"}" "http://127.0.0.1:9200/handler?cmd=doraufoptest"
```

{"data":"this should be printed"}将会被打印

### 健康检查
运行命令

```
curl -v "http://127.0.0.1:9100/health"
```

返回status code为200，响应内容是 health is OK

